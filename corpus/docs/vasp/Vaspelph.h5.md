# vaspelph.h5

Categories: Files, Output files, Electron-phonon interactions

The vaspelph.h5 file contains electron-phonon matrix elements and related quantities.
It is created when `ELPH_DRIVER = mels`.

> **Important:** Within the  projector-augmented-wave method, different definitions of the electron-phonon matrix element exist. In order to choose which one is used and written to vaspelph.h5, please use the ELPH\_DECOMPOSE tag.

> **Mind:** Available as of VASP 6.5.0

It is usually best to avoid writing the electron-phonon matrix elements to disk.
There are several reasons for this:

* The total number of matrix elements required for a particular electron-phonon calculation can be very large, thus requiring a lot of disk space.
* Writing to or reading from the hard drive is usually much slower than keeping data in memory. This can cause a performance bottleneck in your calculation. This is especially true on distributed clusters where additional communication is required.
* When running electron-phonon calculations directly inside VASP, it is possible to avoid calculating some matrix elements. For example, during  transport calculations, only the matrix elements close to the chemical potential have sizeable contributions. The ones further away are not calculated by default, which can give a significant performance boost. This advantage is lost when choosing to write the matrix elements to disk.

However, the information in the vaspelph.h5 file is still useful in some situations.
For example, `ELPH_DRIVER = mels` can be used to plot the electron-phonon matrix along high-symmetry lines or for specific combinations of bands, modes and k/q-points.

## File Layout

This section describes the structure of the HDF5 file used to store electron-phonon matrix elements, electronic eigenvalues, phonon frequencies, and associated metadata (e.g., array sizes, k-point information).
The file is organized into two main groups: **kpoints** and **matrix\_elements**.

* **/kpoints**: Contains data related to the k-point grids, symmetry operations, and mapping between the full Brillouin zone (FBZ) and the irreducible Brillouin zone (IBZ).
* **/matrix\_elements**: Contains information on the electron-phonon interaction, including electron eigenvalues, phonon frequencies, matrix elements, and system dimensions (number of atoms, bands, k-points, spins).

Each group is described in detail below.

### Group: /kpoints

This group contains datasets related to the k-point grid and symmetry mapping.

#### Datasets

nrotk
:   *Shape:* Scalar
:   *Description:* Total number of symmetry operations in **igrpop**.

igrpop
:   *Shape:* {nrotk, 3, 3}
:   *Description:* Stores symmetry operation matrices. Each $3 \times 3$ matrix is associated with one symmetry operation.

indx\_fbz2ibz
:   *Shape:* {nkpts\_kp}
:   *Description:* Maps k-points from the FBZ to the IBZ.

irot\_fbz2ibz
:   *Shape:* {nkpts\_kp}
:   *Description:* Stores the index to the symmetry operation in **igrpop** associated with each FBZ k-point that maps to its corresponding IBZ k-point.

vkpt\_k
:   *Shape:* {nkpts\_k, 3}
:   *Description:* k-points in direct coordinates for the IBZ.

vkpt\_kp
:   *Shape:* {nkpts\_kp, 3}
:   *Description:* k-points in direct coordinates for the FBZ.

wtkpt\_k
:   *Shape:* {nkpts\_k}
:   *Description:* Weights corresponding to each IBZ k-point. These are used for Brillouin zone integrations.

### Group: /matrix\_elements

This group contains datasets for the electron–phonon coupling as well as related electronic and phononic properties.

#### Datasets

nspin
:   *Shape:* Scalar
:   *Description:* Number of spin channels used in the simulation. A value of 1 indicates non-spin-polarized calculations, while 2 indicates spin-polarized.

natoms
:   *Shape:* Scalar
:   *Description:* Total number of atoms in the simulation cell.

nkpts\_k
:   *Shape:* Scalar
:   *Description:* Total number of k-points in the IBZ.

nkpts\_kp
:   *Shape:* Scalar
:   *Description:* Total number of k-points in the FBZ.

nbands\_k
:   *Shape:* Scalar
:   *Description:* Number of electronic bands associated with the IBZ.

nbands\_kp
:   *Shape:* Scalar
:   *Description:* Number of electronic bands associated with the FBZ.

band\_start\_k
:   *Shape*: Scalar
:   *Description*: Starting index for the electronic bands associated with the IBZ k-points.

band\_start\_kp
:   *Shape:* Scalar
:   *Description:* Starting index for the electronic bands associated with the FBZ k-points.

eigenvalues\_k
:   *Shape:* {nspin, nkpts\_k, nbands\_k}
:   *Description:* Electronic eigenvalues for the IBZ k-points.

eigenvalues\_kp
:   *Shape:* {nspin, nkpts\_kp, nbands\_kp}
:   *Description:* Electronic eigenvalues for the FBZ k-points.

elph
:   *Shape:* {nspin, nkpts\_kp, nkpts\_k, 3\*natoms, nbands\_kp, nbands\_k, 2}
:   *Description:* Electron–phonon matrix elements.
:   The last (fastest) dimension is due to complex numbers being stored as two real numbers (real and imaginary parts).
:   **nkpts\_kp** and **nbands\_kp** refer to the initial (Ket) state.
:   **nkpts\_k** and **nbands\_k** refer to the final (Bra) state.

phonon\_eigenvalues
:   *Shape:* {nkpts\_kp, nkpts\_k, 3\*natoms}
:   *Description:* Phonon eigenvalues (frequencies) computed at each k-point.

## Related tags and articles

ELPH\_DRIVER,
ELPH\_RUN,
Electron-phonon potential from supercells
