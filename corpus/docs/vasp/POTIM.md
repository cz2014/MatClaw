# POTIM

Categories: INCAR tag, Ionic minimization, Molecular dynamics, Phonons

POTIM = [real]

|  |  |  |
| --- | --- | --- |
| Default: **POTIM** | = none, | *must* be set if IBRION= 0 (MD) |
|  | = 0.5 | if IBRION= 1, 2, and 3 (ionic relaxation), and 5 (up to VASP.4.6) |
|  | = 0.015 | if IBRION=5, and 6 (as of VASP.5.1) |

Description: POTIM sets the time step in molecular dynamics or the step width in ionic relaxations.

---

* For IBRION = 0, POTIM gives the time step (in fs) in all ab-initio Molecular Dynamics runs, it *has* to be supplied therefore, otherwise VASP crashes immediately after having started.

* For IBRION =1, 2, and 3, which corresponds to ionic relaxation using a quasi-Newton algorithm, conjugate-gradient algorithm, and damped molecular dynamics, respectively, the POTIM tag serves as a scaling constant for the step widths. The quasi-Newton algorithm is especially sensitive to the choice of this parameter.

* For IBRION = 5, and 6, a phonon calculations using the finite differences approach is done, where POTIM is the width of the displacement of each ion to calculate the Hessian Matrix.

:   VASP.4.6 and older releases: POTIM has to be small enough to ensure that the displacements are within the harmonic limit. The vibrational frequencies using the frozen phonon approach are based on the harmonic approximation.

:   > **Mind:** For VASP.5.1 and newer releases, POTIM is automatically reset to 0.015 Å, if the supplied value for POTIM is unreasonably large.

## Related tags and articles

structure optimization, IBRION, NFREE

Examples that use this tag

---
