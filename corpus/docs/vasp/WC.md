# WC

Categories: INCAR tag, Density mixing

WC = [real]  
 Default: **WC** = 1000.

Description: WC specifies the weight factor for each step in Broyden mixing scheme (IMIX=4).

---

* WC>0

:   Set all weights identical to WC (resulting in Pulay's mixing method), up to now Pulay's scheme was always superior to Broyden's 2nd method.

* WC=0

:   Switch to Broyden's 2nd method, i.e., set the weight for the last step equal to 1000 and all other weights equal to 0.

* WC<0 (implemented for test purposes: **not** recommended)

:   Try some automatic setting of the weights according to:

    :   $$W\_{\rm iter}=0.01 |{\rm WC}|/||\rho\_{\rm out}-\rho\_{\rm in}||\_{\rm precond.}\,$$

:   in order to set small weights for the first steps and increase weights for the last steps.

## Related tags and sections

IMIX,
INIMIX,
MAXMIX,
AMIX,
BMIX,
AMIX\_MAG,
BMIX\_MAG,
AMIN,
MIXPRE

Examples that use this tag
