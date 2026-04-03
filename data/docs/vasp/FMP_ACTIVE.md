# FMP_ACTIVE

Categories: INCAR tag, Molecular dynamics, Ensemble properties

FMP\_ACTIVE = logical (aray)

|  |  |  |
| --- | --- | --- |
| Default: **FMP\_ACTIVE** | = NIONS \* False |  |

Description: Select which atom types in the POSCAR-file participate in swapping within the Müller-Plathe method.

---

FMP\_ACTIVE specifies whether or not (.TRUE. or .FALSE., respectively) an atomic type allowed for swapping within the Müller-Plathe method. One item for each of the atomic types defined in POSCAR must be supplied.

> **Mind:** This tag will only be available from VASP 6.4.4

## Related tags and articles

Müller-Plathe method,
FMP\_DIRECTION,
FMP\_SNUMBER,
FMP\_SWAPNUM,
FMP\_PERIOD
