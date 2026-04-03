# LFXC

Categories: INCAR tag, Many-body perturbation theory, Bethe-Salpeter equations

LFXC = .TRUE. | .FALSE.

|  |  |  |
| --- | --- | --- |
| Default: **LFXC** | = .FALSE. |  |

Description: LFXC enables the local exchange-correlation kernel in TD-DFT and TDHF calculations.

---

The local exchange-correlation kernel is determined via

:   :   $f^{\rm loc}\_{\mathrm{xc}}\left(\mathbf{r}, \mathbf{r}'\right) =
        \frac{\delta^{2}\left\{E\_{\mathrm{c}}^{\mathrm{DFT}}+\left(1-c\_{\rm x}\right)
        E\_{\mathrm{x}}^{\mathrm{DFT}}\right\}}{\delta \rho(\mathbf{r}) \delta
        \rho\left(\mathbf{r}'\right)}$,

where $c\_{\rm x}$ is the fraction of the exchange interaction set by AEXX.

## Related tags and articles

BSE calculations

## References

---
