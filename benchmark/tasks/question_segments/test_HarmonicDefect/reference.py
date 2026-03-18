"""Reference solution for test_HarmonicDefect.
Source: test_ccd.py, lines 68-102
"""

from collections import namedtuple
from pathlib import Path

from pymatgen.analysis.defects.ccd import (
    HarmonicDefect,
    _get_wswq_slope,
    plot_pes,
)
from pymatgen.analysis.defects.ccd import HarmonicDefect
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

# hd0
_vaspruns_hd0 = v_ga[(0, -1)]["vaspruns"]
_procar_hd0 = v_ga[(0, -1)]["procar"]
hd0 = HarmonicDefect.from_vaspruns(
    _vaspruns_hd0,
    charge_state=0,
    procar=_procar_hd0,
    store_bandstructure=True,
)

# --- Reference test code ---

# test other basic reading functions for HarmonicDefect
vaspruns = v_ga[(0, -1)]["vaspruns"]
procar = v_ga[(0, -1)]["procar"]
hd0 = HarmonicDefect.from_vaspruns(
    vaspruns,
    charge_state=0,
    procar=procar,
    store_bandstructure=True,
)
assert hd0.defect_band == [(138, 0, 1), (138, 1, 1)]

hd0p = HarmonicDefect.from_directories(
    directories=[test_dir / "v_Ga" / "ccd_0_-1" / str(i) for i in range(3)],
    charge_state=0,
)
assert hd0p.defect_band == [(138, 0, 1), (138, 1, 1)]

hd2 = HarmonicDefect.from_vaspruns(
    vaspruns, charge_state=0, procar=procar, defect_band=((139, 0, 1), (139, 1, 1))
)
assert hd2.spin_index == 1

vaspruns = v_ga[(0, -1)]["vaspruns"]
procar = v_ga[(0, -1)]["procar"]
# check for ValueError when you have non-unique spin for the defect band
with pytest.raises(ValueError) as e:
    hd3 = HarmonicDefect.from_vaspruns(
        vaspruns,
        charge_state=0,
        procar=procar,
        defect_band=((139, 0, 1), (139, 1, 0)),
    )
    hd3.spin
assert "Spin index" in str(e.value)
