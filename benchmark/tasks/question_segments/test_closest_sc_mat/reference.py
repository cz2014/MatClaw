"""Reference solution for test_closest_sc_mat.
Source: test_supercells.py, lines 37-61
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
import numpy as np

# --- Fixture setup ---

# test_dir
test_dir = Path("/Users/cz/Work/MatTools_temp/src/tool_source_code/pymatgen-analysis-defects/tests/test_files")

# --- Reference test code ---

si_o_structs = loadfn(test_dir / "Si-O_structs.json")
ref_sc_mat = [[2, 1, 2], [2, 0, 3], [2, 1, 1]]

vg = VacancyGenerator()

def get_vac(s, sc_mat):
    vac = next(vg.generate(s, rm_species=["O"]))
    return vac.get_supercell_structure(sc_mat=sc_mat)

def check_uc(uc_struct, sc_mat) -> None:
    vac_sc = get_vac(uc_struct, sc_mat)
    sorted_results = get_closest_sc_mat(uc_struct, vac_sc, debug=True)
    min_dist = sorted_results[0][0]
    close_mats = [r[2] for r in sorted_results if r[0] < min_dist * 1.1]
    is_matched = [np.allclose(ref_sc_mat, x) for x in close_mats]
    assert any(is_matched)

for s in si_o_structs:
    check_uc(s, ref_sc_mat)

uc_struct = si_o_structs[0]
vac_struct = get_vac(uc_struct, ref_sc_mat)
res = get_closest_sc_mat(uc_struct=uc_struct, sc_struct=vac_struct, debug=False)
assert np.allclose(res, ref_sc_mat)
