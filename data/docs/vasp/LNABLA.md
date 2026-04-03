# LNABLA

Categories: INCAR tag, Linear response, Dielectric properties

LNABLA = .TRUE. | .FALSE.  
 Default: **LNABLA** = .FALSE.

Description: LNABLA=.TRUE. evaluates the transversal expression for the frequency dependent dielectric matrix.

---

Usually VASP uses the longitudinal expression for the frequency dependent dielectric matrix.
It is however possible to switch to the computationally somewhat simpler transversal expressions by selecting LNABLA=.TRUE. (Eqs. 17 and 20 in Ref.).
In this simplification the imaginary part of the macroscopic dielectric function is given by

:   $$\epsilon^{(2)}\_{\alpha \beta} (\omega) = \frac{4 \pi^2 e^2 \hbar^4}{\Omega \omega^2 m\_e^2}
    \mathrm{lim}\_{\mathbf{q} \rightarrow 0} \sum\_{c,v, \mathbf{k}} 2 w\_\mathbf{k}
    \delta( \epsilon\_{c\mathbf{k+q}} - \epsilon\_{v\mathbf{k}} - \omega)
    \times \langle u\_{c\mathbf{k}} | i{\mathbf{\nabla}\_{\alpha} - \mathbf{k}}\_{\alpha} | u\_{v\mathbf{k}} \rangle
    \langle u\_{c\mathbf{k}} | i{\mathbf{\nabla}\_{\beta} - \mathbf{k}}\_{\beta} | u\_{v\mathbf{k}} \rangle^\*.$$

Except for the purpose of testing, there is however hardly ever a reason
to use the transversal expression, since it is less accurate.

## Related tags and articles

LOPTICS,
CSHIFT

Examples that use this tag

## References

---
