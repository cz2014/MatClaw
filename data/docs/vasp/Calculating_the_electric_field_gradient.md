# Calculating the electric field gradient

Categories: Howto, NMR

Nuclei with a spin > ± ½ are called quadrupolar nuclei. They have a non-spherical shape and therefore a non-zero electric field gradient (EFG) at the nucleus. The EFG is calculated using LEFG . By including the quadrupole moment of the isotopes, the quadrupole coupling constants *Cq* can be calculated (multiple definitions exist in the literature, ensure that you are correctly comparing). These are measured using nuclear quadrupole resonance (NQR) spectroscopy, a type of zero- to ultralow-field (ZULF) NMR, NMR, and Mössbauer spectroscopy. The theory is covered in the NMR category page and LEFG page.

## Step-by-step instructions

The electric field gradient is calculated post-self-consistent field (post-SCF) using LEFG. A well-converged SCF calculation is therefore crucial. The electric field gradient is very sensitive to several input parameters that must all be independently tested. In particular, small differences in the structure can make big differences to $V\_{zz}$, up to 50 % ; see the Advice section for more details. Make sure to have a well-optimized structure before you begin the convergence tests.

**Step 1 (optional):** Calculate the chemical shielding using a previously converged calculation

Since the chemical shielding is calculated post-SCF, you can use a previously converged WAVECAR with ISTART = 1 and NELM = 1. The corresponding density, CHGCAR is calculated from the WAVECAR file before the first elementary step so it need not be included.

**Step 2a:** Define the nuclear quadrupolar moments

The calculated electric field gradients are not observable in experiment. Instead, the quadrupolar coupling constant can be calculated so long as the nuclear quadrupolar moments are defined in QUAD\_EFG. Each species in your POSCAR file should be defined; there is no need to define each individual ion. A short table of values can be found in Ref. .

**Step 2b (optional):** Determine a suitable energetic break value

The break condition for the self-consistency step EDIFF strongly influences the chemical shielding. A setting of EDIFF = 1E-8 eV is generally recommended. Convergence is taken to be within 0.1 ppm.

**Step 3:** Converge the plane-wave energy cutoff

A large plane-wave energy cutoff is required to fully converge the electric field gradient. Perform multiple calculations while increasing the basis set size, as defined in ENCUT, incrementally (e.g., by 100 eV intervals). Convergence should be aimed to be within 3 significant figures, although this will not be feasible for heavier elements.

**Step 4:** Converge the **k** point mesh

Similar to the basis, the **k** point mesh can strongly influence the coupling constant. The **k** point mesh should be increased incrementally, i.e., 1x1x1, 2x2x2, 3x3x3, until convergence within 3 significant figures is achieved. It is only necessary to converge the **k** point mesh for crystals, gas-phase molecules should use the Γ-point only.

**Step 5:** Compare to experiment

The purpose of these calculations is to compare directly to experiment. The EFG that has been calculated is not directly measurable but the quadrupolar coupling constants *Cq* are.

## Recommendations and advice

Calculating the electric field gradient requires tightly converged settings. As described in the step-wise introduction above, converging with respect to EDIFF, ENCUT, and the **k** point mesh is very important. There are a few additional settings that should be considered.

> **Mind:** Be aware of some specifics relevant to the implementation used:
>
> * Several definitions of $C\_q$ are used in the NMR community, ensure that you are comparing between the same definitions in calculation and experiment.
> * For heavy nuclei inaccuracies are to be expected due to an incomplete treatment of relativistic effects.

### Structure

The electric field gradient can be **extremely** dependent on structure, to the extent that using the experimental structure can improve results. A small difference in the positions of atoms can make a huge difference to the EFG. For the O in TiO2 rutile, a shift in position from 0.305 in internal coordinates to 0.3025 made a difference of 50 % to $V\_{zz}$ for the Ti . This is an atypical case but highlights the importance of using a well-optimized structure, ideally the experimental structure if available. This extreme sensitivity to the structure is indicative of why the quadrupolar coupling constant is so useful for determining information about a system's chemical environment.

### PAW pseudopotentials

The standard PAW pseudopotentials POTCAR used are sufficient for calculating the electric field gradient. Using GW pseudopotentials can significantly improve results. Semi-core electrons can be important, so POTCAR files with *\*\_pv* or *\*\_sv* can improve the results, as will the explicit inclusion of augmentation channels with $d$-projectors.

### Additional tags

To ensure tight precision, the precision should be set to `PREC = Accurate`, rather than `Normal`.
The LASPH should be set to `.TRUE.`, turning on the non-spherical contributions to the gradient of the density inside the PAW spheres.

# Example scripts for convergence tests

Several tests are necessary to obtain various NMR parameters. Make sure to change the example INCAR files to include the tags for your desired calculation. We provide some example scripts below:

> **Important:** Make sure to replace the QUAD\_EFG in the INCAR with the values for the isotopes in your system.

## Energetic break criterion tests

For converging the energetic break criterion for a single ionic step (EDIFF), start with the 1E-4 and then increase by orders of magnitude:

Energetic break criterion:
**INCAR.nmr**

```
ENCUT = 400              
ISMEAR = 0; SIGMA = 0.01 
EDIFF = 1E-4             
PREC = Accurate          
LASPH = .TRUE.           
LEFG = .TRUE.            
QUAD_EFG = 0. -696. 20.44 0. 2.860  # Nuclear quadrupolar moments for Pb I N O D
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

For converging the energy cutoff, start from at least the value of ENMAX given in the POTCAR file and then increase incrementally in steps of 100 eV:

Initial INCAR:
**INCAR.nmr**

```
ENCUT = 400              
ISMEAR = 0; SIGMA = 0.01 
EDIFF = 1E-8             
PREC = Accurate          
LASPH = .TRUE.           
LEFG = .TRUE.            
QUAD_EFG = 0. -696. 20.44 0. 2.860  # Nuclear quadrupolar moments for Pb I N O D
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

## Related tags and articles

LEFG,
QUAD\_EFG

## References
