"""Reference solution for test_boltzmann.
Source: test_recombination.py, lines 15-27
"""

import itertools

from pymatgen.analysis.defects.recombination import (
    analytic_overlap_NM,
    boltzmann_filling,
    get_mQn,
    get_Rad_coef,
    get_SRH_coef,
    pchip_eval,
)
import numpy as np

# --- Reference test code ---

ref_results = [
    0.9791034813819097,
    0.020459854127734073,
    0.00042753972270360594,
    8.934091775449048e-06,
    1.8669141512139823e-07,
    3.901200631921917e-09,
]
results = boltzmann_filling(0.1, 300, n_states=6)
assert np.allclose(results.flatten(), ref_results, rtol=1e-3)
results2 = boltzmann_filling(0.1, [100, 300], n_states=6)
assert np.allclose(results2[:, 1], ref_results, rtol=1e-3)
