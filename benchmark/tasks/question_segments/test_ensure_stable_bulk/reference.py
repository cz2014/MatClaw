"""Reference solution for test_ensure_stable_bulk.
Source: test_thermo.py, lines 321-333
"""

from pathlib import Path
import copy
import os

from matplotlib import pyplot as plt
from monty.serialization import loadfn
from pymatgen.analysis.defects.core import Interstitial, NamedDefect
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
from pymatgen.analysis.phase_diagram import PhaseDiagram
from pymatgen.core import Element, PeriodicSite
import numpy as np

# --- Fixture setup ---

# test_dir
test_dir = Path("/Users/cz/Work/MatTools_temp/src/tool_source_code/pymatgen-analysis-defects/tests/test_files")

# stable_entries_Mg_Ga_N
stable_entries_Mg_Ga_N = loadfn(test_dir / "stable_entries_Mg_Ga_N.json")

# --- Reference test code ---

entries = stable_entries_Mg_Ga_N
pd = PhaseDiagram(stable_entries_Mg_Ga_N)
bulk_comp = Composition("GaN")
fake_bulk_ent = ComputedEntry(bulk_comp, energy=pd.get_hull_energy(bulk_comp) + 2)
# removed GaN from the stable entries
entries = list(
    filter(lambda x: x.composition.reduced_formula != "GaN", stable_entries_Mg_Ga_N)
)
pd1 = PhaseDiagram([*entries, fake_bulk_ent])
assert "GaN" not in [e.composition.reduced_formula for e in pd1.stable_entries]
pd2 = ensure_stable_bulk(pd, fake_bulk_ent)
assert "GaN" in [e.composition.reduced_formula for e in pd2.stable_entries]
