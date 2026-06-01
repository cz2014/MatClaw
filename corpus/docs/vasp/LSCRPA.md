# LSCRPA

Categories: INCAR tag, Constrained-random-phase approximation

LSCRPA = [logical]  
 Default: **LSCRPA** = .FALSE.

Description: LSCRPA selects the spectral cRPA method.

---

When selected the spectral method in constrained RPA (cRPA) calculations is selected. The screening effects in the target space are calculated as follows

:   :   $$\tilde \chi^\sigma\_{{\bf G,G}'}({\bf q},i\omega)\approx
        \frac 1{N\_k}\sum\_{nn'{\bf k}}
        \frac{
        f\_{n\bf k}-f\_{n'\bf k-q}
        }{
        \epsilon\_{n{\bf k}} - \epsilon\_{n'\bf k-q} - i \omega
        }
        \theta\_{n\bf k }^{\sigma}
        \theta\_{n'\bf k-p }^{\sigma'}
        \langle
        u\_{n {\bf k }}^{\sigma }
        |e^{-i \bf (G+q) r}|
        u\_{n'{\bf k-q}}^{ \sigma' }
        \rangle
        \langle
        u\_{n' {\bf k-q}}^{\sigma' }
        |e^{-i \bf (G'-q)r'} |
        u\_{n'{\bf k }}^{ \sigma }
        \rangle$$

Here $\theta\_{n{\bf k}}^\sigma$ are the eigenvalues of the correlated projectors $P\_{mn}^{\sigma({\bf k})} = \sum\_{i\in \cal T} T\_{i m}^{\*\sigma({\bf k})} T\_{i n}^{\sigma({\bf k})}$ ordered according to their leverage scores. This method results in larger effective interactions compared to w-cRPA or the projector method and conserves the number of electrons.

## Related tags and articles

LDISENTANGLED,
LWEIGHTED,
ALGO

Examples that use this tag

## References

---
