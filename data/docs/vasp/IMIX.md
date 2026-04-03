# IMIX

Categories: INCAR tag, Density mixing

IMIX = 0 | 1 | 2 | 4  
 Default: **IMIX** = 4

Description: IMIX specifies the type of density mixing.

---

## IMIX=0: No mixing

:   :   $$\rho\_{\rm mix}=\rho\_{\rm out}\,$$

## IMIX=1: Kerker mixing

:   For Kerker mixing, the mixed density is given by

    :   $$\rho\_{\rm mix}\left(G\right)=\rho\_{\rm in}\left(G\right)+A \frac{G^2}{G^2+B^2}\Bigl(\rho\_{\rm out}\left(G\right)-\rho\_{\rm in}\left(G\right)\Bigr)$$
:   with $A$=AMIX and $B$=BMIX. If BMIX is very small, e.g., BMIX=0.0001, a straight mixing is obtained.

:   > **Mind:** BMIX=0 might cause floating-point exceptions on some platforms.

## IMIX=2: Variant of Tchebycheff mixing

:   VASP uses a variant of the popular Tchebycheff-mixing scheme. Here, the following second order equation of motion is used:

    :   $$\ddot{\rho}\_{\rm in}\left(G\right) = 2\*A \frac{G^2}{G^2+B^2}\Bigl(\rho\_{\rm out}\left(G\right)-\rho\_{\rm in}\left(G\right)\Bigr)-\mu \dot{\rho}\_{\rm in}\left(G\right)$$
:   with $A$=AMIX, $B$=BMIX, and $\mu$=AMIN. A velocity Verlet algorithm is used to integrate this equation. The discretized equation reads:

    :   $$\dot{\rho}\_{N+1/2} = \Bigl(\left(1-\mu/2\right) \dot{\rho}\_{N-1/2} + 2\*F\_N \Bigr)/\left(1+\mu/2\right)$$
:   where

    :   $$F\left(G\right)=A\frac{G^2}{G^2+B^2} \Bigl(\rho\_{\rm out}\left(G\right)-\rho\_{\rm in}\left(G\right)\Bigr)$$
:   and

    :   $\rho\_{N+1}=\rho\_{N+1}+\dot{\rho}\_{N+1/2}$,
:   where the index *N* is the electronic iteration, and *F* is the force acting on the charge.

:   For BMIX≈0, no model for the dielectric matrix is used. For $\mu=2$ a simple straight mixing is obtained. Therefore, $\mu=2$ corresponds to maximal damping, while $\mu=0$ implies no damping. To determine the optimal parameters for $\mu$ and AMIX, first converge to the ground state with the Pulay mixer (IMIX=4). Then, search for the the eigenvalues of the charge-dielectric matrix in the OUTCAR file at the last occurrence of

```
eigenvalues of (default mixing * dielectric matrix)
```

:   The optimal parameters are then given by:

:   :   |  |  |  |
        | --- | --- | --- |
        | AMIX |  | $={\rm AMIX}({\rm as\; used\; in\; Pulay\; run})\*{\rm smallest\; eigenvalue}$ |
        | AMIN |  | $=\mu=2\sqrt{{\rm smallest\; eigenvalue}/{\rm largest\; eigenvalue}}$ |

## IMIX=4: Broyden's 2nd method and Pulay-mixing method (default)

:   For WC=0, VASP uses Broyden's 2nd method, and, for WC>0, VASP uses Pulay-mixing method.
:   The default is a Pulay mixer with an initial approximation for the charge-dielectric function according to Kerker

    :   $$A\times\max\left(\frac{G^2}{G^2+B^2},A\_{\rm min}\right)$$
:   where $A$=AMIX, $B$=BMIX, and $A\_{\rm min}$=AMIN.

:   AMIN=0.4 usually yields good convergence. AMIX strongly depends on the system, for instance, it should be small, e.g., AMIX= 0.02, for metals.
:   In the Broyden scheme, the functional form of the initial mixing matrix is determined by AMIX and BMIX or the INIMIX tag. The metric used in the Broyden scheme is specified through MIXPRE.

## Related tags and articles

INIMIX,
MAXMIX,
AMIX,
BMIX,
AMIX\_MAG,
BMIX\_MAG,
AMIN,
MIXPRE,
WC

Examples that use this tag

## References

---
