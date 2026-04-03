# Electron-phonon accumulators

Categories: Electron-phonon interactions

Performing electron-phonon calculations using the, for example, to compute  transport coefficients or the  renormalization of the electronic band structure, one of the most expensive task is computing the electron-phonon matrix elements.
Accumulators provide a mechanism to efficiently reuse computed matrix elements in the electron–phonon module.
It allows to perform a single VASP run while evaluating multiple derived quantities—such as transport coefficients under different scattering approximations or at varying chemical potentials—without recalculating the matrix elements (for more information on the theory of chemical potentials see chemical potential).
The accumulator technique circumvents the need to repeat these calculations for every set of parameters.

## How it works

The basic idea behind accumulators is to separate the calculation of matrix elements from their subsequent use. Once computed, these elements are “accumulated” into different bins corresponding to various parameter sets. For example, in transport calculations, different accumulators may be defined for:

* Various scattering approximations set via ELPH\_SCATTERING\_APPROX.
* Multiple chemical potentials set via ELPH\_SELFEN\_MU.

Let us look at the following example. If we set

* `ELPH_SCATTERING_APPROX = SERTA MRTA_TAU`
* `ELPH_SELFEN_MU = -0.1 0.0 0.1`

then it would take a total of 6 calculations to get all combinations of scattering approximations and chemical potentials.
It would be very inefficient to recalculate all the electron-phonon matrix elements for each such combination.
Instead, VASP internally creates an accumulator for each combination of ELPH\_SCATTERING\_APPROX and ELPH\_SELFEN\_MU, accumulating the results for all combinations without the need to recompute matrix elements.
This is a much more efficient approach, often with negligible additional computational cost.

> **Mind:** Different temperatures supplied via ELPH\_SELFEN\_TEMPS will *not* create additional accumulators. The temperatures are handled as an array inside each accumulator.

## Output

The output of each accumulator is provided in the OUTCAR file as well as in the vaspout.h5 file.
In both cases, each accumulator is labeled by a unique ID that simply counts the number of accumulators.
In this section, we explain the format of the output.

### Plain-text output in the OUTCAR file

In the OUTCAR file, each accumulator is first listed with its ID, N, and all the relevant information that defines this accumulator is written in a corresponding block.
Here is an example output that defines two self-energy accumulators:

```
Electron self-energy accumulator N =  1
----------------------------------
 Band range:               [       2:       4]
 Number of bands to sum over:     8
 Scattering approximation: constant relaxation-time approximation (CRTA)
 Static self-energy: F
 Complex imaginary shift (delta): 0.000
 Chemical potentials mu(T):
     Temperature (K)             mu (eV)
          0.00000000          9.79452083
        100.00000000          9.80301003
        200.00000000          9.82655169
 Transport energy range:   [   9.434:  10.474]  wich corresponds to    1.040 eV
 Number of selected k-points at which to compute the self-energy: [     3 /     29]
 Selected bands and k-points at which to compute the self-energy:
         2   3   4
     1   T   T   T
     2   T   T   T
     6   T   T   T

Electron self-energy accumulator N =  2
----------------------------------
 Band range:               [       2:       4]
 Number of bands to sum over:     8
 Scattering approximation: self-energy relaxation-time approximation (SERTA)
 Static self-energy: F
 Complex imaginary shift (delta): 0.000
 Chemical potentials mu(T):
     Temperature (K)             mu (eV)
          0.00000000          9.79452083
        100.00000000          9.80301003
        200.00000000          9.82655169
 Transport energy range:   [   9.434:  10.474]  wich corresponds to    1.040 eV
 Number of selected k-points at which to compute the self-energy: [     3 /     29]
 Selected bands and k-points at which to compute the self-energy:
        2   3   4
    1   T   T   T
    2   T   T   T
    6   T   T   T
```

The difference between the two accumulators is in the scattering approximation (set by ELPH\_SCATTERING\_APPROX): one uses CRTA and one uses SERTA.

> **Mind:** The difference between CRTA and SERTA is only relevant in the context of  transport calculations. The computed self-energies do not depend on the scattering approximation.

This way, you can quickly figure out which accumulator corresponds to which combination of computational parameters.
The computed self-energies for each accumulator are then given below.
Here is an example output for the first accumulator and the first temperature:

```
Electron self-energy accumulator N=  1
 T=       0. K
 ispin  ikpt iband       KS eV  re(Fan) eV  im(Fan) eV       DW eV   Fan+DW eV
     1     1     2    9.822840    0.000000   -0.001688    0.000000    0.000000
     1     1     3    9.822840    0.000000   -0.001688    0.000000    0.000000
     1     1     4    9.822841    0.000000   -0.001688    0.000000    0.000000
     1     2     2    7.396326    0.000000   -0.110687    0.000000    0.000000
     1     2     3    9.166331    0.000000   -0.013618    0.000000    0.000000
     1     2     4    9.166332    0.000000   -0.013618    0.000000    0.000000
     1     6     2    8.086060    0.000000   -0.073793    0.000000    0.000000
     1     6     3    8.086060    0.000000   -0.073793    0.000000    0.000000
     1     6     4    8.496795    0.000000   -0.067575    0.000000    0.000000
```

> **Mind:** In this case, only the imaginary part of the self-energy is calculated (useful for transport calculations).

For transport calculations, there are additional *transport* accumulators.
The corresponding OUTCAR output has a structure that is similar to that of the self-energy.
First, the transport accumulators are listed and defined:

```
Transport calculator N =  1
----------------------------------
 transport driver: 2 ! Gauss-Legendre integration
 Scattering approximation: constant relaxation-time approximation (CRTA)
 Static self-energy: F
 Transport number of points:   501
 temperature:    0.000 K
   Transport energy range:   [   9.795:   9.795]  wich corresponds to    0.000 eV
   Average relaxation time:           NaN s
   Number of electrons:    0.0000E+00
   Number of holes:        1.1297E-06
 temperature:  100.000 K
   Transport energy range:   [   9.699:   9.907]  wich corresponds to    0.208 eV
   Average relaxation time:    1.0000E-14 s
   Number of electrons:    0.0000E+00
   Number of holes:        1.1296E-06
 temperature:  200.000 K
   Transport energy range:   [   9.619:  10.035]  wich corresponds to    0.416 eV
   Average relaxation time:    1.0000E-14 s
   Number of electrons:    0.0000E+00
   Number of holes:        1.1298E-06

Transport calculator N =  2
----------------------------------
 transport driver: 2 ! Gauss-Legendre integration
 Scattering approximation: self-energy relaxation-time approximation (SERTA)
 Static self-energy: F
 Transport number of points:   501
 temperature:    0.000 K
   Transport energy range:   [   9.795:   9.795]  wich corresponds to    0.000 eV
   Average relaxation time:           NaN s
   Number of electrons:    0.0000E+00
   Number of holes:        1.1297E-06
 temperature:  100.000 K
   Transport energy range:   [   9.699:   9.907]  wich corresponds to    0.208 eV
   Average relaxation time:    2.1451E-13 s
   Number of electrons:    0.0000E+00
   Number of holes:        1.1296E-06
 temperature:  200.000 K
   Transport energy range:   [   9.619:  10.035]  wich corresponds to    0.416 eV
   Average relaxation time:    4.3674E-13 s
   Number of electrons:    0.0000E+00
   Number of holes:        1.1298E-06
```

This is then followed by the output of the transport coefficients for each accumulator and each temperature.
The corresponding example output looks like this:

```
Transport for self-energy accumulator N=     1
                 T K               mu eV           sigma S/m      mob cm^2/(V.s)       seebeck μV/K         peltier μV     kappa_e W/(m.K)
          0.00000000          9.79452083         87.62375412         54.69155048          0.00000000          0.00000000          0.00000000 Gauss-Legendre grids
        100.00000000          9.80301003         87.61741132         54.69107335        228.06848886      22806.84888640          0.00023958 Gauss-Legendre grids
        200.00000000          9.82655169         87.62716236         54.69106480        377.34594846      75469.18969136          0.00050233 Gauss-Legendre grids

Transport for self-energy accumulator N=     2
                 T K               mu eV           sigma S/m      mob cm^2/(V.s)       seebeck μV/K         peltier μV     kappa_e W/(m.K)
          0.00000000          9.79452083        153.09934046         95.55902268          0.00000000          0.00000000          0.00000000 Gauss-Legendre grids
        100.00000000          9.80301003        149.76360902         93.48293224        228.06843439      22806.84343939          0.00040952 Gauss-Legendre grids
        200.00000000          9.82655169        134.56767701         83.98822174        377.34590243      75469.18048584          0.00077142 Gauss-Legendre grids
```

This allows us to identify the first data set (N = 1) as the CRTA calculation and the second data set (N = 2) as the SERTA calculation.

### Binary output in the vaspout.h5 HDF5 file

The information in each accumulator is also written to the standard vaspout.h5 binary output file.
In this case, the accumulators are organized as HDF5 groups, with the unique accumulator ID being part of the group name.
This is an example output showing the electron-phonon section of the HDF5 file:

```
$ h5ls vaspout.h5/results/electron_phonon/electrons
chemical_potential       Group
dos                      Group
eigenvalues              Group
self_energy_1            Group
self_energy_2            Group
self_energy_3            Group
self_energy_4            Group
self_energy_5            Group
self_energy_6            Group
self_energy_meta         Group
transport_1              Group
transport_2              Group
transport_3              Group
transport_4              Group
transport_5              Group
transport_6              Group
transport_meta           Group
velocity                 Dataset {3, 1, 29, 8}
```

The self\_energy\_N and transport\_N HDF5 groups correspond to the self-energy and transport accumulators with the ID N, respectively.
Meta information regarding the accumulators is contained in the self\_energy\_meta and transport\_meta subgroups.
Each subgroup currently holds three datasets that describe the labeling of the accumulators:

id\_name
:   lists the kind of parameters that accumulators can be created for. Each name refers to one or more INCAR tags.

    selfen\_delta
    :   accumulators created via ELPH\_SELFEN\_DELTA

    nbands\_sum
    :   accumulators created via ELPH\_NBANDS\_SUM

    selfen\_muij
    :   accumulators created via ELPH\_SELFEN\_MU, ELPH\_SELFEN\_CARRIER\_DEN or ELPH\_SELFEN\_CARRIER\_PER\_CELL

    selfen\_approx
    :   accumulators created via ELPH\_SCATTERING\_APPROX

id\_size
:   lists the number of accumulators created for each kind of parameters (in the same order)

ncalculators
:   total number of accumulators (product of all id\_size entries)

So, for example, if the meta-data output looks like this:

```
id_name: "selfen_delta   ", "nbands_sum     ", "selfen_muij    ", "selfen_approx  "
id_size: 1, 1, 3, 2
ncalculators: 6
```

that means there is only one $\mathrm{i} \delta$ value from ELPH\_SELFEN\_DELTA, one band count from ELPH\_NBANDS\_SUM, three different chemical potentials from ELPH\_SELFEN\_MU (or related tags) and two different scattering approximations from ELPH\_SCATTERING\_APPROX, for a total of six accumulators (all combinations).

In addition to the meta-data contained within the \_meta groups, each electron-phonon accumulator describes itself.
For example, here is the data contained with the first self-energy accumulator group:

```
h5ls vaspout.h5/results/electron_phonon/electrons/self_energy_1
band_start               Dataset {SCALAR}
band_stop                Dataset {SCALAR}
bks_idx                  Dataset {1, 29, 3}
carrier_per_cell         Dataset {6}
delta                    Dataset {SCALAR}
efermi                   Dataset {6}
energies                 Dataset {9, 1}
enwin                    Dataset {SCALAR}
id_idx                   Dataset {4}
id_name                  Dataset {4}
nbands                   Dataset {SCALAR}
nbands_sum               Dataset {SCALAR}
nw                       Dataset {SCALAR}
scattering_approximation Dataset {SCALAR}
select_energy_window     Dataset {2}
selfen_dw                Dataset {9, 6}
selfen_fan               Dataset {9, 1, 6, 2}
static                   Dataset {SCALAR}
temps                    Dataset {6}
tetrahedron              Dataset {SCALAR}
```

The id\_name is the same as in the meta-data, and the id\_idx indexes the id\_size.

## Related tags and articles

* Band-structure renormalization
* Transport calculations
* Electronic transport coefficients
* Chemical potential in electron-phonon interactions
* ELPH\_SCATTERING\_APPROX
* ELPH\_SELFEN\_MU
* ELPH\_SELFEN\_MU\_RANGE
* ELPH\_SELFEN\_CARRIER\_DEN
* ELPH\_SELFEN\_CARRIER\_DEN\_RANGE
* ELPH\_SELFEN\_CARRIER\_PER\_CELL
* ELPH\_MODE
* ELPH\_RUN
