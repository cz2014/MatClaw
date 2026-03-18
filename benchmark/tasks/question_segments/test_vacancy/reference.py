"""Reference solution for test_vacancy.
Source: test_core.py, lines 16-29
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
vac = Vacancy(s, s.sites[0])
vac2 = Vacancy(s, s.sites[1])
assert vac == vac2  # symmetry equivalent sites
assert str(vac) == "Ga Vacancy defect at site #0"
assert vac.oxi_state == -3
assert vac.get_charge_states() == [-4, -3, -2, -1, 0, 1]
assert vac.get_multiplicity() == 2
assert vac.get_supercell_structure().formula == "Ga63 N64"
assert vac.name == "v_Ga"
assert vac == vac
assert vac.element_changes == {Element("Ga"): -1}
assert vac.latex_name == r"v$_{\rm Ga}$"
