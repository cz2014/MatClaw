"""Reference solution for test_get_SRH_coef.
Source: test_recombination.py, lines 55-67
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

ref_res = [4.64530153e-14, 4.64752885e-14, 4.75265302e-14]
res = get_SRH_coef(
    T=[100, 200, 300],
    dQ=1.0,
    dE=1.0,
    omega_i=0.2,
    omega_f=0.2,
    elph_me=1,
    volume=1,
    g=1,
)
assert np.allclose(res, ref_res)
