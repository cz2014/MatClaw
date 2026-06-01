# PSTRESS

Categories: INCAR tag, Molecular dynamics, Ensembles, Ionic minimization, Forces

PSTRESS = [real]  
 Default: **PSTRESS** = 0

Description: Sets the external pressure in kB or adds corrections to the stress tensor.

---

The unit of PSTRESS is kB.

During ionic minimization, an energy term $E= V \times \mathrm{PSTRESS}$ is added to the total energy and the value of PSTRESS is subtracted from the diagonals of the stress tensor. This allows to perform structure optimization at a specific external pressure.

In molecular-dynamics calculations within the NpT ensemble, PSTRESS controls the target pressure for the Parinello-Rahman barostat.

Generally, if a negative value is supplied, the system is under effective tensile strain and during relaxations (or molecular dynamics simulations) the volume
will increase. If a positive value is supplied, the system is under compressive strain; this will decrease the volume during relaxations and molecular dynamics simulations.

PSTRESS can also be used to correct errors caused by the Pulay stress, i.e., errors in the calculated stress tensor caused by the incomplete plane wave basis set. To correct for Pulay-stress errors, set PSTRESS to the negative value of the Pulay stress. The Pulay stress is computed by taking the difference between the external pressure at the desired cutoff and a very large energy cutoff (check the lines 'external pressure' in the OUTCAR file and calculate
pressure at cutoff you want to use $-$ pressure at large cutoff; this must be a negative value). Before using this tag in this manner, please read the following section carefully: Volume relaxation.

Examples that use this tag

---
