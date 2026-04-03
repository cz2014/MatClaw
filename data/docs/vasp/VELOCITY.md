# VELOCITY

Categories: INCAR tag, Molecular dynamics

VELOCITY = [logical]  
 Default: **VELOCITY** = .false.

Description: Determines whether the ionic velocities are written to the vaspout.h5 file during an MD run.

> **Mind:** This tag is only available as of VASP.6.4.0.

---

You can use py4vasp to read the velocities into a Python dictionary

```
from py4vasp import calculation
calculation.velocity.read()
```

or to visualize the velocity in the crystal structure

```
from py4vasp import calculation
calculation.velocity.plot()
```

## Related tags and articles

Sampling phonon spectra from molecular-dynamics simulations

Workflows that use this tag
