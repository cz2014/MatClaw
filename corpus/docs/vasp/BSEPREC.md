# BSEPREC

Categories: INCAR tag, Many-body perturbation theory, Bethe-Salpeter equations

BSEPREC = Low | Medium | High | Accurate  
 Default: **BSEPREC** = Medium

Description: Determines the precision of the time-evolution algorithm, where it controls the timestep and the number of steps, and the precision of the Lanczos algorithms, where it sets the convergence threshold for the dielectric function.

---

## Time-evolution algorithm

The timestep in the time-evolution calculation is inversely proportional to the maximum transition energy OMEGAMAX and the number of steps is inversely proportional to the broadening CSHIFT. Depending on the BSEPREC stable these parameters are scaled depending on the precision tag BSEPREC.

:   :   |  |  |  |
        | --- | --- | --- |
        | BSEPREC | OMEGAMAX | CSHIFT |
        | Accurate (a) | $\times 4$ | $\times 1/10$ |
        | High (h) | $\times 3$ | $\times 1/7.5$ |
        | Medium (m) | $\times 2.5$ | $\times1/6.25$ |
        | Low (l) | $\times 2$ | $\times1/5$ |

For example, the number of steps $N\_{\rm steps}$ for BSEPREC = Low can be found via $N\_{\rm steps}=\frac{{\rm OMEGAMAX}\times 2}{{\rm CSHIFT}/5}$

## Lanczos algorithm

> **Mind:** Replaces LANCZOSTHR as of version 6.5.1

The Lanczos algorithm stops once the imaginary part of the dielectric function computed in two consecutive iterations differs bellow a certain threshold for the root-mean-square, i.e. once after $n$ iterations the value of

:   :   $$\mathrm{RMS}[\epsilon\_n] = \sqrt{\frac{1}{N\_\omega}\sum\_{i=1}^{N\_\omega}\left(\Im[\epsilon\_n(\omega\_i)]-\Im[\epsilon\_{n-1}(\omega\_i)]\right)^2}$$

is below a certain value defined by **BSEPREC**.

:   :   |  |  |
        | --- | --- |
        | BSEPREC | $\mathrm{RMS}[\epsilon\_n]$ |
        | Accurate (a) | $10^{-5}$ |
        | High (h) | $10^{-4}$ |
        | Medium (m) | $10^{-3}$ |
        | Low (l) | $10^{-2}$ |

To prevent the algorithm from being too slow, the number of frequencies during the convergence loop is set to $N\_\omega$ = INT(SQRT(NOMEGA)), where NOMEGA is set in the INCAR.

## Related tag and articles

IBSE,
NBANDSV,
NBANDSO,
CSHIFT,
OMEGAMAX

BSE calculations

Time-dependent density-functional theory calculations

Bethe-Salpeter equations

---
