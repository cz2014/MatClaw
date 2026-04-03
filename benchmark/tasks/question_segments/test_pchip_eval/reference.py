"""Reference solution for test_pchip_eval.
Source: test_recombination.py, lines 45-52
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
import pytest

# --- Reference test code ---

x_c = np.linspace(0, 2, 5)
y_c = np.sin(x_c) + 1
xx = np.linspace(-3, 3, 1000)
fx = pchip_eval(xx, x_coarse=x_c, y_coarse=y_c)
int_val = np.trapz(np.nan_to_num(fx), x=xx)
int_ref = np.sum(y_c)
assert int_val == pytest.approx(int_ref, rel=1e-3)
