# Supercell core-hole calculations

Categories: Linear response, Dielectric properties, XAS, Howto

The SCH approach is explained in detail on the following theory page. When the core hole is explicitly introduced in one of the atoms, i.e., a core electron is removed, it is necessary to eliminate the effective interaction of the core hole with its image across the periodic boundary. That requires using a large supercell so that this interaction is negligible. After the self-consistent electronic minimization is converged in the presence of the core hole, the dielectric function is calculated using Fermi's golden rule.

Two different approaches can be used to treat the excited electron. The excited electron can be placed into the lowest conduction band in the **excited electron and core-hole (XCH)** approach, alternatively the excited electron can be accounted for by a negative background charge in the **full core-hole (FCH)** method.

## Pre-calculation

To run a successful calculation you have to make the following preliminary steps:

**Step 1.** Make a super cell for structure

To minimize the interaction between core holes from neighboring cells the supercell size has to be converged. The convergence is very material dependent and has to be in principle done every time for a new material. It is best to do a bottom-up approach, beginning with the from the small cell.

> **Mind:** Although by increasing the cell size the k mesh is implicitly also increased it still has to be also converged since the spectrum can depend also very strongly on the k points.

**Step 2.** Select one atom in the file that will carry the core-hole and provide a POTCAR file for that atom
After making the super cell, one atom has to be made to a new species with a single atom in it that will carry the core-hole. The initial line for the number of atoms and atoms for example can look like this

```
Mg O
32 32
```

If we are for example interested in the K-edge spectrum of Mg, we would have to change the POSCAR file as follows

```
Mg Mg O
1 31 32
```

Since we create a new species this way we need the POTCAR information for it. This is very easily done by taking the POTCAR file for the same species and concatenating it to the POTCAR carrying all species: i.e. *cat POTCAR\_Mg POTCAR*.

The procedure for oxygen would be very similar:

```
Mg O O
32 31 1
```

and *cat POTCAR POTCAR\_O*.

> **Mind:** One typical source of error is that the additional POTCAR is not added to the main POTCAR file or that the order of species is not the same in the POSCAR and POTCAR files.

> **Warning:** It is strongly recommended to use the available GW PAW potentials for the POTCAR files, since many standard potentials don't have projectors with quantum numbers 2 or larger and the GW potentials are more exact for excited states than the standard potentials.

## Calculation

The supercell core-hole calculations (SCH) consist in principle of two steps:

* Self-consistent electronic cycle with a core hole.
* Calculation of the dielectric function of the core electron with the band structure from the SCF run.

In VASP these two steps are all done in a single calculation.

**Step 3. (optional)** Checking calculational parameters in advance

To check calculational paramaters such as e.g. number of bands, number of irreducible k-points, number of electrons, etc. VASP can be run in a dry mode which doesn't do any "actual" calculations but only does the setup up steps:

```
vasp_executable --dry-run
```

This is often needed in SCH calculations, so whenever in the following one is instructed to increase or decrease a parameter it is useful to run VASP in dry mode before to get the reference value, `e.g. grep NELECT OUTCAR` to find the number of electrons NELECT to be specified in the INCAR file.

**Step 4.** Calculate the XAS spectrum for varying cell sizes

Run a SCH calculation using for several different super cells, increasing until convergence is achieved.

> **Mind:** By default, the **XCH method** is selected, since VASP automatically increases the number of electrons NELECT by CLZ if ICORELEVEL=2 is selected. XCH places the electron in the lowest conduction band.
>
> To run an **FCH calculation** the setup is completely analogous to an XCH calculation except the number of electrons NELECT needs to be decreased by CLZ (or set to the value as it was used without ICORELEVEL=2). Then VASP automatically puts a negative background charge to compensate for the missing negative charge.

**Step 5.** Compare to experiment

If experimental data is available, try comparing to it. The peak maxima are unlikely to align, so you will need to shift the calculated spectra to compare with experiment.

## INCAR tags

There are several tags that are required to run an SCH calculation.

### Example INCAR

An example input for the 2s K-edge of Mg in MgO would look like the following:

```
 CH_LSPEC=.TRUE
 CH_NEDOS=1000
 CH_SIGMA=0.3
 ICORELEVEL=2
 CLNT=1
 CLN=2
 CLL=0
 CLZ=1.0
 CH_AMPLIFICATION=32.0
 NBANDS=600
 SIMGA=0.1
 ISMEAR=0
```

### Core hole tags

* ICORELEVEL: To enable core-hole calculations in the final-state approximation with self-consistent field cycles (SCF) one has to set ICORELEVEL=2. Core-hole calculations in the initial-state approximation (ICORELEVEL=1) are also available, but they are physically less relevant and should be only used if especially needed.
* CLNT: This tag selects the species holding the core hole. This number corresponds to the species defined in the POSCAR and POTCAR files.
* CLN: Specifies the $n$ quantum number of the excited electron.
* CLL: Specifies the $l$ quantum number of the excited electron.
* CLZ: Specifies how much of a fraction of the chosen electron should be excited. Usually one always sets CLZ=1.0, but in some cases values lesser than 1 can lead to better agreement with experiment. However, this should be handled with caution since the physics behind is very dubious.

### XAS tags

* CH\_LSPEC: To obtain X-ray absorption spectra (XAS) the following flag has to be set CH\_LSPEC=*.TRUE.*.
* CH\_SIGMA: The broadening of the spectrum is by default of Gaussian form and the broadening width in eV is set by CH\_SIGMA. We recommend using a very small broadening CH\_SIGMA$\le$0.001 in the calculations and to broaden the spectrum in post-processing. Also, the spectrum can be recalculated with different parameters without the need to redo the electronic self-consistent field cycle. For that one can use the converged WAVECAR from the previous calculation and set ALGO=*None* together with the new parameters for the spectrum "CH\_\*" in the INCAR file.
* CH\_NEDOS: Sets the number of grid points on the energy axis of the spectrum.
* CH\_AMPLIFICATION: Scaling of the spectrum by the specified value. This tag is not important but can be useful sometimes if one needs to scale the spectrum a priori. Otherwise, it is recommended to scale the spectrum a posteriori.

### Other important tags

* NBANDS: Number of bands in the calculation. This parameter usually needs to be significantly increased compared to standard DFT calculations, since it sets the number of bands available in the calculation into which the core electron can be excited.
* ISMEAR: This sets the type of smearing (broadening) in the electronic calculation. Mind that there is also a second broadening when calculating the spectrum, which is currently always of Gaussian form. Both broadenings affect the form of the spectrum.
* SIGMA: Sets the smearing (broadening) width in eV within the electronic calculation.

## Output

The dielectric function is written to the following files:

* OUTCAR
* vaspout.h5
* vasprun.xml

Usually for an absorption spectrum all six components of the dielectric tensor are summed up. In most cases the obtained spectrum needs further processing via an energy dependent broadening.

### OUTCAR

The frequency dependent dielectric tensor, which is directly proportional to the absorption spectrum, is written to the OUTCAR file. It starts with the following lines:

```
  frequency dependent IMAGINARY DIELECTRIC FUNCTION (independent particle, no local field effects) density-density
    E(ev)      X         Y         Z        XY        YZ        ZX
 --------------------------------------------------------------------------------------------------------------
```

The energies of the excitations are with respect to the energy levels of the core electron of interest.
The start of the output of the dielectric function with respect to excitation energy is set slightly below the first peak to avoid many zeros over a large energy range, since core states have very large binding energies.

### vaspout.h5

The energies of the excitations are with respect to the energy levels of the core electron of interest.

### vasprun.xml

The energies of the excitations are with respect to the highest occupied bands (without the core hole).

## References
