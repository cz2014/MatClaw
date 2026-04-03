# GGA

Categories: INCAR tag, Exchange-correlation functionals

GGA = PE | RP | PS | AM | LIBXC | ...

Default: The functional specified by LEXCH in the POTCAR if METAGGA and XC are also not specified.

Description: Selects a LDA or GGA exchange-correlation functional.

---

> **Important:** VASP recalculates the exchange-correlation energy inside the PAW sphere and corrects the atomic energies given by the POTCAR file. For this to work, the original LEXCH tag must not be modified in the POTCAR file.

> **Mind:**
>
> * When the OR, BO, MK, ML or CX GGA is used in combination with the nonlocal vdW-DF functional of Dion *et al.*, the GGA component of the correlation should in principle be turned off with AGGAC=0 (see nonlocal vdW-DF functionals).
> * The XC tag, available since VASP.6.4.3, can be used to specify any linear combination of LDA, GGA and METAGGA exchange-correlation functionals.

## Available functionals

This table lists the LDA and GGA functionals available in VASP. The names of functionals which end with "\_X" and "\_C" correspond to exchange-only and correlation functionals, respectively.

| GGA= | Type | Description |
| --- | --- | --- |
| LIBXC (or LI) | LDA/GGA | Any LDA or GGA from the external library Libxc. It is necessary to have Libxc >= 5.2.0 installed and VASP.6.3.0 or higher compiled with precompiler options. The LIBXC1 and LIBXC2 tags (where examples are shown) are also required. |
| CA (or PZ)(1) | LDA | Slater exchange + Perdew-Zunger parametrization of Ceperley-Alder Monte Carlo correlation data. |
| PW92(1) | LDA | Slater exchange + Perdew-Wang parametrization of Ceperley-Alder Monte Carlo correlation data. Available since VASP.6.5.0. |
| SL(1) | LDA | Slater exchange only. Available since VASP.6.4.3. |
| CA\_C (or PZ\_C) | LDA | Correlation-only Perdew-Zunger parametrization of Ceperley-Alder Monte Carlo correlation data. Available since VASP.6.4.3. |
| PW92\_C | LDA | Correlation-only Perdew-Wang parametrization of Ceperley-Alder Monte Carlo correlation data. Available since VASP.6.5.0. |
| VW(1) | LDA | Slater exchange + Vosko-Wilk-Nusair correlation (VWN5). |
| HL(1) | LDA | Slater exchange + Hedin-Lundqvist correlation. |
| WI(1) | LDA | Slater exchange + Wigner correlation (Eq. (3.2) in Ref. ). |
| PE | GGA | Perdew-Burke-Ernzerhof (PBE). |
| PBE\_X | GGA | Exchange-only Perdew-Burke-Ernzerhof. Available since VASP.6.4.3. |
| PBE\_C | GGA | Correlation-only Perdew-Burke-Ernzerhof. Available since VASP.6.4.3. |
| RE | GGA | Revised PBE from Zhang and Yang (revPBE). |
| RP | GGA | Revised PBE from Hammer *et al*. (RPBE). |
| PS | GGA | Revised PBE for solids (PBEsol). |
| AM | GGA | Armiento-Mattsson (AM05). |
| 91(1) | GGA | Perdew-Wang (PW91). |
| B3(1) | GGA | B3LYP with VWN3 for LDA correlation. |
| B5(1) | GGA | B3LYP with VWN5 for LDA correlation. |
| OR(2) | GGA | optPBE exchange + PBE correlation. |
| BO(2) | GGA | optB88 exchange + PBE correlation. PARAM1=0.1833333333 for $\beta$ and PARAM2=0.22 for $\mu$ also need to be specified. |
| MK(2) | GGA | optB86b exchange + PBE correlation. The PARAM1 and PARAM2 tags can be used to modify the parameters $\mu$ and $\kappa$, respectively. |
| ML(2) | GGA | PW86R exchange + PBE correlation. |
| CX(2) | GGA | CX (LV-PW86r) exchange + PBE correlation. |
| BF | GGA | BEEF (requires VASP compiled with -Dlibbeef). |

(1) The Slater LDA exchange includes relativistic effects.

(2) The exchange component was designed in particular to be used as the exchange component of Nonlocal vdW-DF functionals and with AGGAC=0 such that only LDA is used for the local correlation, see list of nonlocal vdW-DF functionals.

## Related tags and articles

LIBXC1,
LIBXC2,
ALDAX,
ALDAC,
AGGAX,
AGGAC,
METAGGA,
XC

Examples that use this tag

## References

---
