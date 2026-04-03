# MAXMIX

Categories: INCAR tag, Density mixing

MAXMIX = [integer]  
 Default: **MAXMIX** = -45

Description: MAXMIX specifies the maximum number of steps stored in the Broyden mixer (IMIX=4).

---

MAXMIX specifies the maximum number of vectors stored in the Broyden/Pulay mixer, in other words, it corresponds to the maximal rank of the approximation of the charge-dielectric function build up by the mixer. MAXMIX can be either negative or positive:

* MAXMIX<0

:   The mixer is reset after each ionic step or if the number of electronic steps exceeds |MAXMIX| (this is the default and similar to the behavior of VASP.4.3 and VASP.3.2).

* MAXMIX>0

:   The charge density mixer is only reset if the storage capabilities are exceeded. The reset is done "smoothly" by removing the five oldest vectors from the iteration history. Therefore, if MAXMIX is positive, the approximation for the charge dielectric function which was obtained in previous ionic steps is "reused" in the current ionic step, and this, in turn, can reduce the number of electronic steps during relaxations and MD's. Especially for relaxations that start from a good ionic starting guess and for systems with a strong charge sloshing behavior the speedup can be significant. We found that for a 12 Å long box containing 16 Fe atoms the number of electronic iterations decreased from 8 to 2-3 when MAXMIX was set to 40. For a carbon surface the number of iterations decreased from 7 to 3. At the same time, the energy stability increased significantly. But be careful, this option increases the memory requirements for the mixer considerably, and thus the option is not recommended for systems where charge sloshing is negligible anyway (like bulk simple metals). The optimal setting for MAXMIX is usually around three times the number of electronic steps required in the first iteration. Too large values for MAXMIX might cause the code to crash (because linear dependencies between input vectors might develop). Too small values for MAXMIX can slow your convergence significantly. For instance, if you need 50 self-consistency cycles, and set MAXMIX to 20, you force the mixer to remove iteration history continuously, which can cause divergence and at least a slow down of the convergence.

* Caution: do not set MAXMIX>0 in the following cases. (i) If your initial positions in the POSCAR file are far from the fully relaxed positions, the ions might move considerably during relaxation. In this case, it is not expedient to "reuse" charge mixing information from the previous ionic steps. (ii) During machine learning, the first-principles calculations are often bypassed for hundreds or even thousands of ionic steps, and the ions might move considerably between first-principles calculations. In these cases using MAXMIX will very often lead to electronic divergence or strange errors during the self-consistency cycle. In general, whenever the column RMS(c) in the OSZICAR files shows a sudden increase in the norm of the charge density residual vector, try to remove the tag MAXMIX from the INCAR file.

> **Mind:** MAXMIX is only available in VASP.4.4 and newer versions, and it is strongly recommended to use this option for molecular dynamics and relaxations.

## Related tags and articles

IMIX,
INIMIX,
AMIX,
BMIX,
AMIX\_MAG,
BMIX\_MAG,
AMIN,
MIXPRE,
WC

Examples that use this tag

---
