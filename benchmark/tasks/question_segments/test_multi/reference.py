"""Reference solution for test_multi.
Source: test_thermo.py, lines 243-298
"""

from collections import defaultdict
from pathlib import Path
import copy
import os

from matplotlib import pyplot as plt
from monty.serialization import loadfn
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

# stable_entries_Mg_Ga_N
stable_entries_Mg_Ga_N = loadfn(test_dir / "stable_entries_Mg_Ga_N.json")

# --- Reference test code ---

data_Mg_Ga, defect_entries_and_plot_data_Mg_Ga, stable_entries_Mg_Ga_N
) -> None:
bulk_vasprun = data_Mg_Ga["bulk_sc"]["vasprun"]
bulk_dos = bulk_vasprun.complete_dos
_, vbm = bulk_dos.get_cbm_vbm()
bulk_entry = bulk_vasprun.get_computed_entry(inc_structure=False)
defect_entries, plot_data = defect_entries_and_plot_data_Mg_Ga
def_ent_list = list(defect_entries.values())

with pytest.raises(
    ValueError,
    match="Defects are not of same type! Use MultiFormationEnergyDiagram for multiple defect types",
):
    inter = Interstitial(
        structure=defect_entries[0].defect.structure,
        site=PeriodicSite(
            "H", [0, 0, 0], defect_entries[0].defect.structure.lattice
        ),
    )
    fake_defect_entry = DefectEntry(
        defect=inter, sc_entry=defect_entries[0].sc_entry, charge_state=0
    )
    FormationEnergyDiagram(
        bulk_entry=bulk_entry,
        defect_entries=[*def_ent_list, fake_defect_entry],
        vbm=vbm,
        pd_entries=stable_entries_Mg_Ga_N,
        inc_inf_values=False,
    )

fed = FormationEnergyDiagram(
    bulk_entry=bulk_entry,
    defect_entries=def_ent_list,
    vbm=vbm,
    pd_entries=stable_entries_Mg_Ga_N,
    inc_inf_values=False,
)
mfed = MultiFormationEnergyDiagram(formation_energy_diagrams=[fed])
cpots = fed.get_chempots(Element("Ga"))
ef = mfed.solve_for_fermi_level(chempots=cpots, temperature=300, dos=bulk_dos)
assert ef > 0

# test the constructor with materials project phase diagram
atomic_entries = list(
    filter(lambda x: len(x.composition.elements) == 1, stable_entries_Mg_Ga_N)
)
pd = PhaseDiagram(stable_entries_Mg_Ga_N)
mfed = MultiFormationEnergyDiagram.with_atomic_entries(
    bulk_entry=bulk_entry,
    defect_entries=def_ent_list,
    atomic_entries=atomic_entries,
    phase_diagram=pd,
    vbm=vbm,
)
assert len(mfed.formation_energy_diagrams) == 1
