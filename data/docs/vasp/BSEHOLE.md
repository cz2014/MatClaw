# BSEHOLE

Categories: INCAR tag, Many-body perturbation theory, Bethe-Salpeter equations

BSEHOLE = [real array]

Description: BSEHOLE sets the coordinates of the fixed hole of the exciton wavefunction

---

If BSEHOLE is set in a BSE calculation, VASP computes exciton wavefunction for the first NBSEEIG states.
The coordinates are provided in direct (fractional) coordinates.

When fixing the position of the particle, ensure that it is not fixed exactly at the center of an atom or coincides with a node of the wavefunction. To avoid that, shift the fixed coordinate slightly away from the center of the atom. Furthermore, the wavefunction of the fixed particle is taken at the nearest $\mathbf{G}$-vector, whose exact position is written in the OUTCAR file

```
hole position is fixed at:
```

or

```
electron position is fixed at:
```

## Related tags and sections

BSEELECTRON, NBSEEIG, BSE calculations, Plotting exciton wavefunction

---
