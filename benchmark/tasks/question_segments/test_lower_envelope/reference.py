"""Reference solution for test_lower_envelope.
Source: test_thermo.py, lines 75-91
"""

import copy
import os

from matplotlib import pyplot as plt
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

# --- Reference test code ---

# Test the lower envelope and transition code with a simple example
lines = [[4, 12], [-1, 3], [-5, 4], [-2, 1], [3, 8], [-4, 14], [2, 12], [3, 8]]
lower_envelope_ref = [
    (4, 12),
    (3, 8),
    (-2, 1),
    (-5, 4),
]  # answer from visual inspection (ordered)
transitions_ref = [(-4, -4), (-1.4, 3.8), (1, -1)]
lower_envelope = get_lower_envelope(lines)
assert lower_envelope == lower_envelope_ref
assert get_transitions(lower_envelope, -5, 2) == [
    (-5, -8),
    *transitions_ref,
    (2, -6),
]
