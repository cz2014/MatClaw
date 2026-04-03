# URijkl

Categories: Files, Output files, Constrained-random-phase approximation

> **Mind:** Available as of VASP.6.5.2.

This file stores the effectively screened off-centre Coulomb integrals

:   :   $$U\_{ijkl}^{\sigma\sigma'} = \int {\rm d}{\bf r}\int {\rm d}{\bf r}'
        w\_{i}^{\*\sigma}({\bf r}) w\_{j}^{\sigma}({\bf r}) U({\bf r},{\bf r}',\omega)
        w\_{k}^{\*\sigma'}({\bf r}'+{\bf R}) w\_{l}^{\sigma'}({\bf r}'+{\bf R})$$

The format is as follows:

```
# U_ijkl = [ij,R|kl,0] 
#  I   J   K   L          RE(V_IJKL)          IM(V_IJKL)
# R:    1  0.000000  0.000000  0.000000
   1   1   1   1        4.3457689208        0.0000000000
   2   1   1   1        0.0000021313        0.0000001349
... 
# R:    2  0.000000  0.000000  1.000000
   1   1   1   1        1.2535567886        0.0000000000
   2   1   1   1        0.0324545667       -0.0000455665
 ...
```

The Coulomb integrals are computed and written as a post-processing step using ALGO=2e4wa.
The process differs for two types of integrals:

* VRijkl (bare off-centre Coulomb integrals): Always written when requested.
* URijkl: Only written if all WFULLxxxx.tmp files matching the selected k-point grid are present in the working directory.

The basis set for these calculations can be specified using the DMFT\_BASIS tag.

Evaluating Coulomb integrals can be computationally intensive,
especially when dealing with a large number of basis functions.

> **Tip:** To improve performance, you can use a coarser sub-grid of the original k-point grid by enabling the LDOWNSAMPLE tag.

## Related files

VIJKL,UIJKL,VRijkl

---
