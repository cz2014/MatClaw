# ANTIRES

Categories: INCAR tag, Many-body perturbation theory, Bethe-Salpeter equations

ANTIRES = 0 | 1 | 2  
 Default: **ANTIRES** = 0

Description: ANTIRES determines whether the Tamm-Dancoff approximation is used or not.

---

* ANTIRES=0 Tamm-Dancoff approximation (TDA)
* ANTIRES=1 yields exact results at ω=0 at roughly the same cost as TDA
* ANTIRES=2 beyond Tamm-Dancoff, coupling between positive and negative frequencies

VASP uses the procedures outlined in reference to include contributions beyond TDA. Beyond-TDA calculations increase the computational time and memory requirements by typically a factor of 2.

## Related tags and articles

BSE calculations

Examples that use this tag

## References

---
