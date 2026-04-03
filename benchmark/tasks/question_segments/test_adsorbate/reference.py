"""Reference solution for test_adsorbate.
Source: test_core.py, lines 146-152
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
ads_fpos = [0, 0, 0.75]
n_site = PeriodicSite(Specie("N"), ads_fpos, s.lattice)
ads = Adsorbate(s, n_site)
assert ads.name == "N_{ads}"
assert str(ads) == "N adsorbate site at [0.00,0.00,0.75]"
