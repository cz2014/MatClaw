"""Reference solution for test_SRHCapture.
Source: test_ccd.py, lines 137-161
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

# hd1
_vaspruns_hd1 = v_ga[(-1, 0)]["vaspruns"]
_procar_hd1 = v_ga[(-1, 0)]["procar"]
hd1 = HarmonicDefect.from_vaspruns(
    _vaspruns_hd1,
    charge_state=1,
    procar=_procar_hd1,
    store_bandstructure=True,
)

# --- Reference test code ---

from pymatgen.analysis.defects.ccd import get_SRH_coefficient

hd0.read_wswqs(test_dir / "v_Ga" / "ccd_0_-1" / "wswqs")
c_n = get_SRH_coefficient(
    initial_state=hd0,
    final_state=hd1,
    defect_state=(138, 1, 1),
    T=[100, 200, 300],
    dE=1.0,
)
ref_results = [1.89187260e-34, 6.21019152e-33, 3.51501688e-31]
assert np.allclose(c_n, ref_results)

# expect RuntimeError
with pytest.raises(RuntimeError) as e:
    get_SRH_coefficient(
        initial_state=hd0,
        final_state=hd1,
        defect_state=hd1.defect_band[-1],
        T=[100, 200, 300],
        dE=1.0,
        use_final_state_elph=True,
    )
assert "WSWQ" in str(e.value)
