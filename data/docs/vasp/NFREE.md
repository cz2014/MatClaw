# NFREE

Categories: INCAR tag, Ionic minimization, Molecular dynamics, Phonons

NFREE = [integer]

|  |  |  |
| --- | --- | --- |
| Default: **NFREE** | = 1 | if IBRION=2 |
|  | = 0 | else |

Description: depending on IBRION, NFREE specifies the number of remembered steps in the history of ionic convergence runs, or the number of ionic displacements in frozen phonon calculations.

---

* IBRION=1 (quasi-Newton algorithm for ionic relaxation):

:   (i) If NFREE is set, only up to NFREE ionic steps are kept in the iteration history (the rank of the approximate Hessian matrix is not larger than NFREE).

:   (ii) If NFREE is **not** specified, the criterion whether information is removed from the iteration history is based on the eigenvalue spectrum of the inverse Hessian matrix: if one eigenvalue of the inverse Hessian matrix is larger than 8, information from previous steps is discarded.
:   For complex problems NFREE can usually be set to a rather large value (i.e. 10-20), however systems of low dimensionality require a careful setting of NFREE (or preferably an exact counting of the number of degrees of freedom). To increase NFREE beyond 20 rarely improves convergence. If NFREE is set to too large, the RMM-DIIS algorithm might diverge.

* IBRION=5 (from VASP.4.5) or IBRION=6 (from VASP.5.1): frozen phonon approach to calculate the zone-center vibrational frequencies of a system.

:   NFREE determines how many displacements are used for each direction and ion. The step size has to be given in INCAR, by the tag POTIM. Displacements should be small enough to ensure that the harmonic approximation is safely fulfilled. If too large values are supplied in the input file, it is defaulted to 0.015 Å up from VASP.5.1 (but *not* in all earlier releases). Expertise shows that this is a very reasonable compromise.

:   NFREE = 2 uses central difference, *i.e* each ion is displaced in each direction by a small positive and negative displacement

:   :   $\pm$ POTIM \* $\hat{x}$,

:   :   $\pm$ POTIM \* $\hat{y}$,

:   :   $\pm$ POTIM \* $\hat{z}$,

:   For NFREE = 4, four displacements are used

:   :   $\pm$ POTIM \* $\hat{x}$ and $\pm$ 2 \* POTIM \* $\hat{x}$,

:   :   $\pm$ POTIM \* $\hat{y}$ and $\pm$ 2 \* POTIM \* $\hat{x}$,

:   :   $\pm$ POTIM \* $\hat{z}$ and $\pm$ 2 \* POTIM \* $\hat{x}$,

:   For NFREE=1, only a single displacement is applied (it is strongly recommend to avoid NFREE=1).

## Related tags and articles

IBRION,
POTIM

Examples that use this tag

---
