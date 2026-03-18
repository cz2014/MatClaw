"""Reference solution for test_fed_plot.
Source: plotting/test_thermo.py, lines 8-10
"""

from collections import defaultdict
from pathlib import Path

from monty.serialization import loadfn
from pymatgen.analysis.defects.core import PeriodicSite, Substitution
from pymatgen.analysis.defects.plotting.thermo import (
    plot_chempot_2d,
    plot_formation_energy_diagrams,
)
from pymatgen.analysis.defects.thermo import DefectEntry
from pymatgen.analysis.defects.thermo import FormationEnergyDiagram
from pymatgen.analysis.phase_diagram import PhaseDiagram
from pymatgen.core import Element
from pymatgen.core import Structure
from pymatgen.core.periodic_table import Specie
from pymatgen.io.vasp.outputs import Vasprun, Locpot

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

# stable_entries_Mg_Ga_N
stable_entries_Mg_Ga_N = loadfn(test_dir / "stable_entries_Mg_Ga_N.json")

# basic_fed
bulk_vasprun_fed = data_Mg_Ga["bulk_sc"]["vasprun"]
bulk_bs_fed = bulk_vasprun_fed.get_band_structure()
vbm_fed = bulk_bs_fed.get_vbm()["energy"]
bulk_entry_fed = bulk_vasprun_fed.get_computed_entry(inc_structure=False)
defect_entries_fed, _ = defect_entries_and_plot_data_Mg_Ga
def_ent_list_fed = list(defect_entries_fed.values())
atomic_entries_fed = list(
    filter(lambda x: len(x.composition.elements) == 1, stable_entries_Mg_Ga_N)
)
pd_fed = PhaseDiagram(stable_entries_Mg_Ga_N)
basic_fed = FormationEnergyDiagram.with_atomic_entries(
    defect_entries=def_ent_list_fed,
    atomic_entries=atomic_entries_fed,
    vbm=vbm_fed,
    inc_inf_values=False,
    phase_diagram=pd_fed,
    bulk_entry=bulk_entry_fed,
)
basic_fed.band_gap = 2

# --- Reference test code ---

fig = plot_formation_energy_diagrams([basic_fed])
assert {d_.name for d_ in fig.data} == {"Mg_Ga", "Mg_Ga:slope"}
