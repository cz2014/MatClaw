# BSEELECTRON

Categories: INCAR tag, Many-body perturbation theory, Bethe-Salpeter equations

BSEELECTRON = [real array]

Description: BSEELECTRON sets the coordinates of the fixed electron of the exciton wavefunction

---

If BSEELECTRON is set in a BSE calculation, VASP computes exciton wavefunction for the first NBSEEIG states.
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

BSEHOLE, NBSEEIG, BSE calculations, Plotting exciton wavefunction

---
