# LPHON_READ_FORCE_CONSTANTS

Categories: INCAR tag, Phonons

LPHON\_READ\_FORCE\_CONSTANTS = .TRUE. | .FALSE.

|  |  |  |
| --- | --- | --- |
| Default: **LPHON\_READ\_FORCE\_CONSTANTS** | = .FALSE. |  |

Description: LPHON\_READ\_FORCE\_CONSTANTS read the force constants from a vaspin.h5 file containing the force constants computed with a previous VASP run.

---

After the computation of the force constants using finite-differences (IBRION=5,6) or density-functional perturbation theory (IBRION=7,8) on a supercell the force constants are written to the vaspout.h5 file.
To plot the phonon dispersion on a different path the user can modify the QPOINTS file and read the force constants computed previously (i.e. without performing the finite-differences computations on supercells again).
To do so copy vaspout.h5 to vaspin.h5 and set LPHON\_READ\_FORCE\_CONSTANTS=.TRUE. in the INCAR file.
Note that when this is set only the phonon dispersion is performed and then VASP quits without running any additional calculation specified in the INCAR file.

> **Mind:** Only available as of VASP 6.4.0.

## Related tags and articles

QPOINTS,
LPHON\_DISPERSION,
PHON\_NWRITE,
LPHON\_POLAR,
PHON\_DIELECTRIC,
PHON\_BORN\_CHARGES,
PHON\_G\_CUTOFF

Examples that use this tag
