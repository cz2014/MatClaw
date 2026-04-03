# PARCHG

Categories: Files, Output files, Charge density

PARCHG is an output file created when partial charge densities are calculated by setting LPARD = .TRUE..
The file has the same structure as the CHG file, containing the structure followed by the charge density on the fine FFT grid, but missing the augmentation occupancies that are written to CHGCAR. The units are also equivalent to CHG and CHGCAR.

The partial density written to PARCHG is part of the valence electron density that was converged selfconsistently in a previous run.
The bands and **k** points that contribute to the partial charges are selected by the IBAND, NBMOD, EINT and KPUSE tags, allowing for fine control of the contributions to the partial charge density.

## PARCHG.nb.nk files

If LSEPB and/or LSEPK are set to .TRUE. variants of the PARCHG file are written, separating the contributing bands and **k** points respectively. The units and format of the files stay the same.

* If `LSEPB = .TRUE.`, **PARCHG.nb.ALLK** files are written, where nb is an index over all bands contributing to the partial charge density.

* If `LSEPK = .TRUE.`, **PARCHG.ALLB.nk** files are created, where nk runs over all **k** points in KPUSE or all **k** points if KPUSE is not set.

* For `LSEPB = .TRUE.` and `LSEPK = .TRUE.`, all combinations are written to **PARCHG.nb.nk** files.

> **Mind:** If VASP 6.5.0 or later is used, the code is compiled with HDF5 support, and LPARDH5 = .TRUE., all output will be redirected to the vaspout.h5 file, where it can be analyzed with py4vasp.

## Format

The PARCHG consists of the following blocks:

* Structure in POSCAR format
* FFT-grid dimensions NGXF, NGYF, NGZF
* Partial charge density times FFT-grid volume is written with multiple real numbers per line until all NGXF\*NGYF\*NGZF values of the block are written.

The real-space mesh (NX,NY,NZ) is uniform and is spanned by the lattice vectors $\vec{a}, \vec{b}, \vec{c}$ defined in the structure block. The coordinates of the mesh points can be restored via

:   :   $(N\_x,N\_y,N\_z) \hat{=} \frac{N\_x-1}{N\_{GXF}}\mathbf{a}+\frac{N\_y-1}{N\_{GYF}}\mathbf{b}+\frac{N\_z-1}{N\_{GZF}}\mathbf{c}$.

The dimensions can be increased by increasing the cutoff energy (ENCUT) or explicitly by setting the fine FFT-grid dimensions (NGXF, NGYF, NGZF).

To arrange the data on the real-space grid in the unit cell, mind that the data runs fastest over NX and slowest over NZ. To be more explicit, the density is written using the following command in Fortran

:   :   `WRITE(IU,FORM) (((C(NX,NY,NZ),NX=1,NGXF),NY=1,NGYF),NZ=1,NGZF)` .

> **Important:** Remember that the values must be divided by the FFT-grid volume and the cell volume to obtain the partial charge density $n(r)$ in units $1/\AA^3$.

Hence,

:   :   $$n(r)=data(r)/(V\_{grid}\*V\_{cell}),$$
    :   $$V\_{grid} = N\_{GXF}\*N\_{GYF}\*N\_{GZF},$$
    :   $V\_{cell} = |\mathbf{a}\cdot(\mathbf{b}\times\mathbf{c})|$,

where $n(r)$ is the partial charge density in units 1/Å$^3$.

### Spin-polarized calculation

In spin-polarized calculations, two data sets are stored in the PARCHG file.
The first set contains the total partial density (spin up + spin down), and the second is the magnetization density (spin up - spin down). Each block is separated by a blank line and a line containing the fine FFT grid dimensions NGXF NGYF NGZF.

* Structure
* FFT-grid dimensions
* Partial charge density times FFT-grid volume (spin up + spin down)
* FFT-grid dimensions
* Partial magnetization density (spin up - spin down)

## Related tags and articles

LPARD,
LPARDH5,
IBAND,
EINT,
NBMOD,
KPUSE,
LSEPB,
LSEPK,
Band-decomposed charge densities

---
