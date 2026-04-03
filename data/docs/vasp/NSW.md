# NSW

Categories: INCAR tag, Ionic minimization, Molecular dynamics

NSW = [integer]  
 Default: **NSW** = 0

Description: NSW sets the maximum number of ionic steps.

---

IBRION = 0:

:   NSW gives the number of steps in all molecular dynamics runs. It *has* to be supplied, otherwise VASP exits immediately after having started. We recommend splitting long MD runs containing ab-initio calculations into multiple calculations with NSW⪅20000. For ML\_MODE=run larger values of NSW should be possible, but consider setting ML\_OUTBLOCK.

IBRION != 0:

:   In all minimization algorithms (quasi-Newton, conjugate gradient, and damped molecular dynamics) NSW defines the maximum number of ionic steps.

Within each ionic step at most NELM electronic steps are performed. It is fewer if the convergence criterium set by EDIFF is met before. Forces and stresses are calculated according to the setting of ISIF for each ionic step.

## Related tags and articles

structure optimization, NBLOCK, KBLOCK, ML\_OUTBLOCK

Examples that use this tag
