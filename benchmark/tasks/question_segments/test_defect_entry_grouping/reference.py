"""Reference solution for test_defect_entry_grouping.
Source: test_thermo.py, lines 396-412
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

defect_entries_dict, _ = defect_entries_and_plot_data_Mg_Ga
defect_entries = list(defect_entries_dict.values())
for g_name, g in group_defect_entries(defect_entries=defect_entries):
    for de in g:
        assert de.defect.name == g_name

named_defect_entries = copy.deepcopy(defect_entries)
bulk_formula = defect_entries[0].defect.structure.composition.reduced_formula
for de in named_defect_entries:
    de.defect = NamedDefect(
        name=de.defect.name, bulk_formula=bulk_formula, element_changes=None
    )

for g_name, g in group_defect_entries(defect_entries=named_defect_entries):
    for de in g:
        assert de.defect.name == g_name
