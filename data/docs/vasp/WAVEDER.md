# WAVEDER

Categories: Files, Input files, Output files, Dielectric properties

The WAVEDER binary file is written when LOPTICS = True  is set in the INCAR file. It contains the derivative of the Kohn-Sham orbitals with respect to the Bloch vector **k**, written in units of $\AA$. More precisely, it contains the following matrix

:   $$\braket{\tilde u\_{n'\mathbf{k}s} | \tilde u\_{n\mathbf{k}+k\_i s} }= \langle \tilde\psi\_{n'\mathbf k s} |{\bf S} | \frac{\partial \tilde\psi\_{n\mathbf k s}}{\partial k\_i}\rangle = \frac{1}{\epsilon\_{n\mathbf k s} -\epsilon\_{n'\mathbf k s}} \langle \tilde\psi\_{n'\mathbf k s} | \frac{\partial (\mathbf{ H} - \epsilon\_{n\mathbf k s} \mathbf{S})}{\partial k\_i} | \tilde\psi\_{n\mathbf k s} \rangle,$$

where $\ket{\tilde u\_{n\mathbf{k}s}}$ is the cell periodic part of the pseudo-wave function, $\ket{\tilde\psi\_{n\mathbf k s}}$.

These matrix elements correspond to the dipole moment between the states $\tilde\psi\_{n'\mathbf k s}$ and $\tilde\psi\_{n\mathbf k s}$, which are important in the context of dielectric properties. They serve as input for GW and Bethe-Salpeter calculations, as well as the time-evolution algorithm.

In the case of degenerate states, the matrix elements are set to zero, within numerical accuracy.

> **Important:** Please note that only the matrix elements where $n$ or $n'$ correspond to a pair of an occupied and an unoccupied state are calculated and written to the WAVEDER file. Matrix elements involving both occupied or both unoccupied states are not computed.

To include more empty states in the calculation, set the NBANDS tag in the INCAR file to a larger value with respect to the default. The default value of NBANDS can be obtained with a VASP  a dry run. Setting NBANDS is generally recommended for LOPTICS = True , since the dielectric function is computed using a summation over empty states (see the page for LOPTICS for more information).

## Format

The header of the WAVEDER file contains the following information:

* Total number of bands (NBANDS), number of bands used in evaluation of matrix elements, number of k-points, number of spin channels (1 for unpolarised or non-collinear calculations, 2 for polarised calculations).
* Frequency node of the real part of the dielectric function, i.e. the solution for $\Re[\epsilon(\omega)] = 0$.
* Plasmon frequency.

They are then followed by the matrix elements $\braket{\tilde\psi\_{n'\mathbf k} |{\bf S} | \frac{\partial \tilde\psi\_{n\mathbf k}}{\partial k\_i}}$. This is stored in an five-indexed array, with the indices' order being $(n',n,\mathbf k, i)$, where $i=1,2,3$ for the Cartesian direction. The maximum value of each index is defined in the file header, as mentioned above. For collinear spin-polarized calculations (`ISPIN = 2`) the $\uparrow\uparrow$ and $\downarrow\downarrow$ matrix elements are computed. For noncollienar magnetic calculations (`LNONCOLLINEAR = True`) the KS orrbitals are stored as spinors and the $\uparrow\uparrow$, $\uparrow\downarrow$, $\downarrow\uparrow$ and $\downarrow\downarrow$ components are computed.

## Usage

If the WAVEDER file is read successfully, it can be used as a starting point in the following types of calculations:

* GW calculations
* BSE calculations
* Time evolution

The information on the number of bands, k-points, and spin channels is used by VASP in subsequent calculations to check for compatibility between runs. If these parameters are different between different runs, the matrix elements inside the WAVEDER file are not read. A warning will then be printed to the standard output reporting that the WAVEDER file is incompatible with the present calculation and advising to run the previous step (i.e., the calculation where LOPTICS = TRUE ).

Information on the frequency node of the real part of the dielectric function is used in defining the frequency grid for GW calculations and the time-evolution algorithm, while the plasmon frequency is used for computing the Drude-term contribution to the dielectric function. This term used in GW calculations to include the intra-band contribution to the dielectric function.

## Related tags and sections

LOPTICS, GW calculations, BSE calculations, Time-evolution algorithm

---
