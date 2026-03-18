"""Reference solution for test_formation_from_directory.
Source: test_thermo.py, lines 301-318
"""

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
from pymatgen.analysis.phase_diagram import PhaseDiagram
from pymatgen.core import Element, PeriodicSite
from pymatgen.core import Structure
from pymatgen.core.periodic_table import Specie
import numpy as np

# --- Fixture setup ---

# test_dir
test_dir = Path("/Users/cz/Work/MatTools_temp/src/tool_source_code/pymatgen-analysis-defects/tests/test_files")

# gan_struct
gan_struct = Structure.from_file(test_dir / "GaN.vasp")

# defect_Mg_Ga
ga_site = gan_struct[0]
mg_site = PeriodicSite(Specie("Mg"), ga_site.frac_coords, gan_struct.lattice)
defect_Mg_Ga = Substitution(gan_struct, mg_site)

# stable_entries_Mg_Ga_N
stable_entries_Mg_Ga_N = loadfn(test_dir / "stable_entries_Mg_Ga_N.json")

# --- Reference test code ---

test_dir, stable_entries_Mg_Ga_N, defect_Mg_Ga
) -> None:
sc_dir = test_dir / "Mg_Ga"
qq = []
for q in [-1, 0, 1]:
    qq.append(q)
    dmap = {"bulk": sc_dir / "bulk_sc"}
    dmap.update(zip(qq, map(lambda x: sc_dir / f"q={x}", qq)))
    assert len(dmap) == len(qq) + 1
    fed = FormationEnergyDiagram.with_directories(
        directory_map=dmap,
        defect=defect_Mg_Ga,
        pd_entries=stable_entries_Mg_Ga_N,
        dielectric=10,
    )
    trans = fed.get_transitions(fed.chempot_limits[1], x_min=-100, x_max=100)
    assert len(trans) == 1 + len(qq)
