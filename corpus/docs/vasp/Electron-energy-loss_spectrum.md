# Electron-energy-loss spectrum

Categories: VASP, Linear response, Dielectric properties, Many-body perturbation theory, Howto

One of the many ways in which it is possible to probe neutral excitations in a material is by injecting electrons into the sample. These are called electron-energy-loss spectroscopy experiments, where the incoming electron can create bound electron-hole pairs (i.e. excitons), plasmons, or even higher-order multi-pair excitations.

The incoming electron acts as an external potential, $V\_\mathrm{ext}(\mathbf r', t')$, which induces a charge density in the material, $\rho\_\mathrm{ind}(\mathbf r, t)$. Within linear-response theory these two quantities can be related by the reducible polarisability function, $\chi$, via a Green-Kubo relation

:   :   $$\rho\_\mathrm{ind}(\mathbf r, t) = \int \mathrm d^3r'\mathrm d t \chi(\mathbf r, t,\mathbf r', t')V\_\mathrm{ext}(\mathbf r', t').$$

If the external potential is taken as proportional to a plane-wave of momentum $\mathbf q$, then the electron energy-loss spectrum (EELS) can be taken from the imaginary part of the inverse dielectric function, $\epsilon^{-1}(\mathbf q,\omega)$, since $\epsilon^{-1} = 1 + v\chi$

:   :   $$\mathrm{EELS}(\mathbf q,\omega) = -\mathrm{Im}\left[\epsilon^{-1}(\mathbf q,\omega)\right].$$

# Inclusion of local fields

In general, the microscopic quantity $\epsilon^{-1}$ is a function of two coordinates, i.e. $\epsilon^{-1} := \epsilon^{-1}(\mathbf r , \mathbf r', \omega)$. This has important consequences on inhomogeneous systems where a homogeneous, constant, external electric field can induce fluctuations at the interatomic scale, and thus create microscopic fields. A direct consequence of the inhomogeneous character of the system is that in reciprocal space $\epsilon$ has to be written as $\epsilon\_{\mathbf G, \mathbf G'}(\mathbf q, \omega)$, where $\mathbf G$ is a reciprocal lattice vector. The microscopic fields are then the $\mathbf G \neq 0$ components of the tensor.

From $\epsilon^{-1} = 1 + v\chi$ it is possible to see that a problem arises when $\mathbf q \to 0$, i.e. the optical limit. In reciprocal space, this equation becomes

:   :   $$\epsilon^{-1}\_{\mathbf G, \mathbf G'}(\mathbf q, \omega) = \delta\_{\mathbf G, \mathbf G'} + \frac{4\pi}{|\mathbf q + \mathbf G|^2}\chi\_{\mathbf G, \mathbf G'}(\mathbf q, \omega)$$

where $v(\mathbf q + \mathbf G) = 4\pi/|\mathbf q + \mathbf G|^2$ is the Coulomb potential. At $\mathbf q= 0$, all components without microscopic fields are divergent. To circumvent this issue, the evaluation of $\epsilon^{-1}$ is replaced the Coulomb potential with

:   :   $$\bar v(\mathbf q + \mathbf G) = \left\{
        \begin{array}{ll}
        0, & \mathbf G=0 \\
        4\pi/|\mathbf q + \mathbf G|^2, & \mathbf G\neq 0
        \end{array}
        \right.,$$

leaving the $v\_0\chi\_{00}$ component to be dealt with separately and then added at the end.

# Micro-macro connection and relation to measured quantities

It is important to note that the actual measured quantity, $\epsilon\_\mathrm{M}(\mathbf q, \omega)$, does not depend on the microscopic fields. To connect both the microscopic and macroscopic quantities, an averaging procedure is taken out, so that

:   :   $$\epsilon\_{\mathrm M}(\mathbf q,\omega) = \frac{1}{\epsilon\_{\mathbf G = 0, \mathbf G'=0}^{-1}(\mathbf q,\omega)}.$$

Since VASP computes the macroscopic function, EELS can be extracted from the final result via

:   :   $$\mathrm{EELS}(\omega) = -\mathrm{Im}\left[\frac{1}{\epsilon\_{\mathrm M}(\mathbf q,\omega)}\right]$$

Note that the inclusion of local fields and the connection to the macroscopic observable must be considered regardless of the level of approximation to the polarisability function, $\chi$. Within VASP, this can be done at several levels of approximation, which are discussed in the next section.

# Computing EELS with VASP

## EELS from density functional theory (DFT)

The simplest calculation that yields a macroscopic dielectric function is a ground state calculation using DFT, with the tags NBANDS and LOPTICS. Using bulk silicon as an example with the following INCAR

```
SYSTEM = Si
NBANDS = 48
ISMEAR = 0 ; SIGMA = 0.1
ALGO = N
LOPTICS = .TRUE.
CSHIFT = 0.4
```

the macroscopic dielectric function can be extracted from the vasprun.xml file at the end of the calculation by first running the following script

```
awk 'BEGIN{i=0} /<dielectricfunction comment="density-density">/,\
                /<\/dielectricfunction>/ \
                 {if ($1=="<r>") {a[i]=$2 ; b[i]=($3+$4+$5)/3 ; c[i]=$4 ; d[i]=$5 ; i=i+1}} \
     END{for (j=0;j<i/2;j++) print a[j],b[j],b[j+i/2]}' vasprun.xml > dielectric_function.DFT.dat
```

which writes the trace of the tensor to a file called `dielectric_function.DFT.dat`. Plotting the EEL spectrum can be done with visualization software like Gnuplot, using the following command as an example:

```
p 'dielectric_function.DFT.dat' u 1:($2/($2**2+$3**2)) w l lc rgb 'black' t 'DFT'
```

Imaginary part of the inverse macroscopic dielectric function for bulk Si from DFT.

The results of this DFT calculation should be analyzed with the following considerations in mind. Firstly, this calculation is performed only for $\mathbf q = 0$, with no local fields considered. Because of this, the dielectric function from DFT is often called the independent particle random-phase approximation dielectric function. Secondly, no interactions between electrons and holes are included in the evaluation of the dielectric function. To account for both local-field effects and the electron-hole interaction, approximations beyond DFT must be taken into account.

Plotting the EELS can also be done using py4vasp as a Python module. Take the next script as an example, where the vaspout.h5 had its name changed to `vaspout.DFT.h5`:

```
import py4vasp
import numpy as np
import matplotlib.pyplot as plt

calc = py4vasp.Calculation.from_file('vaspout.DFT.h5')

energies = calc.dielectric_function.read('')['energies']
# Only the xx-component of the dielectric function is read
epsilon  = calc.dielectric_function.read('')['dielectric_function'][1][1][:]

eels = -np.imag(1.0/epsilon)

plt.plot(energies, eels, label='DFT')
plt.ylabel(r'-Im[$\epsilon^{-1}_M$]')
plt.xlabel('Energy loss [eV]')
plt.legend()
plt.show()
```

EEL spectrum from DFT plotted with py4vasp.

Note that for the case of bulk Silicon, since the material is centrosymmetric, it suffices to plot one component of the 3x3 tensor. For non-symmetric systems, it is better to take the trace of the dielectric function.

## EELS from time-dependent density functional theory (TDDFT)

VASP can compute the macroscopic dielectric function employing TDDFT calculations using different functionals. Such calculations not only account for the electron-hole interaction beyond the independent particle level but also include local fields and can be performed at points in the Brillouin zone other than $\Gamma$.

The evaluation of $\epsilon\_{\mathrm M}$ is performed via Casida's equation, set with ALGO=TDHF in the INCAR. The following INCAR will be used as an example, where the electron-hole interaction is included using a model dielectric function. The specific solver that details how $\epsilon\_\mathrm{M}$ is built is chosen with the tag IBSE. Other options are available, with more information to be found on the Bethe-Salpeter equations page.

```
SYSTEM    = Si
ISMEAR    = 0 
SIGMA     = 0.1
NBANDS    = 48     
ALGO      = TDHF
CSHIFT    = 0.4
IBSE      = 0
NBANDSO   = 4       ! number of occupied bands
NBANDSV   = 8       ! number of unoccupied bands
LHARTREE  = .TRUE.
LADDER    = .TRUE.
LFXC      = .FALSE.
LMODELHF  = .TRUE. 
AEXX      = 0.083
HFSCREEN  = 1.22
```

At the end of the calculation, the dielectric function can be extracted from the vasprum.xml or vaspout.h5 files. Results are shown at the end of the next subsection in order to compare TDDFT and many-body perturbation theory approaches.

## EELS from many-body perturbation theory (MBPT)

The addition of electron-hole interactions to the dielectric function can also be done performing calculations at the MBPT level, with ALGO=BSE. The caveat is that VASP requires a previous GW calculation in order to generate the WFULLxxxx.tmp files, where the dielectric screening is stored.

Like in the TDDFT case, users can select which algorithm to use when evaluating $\epsilon\_\mathrm{M}$ via the tag IBSE. In the INCAR file used as an example below, the exact diagonalization solver is employed

```
SYSTEM    = Si
ISMEAR    = 0 
SIGMA     = 0.1
NBANDS    = 48     
ALGO      = BSE
CSHIFT    = 0.4
IBSE      = 2
NBANDSO   = 4       ! number of occupied bands
NBANDSV   = 8       ! number of unoccupied bands
LHARTREE  = .TRUE.
LADDER    = .TRUE.
```

and the same number of virtual and occupied states are used, but now, no information is given about any parameters to model the electron-hole interaction.

Extracting the data at the end of the calculation can be done for both MBPT and TDDFT using the following script. Edit it to use the right vasprun.xml file.

```
awk 'BEGIN{i=0} /<dielectricfunction>/,\
                /<\/dielectricfunction>/ \
                 {if ($1=="<r>") {a[i]=$2 ; b[i]=($3+$4+$5)/3 ; c[i]=$4 ; d[i]=$5 ; i=i+1}} \
     END{for (j=0;j<i/2;j++) print a[j],b[j],b[j+i/2]}' vasprun.BSE.xml > dielectric_function.BSE.dat
```

> **Mind:** If both TDDFT and MBPT calculations are run in the same directory, VASP will overwrite the vasprun.xml and vaspout.h5 files, making it impossible to compare both calculations. Please be sure to either change the name of this file after each calculation or perform both calculations in different directories.

Plotting both results can be done in gnuplot using

```
p 'dielectric_function.BSE.dat' u 1:($2/($2**2+$3**2)) w l lc rgb 'black' t 'BSE', \
'dielectric_function.TDHF.dat' u 1:($2/($2**2+$3**2)) w l lc rgb 'red' t 'TDHF'
```

which results in the following figure.

Imaginary part of the inverse macroscopic dielectric function for bulk Si from both BSE and TDHF at $\Gamma$-point.

Both spectra look very similar, the differences is due to the treatment of the electron-hole interaction in both TDDFT and BSE case. This is both, a consequence of the appropriate choice of AEXX and HFSCREEN parameters, as well as the fact that bulk Silicon is a centrosymmetric material, so the model dielectric function works well here. However, while the use of a model (diagonal) dielectric function is well suited for bulk Silicon, for systems with lower symmetry, the off-diagonal elements that are ignored here will be important and can lead to larger discrepancies in the results from TDDFT and MBPT.

To plot the EEL spectrum with py4vasp, it should be noted that the type of calculation has to be specified when reading the dielectric function. It is simply a matter of editing the following script

```
import py4vasp
import numpy as np
import matplotlib.pyplot as plt

calc_bse  = py4vasp.Calculation.from_file('vaspout.BSE_Q1.h5')
calc_tdhf = py4vasp.Calculation.from_file('vaspout.TDHF_Q1.h5')

# The type of calculation must be specified, with the addition of the 'BSE' string
energies = calc_bse_q1.dielectric_function.read('BSE')['energies']
epsilon_bse  = calc_bse.dielectric_function.read('BSE')['dielectric_function'][1][1][:]
# The type of calculation must be specified, with the addition of the 'TDHF' string
epsilon_tdhf = calc_tdhf.dielectric_function.read('TDHF')['dielectric_function'][1][1][:]

eels_bse  = -np.imag(1.0/epsilon_bse)
eels_tdhf = -np.imag(1.0/epsilon_tdhf)

plt.plot(energies, eels_bse,  '', label='BSE')
plt.plot(energies, eels_tdhf, '', label='TDHF')
plt.ylabel(r'-Im[$\epsilon^{-1}_M$]')
plt.xlabel('Energy loss [eV]')
plt.legend()
plt.show()
```

which will produce the following plot for EELS.

EELS plot using py4vasp for bulk Si from both BSE and TDHF at $\Gamma$-point.

# Calculations at finite momentum

> **Warning:** With VASP, finite momentum calculations at TDDFT or BSE level, i.e. ALGO=TDHF or BSE, must always use ANTIRES=2 regardless of the solver, functional, or approximation used for the electron-hole interaction. Otherwise, the results will be unphysical!

The macroscopic dielectric function can be evaluated at other points in the Brillouin zone. First, it is important to check the point list in the OUTCAR or IBZKPT from the ground-state calculation. In the OUTCAR the points are listed in this section

```
 Subroutine IBZKPT returns following result:
 ===========================================

 Found     16 irreducible k-points:

 Following reciprocal coordinates:
            Coordinates               Weight
  0.000000  0.000000  0.000000      1.000000
  0.166667  0.000000  0.000000      8.000000
  0.333333  0.000000  0.000000      8.000000
...
```

with the first three entries being the reduced coordinates, the fourth entry being the weight of the respective point. The same information is also repeated in the IBZKPT file, where the points are listed as

```
Automatically generated mesh
      16
Reciprocal lattice
    0.00000000000000    0.00000000000000    0.00000000000000             1
    0.16666666666667    0.00000000000000    0.00000000000000             8
    0.33333333333334    0.00000000000000    0.00000000000000             8
...
```

The point at which $\epsilon\_M(\mathbf q,\omega)$ is going to be computed is then selected in the INCAR file with the tag KPOINT\_BSE. The syntax is

```
 KPOINT_BSE = index_of_k-point  n1 n2 n3
```

where the first entry is the index of the point on the list found in the OUTCAR or IBZKPT files, and $n\_i,\, i=1,2,3$ optional integer arguments. If present, these three indices can be used the evaluate the dielectric function at a k point outside of the first Brillouin zone corresponding to

:   $$\mathbf{k} + n\_{1} \mathbf{b}\_{1}+ n\_{2} \mathbf{b}\_{2} + n\_{3} \mathbf{b}\_{3}.$$

Still using bulk silicon as an example, the following INCAR evaluates $\epsilon\_M(\mathbf q,\omega)$ at the second k-point on the list

```
SYSTEM = Si
NBANDS = 48
NBANDSO = 4 ; NBANDSV = 8
ISMEAR = 0 ; SIGMA = 0.1
EDIFF = 1E-8
ALGO = BSE
LADDER = .TRUE.
LHARTREE = .TRUE.
ANTIRES = 2
CSHIFT = 0.4
IBSE = 2
KPOINT_BSE = 2
OMEGAMAX = 30
```

Extracting the dielectric function from the vasprun.xml file is done similarly as $\Gamma$-point calculations, but with a small caveat that the dielectric function now only has one single component. Use the following script

```
awk 'BEGIN{i=0} /<dielectricfunction>/,\
                /<\/dielectricfunction>/ \
                 {if ($1=="<r>") {a[i]=$2 ; b[i]=$3 ; c[i]=$4 ; d[i]=$5 ; i=i+1}} \
     END{for (j=0;j<i/2;j++) print a[j],b[j],b[j+i/2]}' vasprun.xml > dielectric_function.TDHF.dat
```

to extract the data and plot the EELS result using Gnuplot.

Imaginary part of the inverse macroscopic dielectric function for bulk Si from both BSE and TDHF for KPOINT\_BSE=2. In this example it corresponds to the coordinates $(0.5,0.0,0.0)$ in reciprocal space.

Much like calculations at $\Gamma$, results from model TDDFT are very close to those from MBPT. The reduction in intensity for spectra away from $\Gamma$ is normal. This is due to the fact that matrix elements are now away from the dipole approximation.

To plot the same results with py4vasp, the new shape of the dielectric function has to be taken into account, and so no indexing is added to the epslion array

```
import py4vasp
import numpy as np
import matplotlib.pyplot as plt

calc_bse  = py4vasp.Calculation.from_file('vaspout.BSE.h5')
calc_tdhf = py4vasp.Calculation.from_file('vaspout.TDHF.h5')

energies = calc_bse.dielectric_function.read('BSE')['energies']

# Notice that the dielectric function no has a single component, so there is no need for indexing the 
# array
epsilon_bse  = calc_bse.dielectric_function.read('BSE')['dielectric_function']
epsilon_tdhf = calc_tdhf.dielectric_function.read('TDHF')['dielectric_function']

eels_bse  = -np.imag(1.0/epsilon_bse)
eels_tdhf = -np.imag(1.0/epsilon_tdhf)

plt.plot(energies, eels_bse,  '', label='BSE')
plt.plot(energies, eels_tdhf, '', label='TDHF')
plt.ylabel(r'Im[$\epsilon^{-1}_M$]')
plt.xlabel('Energy loss [eV]')
plt.legend()
plt.show()
```

which will generate the following plot.

EELS plot for KPOINT\_BSE=2 using py4vasp.

## Related Tags and Sections

ALGO,
LOPTICS,
LHFCALC,
LADDER,
LHARTREE,
NBANDSV,
NBANDSO,
OMEGAMAX,
LFXC,
ANTIRES,
BSE calculations,
Time-dependent density-functional theory calculations

## References
