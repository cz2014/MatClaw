"""Reference solution for test_get_local_extrema.
Source: test_utils.py, lines 19-28
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
from pymatgen.core import Structure
from pymatgen.core.periodic_table import Specie
from pymatgen.io.vasp.outputs import Chgcar
import numpy as np

# --- Fixture setup ---

# test_dir
test_dir = Path("/Users/cz/Work/MatTools_temp/src/tool_source_code/pymatgen-analysis-defects/tests/test_files")

# gan_struct
gan_struct = Structure.from_file(test_dir / "GaN.vasp")

# --- Reference test code ---

data = np.ones((48, 48, 48))
chgcar = Chgcar(poscar=gan_struct, data={"total": data})
frac_pos = [[0, 0, 0], [0.25, 0.25, 0.25], [0.5, 0.5, 0.5], [0.75, 0.75, 0.75]]
for fpos in frac_pos:
    idx = np.multiply(fpos, chgcar.data["total"].shape).astype(int)
    chgcar.data["total"][idx[0], idx[1], idx[2]] = 0
loc_min = get_local_extrema(chgcar, frac_pos)
for a, b in zip(sorted(loc_min.tolist()), sorted(frac_pos)):
    assert np.allclose(a, b)
