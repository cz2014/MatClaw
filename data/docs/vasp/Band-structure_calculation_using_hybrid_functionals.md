# Band-structure calculation using hybrid functionals

Categories: Hybrid functionals, Band structure, Howto

Band-structure calculations for hybrid functionals require multiple steps. Below we give a step-by-step introduction and an example. Additionally, we provide some advice to reduce computational and human effort.

## Step-by-step instructions

For hybrid functionals, the Hamiltonian cannot be expressed in terms of the electronic charge density alone. Instead, the Kohn-Sham orbitals on a regular **k** mesh are required for any calculation within the formalism of hybrid functionals. The regular **k** mesh must be supplied in the KPOINTS file. Consequently, restarting a hybrid calculation requires the WAVECAR file of the previous self-consistent-field (SCF) run. This is in contrast to density-functional theory (DFT), where the electronic charge density written to the CHGCAR file suffices to restart a DFT calculation. In order to reach convergence more quickly, it is good practice to first compute the DFT result in a SCF calculation.

**Step 1 (optional):** Run an SCF calculation to obtain a converged WAVECAR file for DFT.

Band-structure calculations generally compute the Kohn-Sham orbitals and eigenenergies along a path in reciprocal space which usually connects high-symmetry points in the first Brillouin zone. Some external tools help to identify the high-symmetry points and **k** points along a high-symmetry path for materials of any symmetry.

**Step 2:** Determine the high-symmetry path along which VASP should compute the band structure.

There are two options to simultaneously supply a regular **k** mesh *and* **k** points along a high-symmetry path to VASP.

:   1. Provide an explicit list of **k** points with zero-weighted **k** points.
    :   Here, the explicit list of the irreducible **k** points of the regular **k** mesh can be copied from the IBZKPT file of a previous run to the KPOINTS file. For instance, use the IBZKPT file of step 1. These irreducible **k** points must be weighted by their multiplicity according to the system's symmetry. Additionally, the **k** points along a high-symmetry path must be added to the KPOINTS file with the value of all weights set to zero.

:   2. Provide an additional KPOINTS\_OPT file that can specify the high-symmetry path in line mode.
    :   Generally, the KPOINTS file and the KPOINTS\_OPT file accept the same format. But again, the regular **k** mesh needs to be supplied in the KPOINTS file and the high-symmetry path in the KPOINTS\_OPT file. We therefore recommend using the Γ-centered mesh or Monkhorst-Pack mesh, and line mode, respectively.

The KPOINTS\_OPT method is more convenient because it allows using the automatic generation modes for the **k** points. The computational cost and memory requirement can vary for the two methods due to the scaling behaviour with the number of **k** points.

**Step 3:** Supply a regular **k** mesh and **k** points along a high-symmetry path either using the explicit list including zero-weighted **k** points or using a KPOINTS\_OPT file.

By default VASP uses auxiliary functions (HFALPHA) for the truncation of the Coulomb singularity, but this method leads to discontinuities in band-structure calculations. We recommend using the Coulomb truncation (HFRCUT) instead. In particular, HFRCUT=-1 converges best for systems with a band gap.

**Step 4:** Set HFRCUT in the INCAR file and restart the hybrid calculation from the DFT WAVECAR file.

**Step 5:** Plot the band structure, e.g., using py4vasp. In a python notebook in the directory of the calculation, you can execute

```
import py4vasp as pv
calc = pv.Calculation.from_path(".")
calc.band.plot()
# calc.band.plot("kpoints_opt") # if the high-symmetry path is in KPOINTS_OPT
```

## Recommendations and advice

In case a KPOINTS\_OPT file is present, VASP computes the band energies for the **k** points of the KPOINTS\_OPT file after SCF is reached within the same submitted job. Their convergence is checked independently by requiring the sum over occupied band energies not to change in two successive iterations. Hence, for the computational time, there is no advantage to restart from a converged hybrid calculation, but in principle it is possible.

In contrast, the method using an explicit list including zero-weighted **k** points computes the band energies for all **k** points at each SCF step. The convergence criterion considers the total energy and, thus, does not account for convergence of KS orbitals at zero-weighted **k** points. Taking the KS orbitals of the zero-weighted **k** points along the entire SCF run makes their convergence highly likely. However, restarting from a converged hybrid calculation can result in premature stopping. This can be counteracted by setting the NELMIN tag to a higher value. Especially if the hybrid calculation needs many SCF steps to reach convergence and each SCF step is very expensive when including zero-weighted **k** points, one may consider to restart from a converged hybrid calculation with NELMIN set to a large number. We recommend carefully checking the convergence of the band structure in this case.

> **Tip:** For a band-structure calculation with an explicit list including zero-weighted **k** points, avoid restarting from a converged hybrid WAVECAR file.

It is possible to achieve very fine sampling along the **k** path with both methods, but there are some aspects to take into account. As mentioned, the computational cost and memory requirement can vary for the two methods due to the scaling with the number of **k** points. For the KPOINTS\_OPT method, the number of **k** points treated simultaneously can be controlled by means of the KPOINTS\_OPT\_NKBATCH tag. For the explicit list including zero-weighted **k** points, VASP may exceed the available memory if the number of zero-weighted **k** points is large. In that case, split the hybrid band-structure calculation into multiple calculations. For each calculation, add part of the zero-weighted **k** points.

> **Tip:** Make fine sampling computationally feasible using the KPOINTS\_OPT\_NKBATCH tag or splitting the calculation with part of the zero-weighted **k** points.

Let us stress a significant difference between hybrid band-structure calculations and DFT band-structure calculations. The electronic charge density suffices for density functionals to define the Hamiltonian, and no regular **k** mesh is required during DFT band-structure calculations. However, if no regular **k** mesh is provided, the electronic charge density must be fixed during the DFT band-structure calculation by setting ICHARG=11 in the INCAR file.

> **Warning:** The electronic charge density must not be fixed for any hybrid calculation, i.e., never set ICHARG=11!

> **Tip:** To understand how the two methods work in practice, try using them with a DFT calculation as if it were a hybrid calculation.

If you forgot setting HFRCUT you may be able to mitigate the band structure. Semi-core states can be assumed to be dispersionless but you will see the same discontinuities featured on the semi core states. By subtracting the faulty dispersion of the semi-core state from all bands, you can recover the true dispersion of the conduction bands.

## Example of **k** points for hybrid band-structure calculation

For instance, for cubic-diamond Si with the following POSCAR file

```
 cd Si
 5.5
  0.0    0.5     0.5 
  0.5    0.0     0.5 
  0.5    0.5     0.0 
   Si
   2
 Fractional
  -0.125 -0.125 -0.125
   0.125  0.125  0.125
```

we can generate a regular k mesh using the following KPOINTS file

```
 Regular k-points mesh
 0
 Monkhorst-Pack method
  3 3 3 
  0 0 0
```

The resulting IBZKPT file contains the following lines:

```
 Automatically generated mesh
      4
 Reciprocal lattice
   0.00000000000000    0.00000000000000    0.00000000000000             1
   0.33333333333334    0.00000000000000   -0.00000000000000             8
   0.33333333333334    0.33333333333334   -0.00000000000000             6
  -0.33333333333334    0.33333333333334    0.00000000000000            12
```

For the explicit **k**-points list, copy the regular **k** mesh from the IBZKPT file and add, e.g., 5 **k** points from Γ to X with zero weight:

```
 Explicit k-points list
      9
 Reciprocal lattice
   0.00000000000000    0.00000000000000    0.00000000000000             1
   0.33333333333334    0.00000000000000   -0.00000000000000             8
   0.33333333333334    0.33333333333334   -0.00000000000000             6
  -0.33333333333334    0.33333333333334    0.00000000000000            12
   0.00000000       0.00000000       0.00000000 0   
   0.12500000       0.00000000       0.12500000 0
   0.25000000       0.00000000       0.25000000 0
   0.37500000       0.00000000       0.37500000 0
   0.50000000       0.00000000       0.50000000 0
```

For the KPOINTS\_OPT method, the same path from Γ to X can be specified by creating the following KPOINTS\_OPT file

```
 k points for band structure
 5  ! intersections 
 line-mode
 Fractional
   0.0000000000     0.0000000000     0.0000000000 Γ
   0.5000000000     0.0000000000     0.5000000000 X
```

And continue using the following KPOINTS file

```
 Regular k-points mesh
 0
 Monkhorst-Pack method
  3 3 3 
  0 0 0
```

## Related tags and articles

KPOINTS, KPOINTS\_OPT, List of hybrid functionals, Hybrid functionals: formalism, Coulomb singularity

## References
