# Preparing a POTCAR

Categories: Pseudopotentials, Howto

The POTCAR file is a mandatory input file that holds the pseudopotential for each element in the structure. The templates for each element can be downloaded from the VASP Portal.
There are sometimes multiple templates for one element with subtle differences.

## Step-by-step instructions

**Step 1:** Select the latest version of POTCAR files unless you need to use an older one to reproduce a result.

**Step 2:** Choose

* standard potentials for calculations depending mainly on occupied states, e.g., within density-functional theory, using hybrid functionals, or
* GW variants if the calculation requires high accuracy for unoccupied states, i.e., for optical response and many-body perturbation theory.

**Step 3:** Select a POTCAR for a certain family of exchange-correlation (XC) functionals.

:   > **Tip:** The standard choice is to use the PBE version based on LEXCH=PE which has a high transferability to other XC functionals.

:   All potentials are constructed based on solving the scalar relativistic Schrödinger equation for a reference system with a certain XC functional. In most versions, one set is available for the LDA, and one for the GGA. The transferability to other XC functionals is seamless by specifying the XC tag in the INCAR.

**Step 4 (optional):** Choose a different variant (reference atomic valence configuration, etc.) specified by the suffix.

:   > **Tip:** The standard choice is to use the bold version in the list of PAW potentials.

:   See choosing pseudopotentials.

:   > **Important:** Generally opt for the recommended POTCAR files, but test if the property of interest is sensitive to the choice of the pseudopotential. It may be possible to choose a computationally cheaper version or necessary to select a more demanding one.

**Step 5:** For a single element in the structure, you can copy the POTCAR to the working directory, e.g,

```
 cp /path/to/pot/Al/POTCAR .
```

:   For structures with multiple elements, the selected POTCAR files must be concatenated to create one POTCAR file containing all species present in the structure. Combine the potentials by entering, for instance,

```
 cat /path/to/pot/Al/POTCAR /path/to/pot/C/POTCAR /path/to/pot/H/POTCAR > POTCAR
```

:   The order of the potentials must correspond to the order of the species in the POSCAR file.

:   > **Tip:** If species names are given in the POSCAR, and the order does not match the order in the POTCAR, a warning is printed, but VASP will still run.

## Recommendations and advice

> **Important:** Except for the 1st-row elements, all PAW potentials are designed to work at an energy cutoff (ENMAX tag in the POTCAR) of roughly 250 eV. This is a key aspect of making the calculation computationally cheap. We recommend performing a convergence study of the quantity of interest with respect to the energy cutoff (ENCUT tag in the INCAR).

> **Mind:** Mismatched order of species in the POSCAR and POTCAR files is a common mistake! Add species names to your POSCAR to receive a warning if this happens.

> **Mind:** You can mix and match POTCAR families. Even combining pseudopotentials generated with different XC functionals is possible, however make sure to specify the XC functional in the INCAR, see XC.

## Example for preparing a POTCAR for the Heusler alloy TiCo2Si

In this example, we want to prepare a POTCAR for a PBE calculation of ferromagnetic TiCo2Si. We are interested in the energy difference between the ferromagnetic and the nonmagnetic solutions.

The structure is defined by the following POSCAR:

```
TiCo2Si
 1.0
  0.0000000000000000    2.8580789844367893    2.8580789844367893
  2.8580789844367893    0.0000000000000000    2.8580789844367893
  2.8580789844367893    2.8580789844367893    0.0000000000000000
Co Si Ti
 2  1  1
direct
  0.7500000000000000    0.7500000000000000    0.7500000000000000 Co
  0.2500000000000000    0.2500000000000000    0.2500000000000000 Co
  0.0000000000000000    0.0000000000000000    0.0000000000000000 Si
  0.5000000000000000    0.5000000000000000    0.5000000000000000 Ti
```

We will use the potpaw\_PBE.64 potential set, and since we are interested in small energy differences caused by different magnetic solutions, we should use potentials with additional semicore-states in the valence for the 3d metals. The Co\_pv and Ti\_sv potentials seem appropriate for the transition metals. We do not expect Si to become magnetic and are not interested in unoccupied states, so the Si potential is a good choice compared to the harder, computationally more demanding Si\_GW or even Si\_sv\_GW.

On a UNIX machine, one can use the `cat` command to concatenate files together. One can redirect the output from `stdout` to a file using the `>` operator. The order in the POSCAR dictates the order in the POTCAR:

```
cat ~/potpaw_PBE.64/Co_pv/POTCAR ~/potpaw_PBE.64/Si/POTCAR ~/potpaw_PBE.64/Ti_sv/POTCAR > ~/scratch/TiCo2Si/POTCAR
```

## Related tags and sections

Available potentials, POTCAR, Choosing pseudopotentials, Projector-augmented-wave formalism
