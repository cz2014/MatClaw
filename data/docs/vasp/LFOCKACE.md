# LFOCKACE

Categories: INCAR tag, Exchange-correlation functionals, Hybrid functionals

LFOCKACE = .TRUE. | .FALSE.  
 Default: **LFOCKACE** = .TRUE.

|  |  |  |
| --- | --- | --- |
| Default: **LFOCKACE** | = .TRUE. | for VASP.6 |
|  | = N/A | for VASP.5.X and older |

Description: LFOCKACE determines whether the Adaptively Compressed Exchange Operator is used.

* N.B.:Available for CPU and OpenACC version of VASP.6 when compiled with -Dfock\_dblbuf.

---

For LFOCKACE=.TRUE. the Cholesky decomposition $X=LL^\dagger$ of the Fock exchange matrix $X\_{ij} = \langle \tilde\psi\_i \mid \tilde V\_X \mid \tilde\psi\_j \rangle$ is calculated and the adaptively compressed exchange operator $\tilde V\_{ACE} = -\sum\_i \mid \tilde X\_i \rangle \langle \tilde X\_i \mid$ is used for the action of the Fock exchange on the pseudo orbitals. This method can be used for hybrid functionals in combination with the Davidson algorithm (ALGO=Normal) to save a factor of $\approx 3$ in computation time.

For LFOCKACE=.FALSE. the conventional orbital representation is used.

Note: it is good scientific practice to cite the original publication (Ref. ) if you use this feature. The feature is used by default, if the Davidson algorithm (ALGO = Normal) is used; ACE is not used for ALGO = Damped or ALGO = All.

## Related tags and articles

AEXX,
AEXX,
AGGAX,
AGGAC,
LHFCALC,
List of hybrid functionals,
Hybrid functionals: formalism

Examples that use this tag

## References

---
