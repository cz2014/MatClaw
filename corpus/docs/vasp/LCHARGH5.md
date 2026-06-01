# LCHARGH5

Categories: INCAR tag, Charge density

LCHARGH5 = [logical]  
 Default: **LCHARGH5** = LH5

Description: Determines whether the charge densities are written to vaspwave.h5.

---

In most case it is enough to set LH5 and/or LCHARG with the following exception: Explicitly set

```
 LCHARGH5=True
 LH5=False
```

in order to get the charge density to the vaspwave.h5 for plotting with py4vasp while running a calculation where restart information (wave functions, etc) is written to legacy files (WAVECAR).

> **Mind:** LCHARGH5 is available as of VASP version 6.0

## Related tags and articles

LWAVE, LWAVEH5, LCHARG, LH5
