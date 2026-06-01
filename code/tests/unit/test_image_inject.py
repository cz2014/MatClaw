"""Unit test for the image-injection callback mechanism (offline, no LLM).

Verifies `_inject_workspace_images` detects new workspace PNGs and attaches them to a step's
`observations_images`. The "can the model actually see an image" check is a separate Live-tier
test: `test_live_smoke.py::test_live_gemini_vision` (Gemini 3.5 Flash + a synthetic image).
"""

from __future__ import annotations

import PIL.Image


def test_callback_unit(tmp_path):
    """_inject_workspace_images finds new PNGs and sets observations_images (once each)."""
    from core._smol import ActionStep
    from core._smol.memory import Timing

    from core.agent import _inject_workspace_images

    work = tmp_path
    PIL.Image.new("RGB", (2, 2), color="red").save(work / "test.png")

    cb = _inject_workspace_images(work)

    # First call: finds test.png
    step = ActionStep(step_number=0, timing=Timing(start_time=0.0))
    cb(step, None)
    assert step.observations_images is not None
    assert len(step.observations_images) == 1
    assert isinstance(step.observations_images[0], PIL.Image.Image)

    # Second call, fresh step: file already seen -> no new images
    step2 = ActionStep(step_number=1, timing=Timing(start_time=1.0))
    cb(step2, None)
    assert step2.observations_images is None

    # A new PNG is detected
    PIL.Image.new("RGB", (3, 3), color="blue").save(work / "test2.png")
    step3 = ActionStep(step_number=2, timing=Timing(start_time=2.0))
    cb(step3, None)
    assert step3.observations_images is not None
    assert len(step3.observations_images) == 1


if __name__ == "__main__":
    import tempfile
    from pathlib import Path

    with tempfile.TemporaryDirectory() as d:
        test_callback_unit(Path(d))
    print("PASS: test_callback_unit")
