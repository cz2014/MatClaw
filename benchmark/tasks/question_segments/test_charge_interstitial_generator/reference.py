"""Reference solution for test_charge_interstitial_generator.
Source: test_generators.py, lines 74-81
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

gen = ChargeInterstitialGenerator().get_defects(chgcar_fe3o4, {"Ga"})
cnt = 0
for defect in gen:
    assert isinstance(defect, Interstitial)
    assert defect.site.specie.symbol == "Ga"
    cnt += 1
assert cnt == 2
