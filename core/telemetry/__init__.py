"""OpenTelemetry instrumentation for smolagents with Phoenix backend."""

import os
import logging

_logger = logging.getLogger(__name__)

TELEMETRY_ENV_VAR = "MLFF_ENABLE_TELEMETRY"


def setup_telemetry(project_name: str = "matclaw") -> bool:
    """Initialize OpenTelemetry tracing with Phoenix backend.

    Must be called BEFORE creating any agents.

    Args:
        project_name: Name for the tracing project in Phoenix UI.

    Returns:
        True if telemetry was initialized, False if skipped.

    Raises:
        ImportError: If telemetry is enabled but packages are missing.
    """
    if os.environ.get(TELEMETRY_ENV_VAR, "").lower() not in ("1", "true", "yes"):
        return False

    try:
        from phoenix.otel import register
        from openinference.instrumentation.smolagents import SmolagentsInstrumentor
    except ImportError as e:
        raise ImportError(
            f"Telemetry enabled but packages missing: {e}. "
            f"Install with: pip install -e '.[telemetry]'"
        ) from e

    register(project_name=project_name)
    SmolagentsInstrumentor().instrument()

    _logger.info("Telemetry initialized: project=%s", project_name)
    return True
