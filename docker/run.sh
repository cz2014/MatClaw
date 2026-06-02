#!/usr/bin/env bash
#
# Hardened launcher for the MatClaw container (P3). Runs the WHOLE agent process
# in one disposable container; the container is the security boundary.
#
# Usage:
#   docker/run.sh run --project perlmutter --task /work/workspace/task.txt
#   docker/run.sh run --resume
#   docker/run.sh --help
#
# Tunables (env):
#   IMAGE=matclaw:dev        image tag (built on first use if missing)
#   MEM=8g  CPUS=4  PIDS=512  resource caps
#   MATCLAW_MONGO_HOST=host.docker.internal   host alias for the shared Mongo
#   MATCLAW_ENV_VOLUME=matclaw-env            optional named volume -> /home/agent
#                                             (persists uv/pip caches + agent home
#                                              across runs; installs reinstall fast)
#   MATCLAW_FORWARD_ENV="VAR1 VAR2"           extra env vars to forward beyond the ones the
#                                             configs reference via ${VAR}
#   MATCLAW_WORKSPACE=/path/to/run            host workspace dir (default: repo workspace/);
#                                             point outside the repo to keep run data separate
#   MATCLAW_CONFIGS=/path/to/config           host config dir (default: repo configs/);
#                                             point outside the repo to keep run config separate
#
# Prerequisites on the host (shared singletons -- see the plan, topology):
#   - MongoDB on 127.0.0.1:27017
#   - one `jf -p <project> runner run` per HPC project
#   - ~/.ssh, ~/.jfremote, and a repo-root .env with the API keys
#
# Operator guide: docs/references/docker-runtime.md

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${REPO_ROOT}"

# Run data (workspace) and run config may live OUTSIDE the repo (e.g. under
# /work/matclaw_runs) via these overrides; default to the repo dirs so existing
# usage is unchanged.
WORKSPACE_SRC="${MATCLAW_WORKSPACE:-${REPO_ROOT}/workspace}"
CONFIGS_SRC="${MATCLAW_CONFIGS:-${REPO_ROOT}/configs}"

IMAGE="${IMAGE:-matclaw:dev}"
MEM="${MEM:-8g}"
CPUS="${CPUS:-4}"
PIDS="${PIDS:-512}"
MONGO_HOST="${MATCLAW_MONGO_HOST:-host.docker.internal}"

# Build on first use, matching the host UID/GID so the read-only-mounted SSH keys
# (perms 700/600) are readable by the non-root container user.
if ! docker image inspect "${IMAGE}" >/dev/null 2>&1; then
    echo "[run.sh] image ${IMAGE} not found; building..."
    docker build -f docker/Dockerfile \
        --build-arg UID="$(id -u)" --build-arg GID="$(id -g)" \
        -t "${IMAGE}" .
fi

mkdir -p "${WORKSPACE_SRC}"

ARGS=(
    --rm
    --init
    --user "$(id -u):$(id -g)"
    --cap-drop ALL
    --security-opt no-new-privileges
    --memory "${MEM}" --cpus "${CPUS}" --pids-limit "${PIDS}"
    -e "MATCLAW_MONGO_HOST=${MONGO_HOST}"
)

# DETACH=1 -> dockerd-supervised background run (headless, no TTY); else interactive -it.
if [ -n "${DETACH:-}" ]; then
    ARGS+=(-d); [ -n "${NAME:-}" ] && ARGS+=(--name "$NAME")
else
    ARGS+=(-it)
fi

# Secrets (never baked into the image). Forward ONLY the env vars the configs actually reference via
# ${VAR} -- whatever names the user chose (GEMINI_API_KEY, a custom GEMINI_KEY, ...) -- for any that
# are set in the host shell. Nothing is hardcoded: the ${VAR} pattern mirrors MatClaw's own
# substitution (core/agent.py `_ENV_PATTERN` + os.path.expandvars), so this reads the config's
# declared env needs, not a guessed key list. Bare `$VAR` is unconventional here (and would false-
# match $HOME/$PATH); use MATCLAW_FORWARD_ENV="VAR1 VAR2" for anything the config does not template.
# A repo-root .env is also applied if present.
_keys=""
[ -d "${CONFIGS_SRC}" ] && _keys=$(grep -rhE '\$\{[A-Za-z_][A-Za-z0-9_]*\}' "${CONFIGS_SRC}" 2>/dev/null \
    | grep -vE '^[[:space:]]*#' | grep -oE '\$\{[A-Za-z_][A-Za-z0-9_]*\}' | tr -d '${}')
for _k in $(printf '%s\n' ${_keys} ${MATCLAW_FORWARD_ENV:-} | sort -u); do
    [ -n "${!_k:-}" ] && ARGS+=(-e "${_k}")
done
[ -f .env ] && ARGS+=(--env-file .env)

# Reach the shared host Mongo. Docker Desktop (mac/win) resolves
# host.docker.internal automatically; on Linux add the host-gateway mapping.
if [ "$(uname -s)" = "Linux" ]; then
    ARGS+=(--add-host "host.docker.internal:host-gateway")
fi

# Mounts: workspace rw; config rw so the agent can append to experience.md, which
# lives INSIDE the config dir (no separate experience.md mount); corpus ro from the
# project root; ssh/jfremote ro (staged, rewritten by the entrypoint); optional volume.
ARGS+=(
    -v "${WORKSPACE_SRC}:/work/workspace"
    -v "${CONFIGS_SRC}:/work/configs"
    -v "${PWD}/corpus:/work/corpus:ro"
    -v "${HOME}/.ssh:/opt/ssh-host:ro"
    -v "${HOME}/.jfremote:/opt/jfremote-host:ro"
)
[ -n "${MATCLAW_ENV_VOLUME:-}" ] && \
    ARGS+=(-v "${MATCLAW_ENV_VOLUME}:/home/agent")

# Default `run` to the mounted repo configs/ unless the caller set --config.
MATCLAW_ARGS=("$@")
if [ "${1:-}" = "run" ] && [[ " $* " != *" --config "* ]]; then
    MATCLAW_ARGS+=(--config /work/configs)
fi

exec docker run "${ARGS[@]}" "${IMAGE}" "${MATCLAW_ARGS[@]}"
