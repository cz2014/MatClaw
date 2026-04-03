"""Reference solution for test_dielectric_func.
Source: test_ccd.py, lines 164-189
"""

from collections import namedtuple
from pathlib import Path

from pymatgen.analysis.defects.ccd import (
    HarmonicDefect,
    _get_wswq_slope,
    plot_pes,
)
from pymatgen.analysis.defects.plotting.optics import plot_optical_transitions
from pymatgen.io.vasp.outputs import Waveder
import numpy as np
import pandas as pd
import pytest

# --- Fixture setup ---

# test_dir
test_dir = Path("/Users/cz/Work/MatTools_temp/src/tool_source_code/pymatgen-analysis-defects/tests/test_files")

# --- Reference test code ---

dir0_opt = test_dir / "v_Ga" / "ccd_0_-1" / "optics"
hd0 = HarmonicDefect.from_directories(
    directories=[dir0_opt],
    store_bandstructure=True,
)
hd0.waveder = Waveder.from_binary(dir0_opt / "WAVEDER")
energy, eps_vbm, eps_cbm = hd0.get_dielectric_function(idir=0, jdir=0)
inter_vbm = np.trapz(np.imag(eps_vbm[:100]), energy[:100])
inter_cbm = np.trapz(np.imag(eps_cbm[:100]), energy[:100])
assert pytest.approx(inter_vbm, abs=0.01) == 6.31
assert pytest.approx(inter_cbm, abs=0.01) == 0.27

df, cmap, norm = plot_optical_transitions(hd0, kpt_index=0, band_window=5)
assert isinstance(df, pd.DataFrame)
assert len(df) == 11

df, cmap, norm = plot_optical_transitions(
    hd0,
    kpt_index=-100,
    band_window=5,
    user_defect_band=(100, 0, 0),
    shift_eig={100: 0},
)
assert df.iloc[5]["ib"] == 100
assert df.iloc[5]["jb"] == 100
