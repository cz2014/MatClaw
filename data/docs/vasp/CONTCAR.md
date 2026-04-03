# CONTCAR

Categories: Files, Output files, Symmetry

The CONTCAR file contains information about the structure, e.g., the ionic positions. It has a format that is compatible with the POSCAR file. The file is written after each ionic step and at the end of a completed calculation. It can thus be copied to the POSCAR file to restart a calculation.

## Molecular dynamics

For molecular-dynamics (MD) runs (IBRION=0), the CONTCAR file contains the MD trajectories. In particular, the structure parameters, velocities, and predictor-corrector coordinates are needed as input to restart an MD simulation.

* 1st block: Lattice parameters and ionic positions.
* 2nd block: Initial velocities for atoms.
* 3rd block: Predictor-corrector coordinates.

> **Mind:** Whether the ionic positions are rebased into the unit cell depends on the choice for the MDALGO tag for historical reasons.

> **Warning:** To continue an MD calculation from a CONTCAR file but with a different ensemble (e.g. switching from NVT ensemble to NpT ensemble) the predictor-corrector coordinates must be removed; otherwise the calculations will crash. If no velocities are copied to the POSCAR file then random velocities are drawn from a Maxwell-Boltzmann distribution at the selected temperature TEBEG.

## Structure relaxation

For structure relaxation, the CONTCAR file contains the positions of the last ionic step of the relaxation. If the relaxation run has not yet converged one should copy CONTCAR to POSCAR before continuing. For static calculations, the CONTCAR file contains the same information as the POSCAR file.

## Related tags and articles

POSCAR, structure relaxation, structure optimization, XDATCAR, IBRION

---
