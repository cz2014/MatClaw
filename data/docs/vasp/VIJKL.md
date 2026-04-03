# VIJKL

Categories: Files, Output files, Constrained-random-phase approximation

This file stores the bare Coulomb integrals

:   :   $$V\_{ijkl}^{\sigma\sigma'} = \int {\rm d}{\bf r}\int {\rm d}{\bf r}'
        \frac{ w\_{i}^{\*\sigma}({\bf r}) w\_{j}^{\sigma}({\bf r}) w\_{k}^{\*\sigma'}({\bf r}') w\_{l}^{\sigma'}({\bf r}')}{|{\bf r}-{\bf r}'|}$$

The format is as follows:

```
# V_ijkl = [ij,R|kl,0] 
#  I   J   K   L          RE(V_IJKL)          IM(V_IJKL)
   1   1   1   1       14.4576272582        0.0000000000
   2   1   1   1        0.0000010313        0.0000031049
 ...
```

## Related files

UIJKL,URijkl,VRijkl

---
