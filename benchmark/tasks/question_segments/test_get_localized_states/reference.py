"""Reference solution for test_get_localized_states.
Source: test_utils.py, lines 92-115
"""

from pathlib import Path

from pymatgen.analysis.defects.core import Interstitial, PeriodicSite, Vacancy
from pymatgen.analysis.defects.utils import (
    ChargeInsertionAnalyzer,
    TopographyAnalyzer,
    cluster_nodes,
    get_avg_chg,
    get_local_extrema,
    get_localized_states,
    get_plane_spacing,
    group_docs,
)
from pymatgen.analysis.structure_matcher import StructureMatcher
from pymatgen.core.periodic_table import Specie
from pymatgen.io.vasp.outputs import Chgcar
from pymatgen.io.vasp.outputs import WSWQ, Vasprun, Procar
import numpy as np

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
vr = vaspruns[1]
bs = vr.get_band_structure()
get_localized_states(bs, procar=procar)
loc_bands = set()
for iband, _ikpt, _ispin, _val in get_localized_states(bs, procar=procar):
    loc_bands.add(iband)
assert loc_bands == {
    138,
}

vaspruns = v_ga[(-1, 0)]["vaspruns"]
procar = v_ga[(-1, 0)]["procar"]
vr = vaspruns[1]
bs = vr.get_band_structure()

loc_bands = set()
for iband, _ikpt, _ispin, _val in get_localized_states(
    bs, procar=procar, band_window=100
):
    loc_bands.add(iband)
assert loc_bands == {75, 77}  # 75 and 77 are more localized core states
