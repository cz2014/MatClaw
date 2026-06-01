# FERWE

Categories: INCAR tag, Electronic occupancy, Density of states

FERWE = [real array]

Description: FERWE sets the occupancies of the states for ISMEAR=-2.

---

To set the occupancies, specify

```
 FERWE = f(1) f(2) f(3) ... f(NBANDS×Nk)
```

The occupancies must be specified for all bands and k points.
The band index runs fastest.
The occupancies must be between 0 and 1.
In the case of spin-polarized calculations (`ISPIN = 2`), FERWE sets the occupancies of the states in the up-spin channel.
Specify the occupancies of the states in the down-spin channel by means of the FERDO tag.

Note that the partial occupancies are also written to the OUTCAR file

```
k-point     8 :       0.3750    0.0000    0.0000
 band No.  band energies     occupation
     1      -2.0636      2.00000
     2       0.1506      2.00000
     3       6.0155      1.99808
     4       6.0188      1.99432
     5       7.3309      1.71014
     6       7.3311      1.54777
     7       8.0841      0.28501
     8       8.0894      0.18039
     9       9.5834      0.00086
    10       9.5880      0.00071
    11      13.0368      0.00000
    12      14.3253      0.00000
```

Keep in mind that for systems without spin-polarization the occupations are twice as large in the OUTCAR file than what you should provide for FERWE because of spin degeneracy.

> **Mind:** VASP changes the number of bands NBANDS to accommodate your parallel setup. If NBANDS is inconsistent with the number of elements you provide with FERWE VASP will exit with an error message. The used NBANDS is indicated in the error message. Adjust the occupancies provided to FERWE to this new value. Alternatively, you can choose an NBANDS as the common factor of all your parallel setups to avoid changes in the number of bands (see here).

You can use FERWE to keep occupancies fixed during ionic relaxations or molecular dynamics simulations.
However, keeping the orbital occupancies fixed, requires that the orbital order does not change during the self-consistency cycle or during the optimization of the orbitals.
Imagine, for instance, that the eigenenergy of the 65th orbital moves below the orbital energy of the 64th orbital.
By default, VASP will order the eigenenergies so that enforcing FERWE will move the electrons to the originally unoccupied 65th orbital because it has now the lower energy.
This problem can be often circumvented by specifying `LDIAG = .FALSE.` in the INCAR file.

## Related tags and articles

FERDO,
ISMEAR,
NBANDS,
LDIAG

Examples that use this tag
