# NGYROMAG

Categories: INCAR tag, NMR

NGYROMAG = [real array]  
 Default: **NGYROMAG** = NTYP\*1.0

Description: NGYROMAG specifies the nuclear gyromagnetic ratios (in MHz, for H0 = 1 T) for the atomic types on the POTCAR file.

---

By means of the NGYROMAG-tag one can specify the nuclear gyromagnetic ratio:

```
NGYROMAG = gamma_1  gamma_2 ... gamma_N
```

where one should specify one number for each of the *N* species on the POSCAR file, i.e. if C, H, N, and O are listed as species in the POSCAR file, then there should be four numbers in NGYROMAG, regardless of how many total atoms there are.

> **Important:** If one does not set NGYROMAG in the INCAR file, VASP assumes a factor of 1 for each species.

NGYROMAG is given in units of MHz/T, see Ref. for a table of different gyromagnetic ratios. A more extensive list is available on which converts isotopic magnetic moments from Ref. and converts them using the definition of the gyromagnetic ratio defined in Ref. .

## Related tags and articles

LHYPERFINE

Calculating the hyperfine coupling constant

Examples that use this tag

---
