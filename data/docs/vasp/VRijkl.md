# VRijkl

Categories: Files, Output files, Constrained-random-phase approximation

> **Mind:** Available as of VASP.6.5.2.

This file is written for ALGO=2e4wa and stores all off-centre Coulomb integrals
commensurate with the selected k-point grid

:   :   $$V\_{ijkl}^{\sigma\sigma'} = \int {\rm d}{\bf r}\int {\rm d}{\bf r}'
        \frac{ w\_{i}^{\*\sigma}({\bf r}) w\_{j}^{\sigma}({\bf r}) w\_{k}^{\*\sigma'}({\bf r}'+{\bf R}) w\_{l}^{\sigma'}({\bf r}'+{\bf R})}{|{\bf r}-{\bf r}'|}$$

The format is as follows:

```
# V_ijkl = [ij,R|kl,0] 
#  I   J   K   L          RE(V_IJKL)          IM(V_IJKL)
# R:    1  0.000000  0.000000  0.000000
   1   1   1   1       14.4576272582        0.0000000000
   2   1   1   1        0.0000010313        0.0000031049
... 
# R:    2  0.000000  0.000000  1.000000
   1   1   1   1        4.6546536926        0.0000000000
   2   1   1   1        0.0617934919       -0.0000371600
 ...
```

A proper WAVECAR file must be present in the working directory. The basis can be selected with DMFT\_BASIS.

Evaluation of Coulomb integrals can be computationally demanding if the number of basis functions becomes large.

> **Tip:** Use LDOWNSAMPLE to reduce k-point grid density for faster calculations.

## Related files

VIJKL,VIJKL,URijkl

---
