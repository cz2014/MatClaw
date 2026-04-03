"""Reference solution for test_defect_entry.
Source: test_thermo.py, lines 94-119
"""

from collections import defaultdict
from pathlib import Path
import copy
import os

from matplotlib import pyplot as plt
from pymatgen.analysis.defects.core import Interstitial, NamedDefect
from pymatgen.analysis.defects.core import PeriodicSite, Substitution
from pymatgen.analysis.defects.corrections.freysoldt import plot_plnr_avg
from pymatgen.analysis.defects.thermo import (
    Composition,
    ComputedEntry,
    DefectEntry,
    FormationEnergyDiagram,
    MultiFormationEnergyDiagram,
    ensure_stable_bulk,
    get_lower_envelope,
    get_transitions,
    group_defect_entries,
    plot_formation_energy_diagrams,
)
from pymatgen.analysis.defects.thermo import DefectEntry
from pymatgen.analysis.phase_diagram import PhaseDiagram
from pymatgen.core import Element, PeriodicSite
from pymatgen.core import Structure
from pymatgen.core.periodic_table import Specie
from pymatgen.io.vasp.outputs import Vasprun, Locpot
import numpy as np
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

# gan_struct
gan_struct = Structure.from_file(test_dir / "GaN.vasp")

# defect_Mg_Ga
ga_site = gan_struct[0]
mg_site = PeriodicSite(Specie("Mg"), ga_site.frac_coords, gan_struct.lattice)
defect_Mg_Ga = Substitution(gan_struct, mg_site)

# defect_entries_and_plot_data_Mg_Ga
bulk_locpot = data_Mg_Ga["bulk_sc"]["locpot"]
def _get_defect_entry_data(q):
    computed_entry = data_Mg_Ga[f"q={q}"]["vasprun"].get_computed_entry(inc_structure=True)
    defect_locpot = data_Mg_Ga[f"q={q}"]["locpot"]
    def_entry = DefectEntry(defect=defect_Mg_Ga, charge_state=q, sc_entry=computed_entry)
    frey_summary = def_entry.get_freysoldt_correction(
        defect_locpot=defect_locpot, bulk_locpot=bulk_locpot, dielectric=14
    )
    return def_entry, frey_summary
defect_entries = dict()
plot_data = dict()
for qq in [-2, -1, 0, 1]:
    defect_entry, frey_summary = _get_defect_entry_data(qq)
    defect_entries[qq] = defect_entry
    plot_data[qq] = frey_summary.metadata["plot_data"]
defect_entries_and_plot_data_Mg_Ga = (defect_entries, plot_data)

# --- Reference test code ---

defect_entries, plot_data = defect_entries_and_plot_data_Mg_Ga

def_entry = defect_entries[0]
assert def_entry.corrections["freysoldt"] == pytest.approx(0.00, abs=1e-4)

# test that the plotting code runs
plot_plnr_avg(plot_data[0][1])
plot_plnr_avg(defect_entries[1].corrections_metadata["freysoldt"]["plot_data"][1])

vr1 = plot_data[0][1]["pot_plot_data"]["Vr"]
vr2 = defect_entries[0].corrections_metadata["freysoldt"]["plot_data"][1][
    "pot_plot_data"
]["Vr"]
assert np.allclose(vr1, vr2)

bulk_vasprun = data_Mg_Ga["bulk_sc"]["vasprun"]
bulk_entry = bulk_vasprun.get_computed_entry(inc_structure=False)
def_entry = defect_entries[0]
# raise runtime error if bulk_entry is not provided
with pytest.raises(RuntimeError):
    def_entry.get_ediff()

def_entry.bulk_entry = bulk_entry
ediff = def_entry.sc_entry.energy - bulk_entry.energy
assert def_entry.get_ediff() == pytest.approx(ediff, abs=1e-4)
