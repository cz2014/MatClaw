# FERDO

Categories: INCAR tag, Electronic occupancy, Density of states

FERDO = [real array]

Description: FERDO sets the occupancies of the states in the down-spin channel for ISMEAR=-2 and ISPIN=2.

---

To set the occupancies, specify

```
 FERDO = f(1) f(2) f(3) ... f(NBANDS×Nk)
```

The occupancies must be specified for all bands and k points. The band-index runs fastest. The occupancies must be between 0 and 1.
FERDO has the same format as FERWE, please consider the notes on that page when setting FERDO.

## Related tags and articles

FERWE,
ISMEAR

Examples that use this tag
