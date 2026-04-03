# IVDW

Categories: INCAR tag, Exchange-correlation functionals, Van der Waals functionals

IVDW = 1 | 11 | 12 | 2 | 21 | ...  
 Default: **IVDW** = 0 (no correction)

Description: IVDW specifies a vdW dispersion term of the atom-pairwise or many-body type.

---

## Available vdW atom-pairwise and many-body methods

With all methods listed below, a dispersion correction is added to the total energy, but also to the atomic forces and stress tensor, such that lattice relaxations, molecular dynamics, and vibrational analysis (via finite differences) can be performed. Note, however, that these correction schemes are currently not available for phonon calculations based on density functional perturbation theory.

| IVDW= | Type | Description |
| --- | --- | --- |
| 1 or 10 | pairwise | DFT-D2 method of Grimme. Available as of VASP.5.2.11. |
| 11 | pairwise | DFT-D3 method of Grimme with zero-damping function. Available as of VASP.5.3.4. |
| 12 | pairwise | DFT-D3 method with Becke-Johnson damping function. Available as of VASP.5.3.4. |
| 13 | pairwise | DFT-D4 method. Available as of VASP.6.2 as external package. |
| 3 | pairwise | DFT-ulg method. Available as of VASP.5.3.5. |
| 4 | pairwise | dDsC dispersion correction method. Available as of VASP.5.4.1. |
| 2 or 20 | pairwise | Tkatchenko-Scheffler method. Available as of VASP.5.3.3. |
| 21 | pairwise | Tkatchenko-Scheffler method with iterative Hirshfeld partitioning. Available as of VASP.5.3.5. |
| 202 | many-body | Many-body dispersion energy method (MBD@rsSCS). Available as of VASP.5.4.1. |
| 263 | many-body | Many-body dispersion energy with fractionally ionic model for polarizability method (MBD@rSC/FI). Available as of VASP.6.1.0. |
| 14 | pairwise and many-body | One of the methods available in the Library libMBD of many-body dispersion methods. Available as of VASP.6.4.3 as external package. |

> **Mind:**
>
> * The libMBD implementations (IVDW=14) of the Tkatchenko-Scheffler methods and their MBD extensions are much faster (analytical calculation of the forces) than the VASP implementations (numerical calculation of the forces). Therefore, it is strongly recommended to use the libMBD implementation if available.
> * The parameter LVDW used in previous versions of VASP (5.2.11 and later) to activate the DFT-D2 method is now obsolete. If LVDW=*.TRUE.* is defined, IVDW is automatically set to 1 (unless IVDW is specified in INCAR).

## Related tags and articles

DFT-D2, DFT-D3, DFT-D4,
Tkatchenko-Scheffler method,
Self-consistent screening in Tkatchenko-Scheffler method,
Tkatchenko-Scheffler method with iterative Hirshfeld partitioning,
Many-body dispersion energy,
Many-body dispersion energy with fractionally ionic model for polarizability,
DFT-ulg,
dDsC dispersion correction,
LIBMBD\_METHOD

See also the alternative vdW-DF functionals: LUSE\_VDW, Nonlocal vdW-DF functionals.

Examples that use this tag

---
