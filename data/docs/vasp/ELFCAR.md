# ELFCAR

Categories: Files, Output files

The ELFCAR file is created when the LELF=*.TRUE.* in the INCAR file is set and contains the electron localization function denoted by $ELF$ in Ref. .

The same file format is used as for the CHGCAR file. That is, lattice vectors, atomic coordinates and number of cartesian sampling points $N\_x, N\_y, N\_z$ are written, followed by $ELF(x,y,z)$ with $x$ being the fastest and $z$ the slowest index.

For ISPIN=2, $ELF\_{\uparrow}$ is written first followed by $ELF\_{\downarrow}$.

It is recommended to avoid wrap around errors, when evaluating the ELFCAR file. This can be done by specifying PREC=*High* in the INCAR file.

* N.B. The electronic localization function is not implemented for non-collinear calculations.

## References

---
