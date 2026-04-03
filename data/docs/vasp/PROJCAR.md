# PROJCAR

Categories: VASP, Files, Wannier functions

The PROJCAR file contains information about the projections of the Kohn-Sham orbitals onto the localized orbitals specified with the LOCPROJ tag.
This file is built specifically to be human-readable but contains the same information as the LOCPROJ file.

For every localized orbital that is generated, a line is written with the following information:

* ISITE: the index of the site in the POSCAR file.
* R: the position in fractional coordinates.
* Radial type: can be one of "PAW projector","PS partial wave", "Hydrogen-like" depending on the choice of **Pr**, **Ps** or **Hy**, respectively.

Then, for each Kohn-Sham orbital, the k point and spin indexes are reported.
For each band, VASP writes the value of the projection $\langle \beta\_{lm}^{\alpha}|S|\psi\_{n\mathbf{k}}\rangle$ onto the different angular characters of the radial function. To find a list of the possible angular character, go to LOCPROJ and see the table in **<functions-Ylm-specs>**.

## Related Tags and Sections

LOCPROJ

---
