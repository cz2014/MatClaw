# ACFDT/RPA calculations

Categories: Many-body perturbation theory, ACFDT, Howto, Low-scaling GW and RPA

The adiabatic-connection-fluctuation-dissipation theorem (ACFDT) can be used to derive the random-phase approximation (RPA).
The ACFDT-RPA ground-state energy $E\_{\mathrm{RPA}}$ is the sum of the ACFDT-RPA correlation energy $E\_{c}$ and the Hartree-Fock (HF) energy $E\_{\mathrm{EXX}}$ evaluated non self-consistently using Kohn-Sham orbitals computed within density-functional theory (DFT):

$E\_{\mathrm{RPA}}=E\_{\mathrm{c}}+E\_{\mathrm{EXX}}$.

Note that, here $E\_{\mathrm{EXX}}$ includes also the Hartree energy, the kinetic energy, as well as the Ewald energy of the ions, whereas often in literature $E\_{\mathrm{EXX}}$ refers only to the exact-exchange (EXX) energy evaluated using DFT orbitals.

If ALGO=RPA is set in the INCAR file, VASP calculates the correlation energy within RPA. To this end, VASP first calculates the independent-particle response function, using the unoccupied states given in the WAVECAR file, and then determines the correlation energy using the plasmon-fluctuation equation:

$E\_{c} = \frac{1}{2 \pi} \int\_{0}^{\infty}[ \mathrm{Tr} \, \ln(1-\chi( {\rm i} \omega) V) + \chi( {\rm i} \omega) V ]\, d \omega$.

More information about the theory behind the RPA is found here.

## General recipe to calculate ACFDT-RPA total energies

The ACFDT-RPA total energies can be computed in a four-step procedure or in an all-in-one approach. The all-in-one approach is available as of VASP.6 and can be done in one single step.
Both procedures comprise a self-consistent DFT calculation, diagonalizing the KS Hamiltonian, and the RPA calculation itself. While the all-in-one approach is very convenient, there are several caveats discussed below.

### Four-step procedure to calculate ACFDT-RPA total energy

This four-step procedure is the standard procedure in VASP.5, and is also available in VASP.6 by setting NBANDS in the RPA step.

**Step 1:** a standard DFT run.

:   All occupied orbitals (and as usual in VASP, a few unoccupied orbitals) of the DFT Hamiltonian are calculated. For instance,

```
EDIFF = 1E-8 # required for convergence of RPA total energies
ISMEAR = 0 ; SIGMA = 0.05
```

:   > **Warning:** The convergence of DFT eigenenergies influences the convergence of the RPA correlation energy.

:   > **Tip:** Use the Perdew-Burke-Ernzerhof (PBE) pseudopotentials with a small EDIFF and avoid ISMEAR>0.

:   The DFT run can be done with your favorite setup, but we recommend attaining very high precision (small EDIFF tag) and to use a small smearing width (SIGMA tag), and to avoid higher-order Methfessel-Paxton smearing (see also ISMEAR). That is because Methfessel-Paxton smearing can lead to negative one-electron occupancies, which can result in unphysical correlation energies. We suggest using PBE orbitals as input for the ACFDT-RPA run, but other choices, e.g., local-density-approximation (LDA) or hybrids, are possible as well. For hybrid functionals, we suggest carefully considering the caveats mentioned in Ref. . Specifically, the RPA dielectric matrix yields too weak screening for hybrid functionals, which potentially deteriorates RPA results.

**Step 2:** Compute the HF energy $E\_{\mathrm{EXX}}$ using the DFT orbitals. That is, e.g.,

```
ALGO  = EIGENVAL ; NELM = 1
LWAVE = .FALSE.                ! WAVECAR not written     
LHFCALC = .TRUE. ; AEXX = 1.0  ! ALDAC = 0.0 
ISMEAR = 0 ; SIGMA = 0.05
```

:   Here, LWAVE = .FALSE. avoids an accidental update of the WAVECAR file. Also, VASP automatically sets ALDAC = 1-AEXX, i.e., for AEXX = 1.0, ALDAC = 0.0.

:   > **Tip:** For insulators and semiconductors with a sizable gap, faster k-point convergence of the HF energy can be obtained by setting HFRCUT=-1, although this slows convergence for metals.

**Step 3:** Compute a sufficient number of unoccupied states.

:   In the OUTCAR file of Step 1, search for `maximum number of plane-waves:` and run VASP again with the following INCAR file to determine the unoccupied states by exact diagonalization of the KS Hamiltonian. The KS Hamiltonian must be the same as in step 1, which might be DFT or hybrid.

```
NBANDS = maximum number of plane-waves (times 2 for vasp_gam)
ALGO = Exact    ! exact diagonalization
EDIFF = 1E-8 # required for convergence of RPA total energies
LOPTICS = .TRUE.
ISMEAR = 0 ; SIGMA = 0.05
```

:   For calculations using `vasp_gam`, that is the gamma-point only version of VASP, NBANDS must be set to twice the `maximum number of plane-waves:` found in the OUTCAR file of Step 1. For metals, we recommend to avoid setting LOPTICS=.TRUE., since this slows down k-point convergence .

**Step 4:** Calculate the ACFDT-RPA correlation energy.

```
NBANDS =  maximum number of plane-waves
ALGO = ACFDT
NOMEGA = 12     ! default
ISMEAR = 0 ; SIGMA = 0.05
```

:   The number of imaginary-frequency and imaginary-time-grid points NOMEGA is usually set to 8-24. For large gap insulators NOMEGA = 8 will suffice, while for semiconductors 10-12 suffices.

:   > **Important:** For VASP 6.X, NBANDS must be set in this step.

### All-in-one approach to calculate ACFDT-RPA total energy

VASP will read the WAVECAR file, perform a self-consistent DFT calculation by iterating until convergence is reached, diagonalize the DFT Hamiltonian in the basis set spanned by all KS orbitals, and finally proceed with the RPA calculation. The all-in-one approach is only available as of VASP.6, and it is particularly convenient for the RPAR and GWR algorithms. An example INCAR file is

```
ALGO = RPAR

EDIFF = 1E-8  # required for convergence of RPA total energies
ISMEAR = 0 ; SIGMA = 0.05
 
NOMEGA = 8-24    ! for large gap insulators NOMEGA = 8 will suffice, for semiconductors 10-12 suffices
   
LOPTICS = .TRUE. ! optional 
LPEAD = .TRUE.   ! required for 6.1 and 6.2 if LOPTICS = .TRUE.
```

:   > **Warning:** The tag NBANDS must not be set in the INCAR file.

:   > **Warning:** The convergence of DFT eigenenergies influences the convergence of the RPA correlation energy.

:   > **Tip:** Use the Perdew-Burke-Ernzerhof (PBE) pseudopotentials with a small EDIFF and avoid ISMEAR>0.

The head of the dielectric function can be calculated only for insulators by setting the LOPTICS tag and only the Perturbation-Expression-After-Discretization (PEAD) method is supported, see LPEAD. Furthermore, EDIFF should be small to calculate the DFT orbitals with high precision. Although it is not strictly required, we recommend starting the calculation from a well-converged DFT WAVECAR file.

There are several caveats to the all-in-one approach:

* There is no general support for ACFDT/RPA on top of hybrid functionals. In VASP $\leq$ 6.2, only LDA and gradient corrected functionals are supported. As of VASP 6.2, the all-in-one approach can be used for Hartree-Fock-type calculations, as well as hybrid functionals without range separation. However, range-separated hybrid functionals (including HSE, LMODELHF) yield erroneous results or potentially even crash. Please compare the total energies in a standard DFT/hybrid functional calculation against the energies obtained for the mean-field step in the all-in-one approach: The energies must be exactly the same. If they differ, fall back to the four-step procedure that is explained above.
* To select the new all-in-one approach, it is important "*not to set* NBANDS" in the RPA step. If NBANDS is set in the INCAR file, VASP.6 proceeds with reading the WAVECAR file found in the directory (if not present, random orbitals are used!), and then calculates the correlation energy using these orbitals and one-electron energies.
* The basis set used in the diagonalization is strictly given by all plane waves. That is, there is no option to reduce the basis set size as one can by setting NBANDS in Step 3 and Step 4 of the four-step procedure.
* The exchange energy is only calculated if the low-scaling RPA is selected.
* As of VASP 6.3, the head of the dielectric function (G=0 component) can be calculated by setting LOPTICS = .TRUE.
* In the all-in-one procedure, VASP automatically sets LMAXFOCKAE and NMAXFOCKAE. This changes the energies for hybrid functionals and Hartree-Fock slightly. Hence, you need to set LMAXFOCKAE = 4 also in Step 1 of the four-step procedure to obtain the same results as in the all-in-one procedure.

### Output of ACFDT-RPA total energy

The ACFDT-RPA total energy is calculated for 8 different energy cutoffs and a linear regression is used to extrapolate the results to the infinite cutoff limit, see section below. A successful RPA calculation writes the following lines into the OUTCAR file:

```
      cutoff energy     smooth cutoff   RPA   correlation   Hartree contr. to MP2
---------------------------------------------------------------------------------
            316.767           316.767      -17.5265976349      -26.2640927215
            301.683           301.683      -17.3846505665      -26.0990489039
            287.317           287.317      -17.2429031341      -25.9344769084
            273.635           273.635      -17.0686574017      -25.7325162480
            260.605           260.605      -16.8914915810      -25.5277026697
            248.195           248.195      -16.7202601717      -25.3302982602
            236.376           236.376      -16.5559849344      -25.1415392478
            225.120           225.120      -16.3635400223      -24.9210737434
  linear regression    
  converged value                          -19.2585393615      -28.2627347266
```

Here, the third and fourth columns correspond to the correlation energy (for that specific energy cutoff) in the RPA and the direct second-order Møller–Plesset (MP2) approximation, i.e., the second-order term in RPA. The corresponding results of the linear regression are found in the line starting with `converged value`.

## Low-scaling ACFDT/RPA algorithm

Virtually the same tags and procedures apply to the low-scaling RPA algorithm implemented in VASP 6 . However, ALGO=ACFDT or ALGO=RPA needs to be replaced by either ALGO=ACFDTR or ALGO=RPAR.

With this setting VASP calculates the independent-particle polarizability $\chi(i\omega)$ using Green's functions $G(i\tau)$ on the imaginary time axis $i\tau$ by the contraction formula

$\chi(i\tau\_m) = -G(i\tau\_m)G(-i\tau\_m)$

Subsequently, a compressed Fourier transformation on the imaginary axes $\tau\_m,\omega\_n$ yields

$\chi(i\omega\_n) = \sum\_{m=1}^{N} \gamma\_{nm} \chi(i\omega\_m)$

The remaining step is the evaluation of the correlation energy and is the same as described above.

Crucial to this approach is the accuracy of the Fourier transformation from $\chi(i\tau)\to \chi(i\omega)$, which in general depends on two factors: First, the grid order $N$ that can be set by NOMEGA in the INCAR file. Here, similar choices as for the ALGO=ACFDT are recommended. Second, the grid points $\tau\_m,\omega\_n$ and Fourier matrix $\gamma\_{nm}$ have to be optimized for the same interval as spanned by all possible transition energies in the polarizability. The minimum (maximum) transition energy can be set with the OMEGAMIN (OMEGATL) tag and should be smaller (larger) than the bandgap, i.e., the maximum transition energy, of the previous DFT calculation. VASP determines these values automatically and writes it in the OUTCAR after the lines

```
Response functions by GG contraction:
```

These values should be checked for consistency. Furthermore, we recommend inspecting the grid and transformation errors by looking for the following lines in the OUTCAR file

```
nu_ 1=  0.1561030E+00 ERR=   0.6327933E-05 finished after   1 steps    
nu_ 2= ...
Maximum error of frequency grid:  0.3369591E-06
```

Every frequency point will have a similar line as shown above for the first point. The value after `ERR=` corresponds to the maximum Fourier-transformation error and should be of similar order as the maximum integration error of the frequency grid.

### Output of low-scaling ACFDT/RPA

Selecting the low-scaling RPA algorithm, VASP computes the total energy in the RPA and writes the following output

```
 -----------------------------------------------------
 HF-free energy      FHF    =       -25.11173505 eV
 HF+RPA corr. energy TOTEN  =       -36.96463791 eV
 HF+E_corr(extrapolated)    =       -37.70506951 eV
```

The line `HF+RPA corr. energy TOTEN` contains the total energy calculated with the largest cutoff ENCUTGW.
The line `HF+E_corr(extrapolated)` contains the total energy with the extrapolated value for the RPA correlation energy.

The line `FHF` denotes the exact exchange contribution to the total energy. This contribution is determined with an electronic density
using LMAXFOCKAE. For most systems the resulting energy is in very good agreement with the reference EXX energy obtained in step 2 described above. As of version 6.5.2, exact compatibility with this step can be reached using LFOCKSTD.

> **Tip:** Select exact one-centre terms for the electronic density in exact exchange energies with LFOCKSTD as of version 6.5.2.

### Singles contribution to the correlation energy

The low-scaling RPA algorithm also allows for the determination of the so-called singles contribution, to the total energy represented by following diagrams:

In most textbooks this contribution is assumed to be zero. Ren et al. pointed out that this is true only in the Hartree-Fock basis set. The singles contribution is non-vanishing for other basis sets.

The singles contribution is calculated for LSINGLES=.TRUE.. In this case following additional lines can be found in OUTCAR:

```
HF single shot energy change        -1.23182672
renormalized HF singles             -1.23310555
```

Here, the first line contains the value of the singles as proposed by Klimeš et al., while the second line contains the singles contribution of Ren et al.. In most cases we found that the two values are exceedingly close to each other, which can be understood in the way how the propagator is renormalized.

### Optional: RPA Forces

Optionally, RPA forces can be calculated by adding following line to the INCAR file:

```
 LRPAFORCE = .TRUE.
```

For RPA forces the change in the one-electron density is required.
This is automatically performed with the linear-response routine within VASP.
After a successful run, the following block of data is found in the OUTCAR file.

```
POSITION                                       TOTAL RPA FORCE (eV/Angst)
-----------------------------------------------------------------------------------
     0.17542     -0.22348      0.17542        -0.292069      7.581315     -0.292069
     1.12850      1.31044      1.12850         0.304683     -7.605527      0.304683
-----------------------------------------------------------------------------------
   total drift:                                0.012614     -0.024212      0.012614

SUGGESTED UPDATED POSCAR (direct coordinates)  step
-----------------------------------------------------------------------------------
 -0.00958461  -0.00958461   0.13485779         0.04179056   0.04179056   0.00283088
  0.25787833   0.25787833   0.22191754        -0.04337198  -0.04337198   0.00431513
```

The suggested updated positions are also written to the CONTCAR file (if NSW=0). The updated positions are obtained by multiplying the RPA-forces with the parameter DAMP\_NEWTON and the inverse of the DFT-Hessian (which is also calculated during the RPA force calculations) and adding the resultant vector to the current positions. DAMP\_NEWTON currently defaults to 0.8, but the user might want to change this to 1.0 (no damping), or smaller values if instabilities are observed. The CONTCAR file can be copied to the POSCAR file, and a few such RPA calculations should recover the groundstate structure. Alternatively, standard relaxations (IBRION =1-4) or even MD's can be performed.

> **Tip:** Use LFOCKSTD to improve total energies and RPA forces as of version 6.5.2.

### Caveats: Noise in Energies and RPA Forces

Generally, the energy calculated by the RPA can be quite noisy as a function of the ionic positions, in particular, if PRECFOCK = FAST and NMAXFOCKAE = 1 is set (these are the default values for RPA calculations). Most of the noise is related to the exact exchange energy. To determine if noise is affecting the results, it is useful to calculate the exchange energy separately as explained in step 2 above. If the exchange energy reported there is smooth, and the exchange energy reported by the all-in-one approach is noisy (e.g. shows odd jumps as a function of the positions or volume), it is strongly recommended to consider one or both of the options discussed below.

Currently, to reduce the noise in the energy and forces, it is sensible to set PRECFOCK = Normal (typically doubling the execution time and memory requirement). It is also possible to set LMAXFOCKAE = -1 (which implicitly sets NMAXFOCKAE = 0). This makes the correlation energies and the related forces less noisy, but technically less accurate (i.e. part of the correlation energy will be missing at high transition energies). Overall, RPA forces must be used carefully and only after extensive testing of all relevant parameters.

### Memory bottleneck and Parallelization

The cubic scaling space-time RPA algorithm requires considerably more memory than the corresponding quartic-scaling implementations, two Green's functions $G({\bf r,r'},i\tau\_n)$ have to be stored in real-space. To reduce the memory overhead, VASP exploits Fast Fourier Transformations (FFT) to avoid storage of the matrices on the (larger) real space grid, on the one hand. The precision of the FFT can be selected with PRECFOCK, where usually the values *Fast* sufficient.

On the other hand, the code avoids storage of redundant information, i.e., both the Green's function and polarizability matrices are distributed as well as the individual imaginary grid points. The distribution of the imaginary grid points can be set by hand with the NTAUPAR and NOMEGAPAR tags, which splits the imaginary grid points NOMEGA into NTAUPAR time and NOMEGAPAR groups. For this purpose both tags have to be divisors of NOMEGA.

The default values are usually reasonable choices provided the tag MAXMEM is set correctly and we strongly recommend to set MAXMEM instead of NTAUPAR.

> **Important:** As of version 6.2, MAXMEM is estimated automatically (if not set) from the "MemAvailable" entry of the Linux kernel in "/proc/meminfo".

The required storage for a low-scaling RPA or GW calculation depends mostly on NTAUPAR, the number of MPI groups that share same imaginary time points. A rough estimate for the required bytes is given by

```
(NGX*NGY*NGZ)*(NGX_S*NGY_S*NGZ_S) / ( NCPU  / NTAUPAR ) * 16
```

where "NCPU" is the number of MPI ranks used for the job,"NGX,NGY,NGZ" denotes the number of FFT grid points for the exact exchange and "NGX\_S,NGY\_S,NGZ\_S" the number of FFT grid points for the supercell. Note, both grids are written to the OUTCAR file after the lines

```
FFT grid for exact exchange (Hartree Fock)
FFT grid for supercell:
```

The smaller NTAUPAR is set, the less memory per node the job requires to finish successfully.

The approximate memory requirement is calculated in advance and printed to screen and OUTCAR as follows:

```
min. memory requirement per mpi rank 1234 MB, per node 9872 MB
```

## Some Issues Particular to ACFDT-RPA Calculations on Metals

For metals, the RPA groundstate energy converges the fastest with respect to k-points, if the exchange (Eq. (12) in reference ) and correlation energy are calculated on the same k-point grid, HFRCUT is not set, and the long-wavelength contributions from the polarizability are not considered (see reference ).

To evaluate Eq. (12), a correction energy for $E\_{\mathrm{EXX}}$ related to partial occupancies has to be added to the RPA groundstate energy:

$E\_{\mathrm{RPA}}=E\_{\mathrm{c}}+E\_{\mathrm{EXX}}+E\_{\mathrm{HFc}}$.

In vasp.5.4.1, this value is calculated for any HF type calculation (step 2) and can be found in the OUTCAR file after the total energy (in the line starting with *exchange ACFDT corr. =*).

To neglect the long-wavelength contributions, simply set LOPTICS=*.FALSE.* in the ALGO=*Exact* step (third step), and remove the WAVEDER files in the directory.

## Possible tests and known issues

### Exact one-centre density terms

Beginning with version 6.5.2, it is possible to include exact one-center terms in the density for the exact exchange (EXX) component of RPA total energies and forces by enabling the LFOCKSTD option. Incorporating these one-center terms significantly enhances the accuracy of both total energies and forces-by at least an order of magnitude-compared to results obtained using finite-difference methods. Therefore, it is strongly recommended to activate LFOCKSTD for GW and RPA calculations starting from version 6.5.2. In earlier versions, the one-center contribution to the density was managed using the LMAXFOCKAE setting.

### Basis set convergence

The expression for the ACFDT-RPA correlation energy written in terms of reciprocal lattice vectors reads:

$E\_{\rm c}^{\rm RPA}=\int\_{0}^{\infty} \frac{\mathrm{d}\omega}{2\pi} \sum\_{{\mathbf{q}}\in \mathbf{BZ} }\sum\_{{\mathbf{G}}} \left\{(\mathrm{ln}[1-\tilde\chi^0({\mathbf{q}},\mathrm{i}\omega)V({\mathbf{q}})])\_{{\mathbf{G,G}}} +V\_{{\mathbf{G,G}}}({\mathbf{q}})\tilde\chi^0({\mathbf{q}},{\mathrm{i}}\omega) \right\}$.

The sum over reciprocal lattice vectors has to be truncated at some $\mathbf{G}\_{\mathrm{max}}$, determined by $\frac{\hbar^2|{\mathbf{G}}+{\mathbf{q}}|^2}{2\mathrm{m}\_e}$ < ENCUTGW, which can be set in the INCAR file. The default value is $\frac{2}{3}\times$ ENCUT, which experience has taught us not to change. For systematic convergence tests, instead increase ENCUT and repeat steps 1 to 4, but be aware that the "maximum number of plane-waves" changes when ENCUT is increased. Note that it is virtually impossible, to converge absolute correlation energies. Rather concentrate on relative energies (e.g. energy differences between two solids, or between a solid and the constituent atoms).

Since correlation energies converge very slowly with respect to $\mathbf{G}\_{\rm max }$, VASP automatically extrapolates to the infinite basis set limit using a linear regression to the equation:

$E\_{\mathrm{c}}({\mathbf{G}})=E\_{\mathrm{c}}(\infty)+\frac{A}{{\mathbf{G}}^3}$.

Furthermore, the Coulomb kernel is smoothly truncated between ENCUTGWSOFT and ENCUTGW using a simple cosine like window function (Hann window function).
Alternatively, the basis set extrapolation can be performed by setting LSCK=.TRUE., using the squeezed Coulomb kernel method.

The default for ENCUTGWSOFT is 0.8$\times$ENCUTGW (again we do not recommend to change this default).

The integral over $\omega$ is evaluated by means of a highly accurate minimax integration. The number of $\omega$ points is determined by the flag NOMEGA, whereas the energy range of transitions is determined by the band gap and the energy difference between the lowest occupied and highest unoccupied one-electron orbital. VASP determines these values automatically (from vasp.5.4.1 on), and the user should only carefully converge with respect to the number of frequency points NOMEGA. A good choice is usually NOMEGA=12, however, for large gap systems one might obtain $\mu$eV convergence per atom already using 8 points, whereas for metals up to NOMEGA=24 frequency points are sometimes necessary, in particular, for large unit cells.

Strictly adhere to the steps outlines above. Specifically, be aware that steps two and three require the WAVECAR file generated in step one, whereas step four requires the WAVECAR and WAVEDER file generated in step three (generated by setting LOPTICS=*.TRUE.*).

Convergence with respect to the number of plane waves can be rather slow, and we recommend to test the calculations carefully. Specifically, the calculations should be performed at the default energy cutoff ENCUT, and at an increased cutoff (ideally the default energy cutoff $\times 1.3$). Another issue is that energy volume-curves are sometimes not particularly smooth. In that case, the best strategy is to set

```
ENCUT = 1.3 times default energy cutoff
ENCUTGWSOFT = 0.5 times default energy cutoff
```

where the default energy cutoff is the usual one (maximum ENMAX in POTCAR files). The frequency integration also needs to be checked carefully, in particular for small gap systems (some symmetry broken atoms) convergence can be rather slow, since the one-electron band gap can be very small, requiring a very small minimum $\omega$ in the frequency integration.

### K-point convergence: Spline interpolation

> **Mind:** ESF\_SPLINES is available as of VASP.6.5.0

It is possible to use spline interpolation to improve upon k-point integration errors by rewriting the
RPA correlation energy as an integral
$E\_c^{{\rm RPA}}= \sum\_{{\mathbf{q}}\in \mathbf{BZ} }\sum\_{{\mathbf{G}}} S({\bf q+G})$
over the electronic structure factor:
$S({\bf q}+{\bf G}) =\int {\rm d}\omega
\left\{(\mathrm{ln}[1-\tilde\chi^0({\mathbf{q}},\mathrm{i}\omega)V({\mathbf{q}})])\_{{\mathbf{G,G}}} +V\_{{\mathbf{G,G}}}({\mathbf{q}})\tilde\chi^0({\mathbf{q}},{\mathrm{i}}\omega) \right\}$

If ESF\_SPLINES=T is set, the code stores the electronic structure factor on a coarse grid defined by KPOINTS and performs a tricubic spline interpolation towards finer q-grids iteratively. After each iteration the RPA correlation energy is evaluated and compared to the result of previous interpolation.
If the difference in energy is smaller than ESF\_CONV within ESF\_NINTER interpolation steps, the code considers the q-point integration to be converged and reports the result to OUTCAR in the following format

```
     cutoff energy     smooth cutoff   RPA   correlation   Hartree contr. to MP2  RPA spline-interp.
-----------------------------------------------------------------------------------------------------
           166.667           133.333      -12.9738715106      -19.7255874374      -13.4968000908
           158.730           126.984      -12.8840657072      -19.6294580403      -13.4017404001
           151.172           120.937      -12.7775593388      -19.5151822998      -13.3005326847
           143.973           115.178      -12.6604147404      -19.3892142669      -13.1868498210
           137.117           109.694      -12.5530911576      -19.2733151174      -13.0861120393
           130.588           104.470      -12.4659186304      -19.1786165194      -12.9778587892
           124.369            99.495      -12.3690601643      -19.0725742983      -12.8709666989
           118.447            94.758      -12.2461267475      -18.9372318755      -12.7590723870
 linear regression    
 converged value                          -14.0340307585      -20.8751715586      -14.5828037654
```

The last column contains the result from the spline interpolation for the selected energy cutoffs reported in the first column.

> **Warning:** Delete WAVEDER for this method.

Note that this method is incompatible with k-p perturbation theory, where the
largest q-point integration error $\lim\_{\bf q\to 0} \tilde\chi^0\_{{\bf G G}'}({\bf q},{\rm i}\omega) \cdot {\bf V}\_{\bf G G'}({\bf q})$ is added explicitly to the RPA integral.
This long-wave contribution is stored in WAVEDER, and VASP assumes you want to add this term if the file is present in the working directory.

Also, the long-wave limit is ill-defined for metallic systems, in contrast to the spline interpolation method.

> **Mind:** ESF\_SPLINES can be used for metals.

Nevertheless, for insulators, we still recommend using WAVEDER and not set ESF\_SPLINES for efficiency reasons.

## Related Tags and Sections

* ALGO for response functions and *ACFDT* calculations
* NOMEGA, NOMEGAR number of frequency points
* LHFCALC, switches on HF calculations
* LOPTICS, required in the DFT step to store head and wings
* ENCUTGW, to set cutoff for response functions
* ENCUTGWSOFT
* PRECFOCK controls the FFT grids in HF, GW, RPA calculations
* NTAUPAR controls the number of imaginary time groups in space-time GW and RPA calculations
* NOMEGAPAR controls the number of imaginary frequency groups in space-time GW and RPA calculations
* MAXMEM sets the available memory per MPI rank on each node
* LFINITE\_TEMPERATURE switches on Matsubara (finite temperature) formalism
* ESF\_SPLINES uses tricubic spline interpolation of electronic structure factor to accelerate k-point convergence
* LFOCKSTD exact one-centre terms in EXX part of total energy and RPA forces

## References

---
