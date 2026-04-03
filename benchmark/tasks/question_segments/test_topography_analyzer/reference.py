"""Reference solution for test_topography_analyzer.
Source: test_utils.py, lines 79-89
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
import numpy as np
import pytest

# --- Fixture setup ---

# test_dir
test_dir = Path("/Users/cz/Work/MatTools_temp/src/tool_source_code/pymatgen-analysis-defects/tests/test_files")

# chgcar_fe3o4
chgcar_fe3o4 = Chgcar.from_file(test_dir / "CHGCAR.Fe3O4.vasp")

# --- Reference test code ---

struct = chgcar_fe3o4.structure
ta = TopographyAnalyzer(struct, ["Fe", "O"], [], check_volume=True)
node_struct = ta.get_structure_with_nodes()
# All sites with species X
dummy_sites = [site for site in node_struct if site.specie.symbol == "X"]
assert len(dummy_sites) == 100

# Check value error
with pytest.raises(ValueError):
    ta = TopographyAnalyzer(struct, ["O"], ["Fe"], check_volume=True)
