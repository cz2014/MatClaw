# WANNIER90_WIN

Categories: INCAR tag, Wannier functions

WANNIER90\_WIN = [string]

|  |  |  |
| --- | --- | --- |
| Default: **WANNIER90\_WIN** | = None |  |

Description: WANNIER90\_WIN sets the content of the **wannier90.win** file.

---

The WANNIER90\_WIN tag is a multiline string, where the content of the **wannier90.win** file can be specified. For instance,

```
WANNIER90_WIN = "
exclude_bands 17-64

Begin Projections
Si:sp3
End Projections

# Disentanglement
dis_win_min = -7
dis_win_max = 16
dis_num_iter = 100

guiding_centres = true
"
```

Additionally, the value of some Wannier90 tags is set automatically based on the VASP calculation, e.g., *kpoints*, *atoms*, *unit\_cell*, *mp\_grid*, *spinors*, *num\_bands*, *num\_wann*.

Available as of VASP 6.2.0.

## Related tags and articles

NUM\_WANN,
LWANNIER90,
LWANNIER90\_RUN

Examples that use this tag

---
