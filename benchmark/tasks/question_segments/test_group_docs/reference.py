"""Reference solution for test_group_docs.
Source: test_utils.py, lines 118-160
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

s = gan_struct.copy()
vac1 = Vacancy(s, s.sites[0])
vac2 = Vacancy(s, s.sites[1])
vac3 = Vacancy(s, s.sites[2])
vac4 = Vacancy(s, s.sites[3])

def get_interstitial(fpos):
    n_site = PeriodicSite(Specie("N"), fpos, s.lattice)
    return Interstitial(s, n_site)

# two interstitials are at inequivalent sites so should be in different groups
int1 = get_interstitial([0.0, 0.0, 0.0])
int2 = get_interstitial([0.0, 0.0, 0.25])
sm = StructureMatcher()
# Test that the grouping works without a key function (only structure)
sgroups = group_docs(
    [vac1, vac2, int1, vac3, vac4, int2],
    sm,
    lambda x: x.defect_structure,
)
res = []
for _, group in sgroups:
    defect_names = ",".join([x.name for x in group])
    res.append(defect_names)
# the final sorted groups
assert "|".join(sorted(res)) == "N_i|N_i|v_Ga,v_Ga|v_N,v_N"

# Test that the grouping works with a key function (structure and name)
sgroups = group_docs(
    [vac1, vac2, int1, vac3, vac4, int1, int2],
    sm,
    lambda x: x.defect_structure,
    lambda x: x.name,
)
res = []
g_names = []
for name, group in sgroups:
    defect_names = ",".join([x.name for x in group])
    g_names.append(name)
    res.append(defect_names)
assert "|".join(sorted(res)) == "N_i|N_i,N_i|v_Ga,v_Ga|v_N,v_N"
assert "|".join(sorted(g_names)) == "N_i:0|N_i:1|v_Ga|v_N"
