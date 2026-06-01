# LORBMOM

Categories: INCAR tag, Magnetism

LORBMOM = .TRUE. | .FALSE.  
 Default: **LORBMOM** = .FALSE.

Description: Specifies whether the orbital moments are written out. Only applicable in a calculation using LSORBIT = True .

---

If LORBMOM=.TRUE. is set, VASP will use the projectors of the PAW potentials to calculate the
orbital angular moment within the PAW spheres, and write them to the OUTCAR file. Look for

```
 orbital moment (x)
```

to find the orbital- and site-resolved table.

## Related tags and articles

LSORBIT,
LORBIT

Examples that use this tag

---
