# TMPCAR

Categories: Files, Output files

TMPCAR is a binary file which is generated during dynamic simulations and relaxation jobs using full wave function predication. It contains the ionic positions and wave function of the previous two steps. Those are needed for the extrapolation of the wave functions. It is possible to use the TMPCAR file for MD continuation jobs by setting the flag ISTART=3 in the file INCAR file.

Instead of the TMPCAR file VASP.4.X can also use an internal scratch file. This is faster and more efficient but requires of course more memory (see IWAVPR for more details).

---
