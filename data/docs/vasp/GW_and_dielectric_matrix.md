# GW and dielectric matrix

Categories: Many-body perturbation theory, GW, Theory

For GW calculations the frequency dependent dielectric matrix $\epsilon(\omega)$ in the Random Phase Approximation (RPA) is determined via the polarizability ${\bf \chi}$ and the Coulomb potential $V$ using $\epsilon(\omega)= 1 -V \cdot \chi(\omega)$.

> **Mind:** low-scaling GW algorithms determine the dielectric matrix on the imaginary frequency axis and cannot be used to calculate ${\bf \epsilon}$ on the real frequency axis.

The real-frequency dependent dielectric matrix can be calculated with the quartic-scaling GW implementation, in which usability is limited to relatively small unit cells containing a few dozen atoms at maximum.
Here, two algorithms are available and can be selected via LSPECTRAL. The methods are discussed below.

If only the frequency-dependent dielectric matrix should be computed, ALGO=*CHI* can be used to skip the calculation of GW quasi-particle energies.

> **Mind:** All GW calculations require a preceding DFT calculation with many unoccupied states.

There is a lecture available on our YouTube channel on calculating the optical gap and dielectric properties.

## Spectral Method

The spectral method is selected by LSPECTRAL=*.TRUE.*, which is the default value.
Here, VASP computes the polarizability in two steps.

First, the spectral density of the polarizability is calculated using Fermi's golden rule

$S\_{{\bf G G}'}({\bf q},\omega) = \sum\_{nm}\sum\_{\bf k q} \delta(\epsilon\_{n\bf k} - \epsilon\_{m\bf k-q} -\omega) \left\langle {n\bf k} \right| {\bf G} \left| {m\bf k-q} \right\rangle
\left\langle {m\bf k-q}\right| {\bf G}' \left| {n\bf k}\right\rangle$

The delta function is approximated by a triangular function centered at the transition energy. The real and imaginary part of the polarizability is calculated in a second step using a Hilbert transformation

$\chi\_{{\bf G G}'}({\bf q},\omega) = \int \mathrm{d}\omega'
S\_{{\bf G G}'}({\bf q},\omega')
\left(
\frac{1}{\omega-\omega' - i \eta }
- \frac{1}{\omega+\omega' + i \eta }
\right)$

Here η is an infinitesimal that can be set manually by CSHIFT.

This integration is performed semi-analytically by restricting the integration variable ω' to a frequency grid that is determined by NOMEGA, OMEGATL, OMEGAMIN and OMEGAMAX.

Together with the approximation of the delta function in the spectral density (see above), the integration can be carried out analytically and one arrives essentially at a matrix-vector product

$\chi\_{{\bf G G}'}({\bf q},\omega\_j) = \sum\_{k=1}^{\rm NOMEGA} t\_{jk} S\_{{\bf G G}'}({\bf q},\omega'\_k)$

Only the integration weights $t\_{jk}$ depend essentially on η, i.e. CSHIFT.
From the explicit form of these weights one can deduce that contributions to the dielectric function at low frequencies depend on the smallest grid spacing $\Delta\_{\min}=\omega'\_1-\omega'\_2$. These contributions are suppressed only if $\eta\gt \Delta\_\min$, but yield spurious contributions at low frequencies in the dielectric function otherwise.

Furthermore, the frequency grid $\omega\_j$ of the complex polarizability is not restricted to the same grid as the integration variable. That is $\omega\_k\neq \omega'\_j$ in general. In fact, the resolution of the frequency grid of the polarizability can be much finer and is set with NEDOS.

> **Tip:** To reduce spurious contributions in the imaginary part of the dielectric function at small frequencies one can reduce CSHIFT and increase NOMEGA.

However, reducing CSHIFT in the spectral method introduces additional spikes in the dielectric function. Thus for visualization, one often performs a Lorentzian filter on the raw data, even though such a filter typically shifts peaks of the original dielectric function. There is no particular reason why the Lorentzian filter should be used, since smoothing data is essentially cosmetics; Gaussian smearing is also perfectly acceptable.

A minimal INCAR for such a calculation looks as follows:

```
ALGO = CHI   # skip quasi-particle energies 
NOMEGA = 100 # number of frequency points
```

Next, an alternative approach, which already includes some sort of smoothing of the dielectric function, is presented.

## Direct calculation of the dielectric function

The polarizability can be calculated directly without using a Hilbert transformation via the formula of Adler and Wiser.

$\chi\_{{\bf G G}'}({\bf q},\omega) = \sum\_{nm}\sum\_{\bf k q}
\left(
\frac{\left\langle {n\bf k} \right| {\bf G} \left| {m\bf k-q} \right\rangle
\left\langle {m\bf k-q}\right| {\bf G}' \left| {n\bf k}\right\rangle }{\omega-(\epsilon\_{n\bf k} - \epsilon\_{m\bf k-q}) - i \eta }
- \frac{\left\langle {n\bf k} \right| {\bf G} \left| {m\bf k-q} \right\rangle
\left\langle {m\bf k-q}\right| {\bf G}' \left| {n\bf k}\right\rangle }{\omega+\epsilon\_{n\bf k} - \epsilon\_{m\bf k-q} + i \eta }
\right)$

Here CSHIFT influences the peak width of the dielectric function directly.

This method is selected with LSPECTRAL=*.FALSE.* and yields smoother dielectric functions than the spectral method described above.
Also, the direct calculation requires less memory.

> **Warning:** The direct calculation of the polarizability is much slower than the spectral method.

A minimal INCAR for such a calculation looks as follows:

```
ALGO = CHI          # skip quasi-particle energies 
LSPECTRAL = .FALSE. # direct calculation of chi
NOMEGA = 100        # number of frequency points
```

## Local field effects

Both methods support the inclusion of local field effects in the dielectric function on the RPA level. These effects can be included with with LRPA=*.TRUE.*.

> **Mind:** The GW routine is the only routine capable to include local field effects for the frequency-dependent dielectric function.

## Output

The imaginary and real part of the frequency-dependent dielectric function
is determined in all GW calculations. It can be conveniently grepped
from the OUTCAR file using the command (note the two spaces between the words)

```
grep " dielectric  constant" OUTCAR
```

The first value is the frequency (in eV) and the other two are
the real and imaginary parts of the trace of the dielectric matrix.

Furthermore, VASP writes the following data into the OUTCAR file.

* The head of the microscopic dielectric function (without local field effects): $\epsilon\_{\rm mic}(\omega) = \lim\_{{\bf q}\to 0} \epsilon\_{\bf 00}({\bf q},\omega)$

* Inverse macroscopic dielectric tensor:$\frac{1}{
  \hat {\bf q} \cdot \epsilon\_\infty(\omega)\cdot \hat {\bf q}
  }
  = \lim\_{{\bf q}\to 0} \left[\epsilon^{-1}\right]\_{\bf 00}({\bf q},\omega)$

The latter potentially includes local field effects depending on the value of LRPA.
A detailed explanation of these quantities is found in the  lecture notes on dielectric properties.

> **Warning:** OUTCAR contains only a subset of the complete dielectric function ( the one restricted to NOMEGA points).

The complete frequency dependence (NEDOS frequency points) is written to vasprun.xml and has following format:

```
 <dielectricfunction comment="HEAD OF MICROSCOPIC DIELECTRIC TENSOR (INDEPENDENT PARTICLE)">
  <imag>
   <array>
    <dimension dim="1">gridpoints</dimension>
    <field>energy</field>
    <field>xx</field>
    <field>yy</field>
    <field>zz</field>
    <field>xy</field>
    <field>yz</field>
    <field>zx</field>
    <set> 
     <r>     0.0000     0.0000     0.0000     0.0000     0.0000     0.0000     0.0000 </r>
     <r>     0.4627     0.0000     0.0000     0.0000     0.0000     0.0000     0.0000 </r>
     <r>     0.9250     0.0000     0.0000     0.0000     0.0000     0.0000     0.0000 </r>
     <r>     1.3866     0.0000     0.0000     0.0000     0.0000     0.0000     0.0000 </r>
     <r>     1.8472     0.0000     0.0000     0.0000     0.0000     0.0000     0.0000 </r>
     <r>     2.3065     0.0000     0.0000     0.0000     0.0000     0.0000     0.0000 </r>
        ...   ^          ^          ^          ^          ^          ^          ^   
              |          |          |          |          |          |          |
            energy     eps_xx     eps_yy     esp_zz     esp_xy     eps_yz     eps_xz
```

## Comparison with k-p and density perturbation theory

The calculated microscopic frequency-dependent dielectric function without local field effects is the same function obtained using LOPTICS=*.TRUE.*,
as well as the one obtained from density functional perturbation routines (LEPSILON=*.TRUE.*).
In fact, it is guaranteed that the results are identical to those determined
using a summation over conduction band states (LOPTICS).
Differences for LSPECTRAL=*.FALSE.* must be negligible,
and can be solely related to a different complex shift CSHIFT
(defaults for CSHIFT are different in both routines).
Setting CSHIFT manually in the INCAR file will remedy this issue.
If differences prevail, it might be required to increase NEDOS.
For LSPECTRAL=*.TRUE.*
differences can arise, because

* The GW routine uses fewer frequency points and different frequency grids than the optics routine or

* again from a different complex shift.

Increasing NOMEGA should remove all discrepancies.

## Technical tips

If full GW calculations are not required, it is possible to greatly accelerate
the calculations, by calculating the response functions only
at the $\Gamma$-point. This can be achieved by setting the following values in the INCAR file:

```
 NKREDX = number of k-points in direction of the first lattice vector
 NKREDY = number of k-points in direction of the second lattice vector
 NKREDZ = number of k-points in direction of the third lattice vector
```

The calculation of the QP shifts can be bypassed by setting
ALGO=*CHI*.
Furthermore, if only the static response function is required
the number of frequency points should be set to NOMEGA=1 and
LSPECTRAL=*.FALSE.*

---
