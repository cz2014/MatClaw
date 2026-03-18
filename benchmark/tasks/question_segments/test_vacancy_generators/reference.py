"""Reference solution for test_vacancy_generators.
Source: test_generators.py, lines 14-29
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
import pytest

# --- Fixture setup ---

# test_dir
test_dir = Path("/Users/cz/Work/MatTools_temp/src/tool_source_code/pymatgen-analysis-defects/tests/test_files")

# gan_struct
gan_struct = Structure.from_file(test_dir / "GaN.vasp")

# --- Reference test code ---

vacancy_generator = VacancyGenerator().get_defects(gan_struct)
for defect in vacancy_generator:
    assert isinstance(defect, Vacancy)

vacancy_generator = VacancyGenerator().get_defects(gan_struct, ["Ga"])
cnt = 0
for defect in vacancy_generator:
    assert isinstance(defect, Vacancy)
    cnt += 1
assert cnt == 1

with pytest.raises(ValueError):
    vacancy_generator = list(
        VacancyGenerator().get_defects(gan_struct, rm_species=["Xe"])
    )
