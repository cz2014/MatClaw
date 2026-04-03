# LDAUPRINT

Categories: INCAR tag, Exchange-correlation functionals, DFT+U

LDAUPRINT = 0 | 1  
 Default: **LDAUPRINT** = 0

Description: LDAUPRINT controls the verbosity of a DFT+U calculation.

---

* LDAUPRINT=0: No onsite occupancy matrix is written to the OUTCAR file.
* LDAUPRINT=1: The spin up and spin down onsite occupancy matrices of the atoms types to which a $U$ is applied are written to the OUTCAR file at each iteration (below "onsite density matrix"). The eigenvalues and eigenvectors of the total (spin up + spin down) onsite matrix is also written (below "occupancies and eigenvectors").

## Related tags and articles

LDAU,
LDAUTYPE,
LDAUL,
LDAUU,
LDAUJ,
LMAXMIX

Examples that use this tag

---
