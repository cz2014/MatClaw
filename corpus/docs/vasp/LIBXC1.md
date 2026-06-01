# LIBXC1

Categories: INCAR tag, Exchange-correlation functionals, Hybrid functionals

LIBXC1 = [string] or [integer]

Description: LIBXC1 specifies the exchange or exchange-correlation functional from the library of exchange-correlation functionals Libxc.

---

> **Important:** This feature is available from VASP.6.3.0 onwards that needs to be compiled with -DUSELIBXC.

LIBXC1 and LIBXC2 can be set to a label (string) or number (integer) associated with a functional listed on the Libxc website, e.g., `GGA_X_PBE` and `101` for PBE exchange. The label indicates if this is an exchange (X), correlation (C), or exchange-correlation (XC) functional, and which family it belongs to, namely LDA (LDA or HYB\_LDA), GGA (GGA or HYB\_GGA) or meta-GGA (MGGA or HYB\_MGGA). If LIBXC1 corresponds to an exchange functional, then it can be used in combination with LIBXC2 for the correlation functional.

Libxc is a separate library package that has to be downloaded and compiled before VASP is compiled with the corresponding precompiler options and links to the libraries.

Calculations with Laplacian-dependent meta-GGA functionals and meta-GGA-based hybrid functionals are possible since VASP.6.4.0.

> **Important:** To get correct results with meta-GGA functionals (see discussion at LTBOUNDLIBXC), it is necessary to use Libxc from version 5.2.0 onwards (or the master version for the latest implemented functionals) and to compile it with the option `--disable-fhc`.

## How to

The allowed possibilities for LIBXC1 and LIBXC2 are the following:

* Both LIBXC1  and LIBXC2 are specified and correspond to exchange and correlation functionals, respectively.
* Only LIBXC1  is specified and corresponds to an exchange or exchange-correlation functional.

:   > **Warning:** If LIBXC1  is an exchange-correlation functional, then LIBXC2  can not be used.

* LIBXC1  and LIBXC2 can correspond to functionals of different families, e.g., a meta-GGA and a GGA, respectively.

Regarding other tags in INCAR related to Libxc:

* One also has to specify GGA = LIBXC for LDA, GGA and GGA-based hybrid functionals or METAGGA = LIBXC for meta-GGA functionals and meta-GGA-based hybrid functionals. Note that if one of the tags (LIBXC1  or LIBXC2 ) corresponds to a meta-GGA, while the other corresponds to a GGA or LDA, then METAGGA = LIBXC (and not GGA = LIBXC) has to be specified.
* Many of the functionals implemented in Libxc have parameters that can be modified. This can be done via the tags LIBXC1\_Pn and LIBXC2\_Pn, where $n=1, 2, \ldots$.
* The tag LTBOUNDLIBXC, which is .FALSE. by default, allows to enforce the lower bound on the kinetic-energy density ($\tau\_{\sigma}^{\mathrm{W}}\lt \tau\_{\sigma}$) with $\tau\_{\sigma}=\max(\tau\_{\sigma},\tau\_{\sigma}^{\mathrm{W}})$ before $\tau\_{\sigma}$ is used in a meta-GGA functional from Libxc.

For calculations with hybrid functionals (LHFCALC=True), the following provides some explanations:

* The Libxc functionals whose tag starts with HYB already include the mixing parameter. Therefore, for them, the ALDAX, ALDAC, AGGAX, AGGAC, AMGGAX, and AMGGAC tags can not be used (more information on how to modify the mixing and screening parameters can be found at LIBXC1\_Pn). However, it is still necessary to set AEXX at the proper value.
* If the semilocal component of the hybrid functional is constructed using Libxc functionals that do not contain HYB in the tag, then ALDAX, AGGAX, ALDAC, and AGGAC will be used and multiply

:   $$E\_{\mathrm{x}}^{\mathrm{LDA}}=\int\epsilon\_{\mathrm{x}}^{\mathrm{LDA}}(n)d^{3}r$$
:   $$\Delta E\_{\mathrm{x}}^{\mathrm{GGA}}=\int\left(\epsilon\_{\mathrm{x}}^{\mathrm{GGA}}(n,\nabla n) - \epsilon\_{\mathrm{x}}^{\mathrm{LDA}}(n)\right)d^{3}r$$
:   $$E\_{\mathrm{c}}^{\mathrm{LDA}}=\int\epsilon\_{\mathrm{c}}^{\mathrm{LDA}}(n)d^{3}r$$
:   $$\Delta E\_{\mathrm{c}}^{\mathrm{GGA}}=\int\left(\epsilon\_{\mathrm{c}}^{\mathrm{GGA}}(n,\nabla n) - \epsilon\_{\mathrm{c}}^{\mathrm{LDA}}(n)\right)d^{3}r$$
:   respectively, where $\epsilon\_{\mathrm{x}}^{\mathrm{LDA}}(n)=-\left(3/4\right)\left(3/\pi\right)^{1/3}n^{4/3}$ and $\epsilon\_{\mathrm{c}}^{\mathrm{LDA}}(n)=\epsilon\_{\mathrm{c}}^{\mathrm{GGA}}(n,\nabla n=0)$.

## Examples of INCAR

* PBE

```
GGA = LIBXC
LIBXC1 = GGA_X_PBE # or 101
LIBXC2 = GGA_C_PBE # or 130
```

* SCAN

```
METAGGA = LIBXC
LIBXC1 = MGGA_X_SCAN # or 263
LIBXC2 = MGGA_C_SCAN # or 267
```

* PBEh (PBE0)

```
LHFCALC = .TRUE.
AEXX = 0.25
GGA = LIBXC
LIBXC1 = HYB_GGA_XC_PBEH # or 406
```

* SCAN0

```
LHFCALC = .TRUE.
AEXX = 0.25
METAGGA = LIBXC
LIBXC1 = MGGA_X_SCAN # or 263
LIBXC2 = MGGA_C_SCAN # or 267
```

## Related tags and articles

LIBXC2,
LIBXC1\_Pn,
LIBXC2\_Pn,
LTBOUNDLIBXC,
GGA,
METAGGA,
LHFCALC,
AEXX,
ALDAX,
ALDAC,
AGGAX,
AGGAC,
AMGGAX,
AMGGAC,
List of hybrid functionals

Examples that use this tag

## References

---
