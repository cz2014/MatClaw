"""Reference solution for test_substitution_generators.
Source: test_generators.py, lines 32-49
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

sub_generator = SubstitutionGenerator().get_defects(
    gan_struct, {"Ga": ["Mg", "Ca"]}
)
replaced_atoms = set()
for defect in sub_generator:
    assert isinstance(defect, Substitution)
    replaced_atoms.add(defect.site.specie.symbol)
assert replaced_atoms == {"Mg", "Ca"}

sub_generator = SubstitutionGenerator().get_defects(gan_struct, {"Ga": "Mg"})
replaced_atoms = set()
for defect in sub_generator:
    assert isinstance(defect, Substitution)
    replaced_atoms.add(defect.site.specie.symbol)
assert replaced_atoms == {
    "Mg",
}
