# NELMGW

Categories: INCAR tag, Many-body perturbation theory, GW, Low-scaling GW and RPA

NELMGW = [integer]  
 Default: **NELMGW** = 1

Description: NELMGW sets the number of self-consistent GW steps.
Available as of 6.3.0.

---

This tag is effective for ALGO=EVGW[0] | QPGW[0] | GW[0][R][K] and ignored otherwise.
For instance

```
ALGO = EVGW0
NELMGW = 4
```

performs a  partially self-consistent GW calculations, where $G$ is updated four times.

Omit NBANDS and NELM to select the single-step GW procedure.

## Related tags and articles

ALGO, GW calculations

Examples that use this tag

---
