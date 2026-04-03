# DFT+DMFT calculations

Categories: Howto, Electronic occupancy, Many-body perturbation theory

Density-functional theory plus dynamical mean-field theory (DFT+DMFT) is an advanced extension of DFT that provides a more accurate treatment of strongly correlated materials including dynamical effects at finite temperature compared to DFT+U.
DFT+DMFT calculations are not within VASP, but VASP allows to interface external DMFT codes.
Here, we will guide through the steps to perform a DFT+DMFT calculation using the TRIQS software library, more specifically the TRIQS/solid\_dmft software.
In this following HowTo, we will calculate the local spectral function $A(\omega)$ of NiO using DMFT.

> **Mind:** Available as of VASP 6.5.0

## Theory overview

Similarly to the GW method, DFT+DMFT relies on the Green's functions formalism.
But, in contrast to GW, DMFT is working on a projected sub-space of the KS states, much like DFT+U.
The projection is performed in VASP in the same way it is done for the LDAU tag by projecting the KS states on localized orbitals provided by the PAW formalism:

:   :   $$P^{\mathbf{R}}\_{L,\nu}(\mathbf{k}) = \sum\_i \langle \chi^{\mathbf{R}}\_L | \phi\_i \rangle \langle \tilde{p}\_i | \tilde{\Psi}\_{\nu \mathbf{k}} \rangle,$$

where $|\chi^{\mathbf{R}}\_L\rangle$ are localized basis functions associated with each correlated site R, $|\phi\_i \rangle$ are all-electron partial waves, and $| \tilde{p}\_i\rangle$ are the standard PAW projectors. $L$ is a compound index of local quantum numbers. The raw projectors are orthonormalized and connect the KS basis $\nu$ with the localized orbitals $m$: $P^{\mathbf{R}}\_{m,\nu}(\mathbf{k})$.

In DFT+DMFT theory the central quantity is the lattice Green's function:

:   :   $$G\_{\nu \nu{\prime}}(\mathbf{k}, i\omega\_n) = \left[ \left( i\omega\_n + \mu - \varepsilon\_{\nu \mathbf{k}} \right) \hat{\mathbb{I}} - \hat{\Sigma}^{\text{KS}}(\mathbf{k}, i\omega\_n) \right]^{-1}\_{\nu \nu{\prime}}.$$

where $\varepsilon\_{\nu \mathbf{k}}$ are the KS eigenvalues, $\mu$ is the chemical potential, and $\hat{\Sigma}^{\text{KS}}(\mathbf{k}, i\omega\_n)$ is the DMFT calculated self-energy embedded in the KS space at a given $k$ point and discrete Matsubara frequency $i\omega\_n$. The self-energy contains the electron correlation effects calculated by DMFT. The DMFT equations are solved in the localized basis and then embedded via the projector functions:

:   :   $$\hat{\Sigma}^{\text{KS}}(\mathbf{k}, i\omega\_n) =
        \sum\_{\nu\nu{\prime}} |\Psi\_{\nu \mathbf{k}}\rangle \langle \Psi\_{\nu{\prime} \mathbf{k}}|
        \cdot \sum\_{mm{\prime}} P^\*\_{\nu, m}(\mathbf{k}) \Sigma^\text{imp}\_{mm{\prime}}(i\omega\_n) P\_{m{\prime}, \nu{\prime}}(\mathbf{k}) .$$

The self-energy in DMFT is obtained by first extracting the local Green's function (with an initial guess of $\Sigma^\text{imp}$) in the localized basis:

:   :   $$G^{\text{loc}}\_{m m'}(i\omega\_n) = \sum\_{\mathbf{k}} \sum\_{\nu \nu'} P\_{m \nu}(\mathbf{k}) G\_{\nu \nu'}(\mathbf{k}, i\omega\_n) P^\*\_{m' \nu'}(\mathbf{k})$$

from which we extract a dynamic Weiss field $\mathcal{G}$:

:   :   $$\mathcal{G}\_{m m '} = \left( \left[ \mathbf{G}^\text{loc} \right]^{-1} + \mathbf{\Sigma}^\text{imp} \right)^{-1}\_{m m'}$$

that is used in DMFT to construct an Anderson impurity model, by supplying a local many-body Hamiltonian incorporating the local energy levels plus the interaction Hamiltonian.
By solving the Anderson impurity problem we obtain the impurity Green's function $G^\text{imp}\_{m m'}$ and the impurity self-energy $\Sigma^\text{imp}\_{m m'}$ via Dysons equations:

:   :   $$\Sigma^\text{imp}\_{m m'} = \left[ \mathbf{\mathcal{G}} \right]^{-1}\_{m m'} - \left[ \mathbf{G}^\text{imp} \right]^{-1}\_{m m'}$$

This procedure is iterated until the DMFT self-consistency condition is satisfied:

:   :   $|G^{imp}-G^{loc}| \rightarrow 0$.

Importantly, there is a second self-consistency condition for combined DFT+DMFT calculations. From the lattice Green's function a density matrix can be computed:

:   :   $$N\_{\nu \nu'} (\mathbf{k}) = \frac{1}{\beta} \sum\_{i \omega\_n} G\_{\nu \nu'}(\mathbf{k}, i\omega\_n)$$

that is related to the DFT density by:

:   :   $$\rho(\mathbf{r}) = \sum\_{\mathbf{k}} \sum\_{\nu \nu'} \langle \mathbf{r} | \Psi\_{\nu \mathbf{k}} \rangle N\_{\nu \nu'}(\mathbf{k}) \langle \Psi\_{\nu' \mathbf{k}} | \mathbf{r} \rangle$$

This implies that both the DFT charge density and the obtained DMFT density matrix have to coincide as well. This so-called charge-self-consistency condition implies that we do have to perform a charge density update after each DMFT step (using ICHARG=5). These calculation are called charge self-consistent (CSC) DFT+DMFT calculations. Without the extra CSC steps one refers to the DMFT calculations as one shot (OS).

From the final self-energy or Green's function the spectral function (similar to the DOS in DFT) can be computed, which can be compared to photoemission spectroscopy. DFT+DMFT also allows to calculate other spectral properties and structural properties. See Ref. for more information.

## Technical requirements

To follow the tutorial VASP has to be compiled with HDF5 support and should be newer than version 6.5.0.
Additionally TRIQS has to be installed including its applications ctseg, maxent, dft\_tools, and solid\_dmft in version 3.4.0 or newer. See the following installation instructions. TRIQS can easiest be obtained via conda.

> **Mind:** Currently this tutorial requires the installation of the unstable branch of TRIQS/dft\_tools and TRIQS/solid\_dmft manually from source. The features will be part of the upcoming release 3.4.0 of TRIQS.

## Step-by-step tutorial

NiO is a charge-transfer insulator that becomes anti-ferromagnetic at low temperatures. At higher temperatures NiO is para-magnetic and a prototypical Mott insulator. In the tutorial NiO LSDA+U DFT+U is used to calculate the low temperature magnetic state of NiO. Here, we will calculate the Mott insulating state at higher temperatures using DFT+DMFT.

### Step 1: Perform a SCF DFT calculation

First we will perform a SCF DFT calculation to converge the KS wavefunction and project the KS states on localized Ni-d orbitals. We will later use the Ni-d projectors for DMFT.
The POSCAR file is:

```
 NiO
 4.17
  0.0000000000  0.5000000000  0.5000000000
  0.5000000000  0.0000000000  0.5000000000
  0.5000000000  0.5000000000  0.0000000000
 Ni O
  1 1
 Direct
  0.0000000000  0.0000000000  0.0000000000
  0.5000000000  0.5000000000  0.5000000000
```

The KPOINTS file is:

```
 Automatically generated mesh
 0
 G
 15 15 15
```

For the POTCAR we are using the 'Ni\_pv' and the 'O' pseudopotentials.
The INCAR file is:

```
 SYSTEM  = NiO
 
 ISMEAR = -5
 SIGMA = 0.01
 EDIFF = 1.E-10
 NELMIN = 35
 
 NBANDS = 32
 LORBIT = 14
 LMAXMIX = 4
 EMIN = -6
 EMAX = 18
 NEDOS = 5001
 
 # project to Ni d and O p states
 LORBIT = 14
 LOCPROJ = 1 : d : Pr
```

Importantly, we specify the projectors to be created via the LOCPROJ tag for the Ni-d orbitals.
Additionally, we specify the LORBIT tag to be 14 to optimize the projectors in the given energy range EMIN to EMAX.
The number of bands is slightly increased and the convergence criteria a stringent to converge the KS wavefunction (RMS).
The end of the std out should look like this:

```
 DAV:  34    -0.113700647767E+02   -0.45929E-10    0.41728E-14  3960   0.357E-11    0.670E-04
 DAV:  35    -0.113700647767E+02    0.36380E-11    0.12336E-13  3960   0.224E-11
  LOCPROJ mode
  Computing AMN (projections onto localized orbitals)
    1 F= -.11370065E+02 E0= -.11370065E+02  d E =0.000000E+00
  writing wavefunctions
```

Note here the *LOCPROJ mode* message. Afterwards the projections are stored in the file vaspgamma.h5 and LOCPROJ.

### Step 2: Convert the VASP output to TRIQS input

We will use the converter tool inside of TRIQS/dft\_tools to convert the VASP output to a TRIQS input file. To this end, we prepare a config file *plo.cfg* with the following content:

```
[General]
DOSMESH = -10 10 3001

[Group 1]
SHELLS = 1
EWINDOW = -10 10
BANDS = 5 14

[Shell 1] # Ni d shell
LSHELL = 2
IONS = 1
CORR = True
TRANSFORM = 1.0  0.0  0.0  0.0  0.0
            0.0  1.0  0.0  0.0  0.0
            0.0  0.0  1.0  0.0  0.0
            0.0  0.0  0.0  1.0  0.0
            0.0  0.0  0.0  0.0  1.0
```

For details on the config file see the DFT tools documentation. The converter can be run by creating a small python script with the following content:

```
from triqs_dft_tools.converters.vasp import VaspConverter
import triqs_dft_tools.converters.plovasp.converter as plo_converter

# Generate and store PLOs
plo_converter.generate_and_output_as_text('plo.cfg', vasp_dir='./')

# run the converter
Converter = VaspConverter(filename = 'vasp')
Converter.convert_dft_input()
```

Running the python script via *python converter.py* will create the input file *vasp.h5* that can be used for the DMFT calculation.
The std output contains information about the localized orbitals.
For example the on-site density matrix is printed:

```
 Density matrix:
   Shell 1
 Site diag : True
     Site 1
      1.9541777     0.0000065     0.0000335     0.0000138    -0.0000181
      0.0000065     1.9541833    -0.0000361     0.0000068     0.0000650
      0.0000335    -0.0000361     1.2867504     0.0000023    -0.0000827
      0.0000138     0.0000068     0.0000023     1.9541790    -0.0000303
     -0.0000181     0.0000650    -0.0000827    -0.0000303     1.2868509
       trace:  8.43614117771427
  
   Impurity density: 8.43614117771427
```

We can plot the DFT DOS from VASP together with the DOS of the projected orbitals from VASP via the following python code using py4vasp:

```
import py4vasp
import matplotlib.pyplot as plt
import numpy as np

# get VASP DOS
calc = py4vasp.Calculation.from_file('scf/vaspout.h5')
dft_dos = calc.dos.to_dict()

# load projector (PLO) DOS from TRIQS
plo_dos_Ni = np.loadtxt('scf/pdos_0_0.dat')

fig = plt.figure(figsize=(7,4), dpi=150)

plt.plot(dft_dos['energies'], dft_dos['total'], label=r'VASP total DOS')

# sum PLO DOS for all orbitals
plt.plot(plo_dos_Ni[:,0],np.sum(plo_dos_Ni[:,1:],axis=1), label=r'PLO Ni$_{d}$')

plt.xlim(-10,4)
plt.ylim(0,12)
plt.xlabel(r'$\epsilon - {\text{E}_\text{F}}$ (eV)')
plt.ylabel(r'states/eV')
plt.legend()
plt.show()
```

Resulting in:

DFT total DOS and projector DOS from TRIQS/DFT\_Tools

capturing the Ni-d orbital character. The DMFT calculation will now use this projected DOS as input.

### Step 3: Perform a DMFT calculation

Copy the *vasp.h5* file to a new directory.
Then, we perform first a one-shot DMFT calculation to converge the self-energy, before performing charge-density updates with VASP.
To perform the DMFT calculation, we will use the TRIQS/solid\_dmft.
In general, TRIQS is only a framework which allows the user large flexibility to design their own workflows for DMFT calculations or other methods.
However, we will leverage on solid\_dmft flagship implementation of DMFT in TRIQS, which works by providing a toml config file and executing solid\_dmft.
The following config file prepares the DMFT calculation to solve the DMFT equation with U=8 eV and J=1.0 eV, which are typical values for NiO (compare with the NiO LSDA+U howto).
Create the 'dmft\_config.toml' file with the following content:

```
[general]
seedname = "vasp"
jobname = "U8.0-J1.0-beta20-qmc1e+7"

prec_mu = 0.001
n_iw = 501
n_tau = 10001

enforce_off_diag = false
block_threshold= 0.001

h_int_type = "density_density"
h_int_basis = "vasp"
U = 8.0
J = 1.0

beta = 20

n_iter_dmft = 12
 
dc_type = 0
dc = true
dc_dmft = false

h5_save_freq = 1

[solver]
type = "ctseg"
length_cycle = 500
n_warmup_cycles = 1e+4
n_cycles_tot = 1e+7
perform_tail_fit = true
fit_max_moment = 4
fit_min_w = 20
fit_max_w = 30

[advanced]
dc_fixed_value = 59.0
```

Importantly, we specify the electronic temperature of the calculation via the option 'beta=20' 1/eV to be half of room temperature, U/J are set to the aforementioned values, the *seedname* and *jobname* specify the input file and the output directory in which the calculation will be performed, and *n\_iter\_dmft* specifies the number of DMFT iterations to be performed.
The section *[solver]* specifies the solver to be used, in this case we use the CTSEG solver, and its parameters.
The ctseg solver is a QMC impurity solver operating on the Matsubara axis.
Please refer to the solid\_dmft documentation for more details on the parameters.
The QMC solver parallelizes very well over MPI and we request 1e+7 Monte Carlo steps.

To perform the DMFT calculation we run the following command:

```
 mpirun solid_dmft 1>out 2>err &
```

which will run the DMFT calculation in the background. Check the file *out* for the output of the calculation.
Importantly, solid\_dmft will create a directory *jobname* in which the file *observables\_imp0.dat* can be found that monitors the most important observables per iteration.
On 32 cores the calculation should take around 10 minutes, and the observables file should look like this:

```
  it |         mu |        G(beta/2) per orbital |          orbital occs up+down |  impurity occ
   0 |   -0.00247 |   -0.00897          -0.11937 |    1.97871            1.29990 |       8.53594
   1 |   -0.00247 |   -0.00084          -0.01573 |    1.99582            1.11247 |       8.21241
   .
   .                             ...                             ...
   .
   8 |    0.05280 |   -0.00005          -0.00007 |    1.85604            1.30080 |       8.16972
   9 |    0.04979 |   -0.00004          -0.00007 |    1.84552            1.31608 |       8.16871
  10 |    0.04979 |   -0.00005          -0.00015 |    1.86526            1.28894 |       8.17367
```

The second column shows the chemical potential that is varies in each DMFT iteration to fulfill the electron count of the system.
The next columns monitor $G(\beta/2)$ per localized orbital, which monitors the spectral function at the Fermi level, to indicate metallic or insulating behavior.
The last columns show the orbital occupations and the impurity occupation.
The convergence can be monitored via the file *conv\_obs0.dat*, which should look like this:

```
 it |          δμ |        δocc orb |    δimp occ |       δGimp |         δG0 |          δΣ
  1 | 0.00000e+00 |     1.87428e-01 | 3.23528e-01 | 9.60779e-01 | 1.57707e-01 | 1.08102e+01
  2 | 1.01166e-01 |     1.40548e-02 | 2.02550e-02 | 1.13418e-01 | 2.72140e-04 | 4.85790e+00
  3 | 0.00000e+00 | ... 1.17895e-01 | 1.66725e-02 | 7.43751e-02 | 1.56353e-05 | 5.93806e+00
  4 | 1.73021e-02 |     1.30454e-02 | 3.10489e-03 | 1.33409e-02 | 4.43484e-05 | 2.73892e+00
  5 | 1.80218e-02 |     5.53206e-02 | 6.96508e-03 | 3.57827e-02 | 4.51748e-05 | 7.35875e+00
  6 | 1.05675e-02 |     1.23957e-02 | 1.01379e-04 | 8.96967e-03 | 2.69797e-05 | 3.46404e+00
  ...
```

Note the 'δGimp' column, which shows the DMFT self-consistency condition, but also the first column 'δμ' which shows the convergence of the chemical potential.
The converged self-energy is stored along all other calculated properties in the file 'jobname/seedname.h5'. You can for example plot the self-energy for the Ni $e\_g$ and $t\_{2g}$ orbitals with the following code using the  small helper functions on the bottom:

```
with HDFArchive('dmft_os/U8.0-J1.0-beta20-qmc2e+7/vasp.h5','r') as ar:
    S_os_iw = ar['DMFT_results/last_iter/Sigma_freq_0']

fig, ax = plt.subplots(1,2, figsize=(14,5), dpi=100, sharex=True)
ax = ax.reshape(-1)

plot_sigma_iw(S_os_iw['up_0'],ax,color='C0',label='$t_{2g}$',marker='-')
plot_sigma_iw(S_os_iw['up_2'],ax,color='C1',label='$e_{g}$',marker='-')

ax[0].set_xlim(0,30)
ax[0].set_ylim(-1,2)
ax[1].set_ylim(0,5)

plt.legend()
plt.show()
```

The plot should look similar to this:

Ni-d impurity self-energy from OS DMFT

Showing the Ni $e\_g$ and Ni $t\_{2g}$ orbital self-energies separately (real part left, and imaginary part right).
Both show typical QMC noise at larger frequencies, with a analytic tail-fitting at frequencies larger than 20 eV.

### Step 4: Perform a CSC DFT+DMFT calculation

Now we are ready to perform a CSC DFT+DMFT calculation. We create a new directory for the calculation and copy the following files into it: INCAR, POSCAR, KPOINTS, POTCAR, *plo.cfg*, CHGCAR, WAVECAR, and *dmft\_config.toml*.
solid\_dmft will run VASP for us, but we do have to specify how it is run by adding the following section to the `dmft\_config.toml` file:

```
[dft]
plo_cfg = "plo.cfg"
dft_code = "vasp"
projector_type = "plo"
n_iter = 4
n_cores = 32
mpi_env = "default"
mpi_exe = "/path/to/mpirun"
dft_exec = "/path/to/bin/vasp_std"
```

Here, you have to change the mpi executable and VASP executable path.
Also make sure to adjust the number of cores to be used for the DFT calculations via the *n\_cores* option.
Since VASP is performing an iterative SCF calculation updating the charge density while the KS states are converged we perform a few SCF steps between each DMFT call to converge the KS states with the new charge density from DMFT via *n\_iter*.
Also change the following options in the *dmft\_config.toml* file:

```
csc = true
n_iter_dmft_first = 2
n_iter_dmft_per = 2
n_iter_dmft = 20

load_sigma = true
path_to_sigma = "/path/to/dmft-os/U8.0-J1.0-beta20-qmc1e+7/vasp.h5"
```

This will load the sigma from the file *vasp.h5* in the folder *dmft-os/U8.0-J1.0-beta20-qmc1e+7* and instruct solid\_dmft to perform a CSC calculation.

Also add the following lines to the INCAR file:

```
 ICHARG  = 5      
 AMIX    = 0.08   
 LSYNCH5 = True
```

ICHARG=5 will enable the CSC mode in VASP to communicate with TRIQS. LSYNCH5=True allows TRIQS to write into the hdf5 file created by VASP. Additionally, it may be necessary on some systems to set the following environment variable before running solid\_dmft:

```
 export HDF5_USE_FILE_LOCKING=FALSE
```

This is a general hdf5 library runtime flag allowing for simultaneous read / write access to h5 files. However, it depends on the installation of the library if this is necessary or not.

Run the calculation via *mpirun solid\_dmft 1>out 2>err &*.
Check the directory for the std output and all related DMFT files.
You can see that after each 2 DMFT iterations VASP is called to update the KS states for the new charge density.
In the observables file you will find that the orbital occupation of orbitals now slightly changes from the OS calculation, showing the effect of charge self-consistency:

```
 it |         mu |       G(beta/2) per orbital |       orbital occs up+down | impurity occ
  0 |    0.00278 |   -0.00754         -0.10744 |    1.95350         1.28826 |      8.43701
  1 |    0.04795 |   -0.00030         -0.00142 |    1.90322         1.22302 |      8.15570
  2 |    0.03410 |   -0.00003         -0.00136 |    1.88208         1.25063 |      8.14749
  3 |    0.00424 |   -0.00109         -0.00015 |    1.97017         1.15925 |      8.22899
  4 |    0.00043 |   -0.00011   ...   -0.00023 |    1.97342   ...   1.15596 |      8.23216
  5 |   -0.00020 |   -0.00003         -0.00039 |    1.98029         1.15228 |      8.24544
  .
  .
  .
```

The difference is also visible in the final self-energy comparing OS with CSC:

Ni-d impurity self-energy from CSC DFT+DMFT

The $e\_g$ orbital is now closer to half filling and, thus, more insulating. The large self-energy for $i \omega\_n \rightarrow 0$ is signaling a pole in the self-energy at $\omega=0$ typical for a Mott insulator.

### Step 5: calculating the local spectral function

Next, we are ready to calculate the local spectral function $A(\omega)$ of NiO for the Ni-d orbitals.
This is the easiest post-processing step, since we can simply calculate the local spectral function based on the impurity Green's function $G^\text{imp}\_{m m'}$.
However, since the impurity solver works on the Matsubara axis, we have to find an analytic continuation of the Green's function to the real frequency axis.
The analytic continuation is done using a maximum entropy method in the TRIQS/maxent package.
Prepare a little script in the calculation folder utilizing the post processing functions of solid\_dmft:

```
import solid_dmft.postprocessing.maxent_gf_imp as gimp_maxent

Aimp_csc_w = gimp_maxent.main(external_path='vasp.h5',
                              omega_min=-30, omega_max=15,
                              maxent_error=0.03,
                              sum_spins=True,
                              n_points_maxent=400,
                              n_points_alpha=20)
```

The script utilizes MPI for parallelization so run it via *mpirun python gimp\_maxent.py*.
The script will write the local spectral function into the `*vasp.h5* file.
We can now plot it via the following code:

```
# load the results
with HDFArchive('dmft_csc/vasp.h5','r') as ar:
    A_imp_csc_w = ar['DMFT_results/last_iter/Aimp_maxent_0']

fig, ax = plt.subplots(1,1, figsize=(10,5), dpi=100)

ax.plot(A_imp_csc_w['mesh'], A_imp_csc_w['Aimp_w_line_fit']['total_0'][0,0,:],label='Ni $t_{2g}$')
ax.plot(A_imp_csc_w['mesh'], A_imp_csc_w['Aimp_w_line_fit']['total_2'][0,0,:],label='Ni $e_{g}$')

ax.set_xlim(-10,10)
ax.set_ylim(0,)
ax.set_ylabel(r'A$_{\text{proj}}$ states/eV')
ax.set_xlabel(r'$\omega$ (eV)')

plt.legend()
plt.show()
```

Ni-d projected local spectral function from MaxEnt

We can see that the local spectral function is gapped with the $t\_{2g}$ orbitals completely filled (compare with DFT initial occupations), and the $e\_{g}$ orbital being gapped.
Mind that this is the summed spectral function for up + down spin, with both channels being degenerate.

### Further reading

Similar to DFT, DMFT calculations have many parameters that can be tuned.
Here, all parameters were carefully chosen to converge the DMFT calculation properly, and close to experiment.
Especially, the double counting correction was chosen such that it best fits the experimental data.
To learn more about TRIQS visit the TRIQS Python tutorials page.
And for more concrete DMFT tutorials see the solid\_dmft tutorials.

### Helper functions for python

```
import numpy as np

# plotting
import matplotlib.pyplot as plt

# TRIQS modules
from h5 import HDFArchive
from triqs.gf import *
from triqs.plot.mpl_interface import plt,oplot
  
def plot_sigma_iw(S_iw, ax, color, label='', marker='-o', subtract=True):
    # convert the mesh to a numpy array
    mesh = mesh_to_np_arr(S_iw.mesh)
    mid = len(mesh)//2
    if subtract:
        ax[0].plot(mesh[mid:], S_iw.data[mid:,0,0].real-S_iw.data[-1,0,0].real, marker, color = color, label=label)
    else:
        ax[0].plot(mesh[mid:], S_iw.data[mid:,0,0].real, marker, color = color, label=label)
    ax[1].plot(mesh[mid:], -1*S_iw.data[mid:,0,0].imag, marker, color = color, label=label)

    ax[0].set_xlabel(r"$i \omega_n$ (eV)")
    ax[1].set_xlabel(r"$i \omega_n$ (eV)")
    ax[0].set_ylabel(r"$Re \Sigma (i \omega_n)$  (eV)")
    ax[1].set_ylabel(r"$- Im \Sigma (i \omega_n)$  (eV)")
  
    return
 
def plot_sigma_w(S_w, ax, color, label='', marker='-', subtract=True):
    mesh = mesh_to_np_arr(S_w.mesh)
    mid = len(mesh)//2
    if subtract:
        ax[0].plot(mesh, S_w.data[:,0,0].real-S_w.data[mid,0,0].real, marker, color = color, label=label)
    else:
        ax[0].plot(mesh, S_w.data[:,0,0].real, marker, color = color, label=label)
    ax[1].plot(mesh, -1*S_w.data[:,0,0].imag, marker, color = color, label=label)
 
    ax[0].set_xlabel(r"$\omega$ (eV)")
    ax[1].set_xlabel(r"$\omega$ (eV)")
    ax[0].set_ylabel(r"$Re \Sigma (\omega)$  (eV)")
    ax[1].set_ylabel(r"$- Im \Sigma (\omega)$  (eV)")
    return

def mesh_to_np_arr(mesh):
    from triqs.gf import MeshImTime, MeshReFreq, MeshImFreq

    if isinstance(mesh, MeshReFreq):
        mesh_arr = np.linspace(mesh.w_min, mesh.w_max, len(mesh))
    elif isinstance(mesh, MeshImFreq):
        mesh_arr = np.linspace(mesh(mesh.first_index()).imag, mesh(mesh.last_index()).imag, len(mesh))
    elif isinstance(mesh, MeshImTime):
        mesh_arr = np.linspace(0, mesh.beta, len(mesh))
    else:
        raise AttributeError('input mesh must be either MeshReFreq, MeshImFreq, or MeshImTime')
 
    return mesh_arr
```

## Related tags and articles

vaspgamma.h5, GAMMA, ICHARG, Matsubara formalism

## References
