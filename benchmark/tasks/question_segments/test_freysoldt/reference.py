"""Reference solution for test_freysoldt.
Source: test_corrections.py, lines 12-48
"""

from collections import defaultdict
from pathlib import Path

from pymatgen.analysis.defects.corrections.freysoldt import (
    get_freysoldt_correction,
    plot_plnr_avg,
)
from pymatgen.analysis.defects.corrections.kumagai import (
    get_efnv_correction,
    get_structure_with_pot,
)
from pymatgen.io.vasp.outputs import Vasprun, Locpot
import pytest

# --- Fixture setup ---

# test_dir
test_dir = Path("/Users/cz/Work/MatTools_temp/src/tool_source_code/pymatgen-analysis-defects/tests/test_files")

# data_Mg_Ga
root_dir = test_dir / "Mg_Ga"
data_Mg_Ga = defaultdict(dict)
for fold in root_dir.glob("./*"):
    if not fold.is_dir():
        continue
    data_Mg_Ga[fold.name] = {
        "vasprun": Vasprun(fold / "vasprun.xml.gz"),
        "locpot": Locpot.from_file(fold / "LOCPOT.gz"),
    }

# --- Reference test code ---

"""Older basic test for Freysoldt correction."""
bulk_locpot = data_Mg_Ga["bulk_sc"]["locpot"]
defect_locpot = data_Mg_Ga["q=0"]["locpot"]

freysoldt_summary = get_freysoldt_correction(
    q=0,
    dielectric=14,
    defect_locpot=defect_locpot,
    bulk_locpot=bulk_locpot,
    defect_frac_coords=[0.5, 0.5, 0.5],
)
assert freysoldt_summary.correction_energy == pytest.approx(0, abs=1e-4)

# simple check that the plotter works
plot_plnr_avg(freysoldt_summary.metadata["plot_data"][0])

# different ways to specify the locpot
freysoldt_summary = get_freysoldt_correction(
    q=0,
    dielectric=14,
    lattice=defect_locpot.structure.lattice,
    defect_locpot=defect_locpot,
    bulk_locpot=bulk_locpot,
    defect_frac_coords=[0.5, 0.5, 0.5],
)

defect_locpot_dict = {str(k): defect_locpot.get_axis_grid(k) for k in [0, 1, 2]}
bulk_locpot_dict = {str(k): bulk_locpot.get_axis_grid(k) for k in [0, 1, 2]}
freysoldt_summary = get_freysoldt_correction(
    q=0,
    dielectric=14,
    lattice=defect_locpot.structure.lattice,
    defect_locpot=defect_locpot_dict,
    bulk_locpot=bulk_locpot_dict,
    defect_frac_coords=[0.5, 0.5, 0.5],
)
