# LDISENTANGLED

Categories: INCAR tag, Constrained-random-phase approximation

LDISENTANGLED = [logical]  
 Default: **LDISENTANGLED** = .FALSE.

Description: Selects the disentangled cRPA method.

---

Selects the cRPA method of Miyake, Aryasetiawan, and Imada. Following screening is subtracted from the full RPA polarizability:

:   :   $\tilde \chi^\sigma\_{{\bf G,G}'}({\bf q},i\omega)=
        \frac 1{N\_k}\sum\_{\bf k}\sum\_{nn'\in{\cal T}}
        \frac{
        f\_{n\bf k}-f\_{n'\bf k-q}
        }{
        \tilde\epsilon\_{n{\bf k}} - \tilde\epsilon\_{n'\bf k-q} - i \omega
        }
        \langle
        \tilde u\_{n {\bf k }}^{\sigma }
        |e^{-i \bf (G+q) r}|
        \tilde u\_{n'{\bf k-q}}^{ \sigma' }
        \rangle
        \langle
        \tilde u\_{n' {\bf k-q}}^{\sigma' }
        |e^{-i \bf (G'-q)r'} |
        \tilde u\_{n{\bf k }}^{ \sigma }
        \rangle$,

where $\tilde \epsilon\_{n\bf k}^\sigma$ is the disentangled band structure.

## Related tags and articles

LWEIGHTED,
LSCRPA,
ALGO

Examples that use this tag

## References
