# Plotting exciton wavefunction

Categories: VASP, Many-body perturbation theory, Bethe-Salpeter equations

Charge density of the first bright exciton in hBN.

Plotting the wavefunction or charge density corresponding to an exciton can be instrumental in analyzing the excitonic state's symmetry, position, and localization.

The exciton wavefunction is written as a function of coordinates of two particles (one hole and one electron) $\psi\_\lambda(\mathbf{r}\_e,\mathbf{r}\_h)=\sum\_{vc} A\_{vc}^\lambda \phi\_v^\*(\mathbf{r}\_h)\phi\_c(\mathbf{r}\_e)$ . In order to visualize such a function in 3D space, we need to "fix" one of the coordinates: the position of the electron $\psi\_\lambda(r\_e,\mathbf{r}\_h)$ or the position of the hole $\psi\_\lambda(\mathbf{r}\_e,r\_h)$.

### How to fix the position of the particle

The position of the fixed particle is provided in direct (fractional) coordinates by the tags BSEHOLE or BSEELECTRON for a hole or an electron, respectively. The tag NBSEEIG sets the number of exciton wavefunctions that need to be computed.

When fixing the position of the particle, ensure that it is not fixed exactly at the center of an atom or coincides with a node of the wavefunction. To avoid that, shift the fixed coordinate slightly away from the center of the atom. Furthermore, the wavefunction of the fixed particle is taken at the nearest $\mathbf{G}$-vector, whose exact position is written in the OUTCAR file

```
hole position is fixed at:
```

or

```
electron position is fixed at:
```

### How to plot the exciton wavefunction

VASP computes the charge density of a particular excitonic state, i.e., $\rho\_\lambda(\mathbf{r})=|\psi\_\lambda(r\_e,\mathbf{r}\_h)|^2$ or $\rho\_\lambda(\mathbf{r})=|\psi\_\lambda(\mathbf{r}\_e,r\_h)|^2$, and writes the resulting charge density into CHG.XX files, which can be visualized using standard tools like VESTA, ASE, etc. Here, XX stands for the index $\lambda$ of the state. VASP computes the charge density by transforming the unit cell with k-points into a supercell. Thus, the exciton charge density is written for a supercell of dimensions ${\rm NKX}\times{\rm NKX}\times{\rm NKX}$.
The size of the supercell is written in the OUTCAR file

```
FFT grid for supercell:
```

> **Mind:** The size of CHG.XX files can get very large. Estimate the CHG.XX file size as follows $(\mathrm{NGX\*NKX})\times(\mathrm{NGX\*NKX})\times(\mathrm{NGX\*NKX})\*12$ bytes. Here, NG{X,Y,Z} is the number of grid points and NK{X,Y,Z} is the number of k-points along the axis.

> **Mind:** The exciton charge density only accounts for the plane-wave part of the wavefunction, and the augmentation terms are neglected.

> **Warning:** In VASP 6.4.3 the exciton wavefunction is not correctly calculated in `vasp_std` and `vasp_ncl` if the hole or electron is not fixed at the coordinate (0,0,0). This issue was resolved in VASP 6.5.0

### Degeneracy

The calculated excitonic states can be degenerate, i.e., multiple eigenvectors have the same energy. For the correct analysis, the degenerate states should be added together.

> **Mind:** Calculation of the exciton wavefunction is only supported with IBSE=0 and ANTIRES=0.

## Related tags and sections

CHG, NBSEEIG, BSEHOLE, BSEELECTRON, BSE

## References
