"""Reference solution for test_interstitial_generator.
Source: test_generators.py, lines 58-71
"""

from pathlib import Path

from pymatgen.analysis.defects.core import Interstitial, Substitution, Vacancy
from pymatgen.analysis.defects.generators import (
    AntiSiteGenerator,
    ChargeInterstitialGenerator,
    InterstitialGenerator,
    SubstitutionGenerator,
    VacancyGenerator,
    VoronoiInterstitialGenerator,
    generate_all_native_defects,
)
from pymatgen.core import Structure

# --- Fixture setup ---

# test_dir
test_dir = Path("/Users/cz/Work/MatTools_temp/src/tool_source_code/pymatgen-analysis-defects/tests/test_files")

# gan_struct
gan_struct = Structure.from_file(test_dir / "GaN.vasp")

# --- Reference test code ---

gen = InterstitialGenerator().get_defects(
    gan_struct, insertions={"Mg": [[0, 0, 0]]}
)
l_gen = list(gen)
assert len(l_gen) == 1
assert str(l_gen[0]) == "Mg intersitial site at [0.00,0.00,0.00]"

bad_site = [0.667, 0.333, 0.875]
gen = InterstitialGenerator().get_defects(
    gan_struct, insertions={"Mg": [[0, 0, 0], bad_site]}
)
l_gen = list(gen)
assert len(l_gen) == 1
