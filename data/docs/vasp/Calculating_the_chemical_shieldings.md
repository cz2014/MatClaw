# Calculating the chemical shieldings

Categories: Howto, NMR, Linear response

The chemical shielding tensor *σ* is the relation between the induced and external magnetic fields and describes how much the electrons shield the nuclei from an external field. The absolute chemical shielding is calculated by linear response using LCHIMAG . The chemical shielding is directly related to the chemical shift *δ* recorded in nuclear magnetic resonance (NMR), cf. NMR category page and LCHIMAG page for details, and, indirectly, to the resonance frequency. The theory is covered in the NMR category page and LCHIMAG page.

> **Warning:** The chemical shifts are calculated from the orbital magnetic response under the assumption that the system is an insulator. Smearing schemes intended for metals can generate nonsense.

## Step-by-step instructions

The chemical shielding is calculated post-self-consistent field (post-SCF) using LCHIMAG. A well-converged SCF calculation is therefore crucial. The chemical shielding is very sensitive to several input parameters that must all be independently tested.

**Step 1 (optional):** Calculate the chemical shielding using a previously converged calculation

Since the chemical shielding is calculated post-SCF, you can use a previously converged WAVECAR with ISTART = 1 and NELM = 1. The corresponding density, CHGCAR is calculated from the WAVECAR file before the first elementary step so it need not be included.

**Step 2 (optional):** Determine a suitable energetic break value

The break condition for the self-consistency step EDIFF strongly influences the chemical shielding. A setting of EDIFF = 1E-8 eV is generally recommended. Convergence is taken to be within 0.1 ppm.

**Step 3:** Converge the plane-wave basis

A large plane-wave energy cutoff is required to fully converge the chemical shieldings. Perform multiple calculations while increasing the basis set size, as defined in ENCUT, incrementally (e.g., by 100 eV intervals). Convergence should be aimed to be within 0.1 ppm, although this will not be feasible for heavier elements.

**Step 4:** Converge the **k** point mesh

Similar to the basis, the **k** point mesh can strongly influence the chemical shielding. The **k** point mesh should be increased incrementally, i.e., 1x1x1, 2x2x2, 3x3x3, until convergence within 0.1 ppm is achieved. It is only necessary to converge the **k** point mesh for crystals, gas-phase molecules should use the Γ-point only.

**Step 5:** Compare to experiment

The purpose of these calculations is to compare to experiment. However, the calculated absolute chemical shieldings are not directly comparable to the measured chemical shift due to the lack of a reference. To avoid bias from any single calculation, a series of calculated and their corresponding experimental values are used. The experimental chemical shifts are plotted against the calculated chemical shieldings as is found in Fig. 3 of Ref. .

## Recommendations and advice

Calculating the chemical shielding requires tightly converged settings. As described in the step-wise introduction above, converging with respect to EDIFF, ENCUT, and the **k** point mesh is very important. There are a few additional settings that should be considered.

### PAW pseudopotentials

The standard PAW pseudopotentials POTCAR used are sufficient for calculating the chemical shielding. The GIPAW is applied using the projector functions and partial waves that are stored in the regular POTCAR files. The completeness of these projector functions and partial waves determines the quality of the results. Using slightly different types of POTCAR, e.g., GW (*\*\_GW*) or with additional valence (*\*\_sv*, *\*\_pv*), can change the calculated shielding by a few ppm for the first and second row *sp*-bonded elements (except for H).

The PAW reconstruction with all-electron partial waves is crucial for calculating the field on the nucleus. It is therefore important to use a consistent exchange-correlation functional and so LEXCH in the POTCAR should not be overwritten with an explicit GGA tag in the INCAR if possible.

### Insufficient memory

For calculating the chemical shieldings, speed had been favored over saving memory, resulting in insufficient memory occasionally. Since the linear response calculation is parallel over **k** points, this can be used to economize on memory by performing a regular SCF calculation at high accuracy on the full **k** point mesh and saving the CHGCAR file. Using `ICHARG = 11` start a chemical shielding calculation for each individual **k** point in the first Brillouin zone (IBZ) separately, starting from CHGCAR. The shieldings can then be calculated as a **k** point weighted average of the symmetrized shieldings of the individual **k** points.

### Additional tags

To ensure tight precision, the precision should be set to `PREC = Accurate`, rather than `Normal`.

Several additional INCAR tags should be considered. Specifically, LASPH should be set to `.TRUE.`, turning on the non-spherical contributions to the gradient of the density inside the PAW spheres. Occasionally, e.g. for systems containing H or first-row elements, and short bonds, the two-center contributions to the augmentation currents in the PAW spheres are important. In this case, LLRAUG = .TRUE. should be used .

Calculating the chemical shift can also be sped up by utilizing parallelisation. If you are using multiple k-points, then you can treat these in parallel using KPAR, reducing the overall calculation time.

> **Important:** The treatment of the orbital magnetism is non-relativistic. This is suitable for light nuclei.
>
> The standard POTCARs are scalar-relativistic and account partially for relativistic effects.
> The accuracy can be improved using LBONE, which restores the small B-component of the wave function inside the PAW spheres.
> Spin-orbit coupling is not implemented for chemical shift calculations.

# Example scripts for convergence tests

Several tests are necessary to obtain various NMR parameters. Make sure to change the example INCAR files to include the tags for your desired calculation. We provide some example scripts below:

## Energetic break criterion tests

For converging the energetic break criterion for a single ionic step (EDIFF), start with the 1E-4 and then increase by orders of magnitude:

Energetic break criterion:
**INCAR.nmr**

```
PREC = Accurate        
ENCUT = 400.0          
EDIFF = 1E-4          
ISMEAR = 0; SIGMA = 0.1 
LREAL = A              
LCHIMAG = .TRUE.       
DQ = 0.001             
ICHIBARE = 1           
LNMR_SYM_RED = .TRUE.  
NLSPLINE = .TRUE.
```

Script to loop through EDIFF from 1E-4 eV to 1E-8 eV:

```
for a in 4 5 6 7 8
do
cp INCAR.nmr INCAR
sed -i "s/1E-4/1E-$a/g" INCAR

mpirun -np 4 $PATH_TO_EXECUTABLE/vasp_std

cp OUTCAR OUTCAR.$a
done
```

## **k**-points tests

For converging **k** points, start with the Γ-point and increase the **k**-point mesh incrementally:

Initial Γ-only mesh:
**KPOINTS.nmr**

```
C
0
G
 1 1 1
 0 0 0
```

Script to go through **k**-point meshes from Γ-only to 8x8x8:

```
for a in 1 2 4 6 8
do
cp KPOINTS.nmr KPOINTS
sed -i "s/1 1 1/$a $a $a/g" KPOINTS

mpirun -np 4 $PATH_TO_EXECUTABLE/vasp_std

cp OUTCAR OUTCAR.$a
done
```

## Energy cutoff tests

For converging the energy cutoff, start with the value of ENMAX given in the POTCAR file and then increase incrementally in steps of 100 eV:

Initial INCAR:
**INCAR.nmr**

```
PREC = Accurate        
ENCUT = 400.0          
EDIFF = 1E-8           
ISMEAR = 0; SIGMA = 0.1 
LREAL = A              
LCHIMAG = .TRUE.       
DQ = 0.001             
ICHIBARE = 1           
LNMR_SYM_RED = .TRUE.  
NLSPLINE = .TRUE.
```

Script to loop through ENCUT from 400 eV to 800 eV:

```
for a in 400 500 600 700 800
do
cp INCAR.nmr INCAR
sed -i "s/400/$a/g" INCAR

mpirun -np 4 $PATH_TO_EXECUTABLE/vasp_std

cp OUTCAR OUTCAR.$a
done
```

## References
