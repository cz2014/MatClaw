# KPOINTS_OPT

Categories: VASP, Files, Input files, Band structure

KPOINTS\_OPT is an optional input file to perform an additional one-shot calculation after self-consistency is reached. The format is the same as for the KPOINTS file. VASP first performs a self-consistent calculation using the **k** points specified in the KPOINTS file and then performs an additional one-shot calculation to obtain the Kohn–Sham orbitals and eigenenergies at the **k** points specified in the KPOINTS\_OPT file.

> **Important:**
>
> * The KPOINTS file must contain a uniform **k** mesh, when the KPOINTS\_OPT file should be used afterward.
> * In the case of a functional using the long-range Hartree-Fock exchange (e.g., unscreened hybrid functionals), the default method for treating the Coulomb singularity (HFRCUT=0) is not adapted to do so for states at k-points that have not been included in the calculation of the Fock potential. Instead, HFRCUT=-1 should be used.

KPOINTS\_OPT is read automatically when present. To avoid this, set LKPOINTS\_OPT`=.FALSE.` in the INCAR file.
VASP writes the PROCAR\_OPT file when LORBIT>10 and corresponding fields in the vaspout.h5 file indicated by the keyword *kpoints\_opt*.

> **Mind:** Available as of VASP 6.3.0.

## Related tags and sections

LKPOINTS\_OPT, KPOINTS, KSPACING, PROCAR\_OPT, KPOINTS\_OPT\_NKBATCH
