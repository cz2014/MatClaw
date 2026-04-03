# NMAXFOCKAE and LMAXFOCKAE

Categories: INCAR tag, Exchange-correlation functionals, Hybrid functionals, Many-body perturbation theory, GW

**NMAXFOCKAE** = 1|2

|  |  |  |
| --- | --- | --- |
| Default: **NMAXFOCKAE** | = 1 |  |

**LMAXFOCKAE** = [integer]

|  |  |  |
| --- | --- | --- |
| Default: **LMAXFOCKAE** | = -1 | for Hartree-Fock and hybrid functionals |
|  | = 4 | for post DFT methods |

Description: **NMAXFOCKAE** and **LMAXFOCKAE** determine whether
the overlap densities in the Fock exchange and correlated wave function methods are accurately reconstructed on the plane wave grid (shape restoration). This flag generally only applies to the Fock-exchange part as well as many-body
post DFT methods (GW, RPA, MP2, etc.).

---

## Detailed Discussion

In the PAW method, the difference between the charge density of the all-electron partial waves $\phi\_\beta$ and
the pseudo partial waves $\tilde \phi\_\beta$

$Q\_{\alpha\beta}({\mathbf r})= \phi^\*\_\alpha({\mathbf r})\phi\_\beta({\mathbf r}) - \tilde \phi^\*\_\alpha({\mathbf r})\tilde \phi\_\beta({\mathbf r})$

is usually treated on spherical grids centered at each atom
(one-center terms inside the PAW spheres, see PAW method and more detailed description for LMAXFOCK). To describe long range electrostatic effects, the *moments* of the differences of the all-electron and pseudo charge density
also need to be added on the plane wave grid (compensation density, see PAW method).
These compensation charges exactly restore the moments of the all-electron density on the plane wave
grid. For the Fock exchange the maximum *L* quantum number up to which
the augmentation is done is controlled by LMAXFOCK.

For the RPA, GW, and most post DFT methods, the one-center terms are, however, presently
not implemented. Depending on the material, this can cause sizable errors
in particular for 3d and (to a lesser extent) 2p, 4d and 5d elements.
To correct for this error, an alternative treatment is implemented
on the plane wave grid for the exchange and correlation contributions.
This allows to restore the all-electron densities accurately already on the plane wave grid
by specifying the flags **LMAXFOCKAE** and **NMAXFOCKAE**. This improved
treatment— termed shape restoration —is available for exchange as well as many body correlation contributions.
For exchange, the exact one-center terms are also implemented. This means shape restoration is not required and should not change the results.

To achieve the improved treatment on the plane wave grid, $Q\_{\alpha\beta}({\mathbf r})$ is Fourier transformed to reciprocal space $Q\_{\alpha\beta}(q)$ and then expanded
in a set of orthogonal functions localized at each atomic site. These augmentation charges
are then added to the pseudo charge densities on the plane wave grid. Shape restoration is only accurate up to a certain plane wave cutoff, typically about 150 eV for **NMAXFOCKAE** =1, and 400 eV for **NMAXFOCKAE** = 2. Experience shows that **NMAXFOCKAE** =1 is sufficient to predict very accurate energy differences and quite accurate quasiparticle energies.

For **LMAXFOCKAE**=-1 (the default for DFT and Hartree-Fock calculations), only the moments of the all-electron charge densities are restored on the plane wave grid. This is the default for Hartree-Fock calculations, and the setting is very precise since for Hartree-Fock the one-center terms are implemented in radial grids as for DFT.

If **LMAXFOCKAE** is set to values larger than -1 (and **NMAXFOCKAE**=1), not only the moments of the all-electron charge density are restored on the plane wave grid, but also the all-electron charge density is restored up to a typical plane wave energy of 150 eV (controlled by QMAXFOCKAE). This setting yields very accurate results for post DFT methods (MP2, RPA, GW, etc.) for most sp bonded materials. **LMAXFOCKAE** is used to specify the maximum spherical (*L*) quantum number up
to which this more accurate treatment is used. The default is **LMAXFOCKAE**=4 for post DFT methods.
If no accurate augmentation is desired by the user, simply set **LMAXFOCKAE**=-1 in the INCAR file.

If **LMAXFOCKAE** is set to values larger than -1 and **NMAXFOCKAE**=2, the charge density is restored accurately on the plane wave grid up to a typical plane wave energy of 400 eV. As before, **LMAXFOCKAE** can be used to specify the maximum spherical (*L*) quantum number up
to which this more accurate treatment is used. **NMAXFOCKAE**=2 yields very accurate results for
post DFT methods (MP2, RPA, GW) even for difficult 3d elements. For RPA and MP2 total energy calculations, differences between **NMAXFOCKAE**=1 and **NMAXFOCKAE**=2 are usually tiny for total energy differences. Since the absolute correlation energies might change, it is, however, vital to use the same setting for
**NMAXFOCKAE** and **LMAXFOCKAE**, if energy differences are calculated.
For GW calculations, increasing **NMAXFOCKAE** from 1 to 2 might change QP energies by 100-200 meV for 3d and late 4d and 5d elements. Despite the improve precision, **NMAXFOCKAE**=2 should be used with great caution. Specifically, noise and egg-box effects are introduced as **NMAXFOCKAE** is increased. So use
this flag only after extensive tests.

The setting for **LMAXFOCKAE** should be also considered carefully. Generally, it suffices to set **LMAXFOCKAE** to twice the maximum *l* quantum number found in the POTCAR file.
For instance for sp elements, **LMAXFOCKAE**= 2 suffices. For d elements, **LMAXFOCKAE**= 4 suffices
(a d electron can create charge densities with *L*-quantum numbers up to 4), whereas for f elements, users
should test whether **LMAXFOCKAE**= 6 is required.

More details on shape restoration are explained in Ref. and .

## Usefull Settings

In summary, useful manual settings of **NMAXFOCKAE** and **LMAXFOCKAE** are:

* **LMAXFOCKAE**=-1, to switch off the accurate augmentation altogether (reduces noise in correlation energies).
* **LMAXFOCKAE**=4 (or larger) to force an accurate treatment for the charge augmentation on the plane wave grid (can be selected even in Hartree-Fock type calculations, but causes some additional noise).
* **NMAXFOCKAE**=2, to select the very accurate augmentation on the plane wave grid. Please check whether the VASP default setting for **LMAXFOCKAE** suffices (OUTCAR file). Use this setting only with care, as it can result in very noisy data for coarse FFT grids.

## Related tags and articles

LMAXFOCK, QMAXFOCKAE, LFOCKAEDFT

Examples that use this tag

---
