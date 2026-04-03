# WANPROJ

Categories: Files, Input files, Output files, Constrained-random-phase approximation

The WANPROJ file is generated after Wannierization by setting `LWRITE_WANPROJ = True`.
It contains the Wannier transformation matrices, $U\_{mn \mathbf{k}}$, that transform the Kohn-Sham Bloch orbitals into the localized Wannier orbitals.

If WANPROJ is present, VASP skips the Wannierization procedure and reads the transformation matrices from this file instead.

## Format

The file format is logically split into a header section and a section that contains the actual transformation matrix, $U\_{mn \mathbf{k}}$.
On each line of the file, different values are separated by one or more whitespace characters.
There are no empty lines in the WANPROJ file.

### Header

The header section contains the array dimensions of $U\_{mn \mathbf{k}}$ as well as a list of k-points.
It is structured as follows:

* The first line contains a comment
* The second line contains a list of integers
  + ISPIN: number of spin channels (either 1 or 2)
  + NKPTS: number of k-points in the full first Brillouin zone
  + NB\_TOT: number of Kohn-Sham bands
  + NW: number of Wannier orbitals
* The next NKPTS lines contain information about the k-points
  + The first value is an integer and gives the index of the corresponding k-point
  + The second, third and fourth values are the x, y and z coordinates of the k-point expressed in direct coordinates of the reciprocal lattice

### Transformation matrix

The transformation matrix is written as blocks of data.
Each block corresponds to a particular spin channel and a particular k-point.

* The first line in each block contains information about the block
  + The first value is an integer and labels the current spin channel (either 1 or 2)
  + The second value is also an integer and counts the total number of bands that participate in the Wannier transformation at the current k-point (some bands may not participate due to being outside an energy window or being explicitly excluded from the transformation)
  + The third, fourth and fifth values are the x, y and z coordinates of the current k-point expressed in direct coordinates of the reciprocal lattice
* Each subsequent line in the block contains one matrix element of $U\_{mn \mathbf{k}}$
  + The first value is the index $n$ of the Kohn-Sham band
  + The second values is the index $m$ of the Wannier orbital
  + The third and fourth values are the real and imaginary part of the corresponding matrix element

## Related tags and articles

LWANNIER90,
LWANNIER90\_RUN,
LWRITE\_WANPROJ,
LDOWNSAMPLE,
Constructing\_Wannier\_orbitals,
cRPA of SrVO3

---
