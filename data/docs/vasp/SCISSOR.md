# SCISSOR

Categories: INCAR tag, Bethe-Salpeter equations, Many-body perturbation theory, GW

SCISSOR = [real]

|  |  |  |
| --- | --- | --- |
| Default: **SCISSOR** | = 0 |  |

Description: SCISSOR specifies the shift for the scissor operator in eV.

---

The scissor operator in BSE and GW calculations shifts the unoccupied states relative to the valence states. For example, the scissor operator can be used in the BSE calculations to match the band gap to the known experimental value, thus achieving the right offset in the calculated spectrum. Notably, unlike the self-energy operator in GW, the scissor operator applies a universal shift to all conduction states, i.e., the shift is independent of energy or momentum and leaves the valence states unchanged. The scissor operator only shifts empty states, thus partially occupied orbitals are not affected by it.

## Related tags and articles

BSE calculations

## References

---
