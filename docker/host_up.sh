#!/usr/bin/env bash
#
# host_up.sh -- bring up and VERIFY the host-side singletons that MatClaw's
# containerized runs depend on. Run this once on the host before any
# docker/run.sh launch. Idempotent: safe to re-run.
#
# Why this exists: a containerized run reaches the host Mongo via
# host.docker.internal, which on Linux resolves to the docker bridge gateway
# (e.g. 172.17.0.1) -- NOT 127.0.0.1. A mongod bound to 127.0.0.1 ONLY is
# invisible to the container, so every run silently hangs waiting for Mongo.
# This script always binds mongod to loopback + the bridge gateway and then
# PROVES a container can reach it, so that failure mode cannot recur.
#
# Brings up / checks, in order:
#   1. MongoDB   -- bound to 127.0.0.1 + the docker bridge gateway
#   2. (verify)  -- the gateway bind accepts connections, and (if the image is
#                   built) a throwaway container pings Mongo via host.docker.internal
#   3. jf runner -- the jobflow-remote daemon for the HPC project
#   4. HPC SSH   -- fail-fast reachability check of the Anvil login node
#
# Tunables (env): MONGO_BIN MONGO_DBPATH MONGO_LOG MONGO_PORT IMAGE JF
#                 JF_PROJECT ANVIL_KEY ANVIL_HOST DOCKER_BRIDGE_GATEWAY
# The defaults below are neutral placeholders -- the mongod/jf paths assume the
# binaries are on PATH, and ANVIL_HOST/ANVIL_KEY are stubs. Set them in your host
# environment (or a local wrapper) to match your install and HPC allocation.
#
set -euo pipefail

MONGO_BIN="${MONGO_BIN:-mongod}"                    # mongod on PATH, or an absolute path
MONGO_DBPATH="${MONGO_DBPATH:-$HOME/mongodb/data}"
MONGO_LOG="${MONGO_LOG:-$HOME/mongodb/mongod.log}"
MONGO_PORT="${MONGO_PORT:-27017}"
IMAGE="${IMAGE:-matclaw:dev}"
JF="${JF:-jf}"                                      # jobflow-remote CLI on PATH, or an absolute path
JF_PROJECT="${JF_PROJECT:-anvil}"
ANVIL_KEY="${ANVIL_KEY:-$HOME/.ssh/id_anvil}"       # SSH key for the HPC login node
ANVIL_HOST="${ANVIL_HOST:-user@login.cluster.edu}"  # HPC login (user@host) -- set to your allocation

log() { echo "[host_up] $*"; }
die() { echo "[host_up] ERROR: $*" >&2; exit 1; }

# --- 0. the docker bridge gateway is the address host.docker.internal maps to ---
GATEWAY="${DOCKER_BRIDGE_GATEWAY:-$(docker network inspect bridge \
    --format '{{range .IPAM.Config}}{{.Gateway}}{{end}}' 2>/dev/null)}"
[ -n "$GATEWAY" ] || die "could not determine the docker bridge gateway IP"
BIND="127.0.0.1,${GATEWAY}"
log "docker bridge gateway = ${GATEWAY}; mongod bind target = ${BIND}"

# --- 1. MongoDB on loopback + gateway -------------------------------------------
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

# --- 2. verify the gateway bind, faithfully if the image is built ----------------
log "verifying gateway bind (${GATEWAY}:${MONGO_PORT}) from the host ..."
timeout 4 bash -c "exec 3<>/dev/tcp/${GATEWAY}/${MONGO_PORT}" 2>/dev/null \
    || die "nothing accepts on ${GATEWAY}:${MONGO_PORT}; the mongod bind failed"
log "gateway bind OK"

if docker image inspect "$IMAGE" >/dev/null 2>&1; then
    log "verifying container -> Mongo via host.docker.internal ..."
    docker run --rm --add-host host.docker.internal:host-gateway --entrypoint "" "$IMAGE" \
        python -c "from pymongo import MongoClient; \
MongoClient('host.docker.internal', ${MONGO_PORT}, serverSelectionTimeoutMS=4000).admin.command('ping')" \
        >/dev/null \
        || die "a container cannot reach Mongo via host.docker.internal:${MONGO_PORT}; runs would hang"
    log "container -> Mongo OK"
else
    log "WARN: image ${IMAGE} not built -- skipped the in-container Mongo check (gateway check passed)"
fi

# --- 3. jobflow-remote runner ----------------------------------------------------
if "$JF" -p "$JF_PROJECT" runner status 2>/dev/null | grep -qi "status: running"; then
    log "jf runner for '${JF_PROJECT}' already running"
else
    log "starting jf runner for '${JF_PROJECT}'"
    "$JF" -p "$JF_PROJECT" runner start
fi

# --- 4. HPC SSH reachability (fail-fast) -----------------------------------------
log "checking Anvil SSH (${ANVIL_HOST}) ..."
ssh -i "$ANVIL_KEY" -o BatchMode=yes -o ConnectTimeout=8 "$ANVIL_HOST" 'hostname' >/dev/null \
    || die "Anvil SSH failed (key ${ANVIL_KEY}); jobflow submission will not work"
log "Anvil SSH OK"

log "all host singletons up and verified -- safe to launch docker/run.sh"
