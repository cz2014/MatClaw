# LOCPOT

Categories: Files, Output files, Electrostatics, Potential

The LOCPOT file stores the local potential (in eV). The definition of the written local potential depends on the settings for LVTOT, LVHAR, and WRT\_POTENTIAL.

The format is similar to that of the CHGCAR file, but it does not have the same data arrangement.
For spin-unpolarized calculations (ISPIN=1, LNONCOLLINEAR=F), it contains a single dataset with the scalar potential.
For spin-polarized calculations (ISPIN=2), it contains two datasets: spin up and spin down.
For noncollinear calculations (LNONCOLLINEAR=T), it contains four datasets in the spinor representation of the potential. In other words, it contains the scalar potential and the B-field-like potential $B\_1$, $B\_2$, and $B\_3$ in the basis defined by SAXIS (see LOCPOT-format issue for VASP<6.4.3).

> **Warning:** Note for versions older than vasp.5.1.12: please check whether your version supports this tag (it is written out at the beginning of the OUTCAR file). Versions not supporting LVHAR might or not add $V\_{\text{XC}}(\mathbf{r})$. Please check this by searching for LEXCHG=-1 in main.F. If the line LEXCHG=-1 is commented out $V\_{\text{XC}}(\mathbf{r})$ is added otherwise it is not.

## Related tags and articles

LVACPOTAV,
LVTOT,
LVHAR,
WRT\_POTENTIAL,
POT
