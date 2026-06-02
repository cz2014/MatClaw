#!/usr/bin/env bash
#
# host_up.sh -- bring up and VERIFY the host-side singletons that MatClaw's
# containerized runs depend on. Run this once on the host before any
# docker/run.sh launch. Idempotent: safe to re-run.
#
# Why this exists: a containerized run reaches the host Mongo via
# host.docker.internal, and how that resolves differs by platform:
#   - Linux (native docker): there is NO host.docker.internal forwarding, so a
#     mongod bound to 127.0.0.1 ONLY is invisible to containers and every run
#     silently hangs. mongod must bind to the docker bridge gateway (e.g.
#     172.17.0.1); this script starts/rebinds it accordingly.
#   - macOS (Docker Desktop/Colima): docker runs in a VM that forwards
#     host.docker.internal to the host loopback, so a 127.0.0.1-bound mongod
#     (e.g. brew) is reachable. This script starts it via 'brew services'
#     (brew's own config + data dir), or directly if brew is unavailable.
# Either way it then PROVES a container can reach Mongo, so the failure mode
# cannot recur regardless of platform.
#
# Brings up / checks, in order:
#   1. MongoDB   -- Linux: start/rebind mongod to 127.0.0.1 + the bridge gateway.
#                   macOS: start mongod via brew services (127.0.0.1 only).
#   2. (verify)  -- if the image is built, a throwaway container pings Mongo via
#                   host.docker.internal (the platform-independent guarantee).
#   3. jf runner -- the jobflow-remote daemon for the HPC project
#   4. HPC check -- `jf project check` (workers + stores); the SSH host + key come
#                   from the jfremote project config, NOT from this script
#
# Configuration: host-specific values come from the launcher config -- env vars
# override $XDG_CONFIG_HOME/matclaw/launcher.env, which overrides the placeholder
# defaults below. See docker/launcher.env.example (shared with docker/run.sh).
# Tunables: MONGO_BIN MONGO_DBPATH MONGO_LOG MONGO_PORT IMAGE JF JF_PROJECT
#           DOCKER_BRIDGE_GATEWAY
#
set -euo pipefail

# Layered config: env > launcher.env > the placeholder defaults below.
LAUNCHER_CONF="${MATCLAW_LAUNCHER_CONFIG:-${XDG_CONFIG_HOME:-$HOME/.config}/matclaw/launcher.env}"
[ -f "$LAUNCHER_CONF" ] && . "$LAUNCHER_CONF"

MONGO_BIN="${MONGO_BIN:-mongod}"                    # mongod on PATH, or an absolute path
MONGO_DBPATH="${MONGO_DBPATH:-$HOME/mongodb/data}"
MONGO_LOG="${MONGO_LOG:-$HOME/mongodb/mongod.log}"
MONGO_PORT="${MONGO_PORT:-27017}"
IMAGE="${IMAGE:-matclaw:dev}"
JF="${JF:-jf}"                                      # jobflow-remote CLI on PATH, or an absolute path
JF_PROJECT="${JF_PROJECT:-anvil}"
BREW_MONGO_FORMULA="${BREW_MONGO_FORMULA:-mongodb-community}"  # macOS: brew services formula for mongod

log() { echo "[host_up] $*"; }
die() { echo "[host_up] ERROR: $*" >&2; exit 1; }

OS="$(uname -s)"
log "platform: ${OS}"

# --- 1. MongoDB reachable from containers (platform-specific setup) --------------
case "$OS" in
    Linux)
        # Native docker: a container reaches the host only via the bridge gateway,
        # so mongod must bind to it (host.docker.internal -> host-gateway in run.sh).
        GATEWAY="${DOCKER_BRIDGE_GATEWAY:-$(docker network inspect bridge \
            --format '{{range .IPAM.Config}}{{.Gateway}}{{end}}' 2>/dev/null)}"
        [ -n "$GATEWAY" ] || die "could not determine the docker bridge gateway IP"
        BIND="127.0.0.1,${GATEWAY}"
        log "Linux: docker bridge gateway = ${GATEWAY}; mongod bind target = ${BIND}"
        running="$(pgrep -af "mongod .*--port ${MONGO_PORT}" || true)"
        if [ -n "$running" ]; then
            if echo "$running" | grep -q "$GATEWAY"; then
                log "mongod already running and bound to the gateway -- leaving it"
            else
                log "mongod running but NOT bound to the gateway -- restarting with ${BIND}"
                "$MONGO_BIN" --dbpath "$MONGO_DBPATH" --shutdown \
                    || pkill -f "mongod .*--port ${MONGO_PORT}" || true
                sleep 2
                "$MONGO_BIN" --dbpath "$MONGO_DBPATH" --bind_ip "$BIND" --port "$MONGO_PORT" \
                    --fork --logpath "$MONGO_LOG"
            fi
        else
            log "mongod not running -- starting with ${BIND}"
            "$MONGO_BIN" --dbpath "$MONGO_DBPATH" --bind_ip "$BIND" --port "$MONGO_PORT" \
                --fork --logpath "$MONGO_LOG"
        fi
        # The gateway bind must accept connections from the host side.
        log "verifying gateway bind (${GATEWAY}:${MONGO_PORT}) from the host ..."
        timeout 4 bash -c "exec 3<>/dev/tcp/${GATEWAY}/${MONGO_PORT}" 2>/dev/null \
            || die "nothing accepts on ${GATEWAY}:${MONGO_PORT}; the mongod bind failed"
        log "gateway bind OK"
        ;;
    Darwin)
        # Docker runs in a VM that forwards host.docker.internal to the host
        # loopback, so a 127.0.0.1-bound mongod is reachable. Start it the macOS-
        # native way -- 'brew services' uses brew's own config + data dir (so we
        # use the EXISTING database, not a fresh one) and launchd supervision (so
        # we never run a second mongod alongside it).
        log "macOS: relying on the docker VM to forward host.docker.internal -> host loopback"
        if pgrep -f mongod >/dev/null; then
            log "mongod already running -- leaving it"
        elif command -v brew >/dev/null 2>&1; then
            log "starting mongod via 'brew services start ${BREW_MONGO_FORMULA}'"
            HOMEBREW_NO_ENV_HINTS=1 brew services start "$BREW_MONGO_FORMULA"
        else
            log "no brew found -- starting mongod directly on 127.0.0.1"
            "$MONGO_BIN" --dbpath "$MONGO_DBPATH" --bind_ip 127.0.0.1 --port "$MONGO_PORT" \
                --fork --logpath "$MONGO_LOG"
        fi
        # 'brew services start' is async; wait for the port (no GNU `timeout` on macOS,
        # but a refused localhost connect fails fast, so no hang).
        up=""
        for _ in 1 2 3 4 5 6 7 8 9 10; do
            if (exec 3<>"/dev/tcp/127.0.0.1/${MONGO_PORT}") 2>/dev/null; then up=1; break; fi
            sleep 1
        done
        [ -n "$up" ] || die "mongod did not come up on 127.0.0.1:${MONGO_PORT}"
        log "mongod listening on 127.0.0.1:${MONGO_PORT}"
        ;;
    *)
        die "unsupported platform '${OS}' (expected Linux or Darwin)"
        ;;
esac

# --- 2. PROVE a container can reach Mongo (platform-independent guarantee) --------
if docker image inspect "$IMAGE" >/dev/null 2>&1; then
    log "verifying container -> Mongo via host.docker.internal ..."
    docker run --rm --add-host host.docker.internal:host-gateway --entrypoint "" "$IMAGE" \
        python -c "from pymongo import MongoClient; \
MongoClient('host.docker.internal', ${MONGO_PORT}, serverSelectionTimeoutMS=4000).admin.command('ping')" \
        >/dev/null \
        || die "a container cannot reach Mongo via host.docker.internal:${MONGO_PORT}; runs would hang"
    log "container -> Mongo OK"
else
    log "WARN: image ${IMAGE} not built -- skipped the in-container Mongo check"
fi

# --- 3. jobflow-remote runner ----------------------------------------------------
if "$JF" -p "$JF_PROJECT" runner status 2>/dev/null | grep -qi "status: running"; then
    log "jf runner for '${JF_PROJECT}' already running"
else
    log "starting jf runner for '${JF_PROJECT}'"
    "$JF" -p "$JF_PROJECT" runner start
fi

# --- 4. HPC reachability via jobflow-remote (workers + stores) -------------------
# `jf project check` runs the worker SSH + jobstore + queue checks; the host/key
# live in ~/.jfremote/${JF_PROJECT}.yaml (single source of truth). Note it ALWAYS
# exits 0 and reports status with check/cross glyphs, so we parse its output and
# fail on a red cross ("x ") rather than trusting the exit code.
log "checking '${JF_PROJECT}' workers + stores via jf project check ..."
_chk="$("$JF" -p "$JF_PROJECT" project check 2>&1)"
printf '%s\n' "$_chk"
printf '%s\n' "$_chk" | grep -qE '^[[:space:]]*x ' \
    && die "jf project check reported a failure for '${JF_PROJECT}' (see above); rerun 'jf -p ${JF_PROJECT} project check -e' for details, then fix ~/.jfremote/${JF_PROJECT}.yaml or the runner"
log "jf project check OK"

log "all host singletons up and verified -- safe to launch docker/run.sh"
