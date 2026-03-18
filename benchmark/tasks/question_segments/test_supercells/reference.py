"""Reference solution for test_supercells.
Source: test_supercells.py, lines 13-24
"""

from pathlib import Path

from monty.serialization import loadfn
from pymatgen.analysis.defects.generators import VacancyGenerator
from pymatgen.analysis.defects.supercells import (
    _ase_cubic,
    get_closest_sc_mat,
    get_matched_structure_mapping,
    get_sc_fromstruct,
)
from pymatgen.core import Structure
import numpy as np

# --- Fixture setup ---

# test_dir
test_dir = Path("/Users/cz/Work/MatTools_temp/src/tool_source_code/pymatgen-analysis-defects/tests/test_files")

# gan_struct
gan_struct = Structure.from_file(test_dir / "GaN.vasp")

# --- Reference test code ---

uc = gan_struct.copy()
sc_mat = get_sc_fromstruct(uc)
sc = uc * sc_mat
assert sc_mat.shape == (3, 3)

sc_mat2, _ = get_matched_structure_mapping(uc, sc)
assert sc_mat2.shape == (3, 3)
sc2 = uc * sc_mat2
np.testing.assert_allclose(
    sc.lattice.abc, sc2.lattice.abc
)  # the sc_mat can be reconstructed from the sc
