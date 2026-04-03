# UIJKL

Categories: Files, Output files, Constrained-random-phase approximation

This file stores the effectively screened Coulomb integrals

:   :   $$U\_{ijkl}^{\sigma\sigma'} = \int {\rm d}{\bf r}\int {\rm d}{\bf r}'
        w\_{i}^{\*\sigma}({\bf r}) w\_{j}^{\sigma}({\bf r}) U({\bf r},{\bf r}',\omega)
        w\_{k}^{\*\sigma'}({\bf r}') w\_{l}^{\sigma'}({\bf r}')$$

in following format

```
# U_ijkl = [ij,R|kl,0] 
#  I   J   K   L          RE(V_IJKL)          IM(V_IJKL)
   1   1   1   1        4.3457689208        0.0000000000
   2   1   1   1        0.0000021313        0.0000001349
...
```

## Related files

VIJKL,URijkl,VRijkl

---
