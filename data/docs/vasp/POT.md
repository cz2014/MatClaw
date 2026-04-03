# POT

Categories: Files, Output files, Potential

The POT file contains the local potential (in eV), including the augmentation part. It is written if LVTOT=T, and it can be used to restart a calculation that requires the local potential as a restart quantity, e.g., for the optimized effective potential (OEP) method.

For LVTOT=T and LH5=T, the content of the POT file is written to the restart file vaspwave.h5 instead.

If you are interested in the local potential as a quantity (and not interested in restarting a calculation), we recommend the LOCPOT file and/or setting WRT\_POTENTIAL.

The format is similar to that of the LOCPOT file but it additionally contains the augmentation part at the end of each block.

## Related tags and articles

LOCPOT,
LVTOT,
LVHAR,
WRT\_POTENTIAL
