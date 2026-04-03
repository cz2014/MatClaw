# KPOINTS_ELPH

Categories: Input files, Electron-phonon interactions

KPOINTS\_ELPH is an optional input file to perform an additional one-shot calculation after self-consistency is reached in the context of an electron-phonon calculation. The format is the same as for the KPOINTS file. VASP first performs a self-consistent calculation using the **k** points specified in the KPOINTS file and then performs an additional one-shot calculation to obtain the Kohn–Sham orbitals and eigenenergies at the **k** points specified in the KPOINTS\_ELPH file.

The KPOINTS file must contain a uniform **k** mesh, when the KPOINTS\_ELPH file should be used afterward.

Alternatively, it is possible to choose the k-point mesh by specifying ELPH\_KSPACING which determines the smallest allowed spacing between **k** points in units of $\AA^{-1}$.

> **Mind:** Available as of VASP 6.5.0

## Related tags and sections

* ELPH\_RUN
* KPOINTS
* KPOINTS\_OPT
* ELPH\_KSPACING
