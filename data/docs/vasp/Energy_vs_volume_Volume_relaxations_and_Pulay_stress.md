# Energy vs volume Volume relaxations and Pulay stress

Categories: Ionic minimization, Howto

If you are doing energy-volume calculations or cell shape and volume relaxations you must understand the Pulay stress and related problems.

The Pulay stress arises from the fact that the plane-wave basis set is not complete with respect to changes in the volume. Thus, unless absolute convergence with respect to the basis set has been achieved - the diagonal components of the stress tensor are incorrect. This error is often called "Pulay stress". The error is almost isotropic (i.e. the same for each diagonal component), and for a finite basis set it tends to decrease volume compared to fully converged calculations (or calculations with a constant energy cutoff).

The Pulay stress and related problems affect the behavior of VASP and any plane wave code in several ways: First, it evidently affects the stress tensor calculated by VASP, i.e. the diagonal components of the stress tensor are incorrect, unless the energy cutoff is very large (ENMAX=1.3 \*default is usually a safe setting to obtain a reliable stress tensor). In addition, it should be noted that all volume/cell shape relaxation algorithms implemented in VASP work with a constant basis set. In that way, all energy changes are strictly consistent with the calculated stress tensor, and this, in turn, results in an underestimation of the equilibrium volume unless a large plane wave cutoff is used. Keeping the basis set constant during relaxations has also some strange effect on the basis set. Initially, all G-vectors within a sphere are included in the basis. If the cell shape relaxation starts the direct and reciprocal lattice vectors change. This means that although the number of reciprocal G-vectors in the basis is kept fixed, the length of the G-vectors changes, changing indirectly the energy cutoff. Or to be more precise, the shape of the cutoff region becomes an ellipsoid. Restarting VASP after a volume relaxation causes VASP to adopt a new "spherical" cutoff sphere and thus the energy changes discontinuously.

One thing which is important to understand is that problems due to the Pulay stress can often be neglected if only volume conserving relaxations are performed. This is because the Pulay stress is usually almost uniform and it, therefore, changes the diagonal elements of the stress tensor only by a certain constant amount (see below). In addition, many calculations have shown that Pulay stress-related problems can also be reduced by performing calculations at different volumes using the same energy cutoff for each calculation (this is what VASP does by default) and fitting the final energies to an equation of state. This of course implies that the number of basis vectors is different at each volume. Calculations with many plane-wave codes have shown that such calculations yield reliable results for the lattice constants and the bulk modulus and other elastic properties even at relatively modest energy cutoffs. Constant energy cut-off calculations are less prone to errors caused by the basis set incompleteness than constant basis set calculations. But it should be kept in mind that volume changes and cell shape changes must be rather large in order to obtain reliable results from this method because within the limit of very small distortions the energy changes obtained with this method are equivalent to those obtained from the stress tensor and are therefore affected by the Pulay stress. Only volume changes of the order of 5-10 % guarantee that the errors introduced by the basis set incompleteness are averaged out.

:   > **Mind:** There are two newer wiki articles that have been written on this subject: Volume relaxation and Pulay stress

## Pulay Stress

How to calculate the Pulay stress

The Pulay stress shows only a weak dependency on volume and the ionic configuration. It is mainly determined by the composition. The simplest way to estimate the Pulay stress is to relax the structure with a large basis-set ($1.3\times$ default cutoff is usually sufficient, or PREC=*High* in VASP.4.4). Then re-run VASP for the final relaxed positions and cell parameters with the default cutoff or the desired cutoff. Look for the line 'external pressure' in the OUTCAR file:

```
 external pressure =    -100.29567 kB
```

The corresponding (negative) pressure gives a good estimation of the Pulay stress.

## Accurate bulk relaxations with internal parameters (one)

The general message is: whenever possible avoid volume relaxation at the default energy cutoff. Either increase the basis set by setting ENCUT manually in the INCAR file, or use the method two suggested below. This avoids doing volume relaxations at all. If volume relaxations are the only possible and feasible option please use the following step by step procedure (which minimizes errors to a minimum):

* Relax from starting structure (ISMEAR should be 0 or 1).
* Start a second relaxation from previous CONTCAR file (re-relaxation).
* As a final step, perform one more energy calculation using the tetrahedron method switched on (i.e. ISMEAR=-5), to obtain highly accurate energies (no relaxation for the final run). Possibly increase the energy cutoff even further.

A few things should be remarked here: never used the energy obtained at the end of a relaxation run, if you allow for cell shape relaxations (the final basis set might not correspond to the desired spherical cutoff sphere). Instead, perform one additional static run after completing the relaxation.

If the relaxation will yield a structure with reasonably small structural "errors", the final error in the energy of step 3 is only of second-order (with respect to the structural errors). If you take the energy directly from the relaxation run, errors are usually significantly larger. Another important point is that the most reliable results for the relaxation are obtained if the starting cell parameters are very close to the final cell parameters. If different runs yield different results, then the one run that started from the configuration, which was closest to the relaxed structure, is the most reliable one.

We strongly recommend doing any volume (and to a lesser extent cell shape) relaxation with an increased basis set. ENCUT=$1.3\times$ default cutoff is reasonable accurate in most cases. PREC=*High* does also increase the energy cutoff by a factor of 1.25. At an increased cutoff the Pulay-stress correction is usually not required.

Finally, if the default cutoff is used for the relaxation, the PSTRESS tag should be set in the INCAR file: evaluate the Pulay stress along the guidelines given in the previous section and add an input line to the INCAR file reading (usually a negative number):

```
PSTRESS = Pulay stress
```

From now on all *STRESS* output of VASP is corrected by simply subtracting PSTRESS. In addition, all volume relaxations will take PSTRESS into account.
It should be said again, use PSTRESS only if increasing the cutoff is not a viable option for some reason.

## Accurate bulk relaxations with internal parameters (two)

It is possible to avoid volume relaxation in many cases: The method we have used quite often in the past is to relax the structure (cell shape and internal parameters) for a set of fixed volumes (ISIF=4). The final equilibrium volume and the ground-state energy can be obtained by a fit to an equation of state. The reason why this method is better than volume relaxation is that the Pulay stress is almost isotropic, and thus adds only a constant value to the diagonal elements of the stress tensor. Therefore, the relaxation for a fixed volume will yield highly accurate structures.

The outline for such a calculation is almost the same as in the previous section. But in this case, one has to do the calculations for a set of fixed volumes. At first sight, this seems to be much more expensive than method number one (outlined in the previous section). But in many cases, the additional costs are only small, because the internal parameters do not change very much from volume to volume. The following steps have to be done in these calculations:

* Select one volume and relax from starting structure keeping the volume fixed (ISIF=4; ISMEAR=0 or 1).
* Start a second relaxation from the previous CONTCAR file (if the initial cell shape was reasonable this step can be skipped if the cell shape is kept fixed, you never have run VASP twice).
* As a final step, perform one more energy calculation with the tetrahedron method switched on (ISMEAR=-5), to get very accurate unambiguous energies (no relaxation for the final run).

The method has also other advantages, for instance, the bulk modulus is readily available. We have found in the past that this method can be used safely with the default cutoff.

## FAQ: Why is my energy vs. volume plot jagged

This is a very common question from people who start to do calculations with plane wave codes. There are two reasons why the energy vs. volume plot looks jagged:

* Basis set incompleteness. The basis set is discrete and incomplete, and when the volume changes, additional plane waves are added. That causes small discontinuous changes in the energy.
  + Solutions:
    - Use a larger plane wave cutoff: This is usually the preferred and simplest solution.
    - Use more k-points : this solves the problem, because the criterion for including a plane wave in the basis set is $\vert {\bf G} + {\bf k} \vert \lt {\bf G}\_{\rm cut}$. This means at each k-point a different basis set is used, and additional plane waves are added at each k-point at different volumes. In turn, the energy vs. volume curve becomes smoother.
* A second possible reason for the jagged E(V) curve is the use of PREC=Normal. For PREC=Accurate the FFT grids are chosen such that ${\bf H} \vert \phi\gt$ is exactly evaluated. For PREC=Normal the FFT grids are set to 3/4 of the value that is required for an exact evaluation of ${\bf H} \vert \phi\gt$. This introduces small errors because when the volume changes the FFT grids change discontinuously. In other words, at each volume a different FFT grid is used, causing the energy to jump discontinuously between different volumes.
  + Solutions:
    - Use PREC=Accurate, or increase the plane wave cutoff.
    - Set your FFT grids manually, and choose the one that is used per default for the largest volume (obviously a laborious solution).

---
