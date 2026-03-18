"""Reference solution for test_wswq_slope.
Source: test_ccd.py, lines 124-134
"""

from collections import namedtuple

from pymatgen.analysis.defects.ccd import (
    HarmonicDefect,
    _get_wswq_slope,
    plot_pes,
)
from pymatgen.analysis.defects.plotting.optics import plot_optical_transitions
from pymatgen.io.vasp.outputs import Waveder
import numpy as np
import pandas as pd

# --- Reference test code ---

# Make sure the the slope is automatically defined as the sign of the distoration changes.
mats = [np.ones((3, 5)), np.zeros((3, 5)), np.ones((3, 5))]
FakeWSWQ = namedtuple("FakeWSWQ", ["data"])
fake_wswqs = [FakeWSWQ(data=m) for m in mats]

res = _get_wswq_slope([-0.5, 0, 0.5], fake_wswqs)
assert np.allclose(res, np.ones((3, 5)) * 2)

res = _get_wswq_slope([1.0, 0, -1.0], fake_wswqs)
assert np.allclose(res, np.ones((3, 5)) * 1)
