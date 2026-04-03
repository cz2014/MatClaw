"""Reference solution for test_generate_all_native_defects.
Source: test_generators.py, lines 94-99
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
from pymatgen.io.vasp.outputs import Chgcar

# --- Fixture setup ---

# test_dir
test_dir = Path("/Users/cz/Work/MatTools_temp/src/tool_source_code/pymatgen-analysis-defects/tests/test_files")

# chgcar_fe3o4
chgcar_fe3o4 = Chgcar.from_file(test_dir / "CHGCAR.Fe3O4.vasp")

# --- Reference test code ---

gen = generate_all_native_defects(chgcar_fe3o4)
assert len(list(gen)) == 14

gen = generate_all_native_defects(chgcar_fe3o4.structure)
assert len(list(gen)) == 10
