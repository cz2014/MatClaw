# Practical guide to GW calculations

Categories: Many-body perturbation theory, GW, Howto, Low-scaling GW and RPA

The GW approximation is an approximation to the self-energy. GW calculations are available as of VASP.5.X. For details on the implementation and use of the *GW* routines, we recommend the papers by Shishkin *et al.* and Fuchs *et al.*

# Single step procedure: GW in one go

As of VASP.6.3 all GW approximations can be run in one single run by selecting the corresponding ALGO tag and omitting NBANDS), for instance like so

```
System = SiC
ALGO = EVGW0, QPGW0, EVGW, QPGW, GW0R or GWR # use an algorithgm described below
NELMGW = 1,2,.. # number of self-consistency cycles
ISMEAR = 0 ; SIGMA = 0.05  ! small sigma is required to avoid partial occupancies
LOPTICS = .TRUE.  # for insulators, omit for metals
```

Note, NBANDS must not be present in the INCAR to select this procedure.

> **Important:** In older versions a two step procedure is required, where the first step is always a DFT calculation and the second step the actual GW calculation.

The two-step procedure is described below.

## Caveats

The single-step GW procedure performs a DFT step internally with an exact diagonalization of the Kohn-Sham Hamiltonian using the maximum available NBANDS supported for the chosen ENCUT value.
Consequently, a large number of unoccupied bands is initialized with random plane-wave coefficients. In rare cases, this yields two linearly dependent column vectors in the Hamiltonian and results in LAPACK errors like "ZPOTRF fails". These errors can be prevented using the two-step GW procedure as described below. Furthermore, one can "ramp up" NBANDS to the maximum value by repeatedly restarting the DFT calculation from a pre-converged WAVECAR with fewer bands.

# First step: DFT calculation

*GW* calculations always require a one-electron basis set. Usually this set is obtained from a standard DFT calculation and written into the WAVECAR file and can be calculated for instance the following INCAR file:

```
System = SiC
NBANDS = 512
ISMEAR = 0 ; SIGMA = 0.05  ! small sigma is required to avoid partial occupancies
LOPTICS = .TRUE.
```

Note, that a significant number of empty bands is required for *GW* calculations, so that it might be better to perform the calculations in two steps: first a standard ground-state calculation with few unoccupied orbitals only,

```
System = SiC ground-state occupied orbitals
ISMEAR = 0 ; SIGMA = 0.05  ! small sigma is required to avoid partial occupancies
EDIFF = 1E-8               ! required tight tolerance for ground-state orbitals
```

and, second, a calculation of a large number of unoccupied orbitals

```
System  = SiC unoccupied orbitals
ALGO = Exact               ! use exact diagonalization of the Hamiltonian
NELM = 1                   ! since we are already converged stop after one step
NBANDS = 512               ! maybe even larger                
ISMEAR = 0 ; SIGMA = 0.05  ! small sigma is required to avoid partial occupancies
LOPTICS = .TRUE.
```

Furthermore, note that the flag LOPTICS=.TRUE. is required to write the file WAVEDER, which contains the derivative of the orbitals with respect to **k**.
This derivative is used to construct the head and wings of the dielectric matrix employing **k**·**p** perturbation theory and is important to accelerate k-point convergence for insulators and semiconductors.

> **Warning:** For metals, in general, we recommend omitting the LOPTICS tag and removing the WAVEDER file from the directory.

## Optional: Use Hybrid functionals

Optionally, one can start a *GW* calculation from a hybrid functional, such as HSE.
For hybrid functionals, the two step procedure will accordingly involve the following INCAR files. In the first step, converged HSE03 orbitals are determined (see here for a selection of available hybrid functionals):

```
System  = SiC ground-state occupied orbitals
ISMEAR = 0 ; SIGMA = 0.05
ALGO = Damped ; TIME = 0.5  ! or ALGO = Conjugate
LHFCALC = .TRUE. ; AEXX = 0.25 ; HFSCREEN = 0.3 
EDIFF = 1E-6      ! required tight tolerance for ground-state orbitals
```

Secondly, determine the HSE03 orbitals for unoccupied states:

```
System  = SiC unoccupied orbitals
NBANDS = 512      ! maybe even larger
ALGO = Exact
NELM = 1          ! since we are already converged stop after one step
ISMEAR = 0 ; SIGMA = 0.05
LHFCALC = .TRUE. ; AEXX = 0.25 ; HFSCREEN = 0.3 
LOPTICS = .TRUE. # for insulators
```

# Second step: GW calculation

The actual *GW* calculation is done in a second step. Here different *GW* flavors are possible and are selected with the ALGO tag.

Note that as of VASP.6 the GW ALGO tags have been renamed, see here for VASP.5.X tags.

## Single shot quasiparticle energies: G0W0

This is the simplest *GW* calculation and computationally the most efficient one.
A single-shot calculation is often referred to as G0W0 and calculates the quasiparticle energies from a single *GW* iteration by neglecting all off-diagonal matrix elements of the self-energy and employing a Taylor expansion of the self-energy around the DFT energies $E\_{n{\bf q}}^{(0)}$. The corresponding equation becomes

$E\_{n{\bf q}} = E\_{n{\bf q}}^{(0)} + Z\_{n{\bf q}} \langle \phi^{(0)}\_{n{\bf q}}| \Sigma(E\_{n{\bf q}}^{(0)}) - V\_{xc} |\phi^{(0)}\_{n{\bf q}}\rangle$

with the renormalization factor

$Z\_{n{\bf q}}=\frac{1}{1-{\rm Re}\langle \phi^{(0)}\_{n{\bf q}}| \Sigma'(E\_{n{\bf q}}^{(0)}) | \phi^{(0)}\_{n{\bf q}}\rangle }$

In VASP, G0W0 calculations are selected using an INCAR file such as

```
System  = SiC
NBANDS = 512
ISMEAR = 0 ; SIGMA = 0.05
NELMGW = 1 ! use NELM for VASP.6.2 and older 
ALGO = EVGW0 ! use "GW0" for VASP.5.X
NOMEGA = 50
```

> **Mind:** Convergence with respect to the number of empty bands NBANDS and with respect to the number of frequencies NOMEGA must be checked carefully.

To avoid complicated inter-nested tests, we recommend calculating all orbitals that the plane-wave basis set allows to calculate (except for simple tests). For further reading, please consult the section on ENCUTGW.

After a successful G0W0 run, VASP will write the quasiparticle energies into the OUTCAR file for a set of NBANDSGW bands for every k-point in the Brillouin zone. Look for lines similar to

```
QP shifts <psi_nk| G(iteration)W_0 |psi_nk>: iteration 1
for sc-GW calculations column KS-energies equals QP-energies in previous step 
and V_xc(KS)=  KS-energies - (<T + V_ion + V_H > + <T+V_H+V_ion>^1  + <V_x>^1)

k-point   1 :       0.0000    0.0000    0.0000
 band No.  KS-energies  QP-energies   sigma(KS)   V_xc(KS)     V^pw_x(r,r')   Z            occupation Imag(sigma)

     1      -7.1627      -8.3040     -14.5626     -12.7276     -21.6682       0.6219       2.0000       1.2037
     2      -2.0901      -3.4347     -15.7660     -14.2799     -21.7439       0.9048       2.0000       0.6914
     3      -2.0901      -3.4347     -15.7660     -14.2799     -21.7439       0.9048       2.0000       0.6914
     4      -2.0901      -3.4347     -15.7660     -14.2799     -21.7439       0.9048       2.0000       0.6914
     5       0.4603      -0.4663     -13.7603     -12.5200     -18.1532       0.7471       2.0000       0.2167
     6       0.4603      -0.4663     -13.7603     -12.5200     -18.1532       0.7471       2.0000       0.2167
```

The first column is the band index and the third column denotes the quasiparticle energies $E\_{n{\bf q}}$. Column two, four, five and seven refer to the DFT energies $E\_{n{\bf q}}^{(0)}$, diagonal matrix elements of the self-energy $\langle \phi^{(0)}\_{n{\bf q}}|\Sigma(\omega=E\_{n{\bf q}}^{(0)}) |\phi^{(0)}\_{n{\bf q}}\rangle$, the exchange-correlation potential $\langle \phi^{(0)}\_{n{\bf q}}|V\_{xc} |\phi^{(0)}\_{n{\bf q}}\rangle$ and the renormalization factor $Z\_{n{\bf q}}$ defined above, respectively.

## Partially self-consistent calculations: EVGW0

In most cases, the *best* results (*i.e.*, closest to experiment) are obtained by iterating only $G$ via the spectral representation

$G^{(i)}({\bf r},{\bf r}',\omega)=\sum\_{n{\bf k}}\frac{\phi\_{n{\bf k}}^{\*(0)}
({\bf r})\phi^{(0)}\_{n{\bf k}}
({\bf r}')}{\omega-E^{(i)}\_{n{\bf k}}}$

but keeping $W$ and the orbitals $\phi^{(0)}\_{n{\bf q}}$ fixed to the initial DFT level. This method goes back to Hybertsen and Louie and can be achieved in two ways.

If the spectral method is not selected (LSPECTRAL=.FALSE., requiring much more compute time), the quasiparticle (QP) shifts are iterated automatically four times, and one finds four sets of QP shifts in the OUTCAR file. The first one corresponds to the G0W0 case. The INCAR file is simply:

```
System = SiC
NBANDS = 512
ISMEAR = 0 ; SIGMA = 0.05
ALGO = EVGW0 ! use "GW0" in VASP.5.X
LSPECTRAL =.FALSE.
```

> **Tip:** In self-consistent GW calculations, convergence with the number of updated bands NBANDSGW must be checked carefully.

For technical reasons, it is not possible to iterate $G$ in this manner if LSPECTRAL=.TRUE. is set in the INCAR file (this is the default). In this case, an iteration number must be supplied in the INCAR file using the NELMGW tag. Usually, three to four iterations are sufficient to obtain accurate QP shifts.

```
System = SiC
NBANDS = 512
ISMEAR = 0 ; SIGMA = 0.05
ALGO = EVGW0 ! use "GW0" in VASP.5.X
NELMGW = 4 ! use NELM in VASP.6.2 and older
```

The results are found again in the OUTCAR file

```
QP shifts <psi_nk| G(iteration)W_0 |psi_nk>: iteration 4

k-point   1 :       0.0000    0.0000    0.0000
 band No. old QP-enery  QP-energies   sigma(KS)   T+V_ion+V_H  V^pw_x(r,r')   Z            occupation Imag(sigma)

     1      -8.6924      -8.7107     -14.2871       5.5647     -21.6681       0.6076       2.0000       1.1648
     2      -3.4692      -3.4806     -15.6742      12.1894     -21.7437       0.7304       2.0000       0.6351
     3      -3.4692      -3.4806     -15.6742      12.1894     -21.7437       0.7304       2.0000       0.6351
     4      -3.4692      -3.4806     -15.6742      12.1894     -21.7437       0.7304       2.0000       0.6351
     5      -0.6957      -0.7006     -13.6827      12.9802     -18.1531       0.7264       2.0000       0.2769
     6      -0.6957      -0.7006     -13.6827      12.9802     -18.1531       0.7264       2.0000       0.2769
     7      -0.6957      -0.7006     -13.6827      12.9802     -18.1531       0.7264       2.0000       0.2769
```

In contrast to single shot GW calculations, the second column represent now the QP-energies from the previous iteration.

## Partially self-consistent quasiparticle calculations: QPGW0

If non diagonal components of the self-energy (in the orbital basis) should be included use ALGO=QPGW0. The following setting can be used:

```
System = SiC
NBANDS = 512
ISMEAR = 0 ; SIGMA = 0.05
ALGO = QPGW0 ! or "scGW0" for VASP.5.2.11 and older 
LOPTICS = .TRUE. ; LPEAD = .TRUE. ! ommit this lines for metals
NELMGW = 4 ! use NELM for VASP.6.2 and older
```

In this case, the orbitals are updated as well by constructing a hermitian (energy independent) approximation to the self-energy . The "static" COHSEX approximation can be selected by setting NOMEGA = 1 . To improve convergence to the ground-state, the charge density (and the charge density only) is mixed using a Kerker type mixing in VASP.5.3.2 and more recent versions (see IMIX). The mixing parameters AMIX, BMIX, AMIX\_MAG, BMIX\_MAG, AMIN can be adjusted, if convergence problems are encountered.

We strongly urge the user to monitor convergence by inspecting the lines

```
charge density residual
```

in the OUTCAR files.

Alternatively, the mixing may be switched off by setting IMIX=0 and controlling the step width for the orbitals using the parameter TIME (which defaults to 0.4). This selects a fairly sophisticated damped MD algorithm that is also used for DFT methods when ALGO=Damped. This method is generally more reliable for metals and materials with strong charge sloshing.

After every iteration, VASP writes the following lines into the OUTCAR file

```
QP shifts <psi_nk| G(iteration)W_0 |psi_nk>: iteration 1
    GWSYM:  cpu time   15.8978: real time   15.9528

k-point   1 :       0.0000    0.0000    0.0000
 band No. DFT-energies  QP-energies  QP-e(diag)   sigma(DFT)    Z            occupation

     1      -7.1626      -8.4217      -8.3038      -8.9978       0.6219       2.0000
     2      -2.0899      -3.4394      -3.4347      -3.5765       0.9047       2.0000
     3      -2.0899      -3.4394      -3.4347      -3.5765       0.9047       2.0000
     4      -2.0899      -3.4394      -3.4347      -3.5765       0.9047       2.0000
     5       0.4604      -0.4787      -0.4663      -0.7800       0.7471       2.0000
     6       0.4604      -0.4787      -0.4663      -0.7800       0.7471       2.0000
     7       0.4604      -0.4787      -0.4663      -0.7800       0.7471       2.0000
     8       5.1013       4.1883       4.2149       3.9518       0.7711       2.0000
```

For the first iteration, here, the fourth column should be identical to the third column of the G0W0 results discussed above. The third column reports the quasiparticle energies obtained from including the off-diagonal matrix elements in the eigenvalue equation.

### Caveats

The *QPGW0* (or *scGW0* in VASP.5.2.11 and older) must be used with great caution, particularly in combination with symmetry.
Symmetry is handled in a rather sophisticated manner. Specifically, only the minimal number of required combinations of *q* and *k* points is considered. In this case, symmetry must be applied to restore the full star of *q*. This is done by determining degenerate eigenvalue/eigenvector pairs and restoring their symmetry according to their irreducible representation. Although the procedure is generally relatively reliable, it fails to work properly if the degenerate states do not possess eigenvalues that are sufficiently close due to insufficient convergence in the preceding DFT calculations. That is because states are treated as degenerate if, and only if, their eigenenergies are within 0.01 eV.

For large supercells with low symmetry, we strongly recommend switching off symmetry.

## Self-consistent EVGW and QPGW calculations

Self-consistent *QPGW* calculations are only supported in a QP picture. As for *QPGW*0, it is possible to update the eigenvalues only (ALGO=*EVGW* or *GW* for VASP.5.X), or the eigenvalues and one-electron orbitals (ALGO=*QPGW* or *scGW* in VASP.5.2.11 and older). In all cases, a QP picture is maintained, *i.e.*, satellite peaks (shake ups and shake downs) can not be accounted for in the self-consistency cycle. Self-consistent *QPGW* calculations can be performed by simply repeatedly calling VASP using:

```
System = SiC
NBANDS = 512
ISMEAR = 0 ; SIGMA = 0.05
ALGO = EVGW    ! "GW" in VASP.5.X, eigenvalues only  or alternatively
ALGO = QPGW    ! "scGW" in VASP.5.2.11 and older, eigenvalues and one electron orbitals
```

For QPGW0 or QPGW, nondiagonal terms in the Hamiltonian are accounted for, *e.g.* the linearized QP equation is diagonalized, and the one-electron orbitals are updated .
Alternatively (and preferably), the user can specify an electronic iteration counter using NELMGW (NELM in VASP.6.2 and older):

```
System = SiC
NBANDS = 512
ISMEAR = 0 ; SIGMA = 0.05
NELMGW = 3   ! use NELM in VASP.6.2 and older
ALGO = EVGW  ! "GW" in VASP.5.X 
# or  
ALGO = QPGW  ! "scGW" in VASP.5.2.11 and older
```

In this case, the one-electron energies (=QP energies) are updated 3 times (starting from the DFT eigenvalues) in both G and W. For ALGO=*QPGW* (or ALGO=*scGW* in VASP.5.2.11 and older), the one electron energies and one electron orbitals are updated 3 times . As for ALGO = *QPGW0* (or *scGW0* in vasp.5.2.11 and older), the "static" COHSEX approximation can be selected by setting NOMEGA=1 .

To improve convergence to the ground-state, the charge density is mixed using a Kerker type mixing starting with VASP.5.3.2 (see IMIX). The mixing parameters AMIX, BMIX, AMIX\_MAG, BMIX\_MAG, AMIN can be adjusted, if convergence problems are encountered.
Alternatively, the mixing may be switched off by setting IMIX=0 and controlling the step width for the orbitals using the parameter TIME (which defaults to 0.4). This selects a fairly sophisticated damped MD algorithm that is also used for DFT methods when ALGO=Damped. This method is generally more reliable for metals and materials with strong charge sloshing.

Additional information about this method is found here.

### Caveats

Fully self-consistent QPGW calculations with an update of the orbitals in $G$ and $W$ require significant care and are prone to diverge (QPGW0 calculations are usually less critical). As discussed, above, one can select this mode using:

```
System = SiC
NBANDS = 512
ISMEAR = 0 ; SIGMA = 0.05
ALGO = QPGW  ! or "scGW" in VASP.5.2.11 and older, eigenvalues and one-electron orbitals
NELMGW = number of steps ! use NELM for VASP.6.2 and older
```

However, one *caveat* applies to this case: when the orbitals are updated, the derivatives of the orbitals with respect to $k$ (stored in the WAVEDER file) will become incompatible with the orbitals.
This can cause severe problems and convergence to the incorrect solution.

> **Warning:** For metals, in general, we recommend omitting the LOPTICS tag and removing the WAVEDER file from the directory.

For insulators, VASP (version 5.3.2 or higher) can update the WAVEDER file in each electronic iteration if the finite difference method is used to calculate the first derivative of the orbitals with respect to $k$:

```
System = SiC
NBANDS = 512
ISMEAR = 0 ; SIGMA = 0.05
ALGO = QPGW ! "scGW" in VASP.5.2.11 and older, eigenvalues and one-electron orbitals
NELMGW  = 10 ! use NELM in VASP.6.2 and older
LOPTICS = .TRUE. ; LPEAD = .TRUE.
```

The combination LOPTICS=.TRUE.; LPEAD=.TRUE. is required since $\frac{\delta H-\epsilon\_{n{\bf k}}S}{\delta {k}\_i}$ is not available for *GW* like methods.
LPEAD=.TRUE. circumvents this problem by calculating the derivatives of the orbitals using numerical differentiation on the finite k-point grid (this option is presently limited to insulators).

Vertex corrections are presently not documented. This is a feature still under construction, and we recommend collaborating with the Vienna group if you desperately need that feature.

# Low scaling GW algorithms

The GW implementations in VASP described in the papers of Shishkin *et al.* avoids storage of the Green's function $G$ as well as Fourier transformations between time and frequency domain entirely. That is, all calculations are performed solely on the real frequency axis using Kramers-Kronig transformations for convolutions in the equation of $\chi$ and $\Sigma$ in reciprocal space.

As of VASP.6 a new cubic scaling GW algorithm (called space-time implementation in the following) can be selected. This approach follows the idea of Rojas *et al.* and performs the GW self-consistency cycle on imaginary time $t\to i\tau$ and imaginary frequency axes $\omega\to i\omega$.

> **Tip:** Using the low-scaling GW algorithm also calculates the total energy in the Random Phase approximation (RPA), which is described in a separate article.

## Low scaling, single shot GW calculations: G0W0R

The low-scaling analogue of G0W0 is selected with ALGO=G0W0R.
In contrast to the single-shot GW calculations on the real-axes,
here the self-energy $\Sigma = G\_0 W\_0$ is determined on the imaginary frequency axis.
To this end, the overall scaling is reduced by one order of magnitude and is cubic with respect to the system size,
because a small value for NOMEGA can be used (usually <20).

This algorithm evaluates:

* Single-shot GW quasiparticle energies (from an analytical continuation of the self-energy to the real axis)

* Natural orbitals from the first order change of the density matrix (i.e. $G\_0 \Sigma G\_0$), see the NATURALO tag for more information .

> **Mind:** This selection ignores NELMGW.

Following INCAR file selects the low-scaling GW algorithm:

```
System = SiC
ISMEAR = 0 ; SIGMA = 0.05
LOPTICS = .TRUE.  
ALGO = G0W0R
NOMEGA = 12 ! small number of frequencies necessary
```

Search the OUTCAR file for the following lines

```
  QP shifts evaluated in KS or natural orbital/ Bruckner basis
  k-point   1 :       0.0000    0.0000    0.0000
  band No.  KS-energies   sigma(KS)    QP-e(linear)    Z         QP-e(zeros)     Z        occupation    Imag(E_QP)    QP_DIFF TAG
 
       1      -7.1627      -8.6732      -8.2451       0.7166      -8.2346       0.7026       2.0000      -1.3101       0.0000   2
       2      -2.0901      -3.4155      -3.0350       0.7129      -3.0272       0.7011       2.0000      -0.5582      -0.0000   2
       3      -2.0901      -3.4155      -3.0350       0.7129      -3.0272       0.7011       2.0000      -0.5582       0.0000   2
       4      -2.0901      -3.4155      -3.0350       0.7129      -3.0272       0.7011       2.0000      -0.5582      -0.0000   2
       5       0.4603      -0.8219      -0.4904       0.7414      -0.4814       0.7273       2.0000      -0.1902       0.0000   2
       6       0.4603      -0.8219      -0.4904       0.7414      -0.4814       0.7273       2.0000      -0.1902      -0.0000   2
```

Here column four is obtained by a linearization of the self-energy around the Kohn-Sham energies (second column) and can be compared to the third column of single-shot GW calculations on the real axis.
Column six represents another set of QP-energies that is obtained from the roots of the following equation

$\langle \phi^{(0)}\_{n{\bf q}}| T + V\_{ext}+V\_h+ \Sigma(\omega) | \phi^{(0)}\_{n{\bf q}}\rangle -\omega =0$

These roots represent the poles of the Green's function in the spectral representation.

### Output description

The meaning of each column is explained briefly in the following.

* `band No.` the band index of KS orbital at given k-point
* `KS-energies` eigenenergies corresponding to band index
* `sigma(KS)` diagonal matrix elements of self-energy evaluated at KS energies
* `QP-e(linear)` quasiparticle energies obtained from linearizing frequency dependence of diagonal self-energy around KS energies
* `Z` renormalization factor obtained from five-point stencil for derivative of self-energy w.r.t. frequency
* `QP-e(zeros)` quasiparticle energies obtained from full frequency dependence of self-energy, i.e. real part of complex pole $\omega$ of Green's function
* `Z` renormalization factor obtained from central difference for derivative of self-energy w.r.t. frequency
* `occupation` occupation number for band at given k-point
* `Imag(E_QP)` imaginary part of complex pole $\omega$, i.e. measure for inverse lifetime of quasi-particle
* `QP_DIFF` difference of QP energies (of linearized self-energy) obtained from Eq. 77 of Liu et. al. and M. Grumets thesis.

## Optional: RPA Forces

Optionally, RPA forces can be calculated by adding following line to the INCAR:

```
 LRPAFORCE = .TRUE.
```

After the QP-energies, VASP performs a linear-response calculation that is required for the RPA forces.
Following data block in the OUTCAR file can be found after a successful run:

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

> **Tip:** Use LFOCKSTD to improve total energies and RPA forces as of version 6.5.2.

> **Warning:** Currently RPA forces for metallic systems are not supported.

## Low scaling, partially self-consistent GW calculations: EVGW0R

> **Mind:** available as of vasp 6.4.0

The low-scaling analogue of EVGW0 is selected with ALGO=EVGW0R.
Following INCAR file selects this algorithm:

```
System = SiC
ISMEAR = 0 ; SIGMA = 0.05
LOPTICS = .TRUE.  
ALGO = EVGW0R 
NELMGW = 4  ! number of iterations in G
NOMEGA = 12 ! small number of frequencies necessary
```

After each iteration, a similar block of data as for ALGO=G0W0R calculations is written to OUTCAR showing the NBANDSGW updated quasi-particle energies (poles) of the Green's function.

## Partially self-consistent GW calculations: GW0R

The space-time implementation allows for true self-consistent GW calculations. That is, the solution of the Dyson equation for the Green's function can be obtained with a modest computational effort. The main procedure of a self-consistent GW calculation consists of four main steps

* Obtain Green's function $G^{(j)}\_{\bf G G'}({\bf q},i\omega\_n) = \left[ \delta\_{\bf GG'} - \Sigma^{(j-1)}\_{\bf GG'}({\bf q},i\omega\_n)G^{(j-1)}\_{\bf G G'}({\bf q},i\omega\_n)\right]^{-1}G^{(j-1)}\_{\bf G G'}({\bf q},i\omega\_n)$
* Compute irreducible polarizability $\chi^{(j)}({\bf r},{\bf r}',i\tau\_m) = -G^{(j)}({\bf r},{\bf r}',i\tau\_m)G^{(j)}({\bf r}',{\bf r},-i\tau\_m)$
* Determine screened potential $W^{(j)}\_{{\bf G}{\bf G}'}({\bf q},\omega\_m)=\left[\delta\_{{\bf G}{\bf G}'}-\chi^{(j)}\_{{\bf G}{\bf G}'}({\bf q},\omega\_m)V\_{{\bf G}{\bf G}'}({\bf q})\right]^{-1}V\_{{\bf G}{\bf G}'}({\bf q})$
* Calculate GW self-energy $\Sigma^{(j)}({\bf r},{\bf r}',i\tau\_m) =- G^{(j)}({\bf r},{\bf r}',i\tau\_m)W^{(j)}({\bf r}',{\bf r},i\tau\_m)$

This procedure can be selected with the following INCAR settings

```
System = SiC
ISMEAR = 0 ; SIGMA = 0.05
LOPTICS = .TRUE. ; LPEAD = .TRUE.  
NELMGW = number of iterations wanted ! NELM in 6.2 and older
ALGO = GW0R ! ALGO = scGW0R has the same effect here, that is self-consistency in G, no update in W
```

The number of self-consistency steps can be set with the NELMGW tag.

Due to efficiency, VASP performs each step in the Hartree-Fock basis. This is the reason why there are two sets of QP-energies found after the first iteration (one for the QP-energies in the KS-basis and one for the QP energies in the HF basis)
After the second iteration, only the QP energies obtained in the HF basis are printed, and a similar output as follows is found in the OUTCAR file

```
QP shifts evaluated in HF basis
k-point   1 :       0.0000    0.0000    0.0000
band No.  KS-energies   sigma(KS)    QP-e(linear)    Z         QP-e(zeros)     Z        occupation    Imag(E_QP)    QP_DIFF TAG

     1      -7.1626      -8.6510      -8.2275       0.7154      -8.2173       0.7017       2.0000      -1.3177       0.0000   2
     2      -2.0899      -3.4157      -3.0348       0.7127      -3.0269       0.7008       2.0000      -0.5614       0.0000   2
     3      -2.0899      -3.4157      -3.0348       0.7127      -3.0269       0.7008       2.0000      -0.5614      -0.0000   2
     4      -2.0899      -3.4157      -3.0348       0.7127      -3.0269       0.7008       2.0000      -0.5614       0.0000   2
     5       0.4604      -0.8170      -0.4857       0.7407      -0.4768       0.7266       2.0000      -0.1945       0.0000   2
     6       0.4604      -0.8170      -0.4857       0.7407      -0.4768       0.7266       2.0000      -0.1945      -0.0000   2
     7       0.4604      -0.8170      -0.4857       0.7407      -0.4768       0.7266       2.0000      -0.1945       0.0000   2
     8       5.1013       4.0069       4.2594       0.7693       4.2645       0.7598       2.0000      -0.0602       0.0000   2
```

Here the meaning of each column is the same as for the other low-scaling GW algorithms.

## Fully self-consistent GW caluclations: GWR

If the screened potential should be updated during the self-consistency circle the following INCAR file can be used

```
System = SiC
ISMEAR = 0 ; SIGMA = 0.05
LOPTICS = .TRUE. ; LPEAD = .TRUE.  
NELMGW = number of iterations wanted ! use NELM in VASP.6.2 and older
ALGO = GWR ! ALGO = scGWR has the same effect here, that is self-consistency in G and W
```

The output is similar to partially self-consistent GW calculations, with the difference that *KS-energies* are replaced by the QP energies from previous iteration.

### Caveats

Using this option, similar caveats can be expected as for ALGO=*EVGW* and *QPGW* calculations and we recommend to leave out the LOPTICS and LPEAD line for metals.

The cubic scaling space-time GW algorithm requires considerably more memory than the corresponding quartic-scaling implementations, two Green's functions $G({\bf r,r'},i\tau\_n)$ have to be stored in real-space. To reduce the memory overhead, VASP exploits Fast Fourier Transformations (FFT) to avoid storage of the matrices on the (larger) real space grid, on the one hand. The precision of the FFT can be selected with PRECFOCK, where usually the values *Fast* sufficient.

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

# Related tags and articles

* ALGO for response functions and *GW* calculations
* LOPTICS, derivative of wavefunction w.r.t. $k$
* LPEAD, derivative of wavefunction with finite differences
* LMAXFOCKAE overlap densities and multipoles
* MAXMEM, memory available to one mpi rank on each node
* NOMEGA, NOMEGAR number of frequency points
* LSPECTRAL, use the spectral method for the polarizability
* LSPECTRALGW, use the spectral method for the self-energy
* OMEGAMAX, OMEGATL and CSHIFT
* ENCUTGW, energy cutoff for response function
* ENCUTGWSOFT, soft cutoff for Coulomb kernel
* ODDONLYGW and EVENONLYGW, reducing the *k*-grid for the response functions
* LSELFENERGY, the frequency dependent self energy
* LWAVE, self-consistent *GW*
* NOMEGAPAR, frequency grid parallelization
* NTAUPAR, time grid parallelization
* NATURALO, natural orbitals
* LALL\_IN\_ONE, all-in-one *GW* mode
* IALL\_IN\_ONE, all-in-one *GW* mode
* NBANDSEXACT, number of KS bands in all-in-one mode
* NBANDS\_WAVE, number of bands written to WAVECAR in all-in-one mode
* LSINGLES, singles contribution to correlation energy
* LFOCKSTD exact one-centre terms in EXX part of total energy and RPA forces

Examples that use this tag

# References
