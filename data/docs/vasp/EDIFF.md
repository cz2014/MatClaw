# EDIFF

Categories: INCAR tag, Electronic minimization

EDIFF = [real]  
 Default: **EDIFF** = $10^{-4}$

Description: EDIFF specifies the global break condition for the electronic SC-loop. EDIFF is specified in units of eV.

---

The relaxation of the electronic degrees of freedom stops if the total (free) energy change and the band-structure-energy change ('change of eigenvalues') between two steps are both smaller than EDIFF (in eV). For EDIFF=0, strictly NELM electronic self-consistency steps will be performed.

In most cases, the convergence speed is quadratic, so often the cost for the additional iterations is small. Hence, for well converged calculations, we strongly recommend to decrease EDIFF to 1E-6. For finite difference calculations (e.g. phonons), even EDIFF = 1E-7 might be required in order to obtain precise results. On the other hand, for large systems with many atoms and/or when using METAGGA functionals, attaining an energy convergence of 1E-8 or even 1E-7 might be difficult. So, overall EDIFF= 1E-6 is likely the best compromise.

> **Tip:** You can get information at each electronic step using `NWRITE = 2,3`.

## Related tags and articles

EDIFFG, NWRITE

Examples that use this tag

---
