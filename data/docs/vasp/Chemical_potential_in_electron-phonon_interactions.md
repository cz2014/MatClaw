# Chemical potential in electron-phonon interactions

Categories: Theory, Electron-phonon interactions

The chemical potential $\mu$ (we also use $\eta$ when its meaning can be confused with mobility) is the energy that can be released that due to a change in particle number. Its accurate determination is a key ingredient in the computation of electronic transport coefficients such as electrical conductivity, carrier mobility, and thermopower. These quantities depend sensitively on the occupation of electronic states near the Fermi level, since only states within a few *kBT* of the Fermi energy contribute significantly to transport.
We employ the frozen-band approximation, which assumes that the electronic potential and eigenvalues computed for the undoped system remain unchanged when electrons are added or removed.

Because the occupation of states is governed by the Fermi–Dirac distribution, an accurate evaluation of the chemical potential as a function of temperature and doping is essential. Even small inaccuracies in $\mu$ can lead to large errors in transport properties.

## Definition

At finite temperature, the chemical potential $\mu$ is defined by requiring that the total number of electrons *Ne* equals the number of occupied states:

$N\_e = \frac{1}{N\_\mathbf{k}} \sum\_{n\mathbf{k}} f(\varepsilon\_{n\mathbf{k}}, T, \mu)$

where:

$N\_\mathbf{k}$ is the total number of k-points used to sample the Brillouin zone,

$\varepsilon\_{n\mathbf{k}}$ are the electronic eigenvalues,

$f(\varepsilon, T, \mu) = \frac{1}{e^{\frac{\varepsilon - \mu}{k\_\mathrm{B} T}} + 1}$ is the Fermi–Dirac occupation function

This equation implicitly defines $\mu(T)$ for a given total number of electrons $N\_e$.

## Carrier density and doping

In doped or non-stoichiometric systems, the total number of electrons includes additional carriers introduced by doping. The number of carriers per unit cell (or per simulation cell) is given by:

$N\_\text{carriers} = \frac{1}{N\_\mathbf{k}} \sum\_{n\mathbf{k}} \left[ f(\varepsilon\_{n\mathbf{k}}, T, \mu) - f(\varepsilon\_{n\mathbf{k}}, T, \mu\_0) \right]$

where *μ0* is the chemical potential of the neutral (undoped) system.
Positive *Ncarriers* corresponds to n-type doping (extra electrons), while negative *Ncarriers* corresponds to p-type doping (holes).

The carrier concentration (number of carriers per unit volume) is then:

$n\_e = \frac{N\_e + N\_\text{carriers}}{\Omega}$

where *Ω* is the unit cell or supercell volume.

Alternatively, if the target carrier concentration *ne* is known, the chemical potential can be determined by inverting:

$n\_e = \frac{1}{\Omega N\_\mathbf{k}} \sum\_{n\mathbf{k}} f(\varepsilon\_{n\mathbf{k}}, T, \mu)$

This relation links the chemical potential directly to the carrier density at a given temperature, serving as the foundation for transport coefficient calculations.

## Why the chemical potential matters

At zero temperature in an undoped system, the chemical potential coincides with the Fermi energy. However, in real materials and realistic conditions:

* The system may be doped, i.e., it contains additional electrons or holes.
* The system may be at finite temperature, which modifies the balance between electron and hole occupations.
* The transport coefficients are dominated by states within a narrow energy window around the chemical potential, so even small inaccuracies can lead to large errors.

Thus, in any calculation of electron–phonon interaction and related transport properties, it is crucial to have a consistent way of specifying and determining the chemical potential.

## Different ways to specify carriers

There are several equivalent, but practically distinct, ways of describing the carrier concentration in a solid. Each corresponds to a different way of constraining or shifting the chemical potential in the calculation:

Shift of the chemical potential
:   One can directly specify a shift of the chemical potential with respect to the undoped zero-temperature Fermi energy. This approach is straightforward when the doping is weak and the Fermi level remains inside the same band. This is can be set with the ELPH\_SELFEN\_MU tag. A range can also be supplied using ELPH\_SELFEN\_MU\_RANGE.

Carrier density
:   Alternatively, one can specify the additional carrier density (per volume). This is the natural way to connect with experimental conditions, where doping levels are often given as carrier densities (e.g. 1018 cm-3). The calculation must then solve self-consistently for the chemical potential that yields the specified carrier density. This is can be set with the ELPH\_SELFEN\_CARRIER\_DEN tag. A range can also be supplied using ELPH\_SELFEN\_CARRIER\_DEN\_RANGE.

Extra carriers per unit cell
:   Finally, one may work in terms of the number of additional carriers per unit cell. This is a natural choice in periodic first-principles calculations, where the fundamental unit is the primitive cell. Again, a self-consistent procedure determines the chemical potential consistent with the requested number of carriers. This is can be set with the ELPH\_SELFEN\_CARRIER\_PER\_CELL tag.

Each of these perspectives can be translated into the others, but depending on the context, one choice may be more convenient. For example, experiments usually quote carrier density, while theoretical band-structure calculations naturally yield the relation between chemical potential and extra carriers per cell.

## Related tags and articles

* Transport calculations
* Electron-phonon accumulators
* Electronic transport coefficients
* ELPH\_RUN
* ELPH\_SELFEN\_CARRIER\_DEN
* ELPH\_SELFEN\_CARRIER\_DEN\_RANGE
* ELPH\_SELFEN\_CARRIER\_PER\_CELL
* ELPH\_SELFEN\_TEMPS
* ELPH\_SELFEN\_TEMPS\_RANGE
* ELPH\_SELFEN\_MU
* ELPH\_SELFEN\_MU\_RANGE
* EFERMI
