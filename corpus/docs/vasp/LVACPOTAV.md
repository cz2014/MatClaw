# LVACPOTAV

Categories: Electrostatics, INCAR tag

LVACPOTAV = .True. | .False.  
 Default: **LVACPOTAV** = .False.

Description: Switch on determining the vacuum potential by averaging the local potential over a field-free region.

---

LVACPOTAV switches on the computation of the vacuum potential, i.e., the average of the local potential in the vacuum region.
It computes the average potential by searching regions that are field-free (VACPOTFLAT), and the 2D-averaged charge density is nearly zero. The averaging is done in the direction of IDIPOL and is reported as the vacuum potential in the OUTCAR.

> **Tip:** As LVACPOTAV performs a post-processing step, you may use it together with ALGO = None by restarting a converged calculation.

The vacuum potential is one of the quantities needed to compute the work function. It can be extracted from the OUTCAR by the following bash command

```
 grep upper OUTCAR
```

Note that two vacuum potentials will be produced, one corresponding to the upper termination of the slab and one corresponding to the lower. Depending on the system, one might be more interesting than the other.

> **Tip:** For determining the work function, we suggest using LVACPOTAV along with the LVHAR tag such that only the sum of the Hartree and ionic potentials are used in the calculation of the vacuum potential. This choice is because the exchange-correlation potential might be noisy in the vacuum region but should, in principle, be zero.

> **Mind:** LVACPOTAV is available only for versions after 6.4.3.

Before VASP 6.4.3, the default algorithm reports the 2D-averaged potential four grid points from the the minimum 2D-averaged charge density in the direction of IDIPOL, i.e., no averaging is performed along the surface normal of the 2D-averaged potential.

### Use in conjunction with the dipole correction

A typical use case for LVACPOTAV is together with the dipole correction (including tags LDIPOL and IDIPOL). Switching on the dipole correction is crucial for determining the vacuum potential; without it, there will be no field-free region for dipolar systems.

> **Mind:** Note that LVACPOTAV is currently implemented for IDIPOL between 1 and 3.

### Warnings

In case LVACPOTAV is not able to generate an accurate work function, the following warnings may be found in the OUTCAR file.

#### Vacuum region is likely too small

```
|     Did not find any points to average over, which means that no vacuum     |
|     field-free region was found. Please increase the size of  your cell     |
|     in the dimension of the dipole correction to obtain accurate            |
|     workfunction values.                                                    |
```

A possible solution to this problem is to increase the size of the vacuum dimension in your cell.

#### The minimum charge density in your cell may be too large

```
|     The minimum charge density times volume of the cell along the axis      |
|     of the dipole correction is larger 1E-1, which could mean that your     |
|     workfunction is not accurate as there is no field free region in        |
|     your cell. Please consider either increasing the size of your cell      |
|     along the dipole correction (vacuum dimension) or perhaps               |
|     increasing the precision of your calculation.                           |
```

Possible solutions include:

* Making sure you have a large enough vacuum dimension.
* Increasing the precision of your calculation by changing EDIFF.

## Related tags and articles

DIPOL,
LDIPOL,
IDIPOL,
VACPOTFLAT,
WRT\_POTENTIAL,
LVTOT,
LVHAR

Computing the work function
