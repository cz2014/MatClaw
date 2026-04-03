"""Reference solution for test_get_avg_chg.
Source: test_utils.py, lines 50-56
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
import pytest

# --- Fixture setup ---

# test_dir
test_dir = Path("/Users/cz/Work/MatTools_temp/src/tool_source_code/pymatgen-analysis-defects/tests/test_files")

# gan_struct
gan_struct = Structure.from_file(test_dir / "GaN.vasp")

# --- Reference test code ---

data = np.ones((48, 48, 48))
chgcar = Chgcar(poscar=gan_struct, data={"total": data})
fpos = [0.1, 0.1, 0.1]
avg_chg_sphere = get_avg_chg(chgcar, fpos)
avg_chg = np.sum(chgcar.data["total"]) / chgcar.ngridpts / chgcar.structure.volume
pytest.approx(avg_chg_sphere, avg_chg)
