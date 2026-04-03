"""Reference solution for test_parsing_and_grouping_NamedDefects.
Source: test_core.py, lines 180-197
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

# --- Reference test code ---

bulk_dir = test_dir / "Mg_Ga" / "bulk_sc"
defect_dir = test_dir / "Mg_Ga" / "q=0"
bulk_struct = Structure.from_file(bulk_dir / "CONTCAR.gz")
defect_struct = Structure.from_file(defect_dir / "CONTCAR.gz")

nd0 = NamedDefect.from_structures(
    defect_structure=defect_struct, bulk_structure=bulk_struct
)

assert nd0.element_changes == {Element("Mg"): 1, Element("Ga"): -1}
nd1 = NamedDefect(name="v_Ga", bulk_formula="GaN", element_changes={"Ga": -1})
nd2 = NamedDefect(
    name="Mg_Ga", bulk_formula="GaN", element_changes={"Mg": 1, "Ga": -1}
)
assert str(nd0) == "GaN:Mg_Ga"
assert nd0 != nd1
assert nd0 == nd2
