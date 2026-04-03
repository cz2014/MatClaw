# LRPAFORCE

Categories: INCAR tag, GW, Molecular dynamics, Ionic minimization, Forces, Low-scaling GW and RPA

LRPAFORCE = .TRUE. | .FALSE.  
 Default: **LRPAFORCE** = .FALSE.

Description: LRPAFORCE=.TRUE. calculates forces in the random-phase approximation (RPA).

---

Available as of VASP.6.1.

This tag can be optionally set in low-scaling RPA calculations or  GW calculations. It allows computing the RPA forces on each ion.
Setting

```
ALGO = RPAR ;  LRPAFORCE = .TRUE.
```

or equivalently

```
ALGO = G0W0R ; LRPAFORCE = .TRUE.
```

determines the RPA total energy with corresponding forces and the quasiparticle energies within the GW approximation.

The LRPAFORCE tag can be used in combination with the standard relaxation options IBRION and NSW as explained in the corresponding RPA calculations guide.

Generally, the energy calculated by the RPA can be quite noisy as a function of the ionic positions, in particular, if PRECFOCK = FAST and NMAXFOCKAE = 1 is set
(these are the default values for RPA calculations). Most of the noise is related to the exact exchange energy, and we are working on methods to improve this issue.
Currently, to reduce the noise in the energy and forces, it is sensible to set PRECFOCK = Normal (typically doubling the execution time and memory requirement). It is also possible to set LMAXFOCKAE = -1 (which implicitly sets NMAXFOCKAE = 0). This makes the correlation energies and the related forces less noisy, but technically less accurate (i.e. part of the correlation energy will be missing at high transition energies).
Overall, RPA forces must be used carefully and only after extensive testing of all relevant parameters.

> **Mind:** The RPA stress tensor is not available.

> **Warning:** Only ISIF=0 is supported.

## Related tags and articles

IBRION,
NSW,
ALGO,
NBANDS,
NMAXFOCKAE,
RPA calculations,
 GW calculations
Examples that use this tag

---

## References
