# INIMIX

Categories: INCAR tag, Density mixing

INIMIX = 0 | 1 | 2  
 Default: **INIMIX** = 1

Description: Determines the functional form of the initial mixing matrix in the Broyden scheme (IMIX=4).

---

The initial mixing matrix might influence the convergence speed for complex situations (especially surfaces and magnetic systems), nevertheless INIMIX must not be changed from the default setting: anything which can be done with INIMIX can also be done with AMIX and BMIX, and changing AMIX and BMIX is definitely preferable.

Possible choices for INIMIX are:

* INIMIX=0

:   Linear mixing according to the setting of AMIX

* INIMIX=1

:   Kerker mixing (see IMIX=1) according to the settings of AMIX and BMIX.
:   The mixed density is given by

    :   $$\rho\_{\rm mix}\left(G\right)=\rho\_{\rm in}\left(G\right)+A \frac{G^2}{G^2+B^2}\Bigl(\rho\_{\rm out}\left(G\right)-\rho\_{\rm in}\left(G\right)\Bigr)$$
:   with $A$=AMIX and $B$=BMIX

* INIMIX=2

:   No mixing (equal to INIMIX=0 and AMIX=1, not recommended)

## Related tags and articles

IMIX,
MAXMIX,
AMIX,
BMIX,
AMIX\_MAG,
BMIX\_MAG,
AMIN,
MIXPRE,
WC

Examples that use this tag
