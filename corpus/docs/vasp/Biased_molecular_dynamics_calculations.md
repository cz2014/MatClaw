# Biased molecular dynamics calculations

Categories: Advanced molecular-dynamics sampling, Howto

## How to

* First one needs to setup a standard molecular dynamics run. The bias potentials are supported in both the NVT and NpT MD simulations, regardless of the particular thermostat and/or barostat setting.

:   > **Mind:** Mind that for VASP 5.x the biased molecular dynamics runs have to be chosen by adding 10 to the chosen value of MDALGO. E.g. MDALGO=12 instead of MDALGO=2 has to be chosen for Nose-Hoover thermostat.

* Then one needs to set the geometric parameters and bias potential types. The geometric parameters ξ, also called collective variables, that are controlled via the potentials are defined in the ICONST file. The type of bias potential is also set in this file. The format of this file follows this layout:

```
flag item(1) ... item(N) status
```

Here `flag` specifies the type of geometric parameters (bond lengths, angles, etc.), `item(1) ... item(N)` the actual geometric items (atom numbers, etc.) and the `status` sets the type of used bias potential. Here we advise the user to also look into the description of the full capabilities of the geometric parameters.

* To avoid the update of the bias potential HILLS\_BIN=NSW is set by default.
* Next one needs to set the parameters of the potential in the INCAR (harmonic and step function) file or in the PENALTYPOT file (Gaussian). The following table summarizes the available potentials with their corresponding parameters:

:   |  |  |  |
    | --- | --- | --- |
    | Potential type | `status` in ICONST | INCAR parameters |
    | Harmonic potential | 8 | SPRING\_K, SPRING\_R0, optional SPRING\_V0 |
    | Step function | 4 | FBIAS\_A, FBIAS\_D, and FBIAS\_R0 |
    | Gaussian potential | 5 | parameters set in PENALTYPOT file |

### Available potentials

Fig.1) Graphical representation of (a) harmonic, (b) Fermi function-shaped, and (c) and Gauss function-shaped bias potentials.

In the following details are given on how to control the available bias potentials in VASP that are plotted in Fig.1.

#### Harmonic potentials

:   A sum of Harmonic potentials (curve (a) in Fig.1)

    :   $$\tilde{V}(\xi\_1,\dots,\xi\_{M\_8}) = \sum\_{\mu=1}^{M}\frac{1}{2}\kappa\_{\mu} (\xi\_{\mu}(q)-\xi\_{0\mu})^2 \;$$
:   where the sum runs over all ($M\_8$) coordinates the potential acts upon. The potential is chosen in the ICONST file by setting the `status` to 8. The parameters of the potential are the force constant $\kappa\_{\mu}$ (SPRING\_K) and the minimum or the potential $\xi\_{0\mu}$ SPRING\_R0. These must be set in the INCAR file. Optionally, it is possible to change the value of $\xi\_{0\mu}$ every MD step at a constant rate defined via the INCAR tag SPRING\_V0.

:   > **Mind:** The number of items defined via SPRING\_K, SPRING\_R0, and SPRING\_V0 must be equal to $M\_8$. Otherwise, the calculation terminates with an error message.

:   This form of bias potential is employed in several simulation protocols, such as the umbrella sampling, umbrella integration, or steered MD, and is useful also in cases where the $\xi\_{\mu}$ values need to be restrained.

#### Step function

:   A sum of Fermi-like step functions (curve (b) in Fig.1)

    :   $$\tilde{V}(\xi\_1,\dots,\xi\_{M\_4}) = \sum\_{\mu=1}^{M\_4}\frac{A\_{\mu}}{1+\text{exp}\left [-D\_{\mu}(\frac{\xi(q)}{\xi\_{0\mu}} -1) \right ]} \;$$
:   where the sum runs over all ($M\_4$) coordinates the potential acts upon. The potential is chosen in the ICONST file by setting the `status` to 4. The parameters of the potential are the height of the step ($A\_{\mu}$ set by FBIAS\_A), the slope around the point $\xi\_{0\mu}$ ($D\_{\mu}$ set by FBIAS\_D), and the position of the step ($\xi\_{0\mu}$ set by FBIAS\_R0). These must be set in the INCAR file.

:   > **Mind:** The number of items defined via FBIAS\_A, FBIAS\_D, and FBIAS\_R0 must be equal to $M\_4$. Otherwise, the calculation terminates with an error message.

:   This form of potential is suitable especially for imposing restrictions on the upper (or lower) limit of the value of $\xi$.

#### Gaussian potential

:   A sum of Gauss functions (curve (b) in Fig.1)

    :   $$\tilde{V}(\xi\_1,\dots,\xi\_{M}) = \sum\_{\nu=1}^{N\_5}h\_{\nu}\text{exp}\left [-\frac{\sum\_{\mu=1}^{M\_5}(\xi\_{\mu}(q)-\xi\_{0\nu,\mu})^2}{2w\_{\nu}^2} \right ], \;$$
:   where $N\_5$ is the number of Gaussian functions and $M\_5$ is the number of coordinates the potential acts upon. The potential is chosen in the ICONST file by setting the `status` to 5. The parameters of the potentials, $h\_{\nu}$, $w\_{\nu}$, and $\xi\_{0\nu,\mu}$ are defined in the PENALTYPOT file.

:   This type of bias potential is primarily intended for use in metadynamics, but since Gaussians can be used as basis functions for more general shapes, they can also be used to prepare various atypically shaped bias potentials.

### Output

:   The values of all collective variables defined in the ICONST file for each MD step are listed in the REPORT file. Check the lines after the string Metadynamics.

## Examples of usage

Let us consider the nucleophile substitution reaction of CH$\_3$Cl with Cl$^-$. The reactant is a weak van-der-Waals complex. The corresponding POSCAR file reads

```
vdW complex CH3Cl...Cl 
1.00000000000000
12.0000000000000000    0.0000000000000000    0.0000000000000000
0.0000000000000000    12.0000000000000000    0.0000000000000000
0.0000000000000000    0.0000000000000000    12.0000000000000000
C H Cl
1 3 2
cart
5.91331371  7.11364924  5.78037960
5.81982231  8.15982106  5.46969017
4.92222130  6.65954232  5.88978969
6.47810398  7.03808479  6.71586385
4.32824726  8.75151396  7.80743202
6.84157897  6.18713289  4.46842049
```

Due to the weak interactions between CH$\_3$Cl and Cl$^-$, the complex can collapse at high temperatures. This can be avoided by setting an upper bound for the length of the non-bonding Cl...C interactions.
This can be conveniently achieved by using a Fermi-like step-shaped bias potential. To this end, we need to define the Cl...C distance, i.e., the distance between the atoms 1 and 5, as a coordinate with status 4 in the ICONST file:

```
R 1 5 4
```

Next, we need to set the molecular dynamics parameters and specify the bias potential parameters FBIAS\_A, FBIAS\_D, and FBIAS\_R0 in the INCAR file:

```
# Molecular dynamics part
IBRION = 0
TEBEG = 300
TEEND = 300
MDALGO = 2
POTIM = 2.0
NSW = 10000
# Bias potential part
FBIAS_A  = 1
FBIAS_D  = 50
FBIAS_R0 = 3.5
```

Since the bias potential acts only on one internal coordinate ($M\_4=1$), we need to provide only one number for each of the tags. The chosen bias potential parameters
ensure that repulsive bias forces steeply increase when the C...Cl distance is increased beyond about $3.2 \AA$. This causes a shortening of the distance in the next MD step. Notice that the bias force is essentially negligible for distances below $3 \AA$.
A careful adjustment of FBIAS\_A and FBIAS\_D is needed to ensure that (i) the bias force is large enough to effectively limit the value of $\xi$, and (ii) the interval of $\xi$ values for which the bias forces are significant is broad enough to avoid overcoming via random fluctuations.
A suitable setting can be found by noting that the maximal bias force of $\frac{D\,A}{4\xi\_0}$ is exerted on the system at the point $\xi = \xi\_{0}$. This can be seen by inspecting the analytical expression for the potential.

## Related methods in VASP

* Metadynamics: In contrast to the methods discussed on this page metadynamics continuously updates the bias potential of the system to push it into unvisited parts of phase space.

* Interface pinning: This employs a bias potential to pin the state of an interface between a solid and a liquid. This method uses entirely different INCAR tags than the bias potentials presented on this page.

## References
