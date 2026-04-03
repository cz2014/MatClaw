# LBLUEOUT

Categories: INCAR tag, Advanced molecular-dynamics sampling

LBLUEOUT = .TRUE.|.FALSE.  
 Default: **LBLUEOUT** = .FALSE.

Description: for LBLUEOUT=.TRUE., VASP writes output for the free-energy gradient calculation to the REPORT file (in case VASP was compiled with -Dtbdyn).

---

If LBLUEOUT=.TRUE., the information needed to compute the free-energy gradient is written in the REPORT file after each molecular-dynamics step (MDALGO=1 | 2), check the lines after the header:

```
>Blue_moon
       lambda         |z|^(-1/2)      GkT           |z|^(-1/2)*(lambda+GkT)
```

For the theory of the blue-moon ensemble we refer to here.

## Related tags and articles

IBRION, MDALGO, ICONST, Blue-moon ensemble, Slow-growth approach

Examples that use this tag

---
