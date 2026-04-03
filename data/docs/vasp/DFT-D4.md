# DFT-D4

Categories: Exchange-correlation functionals, Van der Waals functionals, Howto

DFT-D4 is an external package maintained by the Grimme group that can be linked to VASP.
Read the documentation for more information about this package.
DFT-D4 adds van-der-Waals (vdW) interactions to DFT because they are not included in most exchange-correlation functionals.
It approximates the vdW interactions considering only the structure of the system which allows for a fast computation.
Since every functional has different interactions between atoms, DFT-D4 tailors its adjustable parameters to the functional.

For more information regarding these parameters, please refer to the DFT-D4 paper.

## Usage

In most cases, it is sufficient to set IVDW=13 in the INCAR file if VASP was compiled and linked to DFT-D4.
Internally, VASP passes the name of the used exchange-correlation functional to DFT-D4.
Subsequently, DFT-D4 maps this name of the functional to optimized settings for the adjustable parameters of the vdW interaction.
VASP uses these parameters to compute the DFT-D4 energies, forces, and stresses in every ionic step and adds them to the corresponding DFT terms.
As a result, you can relax structures or run MD simulations with an approximate treatment of vdW interactions.

> **Warning:** Below, we explain how to tweak the parameters of DFT-D4. Typically, you should not modify them unless you have a very good reason, e.g., because the interface is not implemented for the exchange-correlation functional you use.

VASP allows setting the following tags in the INCAR file to change the strength of the vdW interaction.

* VDW\_S6, VDW\_S8 determine the strength of the dipole-dipole and dipole-quadrupole interaction.
* VDW\_A1, VDW\_A2 are scaling constants in the Becke-Johnson damping.

## References

## Related tags and articles

IVDW,
VDW\_S6,
VDW\_S8,
VDW\_A1,
VDW\_A2,
DFT-D3,
Linking to DFT-D4
