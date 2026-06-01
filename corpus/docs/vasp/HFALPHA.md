# HFALPHA

Categories: INCAR tag, Exchange-correlation functionals, Hybrid functionals

HFALPHA = [real]

|  |  |  |
| --- | --- | --- |
| Default: **HFALPHA** | = 6/sqrt(ENMAX)/(2π) | if HFRCUT is 0 |

Description: HFALPHA sets the decay constant used in the method of Massida, Posternak, and Baldereschi, which is activated by HFRCUT=0.

---

HFALPHA sets the decay constant in the error-function-like charge distribution for the method of Massida, Posternak, and Baldereschi. The error-function-like charge distribution is used to calculate the difference between the isolated probe charge and the periodically repeated probe charge in a homogenous background. The default for HFALPHA is 6/sqrt(ENMAX)/(2π) in atomic units. This usually yields robust and accurate results in the range of meV compared to the Ewald summation used for a regular k-mesh. This is the default approach used to implement the convergence corrections of the Coulomb singularity in Hartree-Fock calculations. This does not work correctly for bandstructure calculations using the 0-weight scheme or KPOINTS\_OPT because the correction is only applied for points in the regular grid. To overcome this problem we recommend using the Coulomb truncation methods using HFRCUT.

## Related tags and articles

AEXX,
ALDAX,
ALDAC,
AGGAX,
AGGAC,
AMGGAX,
AMGGAC,
LHFCALC,
HFRCUT,
LTHOMAS,
List of hybrid functionals,
Hybrid functionals: formalism,
Coulomb singularity

Examples that use this tag

## References
