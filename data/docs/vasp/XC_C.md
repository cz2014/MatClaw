# XC_C

Categories: INCAR tag, Exchange-correlation functionals, Hybrid functionals

XC\_C = [real array]  
 Default: **XC\_C** = 1.0\*NXC

Description: Multiplication factors for the components of the functional given by the XC tag.

---

XC\_C sets the factors that multiply each component of the functional specified with the XC tag. The number of values specified with XC\_C has to be equal to the number of functional components set with XC (NXC). Examples of how to use XC\_C are provided at XC.

> **Mind:**
>
> * XC\_C is available since VASP.6.4.3.
> * The XC\_C tag can be used together with the ALDAX, ALDAC, AGGAX, AGGAC, AMGGAX, and AMGGAC tags that can be used when LHFCALC=.TRUE.. Such examples are provided at XC.

## Related tags and articles

XC,
GGA,
METAGGA,
ALDAX,
ALDAC,
AGGAX,
AGGAC,
AMGGAX,
AMGGAC

Examples that use this tag

---
