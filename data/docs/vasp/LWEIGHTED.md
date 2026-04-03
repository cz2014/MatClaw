# LWEIGHTED

Categories: INCAR tag, Constrained-random-phase approximation

LWEIGHTED = [logical]  
 Default: **LWEIGHTED** = .FALSE.

Description: LWEIGHTED selects the weighted cRPA method.

---

Selects the cRPA method of Sasioglu, Friedrich and Blügel where following screening are subtracted from the full RPA polarizability:

:   :   $$\tilde \chi^\sigma\_{{\bf G,G}'}({\bf q},i\omega)\approx
        \frac 1{N\_k}\sum\_{nn'{\bf k}}
        \frac{
        f\_{n\bf k}-f\_{n'\bf k-q}
        }{
        \epsilon\_{n{\bf k}} - \epsilon\_{n'\bf k-q} - i \omega
        }
        p\_{n\bf k }^{\sigma}
        p\_{n'\bf k-p }^{\sigma'}
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

## Related tags and articles

LDISENTANGLED,
LSCRPA,
ALGO

Examples that use this tag

## References

---
