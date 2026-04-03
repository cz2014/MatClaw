"""Reference solution for test_get_Rad_coef.
Source: test_recombination.py, lines 70-81
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

get_Rad_coef(
    T=[100, 200, 300],
    dQ=1.0,
    dE=1.0,
    omega_i=0.2,
    omega_f=0.2,
    omega_photon=0.6,
    dipole_me=1,
    volume=1,
    g=1,
)
