# LHFCALC

Categories: INCAR tag, Exchange-correlation functionals, Hybrid functionals

LHFCALC = .TRUE. | .FALSE.  
 Default: **LHFCALC** = .FALSE.

Description: LHFCALC specifies whether a Hartree-Fock/DFT hybrid functional type calculation is performed.

---

If one does not specifically request a particular hybrid functional (see AEXX, ALDAX, ALDAC, AGGAX, AGGAC, AMGGAX, AMGGAC, and the list\_of\_hybrid\_functionals) VASP will default to the PBE0 hybrid functional.

> **Tip:** For the most reliable convergence, select a "direct optimization" algorithm for HF/DFT hybrid functonal type calculations, i.e., `ALGO = Damped` (`IALGO = 53`) or `ALGO = All` (`IALGO = 58`) in the INCAR file. You may also consider `ALGO = Normal` which in combination with `LFOCKACE = TRUE` (the default) can be a fast alternative. Do not use `ALGO = Fast` which is not properly supported (note: no warning is printed).

If the blocked-Davidson algorithm `ALGO = Normal` is used, in many cases the Pulay mixer will be unable to determine the proper ground-state. We hence recommend to select the blocked-Davidson algorithm only in combination with straight mixing or a Kerker like mixing (see the section on mixing). The following combination have been successfully applied for small and medium sized systems

```
LHFCALC = .TRUE. ; ALGO = Normal ; IMIX = 1 ; AMIX = a
```

Decrease the parameter a until convergence is reached.

In most cases, however, it is recommended to use the "Damped" algorithm with suitably chosen timestep. The following setup for the electronic optimization works reliably in most cases:

```
LHFCALC = .TRUE. ; ALGO = Damped ; TIME = 0.5
```

If convergence is not obtained, it is recommended to reduce the timestep TIME.

## Related tags and articles

AEXX,
ALDAX,
ALDAC,
AGGAX,
AGGAC,
AMGGAX,
AMGGAC,
HFSCREEN,
LTHOMAS,
LRHFCALC,
LFOCKACE,
List of hybrid functionals,
Hybrid functionals: formalism

Examples that use this tag

---
