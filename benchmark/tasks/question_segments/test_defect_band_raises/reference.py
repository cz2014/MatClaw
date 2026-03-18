"""Reference solution for test_defect_band_raises.
Source: test_ccd.py, lines 48-65
"""

from collections import namedtuple
from pathlib import Path

from pymatgen.analysis.defects.ccd import (
    HarmonicDefect,
    _get_wswq_slope,
    plot_pes,
)
from pymatgen.analysis.defects.plotting.optics import plot_optical_transitions
from pymatgen.io.vasp.outputs import WSWQ, Vasprun, Procar
from pymatgen.io.vasp.outputs import Waveder
import numpy as np
import pandas as pd
import pytest

# --- Fixture setup ---

# test_dir
test_dir = Path("/Users/cz/Work/MatTools_temp/src/tool_source_code/pymatgen-analysis-defects/tests/test_files")

# v_ga
v_ga = dict()
for q1, q2 in [(0, -1), (-1, 0)]:
    ccd_dir = test_dir / f"v_Ga/ccd_{q1}_{q2}"
    vaspruns = [Vasprun(ccd_dir / f"{i}/vasprun.xml") for i in [0, 1, 2]]
    wswq_dir = ccd_dir / "wswqs"
    wswq_files = sorted(
        [f for f in wswq_dir.glob("WSWQ*")],
        key=lambda x: int(x.name.split(".")[1])
    )
    wswqs = [WSWQ.from_file(f) for f in wswq_files]
    v_ga[(q1, q2)] = {
        "vaspruns": vaspruns,
        "procar": Procar(ccd_dir / "1/PROCAR"),
        "wswqs": wswqs,
    }

# --- Reference test code ---

vaspruns = v_ga[(0, -1)]["vaspruns"]
procar = v_ga[(0, -1)]["procar"]
hd0 = HarmonicDefect.from_vaspruns(
    vaspruns,
    charge_state=0,
    procar=procar,
    store_bandstructure=True,
)
# mis-matched defect band
hd0.defect_band = [(138, 0, 1), (139, 1, 1)]
with pytest.raises(ValueError):
    assert hd0.defect_band_index

# mis-matched defect spin
hd0.defect_band = [(138, 0, 1), (138, 1, 0)]
with pytest.raises(ValueError):
    assert hd0.spin_index == 1
