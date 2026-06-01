# ESTOP

Categories: INCAR tag, MP2

ESTOP = [real]

|  |  |  |
| --- | --- | --- |
| Default: **ESTOP** | = 0.05 |  |

Description: ESTOP specifies the stop condition for stochastic MP2.

---

ESTOP defines the energy accuracy in units of eV for each individual tau-point of the two individual MP2 energy contributions (direct MP2 term + exchange MP2 term). Since the statistical errors of each contribution is independent, the standard deviation of the MP2 energy can be estimated as

$\sigma = \texttt{ESTOP} \* \sqrt{2 \cdot \texttt{NOMEGA}} \;.$

According to our experience, the error of the resulting MP2 energy can then be safely estimated by $\pm 2 \sigma$.

Thus, if you require an MP2 energy with a maximum error of $\Delta$, you should set

$\texttt{ESTOP} = \frac{\Delta}{2 \cdot \sqrt{2 \cdot \texttt{NOMEGA}}} \;.$

See this tutorial for more Information about Laplace transformed MP2.

## Related tags and articles

ALGO,
LMP2LT,
LSMP2LT,
NOMEGA,
NSTORB

---
