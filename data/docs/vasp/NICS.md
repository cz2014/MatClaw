# NICS

Categories: INCAR tag, NMR

```
   Warning: Not yet released!
```

This page contains information about a feature that will be available in a future
release of VASP. In other words, currently you cannot use it even with the latest version of VASP. The information may change significantly until it is released.

The NICS file contains the NMR nucleus-independent chemical shielding (NICS) in ppm. It is written if NUCIND = .TRUE. is set and no POSNICS is present. The format is the same as CHGCAR with a header to define the grid and then 9 blocks that correspond to the indices of the chemical shielding tensor $\sigma\_{ij}$: $\sigma\_{xx}$, $\sigma\_{xy}$, $\sigma\_{xz}$, $\sigma\_{yx}$, $\sigma\_{yy}$, $\sigma\_{yz}$, $\sigma\_{zx}$, $\sigma\_{zy}$, and $\sigma\_{zz}$.

## Related tags and articles

LCHIMAG,
NUCIND,
LNICSALL
