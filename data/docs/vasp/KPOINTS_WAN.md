# KPOINTS WAN

Categories: VASP, Files, Input files, Wannier functions

KPOINTS\_WAN is an optional input file to obtain eigenstates and eigenenergies at the specified **k** points from Wannier functions.
The format is the same as for the KPOINTS file.

> **Important:** The VASP calculation must include the construction of Wannier functions, e.g., using LSCDM or LWANNIER90.

KPOINTS\_WAN is read automatically when present. To avoid this, set LKPOINTS\_WAN`=.FALSE.` in the INCAR file.
VASP writes corresponding fields in the vaspout.h5 file and vasprun.xml file indicated by the keyword *kpoints\_wan*.

> **Mind:** Available as of VASP 6.3.0.

## Related tags and sections

KPOINTS, KPOINTS\_OPT, LKPOINTS\_WAN, PROCAR\_WAN, LSCDM, LWANNIER90, LOCPROJ
