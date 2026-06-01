# syntax=docker/dockerfile:1
#
# MatClaw runtime image (P3) -- containerizes the WHOLE `matclaw run` process.
# The in-process LocalPythonExecutor is bounded by this container; the container
# is the security boundary (see docs/exec-plans/.../2026-05-31_p3_docker_runtime.md).
#
# Build from the repo root:
#   docker build -f docker/Dockerfile \
#     --build-arg UID=$(id -u) --build-arg GID=$(id -g) -t matclaw:dev .
#
# Run via the hardened wrapper:  docker/run.sh run --project perlmutter --task /work/workspace/task.txt
# Operator guide:                docs/references/docker-runtime.md

ARG PYTHON_VERSION=3.12

# ------------------------------------------------------------------------------
# Stage 1: builder -- resolve + install the pinned dependency set with uv.
# This pre-installs today's allow-list / common scientific stack (numpy, scipy,
# pymatgen, ase, atomate2, jobflow(-remote), dpdata, matplotlib, ...) so the
# opened runtime (P4) rarely needs to install at run time.
# ------------------------------------------------------------------------------
FROM python:${PYTHON_VERSION}-slim AS builder

# uv pinned for reproducible builds (the uv that produced code/uv.lock; bump deliberately).
COPY --from=ghcr.io/astral-sh/uv:0.10.11 /uv /uvx /bin/

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

# Compilers for any dependency without a manylinux wheel.
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
    && rm -rf /var/lib/apt/lists/*

# IMPORTANT: keep the project at the SAME path (/app) in both stages so the
# editable install's path reference resolves at runtime, and the venv lives at
# /app/.venv (its absolute paths must match between stages).
WORKDIR /app

# Layer 1 (cached): dependencies only, from the committed lockfile.
COPY code/pyproject.toml code/uv.lock code/.python-version ./
RUN uv sync --frozen --no-install-project --no-dev

# Layer 2: the project source + install the matclaw package (core/, remote_jobs/).
COPY code/ ./
RUN uv sync --frozen --no-dev

# ------------------------------------------------------------------------------
# Stage 2: runtime
# ------------------------------------------------------------------------------
FROM python:${PYTHON_VERSION}-slim AS runtime

# Runtime tooling the agent uses inside the container:
#   ca-certificates  TLS trust (LLM APIs, PyPI, Mongo TLS)
#   ripgrep          the P4 search_code helper (image built P4-ready)
#   openssh-client   ssh-keyscan (known_hosts seeding) + ad-hoc ssh/scp
#   git, curl        VCS installs + ad-hoc downloads
#   build-essential  compile source-only packages the agent installs at run time
RUN apt-get update && apt-get install -y --no-install-recommends \
        ca-certificates \
        ripgrep \
        openssh-client \
        git \
        curl \
        build-essential \
    && rm -rf /var/lib/apt/lists/*

# Non-root user. Match the host owner of ~/.ssh so the read-only-mounted keys are
# readable: pass --build-arg UID=$(id -u) --build-arg GID=$(id -g) at build time.
ARG UID=1000
ARG GID=1000
RUN groupadd -g "${GID}" agent 2>/dev/null || groupmod -n agent "$(getent group ${GID} | cut -d: -f1)" 2>/dev/null || true \
    && useradd -m -u "${UID}" -g "${GID}" -s /bin/bash agent

# Bring the source + uv-built venv across at the identical path (/app, /app/.venv).
COPY --from=builder /app /app

ENV PATH="/app/.venv/bin:${PATH}" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    # caches default under the agent home; mount the optional matclaw-env volume
    # at /home/agent to persist them (fast re-installs) across disposable runs.
    UV_CACHE_DIR=/home/agent/.cache/uv \
    PIP_CACHE_DIR=/home/agent/.cache/pip \
    MPLCONFIGDIR=/home/agent/.config/matplotlib

# Entrypoint: rewrite the jfremote Mongo host -> host.docker.internal, seed
# known_hosts, then exec matclaw. See docker/entrypoint.sh.
COPY docker/entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh \
    && mkdir -p /work/workspace /home/agent/.cache /home/agent/.config \
    && chown -R "${UID}:${GID}" /app /home/agent /work

USER agent
WORKDIR /work/workspace

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
CMD ["--help"]
