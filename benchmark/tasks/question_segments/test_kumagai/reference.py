"""Reference solution for test_kumagai.
Source: test_corrections.py, lines 78-91
"""

from pathlib import Path

from pymatgen.analysis.defects.corrections.freysoldt import (
    get_freysoldt_correction,
    plot_plnr_avg,
)
from pymatgen.analysis.defects.corrections.kumagai import (
    get_efnv_correction,
    get_structure_with_pot,
)
import pytest

# --- Fixture setup ---

# test_dir
test_dir = Path("/Users/cz/Work/MatTools_temp/src/tool_source_code/pymatgen-analysis-defects/tests/test_files")

# --- Reference test code ---

sb = get_structure_with_pot(test_dir / "Mg_Ga" / "bulk_sc")
sd0 = get_structure_with_pot(test_dir / "Mg_Ga" / "q=0")
sd1 = get_structure_with_pot(test_dir / "Mg_Ga" / "q=1")

res0 = get_efnv_correction(
    0, sd0, sb, dielectric_tensor=[[1, 0, 0], [0, 1, 0], [0, 0, 1]]
)
assert res0.correction_energy == pytest.approx(0, abs=1e-4)

res1 = get_efnv_correction(
    1, sd1, sb, dielectric_tensor=[[1, 0, 0], [0, 1, 0], [0, 0, 1]]
)
assert res1.correction_energy > 0
