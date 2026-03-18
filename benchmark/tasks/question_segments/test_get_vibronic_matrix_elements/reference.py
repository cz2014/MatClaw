"""Reference solution for test_get_vibronic_matrix_elements.
Source: test_recombination.py, lines 30-42
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

# precompute values of the overlap
dQ, omega_i, omega_f = 0, 0.2, 0.2
Ni, Nf = 5, 5
ovl = np.zeros((Ni, Nf), dtype=np.longdouble)
for m, n in itertools.product(range(Ni), range(Nf)):
    ovl[m, n] = analytic_overlap_NM(dQ, omega_i, omega_f, m, n)

e, matel = get_mQn(
    omega_i=omega_i, omega_f=omega_f, m_init=0, Nf=Nf, dQ=dQ, ovl=ovl
)
ref_result = [0.0, 3984589.0407885523, 0.0, 0.0, 0.0]
assert np.allclose(matel, ref_result)
