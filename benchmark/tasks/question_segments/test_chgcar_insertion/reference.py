"""Reference solution for test_chgcar_insertion.
Source: test_utils.py, lines 59-76
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

chgcar = chgcar_fe3o4
insert_ref = [
    (
        0.03692438178614583,
        [[0.0, 0.0, 0.0], [0.0, 0.0, 0.5], [0.0, 0.5, 0.0], [0.5, 0.0, 0.0]],
    ),  # corners and edge centers
    (
        0.10068764899215804,
        [[0.375, 0.375, 0.375], [0.625, 0.625, 0.625]],
    ),  # center of Fe-O cages
]
cia = ChargeInsertionAnalyzer(chgcar)
insert_groups = cia.filter_and_group(max_avg_charge=0.5)
for (avg_chg, group), (ref_chg, ref_fpos) in zip(insert_groups, insert_ref):
    fpos = sorted(group)
    pytest.approx(avg_chg, ref_chg)
    assert np.allclose(fpos, ref_fpos)
