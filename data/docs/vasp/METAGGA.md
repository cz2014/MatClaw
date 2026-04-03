# METAGGA

Categories: INCAR tag, Exchange-correlation functionals

METAGGA = SCAN | LIBXC | MBJ | ...

Default: The functional specified by LEXCH in the POTCAR if GGA and XC are also not specified.

Description: Selects a meta-GGA exchange-correlation functional.

---

> **Mind:**
>
> * If you select a meta-GGA functional, make sure that you use  POTCAR files that are suited for meta-GGA functionals. However, note that this requirement does not concern the deorbitalized meta-GGAs, i.e. those that do not depend on the kinetic-energy density, like SCAN-L.
> * Depending on the meta-GGA that is chosen, it may be recommended to use a PAW potential that is more accurate than the standard/recommended one. This is particularly the case with functionals (e.g., MBJ or the Minnesota functionals like M06-L) that are very different from the standard ones like PBE or SCAN. The reason is that for such *special* functionals, using a PAW potential that includes more states in the valence or that is harder may be required to obtain results that are closer to the results that would be obtained with an all-electron code. That also means that it may be a good idea to do test calculations with different PAW potentials.
> * For accuracy, it is strongly recommended to set LASPH=.TRUE. to  account for aspherical contributions to the PAW one-centre terms.
> * Since VASP.6.4.0 it is possible to use hybrid functionals that mix meta-GGA and Hartree-Fock exchange (AEXX). Furthermore, two new tags, AMGGAX and AMGGAC, were created.
> * The XC tag, available since VASP.6.4.3, can be used to specify any linear combination of LDA, GGA and METAGGA exchange-correlation functionals.
> * The results obtained with the meta-GGA functionals that depend on the Laplacian of the density $\nabla^2n$ (e.g., SCAN-L) may not be reliable for large values of the energy cutoff ENCUT due to numerical instability. According to some tests, it is not recommended to use values of ENCUT above 800 eV.

## Available functionals

This table lists the meta-GGA functionals available in VASP. There are essentially two types of meta-GGAs, that differ in the variable on which they depend (in addition to $n$ and $\nabla n$): the kinetic-energy density $\tau$ or the Laplacian of the density $\nabla^2n$. The names of functionals which end with "\_X" and "\_C" correspond to exchange-only and correlation functionals, respectively. Note that the implementation of $\tau$-dependent meta-GGA functionals is described in .

| METAGGA= | Variable | Description |
| --- | --- | --- |
| LIBXC |  | Any MGGA from the external library Libxc. It is necessary to have Libxc >= 5.2.0 installed and VASP.6.3.0 or higher compiled with precompiler options. The LIBXC1 and LIBXC2 tags (where examples are shown) are also required. |
| TPSS, TPSS\_X or TPSS\_C(1) | $\tau$ | TPSS. |
| RTPSS, RTPSS\_X or RTPSS\_C(1) | $\tau$ | revTPSS is a revised version of TPSS. |
| M06L, M06L\_X or M06L\_C(1) | $\tau$ | M06-L. |
| MS0, MS0\_X or MS0\_C(1) | $\tau$ | MS0 corresponds to $\kappa=0.29$, $c=0.28771$ and $b=1.0$. Note that the correlation component, called vPBEc or regTPSS in the literature, is a GGA. Available since VASP.5.4.1. |
| MS1, MS1\_X or MS1\_C(1) | $\tau$ | MS1 corresponds to $\kappa=0.404$, $c=0.18150$ and $b=1.0$. Note that the correlation component, called vPBEc or regTPSS in the literature, is a GGA. Available since VASP.5.4.1. |
| MS2, MS2\_X or MS2\_C(1) | $\tau$ | MS2 corresponds to $\kappa=0.504$, $c=0.14601$ and $b=4.0$. Note that the correlation component, called vPBEc or regTPSS in the literature, is a GGA. Available since VASP.5.4.1. |
| SCAN, SCAN\_X or SCAN\_C(1) | $\tau$ | SCAN. May possibly lead to numerical instabilities. rSCAN or r$^{2}$SCAN are more stable and should give similar results. Available since VASP.5.4.4. |
| RSCAN, RSCAN\_X or RSCAN\_C(1) | $\tau$ | rSCAN is a regularized version of SCAN that is numerically more stable. |
| R2SCAN, R2SCAN\_X or R2SCAN\_C(1) | $\tau$ | r$^{2}$SCAN is a regularized version of SCAN that is numerically more stable. Available since VASP.6.2.0, or in version 5.4.4 by patch 4. |
| SREGTM1, SREGTM2 or SREGTM3 | $\tau$ | sregTM versions 1, 2 or 3 of a regularized Tao-Mo functional. Available since VASP.6.4.3. |
| TASK\_X(2) | $\tau$ | TASK exchange. Available since VASP.6.5.0. |
| LAK, LAK\_X or LAK\_C | $\tau$ | LAK. Available since VASP.6.5.0. |
| MSPBEL, MSRPBEL or MSB86BL | $\tau$ | MS-PBEl, MS-RPBEl or MS-B86bl. Available since VASP.6.5.0. |
| RMSPBEL, RMSRPBEL or RMSB86BL | $\tau$ | rMS-PBEl, rMS-RPBEl or rMS-B86bl. Available since VASP.6.5.0. |
| SCANL | $\nabla^2n$ | SCAN-L is a deorbitalized version of SCAN. Available since VASP.6.4.0. |
| RSCANL | $\nabla^2n$ | rSCAN-L is a deorbitalized version of rSCAN. Available since VASP.6.4.0. |
| R2SCANL | $\nabla^2n$ | r$^2$SCAN-L is a deorbitalized versions of r$^2$SCAN. Available since VASP.6.4.0. |
| OFR2 | $\nabla^2n$ | Orbital-free regularized-restored SCAN (OFR2). Available since VASP.6.4.0. |
| SREGTM2L | $\nabla^2n$ | v2-sregTM-L is a deorbitalized versions of v2-sregTM. Available since VASP.6.4.0. |
| MBJ(3) | $\nabla^2n,\tau$ | Modified Becke-Johnson potential. The CMBJA, CMBJB and CMBJE tags correspond to $\alpha$, $\beta$ and the power $e=1/2$ (that can be modified) in Eq. (3) of Ref. , respectively. The default values are $\alpha=-0.012$, $\beta=1.023$ bohr$^{1/2}$ and $e=1/2$. |
| LMBJ(3) | $\nabla^2n,\tau$ | The local MBJ (LMBJ) potential. The CMBJA, CMBJB, CMBJE, SMBJ, and RSMBJ tags correspond to $\alpha$, $\beta$, the power $e=1$ (that can be modified) of $\bar{g}$, $\sigma$ and $r\_{s}^{\mathrm{th}}$ in Eqs. (5)-(7) of Ref. , respectively. The default values are (see erratum of Ref. ) $\alpha=0.488$, $\beta=0.5$ bohr, $e=1$, $\sigma=2$ $\AA$ ($=3.78$ bohr), and $r\_{s}^{\mathrm{th}}=7$ bohr (which corresponds to $n\_{\mathrm{th}}=6.96\times10^{-4}$ e/bohr$^{3}$). |

(1) The exchange-only and correlation-only implementations are available since VASP.6.4.3.

(2) In Ref. TASK exchange is combined with LDA-PW92 correlation. This can be done with XC=TASK\_X PW92\_C in INCAR.

(3) A few points about the MBJ and LMBJ potentials:

:   * These are *potential-only* methods, *i.e.*, there is no corresponding exchange-correlation energy $E\_{xc}$. The used expression for $E\_{xc}$ is LDA, which is an arbitrary choice. This means that MBJ and LMBJ calculations can never be self-consistent with respect to the total energy, and thus we cannot compute Hellmann-Feynman forces (*i.e.*, no ionic relaxation, etc.). Actually, these potentials aim solely at a description of the electronic properties, primarily the band gap, or magnetic moments.
    * MBJ and LMBJ calculations may converge very slowly, so the number of maximum electronic steps (NELM) should be set higher than usual.
    * In the presence of an extended vacuum region (e.g., surfaces) or an interface, the average of $|\nabla n|/n$ has no meaning. Therefore, MBJ calculations should be done with a fixed value of $c$, which can be done with the CMBJ tag., or alternatively with the LMBJ that was proposed for the purpose to be applicable to systems with vacuum or interfaces.

## POTCAR files: required information

Calculations with a meta-GGA that depends on the kinetic-energy density require POTCAR files that include information on the kinetic-energy density of the core electrons. Almost all recent POTCAR files do fulfill this requirement, but there are some notable exceptions like O\_GW. To check whether a particular POTCAR contains this information, type:

```
grep kinetic POTCAR
```

This should yield at least the following lines (for each element on the file):

```
kinetic energy-density
mkinetic energy-density pseudized
```

and for PAW datasets with partial core corrections:

```
kinetic energy density (partial)
```

> **Mind:** For POTCAR files without core electrons (H, He, Li\_sv, Be\_sv, and \_GW variants thereof) the `grep` command given above will not return the line about pseudized kinetic energy-density, since all electrons are considered as valence. These potentials can nevertheless be used for all meta-GGA functionals.

## Aspherical contributions related to one-center terms

LASPH =.TRUE. should be selected if a meta-GGA functional is selected. If LASPH =.FALSE.,
the one-center contributions are only calculated for a spherically averaged density and kinetic-energy
density. This means that the one-center contributions to the Kohn-Sham potential are also spherical.
Since the PAW method describes the entire space using plane waves, errors are often small even
if the non-spherical contributions to the Kohn-Sham potential are neglected inside the PAW spheres
(additive augmentation, as opposed to the APW or FLAPW method where the plane wave contribution only
describes the interstitial region between the atoms). Anyhow, if the density is strongly non-spherical
around some atoms in your structure, LASPH =.TRUE. must be selected. Non-spherical terms are particularly encountered
in d- and f-elements, dimers, molecules, and solids with strong directional bonds.

## Convergence issues

If convergence problems are encountered, it is recommended to preconverge the
calculations using the PBE functional and start the calculation from the WAVECAR file corresponding to the PBE ground state. Furthermore,
ALGO = A (conjugate gradient algorithm for orbitals) is often more stable
than charge density mixing, in particular if the system contains vacuum regions.

## Related tags and articles

LIBXC1,
LIBXC2,
GGA,
XC,
CMBJ,
CMBJA,
CMBJB,
CMBJE,
SMBJ,
RSMBJ,
LASPH,
LMAXTAU,
LMIXTAU,
LASPH,
AMGGAX,
AMGGAC,
Band-structure calculation using meta-GGA functionals

Examples that use this tag

## References

---
