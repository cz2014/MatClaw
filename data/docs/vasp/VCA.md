# VCA

Categories: INCAR tag, Projector-augmented-wave method

VCA = [real array]  
 Default: **VCA** = read from the POTCAR file

Description: VCA is short for the virtual crystal approximation; the tag allows to "weight" each species found in the POTCAR file.

---

The tag VCA must be supplied for each atom type or species found in the POTCAR and POSCAR file, respectively.
It weights the corresponding POTCAR files according to the values given in the INCAR file, with the default
being 1. For instance, the formal valency found in the POTCAR files is multiplied by the supplied values. Likewise, the local potential,
the augmentation charges, and the non-local pseudopotential strength parameters are scaled by the supplied values.

It is possible to use this flag to perform calculations in the framework of the virtual crystal approximation.
Say you want to simulate Sn doping in a Ge lattice. This can be achieved using a POTCAR file with a Ge and Sn data set and the following
POSCAR file:

```
cd:
  1.00000000000000
    2.82173    2.82173    0.00000
    0.00000    2.82173    2.82173
    2.82173    0.00000    2.82173
  Ge   Sn
    2     2
Direct
 0.00  0.00  0.00
 0.25  0.25  0.25
 0.00  0.00  0.00
 0.25  0.25  0.25
```

If VCA is set to

```
 VCA = 0.99 0.01
```

the Ge atoms are weighted with a weight of 0.99, whereas the Sn atoms are weighted by 0.01 (see for an example application).
The implementation in VASP closely follows the methodology suggested by Bellaiche and Vanderbilt .

Caveats: Unfortunately, results of this kind of VCA calculations are often not very reliable. The problems are even apparent in the original publications . The
key point is that the used PAW potentials need to be constructed so that the pseudo atomic waves are very similar for the potentials that are "mixed" (in the example above, this would be the Ge and Sn potentials). This can be achieved by carefully optimizing the radial cutoffs. Furthermore, the local potentials of the two POTCAR files need to be very similar. This means that results for many standard potentials are not accurate. For instance, Vegard's law is often not even approximately observed (instead, the volume is too large at 50 % mixing). The problem is particularly severe if semi-core states are treated as valence states. For instance, for the Ge and Sn alloy, the d electrons had to be treated as core electrons to obtain reasonable results. Any attempts to treat the d electrons as valence states lead to grossly incorrect results.

**Mind:** This tag is currently not supported in combination with IBRION = 5-8 for computing second derivatives, Hessian matrices, and phonon frequencies.

## Related tags and articles

LVCADER

## References
