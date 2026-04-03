# LEXCH

Categories: Exchange-correlation functionals, POTCAR tag

LEXCH = [string] 
LEXCH = CA.OR.PBE

|  |  |  |
| --- | --- | --- |
| Default:  **LEXCH** | = CA | for LDA pseudopotentials |
|  | = PE | for GGA pseudopotentials |

Definition: Set the default exchange-correlation functional.

---

The functional specified by LEXCH was used as a reference when the PAW potential was created. The transferability of PAW potentials to other exchange-correlation functionals is quite good. So, the functional used during the calculation can be freely adjusted (despite the very prominent warning in the stdout).

## Related tags and articles

Exchange-correlation functionals, XC, XC\_C GGA, METAGGA, POTCAR, pseudopotentials
