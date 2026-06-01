# CHGCAR

Categories: Files, Input files, Output files, Electronic ground-state properties, Charge density

The CHGCAR file stores the charge density and the PAW one-center occupancies. It is written by default, but it can be avoided (LCHARG) or redirected to vaspwave.h5 (LH5).
The CHGCAR file can be read to restart a calculation (ICHARG).

> **Tip:** We recommend starting from the CHGCAR file when repeatedly restarting with small changes in the input parameters, e.g., the **k**-point mesh (KPOINTS).

The CHG file also stores the charge density without the PAW one-center occupancies and is intended for visualization and post-processing.

## Format

The CHGCAR consists of the following blocks:

* Structure in POSCAR format
* FFT-grid dimensions NGXF, NGYF, NGZF
* Charge times FFT-grid volume is written with multiple real numbers per line until all NGXF\*NGYF\*NGZF values of the block are written.
* Augmentation occupancies

The real-space mesh (NX,NY,NZ) is uniform and is spanned by the lattice vectors $\vec{a}, \vec{b}, \vec{c}$ defined in the structure block. The coordinates of the mesh points can be restored via

:   :   $(N\_x,N\_y,N\_z) \hat{=} \frac{N\_x-1}{N\_{GXF}}\mathbf{a}+\frac{N\_y-1}{N\_{GYF}}\mathbf{b}+\frac{N\_z-1}{N\_{GZF}}\mathbf{c}$.

The dimensions can be increased by increasing the cutoff energy (ENCUT) or explicitly by setting the fine FFT-grid dimensions (NGXF, NGYF, NGZF).

To arrange the data on the real-space grid in the unit cell, mind that the data runs fastest over NX and slowest over NZ. To be more explicit, the density is written using the following command in Fortran

:   :   `WRITE(IU,FORM) (((C(NX,NY,NZ),NX=1,NGXF),NY=1,NGYF),NZ=1,NGZF)` .

> **Important:** Remember that the values must be divided by the FFT-grid volume and the cell volume to obtain the charge density $n(r)$ in units 1/Å$^3$.

Hence,

:   :   $$n(r)=data(r)/(V\_{grid}\*V\_{cell}),$$
    :   $$V\_{grid} = N\_{GXF}\*N\_{GYF}\*N\_{GZF},$$
    :   $V\_{cell} = |\mathbf{a}\cdot(\mathbf{b}\times\mathbf{c})|$,

where $n(r)$ is the charge density in units 1/Å$^3$. Sanity check: The integral of $n(r)$ over the unit cell yields the number of valence electrons (NELECT),

:   :   $\text{NELECT}=\int\_{V\_{cell}} n(\mathbf{r}) d^3\mathbf{r}= \sum\_{N\_X,N\_Y,N\_Z} data(N\_X,N\_Y,N\_Z)/(N\_{GXF}\*N\_{GYF}\*N\_{GZF})$.

By our convention, the charge density $n(r)$ is in units 1/Å$^3$ and \*\*not\*\* e/Å$^3$ because the potential (e.g. LOCPOT, WRT\_POTENTIAL) is assumed to be in eV. However, e$=1$, so while this convention makes the sign of $n(r)$ less ambiguous, it has no effect on the numerical values.

> **Warning:** The augmentation occupancies are written up to the *l*-quantum number set by the LMAXMIX.

Restarting calculations without one-center PAW occupancy matrices up to the appropriate *l*-quantum number leads to loss of information. This is particularly problematic for calculations with fixed charge density, e.g., band-structure calculations. See LMAXMIX for more details.

### Magnetic calculations

For magnetic calculations, the CHGCAR file contains additional data blocks for the magnetization. In particular, for spin-polarized calculations (ISPIN=2), the first set contains the total charge density (spin up + spin down) and the second one is the magnetization density (spin up - spin down):

* Structure
* FFT-grid dimensions
* Charge density times FFT-grid volume (spin up + spin down)
* Augmentation occupancies
* FFT-grid dimensions
* Magnetization density (spin up - spin down)
* Augmentation occupancies

For noncollinear calculation (LNONCOLLINEAR=T), contains the total charge density and the magnetization density in the spinor basis set by SAXIS:

* Structure
* FFT-grid dimensions
* Charge density times FFT-grid volume
* Augmentation occupancies
* Augmentation occupancies (imaginary part)
* FFT-grid dimensions
* Magnetization density times FFT-grid volume \*\*in $\sigma\_1$ direction\*\*
* Augmentation occupancies
* Augmentation occupancies (imaginary part)
* FFT-grid dimensions
* Magnetization density times FFT-grid volume in $\sigma\_2$ direction
* ...
* FFT-grid dimensions
* Magnetization density times FFT-grid volume in $\sigma\_3$ direction
* ....

## Molecular dynamics and structure relaxation (IBRION)

In the case of molecular-dynamics (MD) simulations (IBRION=0), CHGCAR contains the extrapolated charge density for the next step, which corresponds to the atomic structure in the CONTCAR file. Although it makes the charge density incompatible with the last atomic coordinates in the OUTCAR file, it allows one to use the CHGCAR and the CONTCAR files consistently for continuing the MD simulation.

> **Warning:** In MD simulations, the charge density in CHGCAR is not the self-consistent charge density for the structure in the CONTCAR file. Hence, one should not perform a band-structure calculation directly after the MD simulation.

For static and relaxation calculations (IBRION=-1,1,2), the charge density in CHGCAR is the self-consistent charge density for the last iteration. Hence, it can be used for accurate band structure calculations.

## Related tags and articles

WAVECAR,
CHG,
LCHARG,
ICHARG,
LMAXMIX,
FFT-grid dimensions: ENCUT, NGXF, NGYF, NGZF
