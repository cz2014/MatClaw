"""Reference solution for test_interstitial.
Source: test_core.py, lines 117-143
"""

from pathlib import Path

from pymatgen.analysis.defects.core import (
    Adsorbate,
    DefectComplex,
    Interstitial,
    NamedDefect,
    PeriodicSite,
    Substitution,
    Vacancy,
)
from pymatgen.analysis.defects.finder import DefectSiteFinder
from pymatgen.core import Structure
from pymatgen.core.periodic_table import Element, Specie
import numpy as np

# --- Fixture setup ---

# test_dir
test_dir = Path("/Users/cz/Work/MatTools_temp/src/tool_source_code/pymatgen-analysis-defects/tests/test_files")

# gan_struct
gan_struct = Structure.from_file(test_dir / "GaN.vasp")

# --- Reference test code ---

s = gan_struct.copy()
inter_fpos = [0, 0, 0.75]
n_site = PeriodicSite(Specie("N"), inter_fpos, s.lattice)
inter = Interstitial(s, n_site)
assert inter.oxi_state == 3
assert inter.get_charge_states() == [-1, 0, 1, 2, 3, 4]
assert np.allclose(inter.defect_structure[0].frac_coords, inter_fpos)
sc = inter.get_supercell_structure()
assert sc.formula == "Ga64 N65"
assert inter.name == "N_i"
assert str(inter) == "N intersitial site at [0.00,0.00,0.75]"
assert inter.element_changes == {Element("N"): 1}
assert inter.latex_name == r"N$_{\rm i}$"

# test target_frac_coords with get_supercell_structure
finder = DefectSiteFinder()
fpos = finder.get_defect_fpos(sc, inter.structure)
assert np.allclose(fpos, [0, 0, 0.398096581])
# change target coords:
inter_sc_struct = inter.get_supercell_structure(target_frac_coords=[0.3, 0.5, 0.9])
fpos = finder.get_defect_fpos(inter_sc_struct, inter.structure)
assert np.allclose(fpos, [0.25, 0.5, 0.89809658])  # closest equivalent site

inter2 = Interstitial(s, n_site)
inter2.user_charges = [-100, 102]
assert inter2.get_charge_states() == [-100, 102]
