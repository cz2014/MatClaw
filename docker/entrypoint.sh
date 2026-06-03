#!/usr/bin/env bash
#
# MatClaw container entrypoint (P3).
#
# Fixes the two things that differ inside the container, then hands off to matclaw:
#   1. Mongo reachability: the mounted jfremote config says host 127.0.0.1, which
#      inside a container means the container itself. Rewrite it to the host
#      (host.docker.internal) so the agent reaches the shared host Mongo.
#   2. SSH: normalize a writable copy of the read-only-mounted keys and pre-seed
#      known_hosts for the configured HPC hosts (so an autonomous run never blocks
#      on a host-key prompt).
#
# Read-only host mounts (staging): /opt/jfremote-host, /opt/ssh-host.
# See docs/references/docker-runtime.md.

set -euo pipefail

MATCLAW_MONGO_HOST="${MATCLAW_MONGO_HOST:-host.docker.internal}"
# Staging paths are overridable (env) so the rewrite logic is unit-testable without Docker.
JF_SRC="${MATCLAW_JFREMOTE_SRC:-/opt/jfremote-host}"
JF_DST="${HOME}/.jfremote"
SSH_SRC="${MATCLAW_SSH_SRC:-/opt/ssh-host}"
SSH_DST="${HOME}/.ssh"

# 1. jfremote config: copy to a writable location and rewrite, in every project YAML:
#    (a) the loopback Mongo host (queue store + docs store + GridFS additional store)
#        -> the host alias, so the agent reaches the shared host Mongo; and
#    (b) every SSH `key_filename` -> the in-container ssh dir. The mounted config holds
#        HOST paths (e.g. /home/<host-user>/.ssh/key_anvil); inside the container the
#        keys are re-staged under ${SSH_DST} by basename (block 2), so any in-container
#        SSH -- jobflow-remote and the remote_* tools -- must read them from there, not
#        the host path (which does not exist in the container). Without (b) every
#        remote_* call fails with ENOENT on the host key path.
if [ -d "${JF_SRC}" ]; then
    mkdir -p "${JF_DST}"
    cp -a "${JF_SRC}/." "${JF_DST}/"
    # Portable in-place rewrite (no `sed -i`: works on both GNU and BSD sed).
    find "${JF_DST}" -type f \( -name '*.yaml' -o -name '*.yml' \) 2>/dev/null | while IFS= read -r f; do
        sed -e "s/127\.0\.0\.1/${MATCLAW_MONGO_HOST}/g" \
            -e "s/localhost/${MATCLAW_MONGO_HOST}/g" \
            -e "s#\(key_filename:[[:space:]]*\)[^[:space:]]*/#\1${SSH_DST}/#g" \
            "$f" > "${f}.matclaw.tmp" && mv "${f}.matclaw.tmp" "$f"
    done
    export JFREMOTE_PROJECTS_FOLDER="${JF_DST}"
fi

# 2. SSH keys: tighten perms on a writable copy; pre-seed known_hosts for the HPC
#    hosts named in the jfremote config (everything that is not the Mongo host).
if [ -d "${SSH_SRC}" ]; then
    mkdir -p "${SSH_DST}"
    cp -a "${SSH_SRC}/." "${SSH_DST}/" 2>/dev/null || true
    chmod 700 "${SSH_DST}" 2>/dev/null || true
    find "${SSH_DST}" -type f -exec chmod 600 {} + 2>/dev/null || true
    if [ -d "${JF_DST}" ] && command -v ssh-keyscan >/dev/null 2>&1; then
        hosts="$(grep -rhoE 'host:[[:space:]]*[A-Za-z0-9._-]+' "${JF_DST}" 2>/dev/null \
            | awk '{print $2}' \
            | grep -vE "^(127\.0\.0\.1|localhost|${MATCLAW_MONGO_HOST})$" \
            | sort -u || true)"
        for h in ${hosts}; do
            ssh-keyscan -T 5 "${h}" >> "${SSH_DST}/known_hosts" 2>/dev/null || true
        done
        chmod 600 "${SSH_DST}/known_hosts" 2>/dev/null || true
    fi
fi

# 3. Hand off. PID 1 reaping is handled by `docker run --init`.
exec matclaw "$@"
