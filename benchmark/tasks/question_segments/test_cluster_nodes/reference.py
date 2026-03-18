"""Reference solution for test_cluster_nodes.
Source: test_utils.py, lines 31-47
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

frac_pos = [
    [0, 0, 0],
    [0.25, 0.25, 0.25],
    [0.5, 0.5, 0.5],
    [0.75, 0.75, 0.75],
]
added = [
    [0.0002, 0.0001, 0.0001],
    [0.0002, 0.0002, 0.0003],
    [0.25001, 0.24999, 0.24999],
    [0.25, 0.249999, 0.250001],
]  # all the displacements are positive so we dont have to worry about periodic boundary conditions
clusters = cluster_nodes(frac_pos + added, gan_struct.lattice)

for a, b in zip(sorted(clusters.tolist()), sorted(frac_pos)):
    assert np.allclose(a, b, atol=0.001)
