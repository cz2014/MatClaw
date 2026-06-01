# Partial charge densities and STM simulations

Categories: Charge density, Howto, Electronic ground-state properties

The partial (band-decomposed) charge density can be used to analyze the contributions of different orbitals or energy ranges to a specific region in real space. It helps in gaining insight and visualizing electronic, magnetic, or transport properties, and is especially important when simulating scanning-tunneling-microscopy (STM) images.
In VASP, the calculation of partial charges is a quick postprocessing step that is selected by setting LPARD = .TRUE. in the INCAR file. It is necessary to provide a WAVECAR from a converged ground state calculation as an input file. To select the contributing **k** points and bands, various options exist, which can be selected via the NBMOD, IBAND, EINT, and KPUSE tags.

> **Mind:** All charge densities, including the band-decomposed charge densities, are symmetrized using both the space and point group symmetries. However, when calculating partial charge from selected **k** points, this can lead to wrong results due to wrong **k** point weights. In that case, the symmetry must be turned off during the initial ground state calculation from which the WAVECAR is generated, as well as during the subsequent band-decomposed charge density calculation.

> **Warning:** Band-decomposed partial charge density postprocessing is not supported for noncollinear magnetic calculations (LNONCOLLINEAR = .TRUE.).

## Input tags for selecting and writing the partial charges

The following list briefly explains the various INCAR tags that control the behavior of the band-decomposed charge density decomposition. Please refer to the documentation of each tag for further details.

* LPARD: Toggles the partial charge postprocessing on or off. If only this tag is set, the valence charge density is computed for all occupied bands and written to the CHGCAR file (without the augmentation occupancies usually written to that file).
* LPARDH5 Switches the output to the vaspout.h5 file. This tag is only available as of VASP.6.5.0.
* IBAND: An integer array specifying the bands to include in the partial charge density. If IBAND is specified, NBMOD is automatically set to the number of selected bands.
* EINT: Specifies an energy interval. Any energy bands with eigenvalues within this range will contribute to the calculation of the partial charge density. If the value of the NBMOD tag is set to -3, the energy values are interpreted as relative to the Fermi energy $\epsilon\_f$. If the NBMOD tag is not set or is set to -2, the provided energy values will be considered as absolute total energies.
* NBMOD: This tag controls the mode of selecting bands that should contribute to the calculation of partial charges.
  + NBMOD = n: Use n bands (set automatically if IBAND is used).
  + NBMOD = 0: Use all bands (occupied and empty).
  + NBMOD = -1: Use all occupied bands (and write to CHGCAR instead of PARCHG if PARCHGH5 = .FALSE.)
  + NBMOD = -2: To choose the bands that contribute, you can utilize an energy interval defined by the tag EINT.
  + NBMOD = -3: Use an energy interval relative to the Fermi energy $\epsilon\_f$ to select contributing bands (defined by EINT).
* KPUSE: Specifies which **k** points are used in the evaluation of the partial charge density.
* LSEPB: Specifies whether to write the partial charge density for selected bands individually or merge them.
* LSEPK: Specifies whether to write the partial charge density for selected **k** points individually or merge them.

## Output files

The partial valence charge density is written in the PARCHG file. If you want to separate the output by **k** points or bands, setting LSEPB and/or LSEPK allows you to write it to multiple PARCHG.\*.\* files.
If the code is compiled with HDF5 support, `LPARDH5 = .TRUE.` redirects all output to the vaspout.h5 file. In that case py4vasp can be used to analyze the output and plot simulated STM pictures.

> **Mind:** For spin-polarized calculations, the PARCHG and its variants hold the total density and the magnetization density. For instance, if the 4th band is selected (IBAND = 4) the first data set in the PARCHG file corresponds to the summed density of the 4th spin up and 4th spin down orbital, whereas the second data set holds the difference between the 4th spin-up and 4th spin-down orbital (magnetization density). Hence, to obtain the charge density corresponding to a specific orbital of a specific spin channel some post-processing of the PARCHG file might be required (building differences or sums). A simple workaround is to use EINT and specify sufficient digits to select only one orbital from either the spin-up or spin-down channel.

## Step-by-step instructions for simulating an STM picture

In this example, we will produce a partial charge density useful for STM picture simulation. Note that the bias voltage and tip distance from an experiment do not always translate one-to-one to the simulation.

**Step 1**: Ensure that the ground-state calculation has a well-converged charge density (low rms(c) in the standard output or the OSZICAR).
The **k** point mesh should be well converged to get good results for STM simulations.

**Step 2**: Copy POSCAR, KPOINTS, and WAVECAR to a new directory.

**Step 3**: Prepare an appropriate INCAR file in the new directory, making sure you specify the same settings for ENCUT, ISYM, and ISPIN as in the ground-state calculation. This could be a possible INCAR:

```
SYSTEM = STM simulation
ENCUT = 520
ISPIN = 2
LPARD = .TRUE.
LPARDH5 = .TRUE.
NBMOD = -3
EINT = -0.2 0.05
LSEPB = .FALSE.
LSEPK = .FALSE.
```

LPARD = .TRUE. activates the partial charge mode and assures that the WAVECAR file is read.
LPARDH5 = .TRUE. redirect the output to the vaspout.h5 file allowing the use of py4vasp for plotting the simulated STM picture.
ENCUT and ISPIN settings are copied over from the ground-state calculation. NBMOD = -3 and EINT = -0.2 0.05 ensure that the bands from $\epsilon\_f-0.2$ to $\epsilon\_f+0.05$ eV are included (corresponding to a negative bias voltage of about 0.2 Volt). The two remaining tags, LSEPB and LSEPK are set to their default values (.FALSE.) and are there for clarity only. We want to sum up the contributions of all bands in the energy range at all **k** points without separating any of this information.

**Step 4**: Run VASP. No electronic (or ionic) minimization is performed, so the calculation is rapid and does not require parallelization.

**Step 5**: (optional, requires py4vasp): execute the following Python script in a Python environment where py4vasp is installed:

```
from py4vasp import Calculation
calc = Calculation.from_file('/path/to/your/vaspout.h5')
calc.partial_density.to_stm(selection='constant_height(total)', tip_height=4, supercell=[7,7])
```

This will plot the simulation of an STM image in constant height mode, with the tip 4Å above the surface. A 7 by 7 supercell is plotted. Under the hood, the data is pre-processed with Gaussian smoothening for the STM plot. More convenient methods are provided in py4vasp to work with the partial charge data.

**Alternative Step 5** (optional, if VASP is compiled without HDF5 support): Load the resulting PARCHG file with your favorite visualization program to view constant-height images by looking at slices through the data or constant current images by using isosurfaces.

## Example

The images below show an experimental (on the left) and a simulated (on the right) scanning tunneling image of Graphene. The experimental image was measured at room temperature in air at the Department for Earth and Environmental Sciences, LMU, and Center for NanoScience (CeNS), Munich. The simulated image was created with py4vasp at very similar settings as described in the section above.

There are tutorials to calcualte the constant height STM and constant current STM in part 3 of the surface tutorials on our website.

## Related tags and articles

LPARD,
IBAND,
EINT,
NBMOD,
KPUSE,
LSEPB,
LSEPK,
PARCHG,
CHGCAR,
WAVECAR
