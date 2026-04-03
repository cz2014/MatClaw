"""Reference solution for test_ase_supercells.
Source: test_supercells.py, lines 27-34
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
import pytest

# --- Fixture setup ---

# test_dir
test_dir = Path("/Users/cz/Work/MatTools_temp/src/tool_source_code/pymatgen-analysis-defects/tests/test_files")

# gan_struct
gan_struct = Structure.from_file(test_dir / "GaN.vasp")

# --- Reference test code ---

sc_mat = _ase_cubic(gan_struct, min_atoms=4, max_atoms=8, min_length=1.0)
sc = gan_struct * sc_mat
assert 4 <= sc.num_sites <= 8

# check raise
with pytest.raises(RuntimeError):
    _ase_cubic(gan_struct, min_atoms=4, max_atoms=8, min_length=10)
