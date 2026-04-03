# QUAD_EFG

Categories: INCAR tag, NMR

QUAD\_EFG = [real array]  
 Default: **QUAD\_EFG** = NTYP\*1.0

Description: nuclear quadrupole moment (in millbarn) for the atomic types on the POTCAR file.

---

Setting the QUAD\_EFG tag allows the conversion of the *V*zz (see LEFG) values into the quadrupole coupling constants *C*q often encountered in NMR literature.
The conversion formula is as follows (*Q* is the element and isotope specific quadrupole moment):

:   $$C\_q = \frac{e Q V\_{zz}}{h}.$$

> **Tip:** Several definitions of $C\_q$ are used in the NMR community.

The QUAD\_EFG tag specifies the nuclear quadrupole moment in millibarns for each atomic species, in the same
order as in the POTCAR file. The output *C*q is in MHz. An online compilation of nuclear quadrupole moments can be found online in a database or in Ref. (updated numbers in Ref. ).

Suppose a solid contains Al, C, and Si, then the QUAD\_EFG tag could read:

```
QUAD_EFG = 146.6 33.27 0.0
```

27Al is the stable isotope of Al with a natural abundance of 100% and *Q*=146.6.
The stable isotopes 12C and 13C are not quadrupolar nuclei, however, the radioactive
11C is. It has *Q*=33.27. For Si, all stable isotopes have I≤1/2, making it redundant to calculate a *C*q. No moments are known for the other isotopes.

> **Important:** For heavy nuclei inaccuracies are to be expected because of an incomplete treatment of relativistic effects.

## Related tags and articles

LEFG

Examples that use this tag

## References
