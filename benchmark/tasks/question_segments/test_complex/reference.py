"""Reference solution for test_complex.
Source: test_core.py, lines 155-177
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
o_site = PeriodicSite(Specie("O"), s[3].frac_coords, s.lattice)
sub = Substitution(s, o_site)  # O substituted on N site
vac = Vacancy(s, s.sites[0])  # Ga vacancy
inter = Interstitial(
    s, PeriodicSite(Specie("H"), [0, 0, 0.75], s.lattice)
)  # H interstitial
dc = DefectComplex([sub, vac])
assert dc.name == "O_N+v_Ga"
sc_struct = dc.get_supercell_structure()
assert sc_struct.formula == "Ga63 N63 O1"
dc.oxi_state == sub.oxi_state + vac.oxi_state
dc.element_changes == {Element("Ga"): -1, Element("N"): -1, Element("O"): 1}
dc.defect_structure.formula == "Ga1 N1 O1"

dc2 = DefectComplex([sub, vac, inter])
assert dc2.name == "O_N+v_Ga+H_i"
sc_struct = dc2.get_supercell_structure(dummy_species="Xe")
assert sc_struct.formula == "Ga63 H1 Xe1 N63 O1"  # Three defects only one dummy

assert dc2 == dc2
assert dc2 != dc
