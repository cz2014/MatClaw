# LAECHG

Categories: INCAR tag, Projector-augmented-wave method, Charge density

LAECHG = .TRUE. | .FALSE.  
 Default: **LAECHG** = .FALSE.

Description: when LAECHG=.TRUE. the *all-electron* charge density will be reconstructed explicitly and written to files.

---

If LAECHG=.TRUE. is set VASP will reconstruct the *all-electron* charge density on the so-called "fine" FFT-grid.
This "fine" FFT-grid consists of NGXF×NGYF×NGZF points in real space (*i.e.*, the grid that is used to represent the augmented pseudo charge densities of the USPP and PAW methods).

In fact, for LAECHG=.TRUE., VASP will reconstruct three distinct *all-electron* densities:

1. the core density.
2. the proto-atomic valence density (overlapping atomic charge densities).
3. the self-consistent valence density.

These are written to the files AECCAR0, AECCAR1, and AECCAR2, respectively.
The first two of these files are written at the start of the run, whereas the last is written at the end after self-consistency has been reached.

**N.B.:** In the language of the PAW method an "all-electron" density does **not** refer to the *density of all electrons*, instead it denotes a density that includes all the nodal features near the nucleus associated with the *true* (as opposed to the *pseudized*) one-electron orbitals.
Within the PAW method, the *all-electron* density arising from the one-electron pseudo orbitals $\{ \widetilde{\psi}\_{n\mathbf{k}} \}$ is given by:

:   $$n(\mathbf{r})=
    \sum\_{n{\mathbf{k}}} f\_{n{\mathbf{k}}}
    \langle \widetilde{\psi}\_{n\mathbf{k}}| \mathbf{r}\rangle\langle \mathbf{r}| \widetilde{\psi}\_{n\mathbf{k}} \rangle +
    \sum\_{\alpha, \beta}
    (
    \phi^\ast\_\alpha(\mathbf{r})
    \phi\_\beta (\mathbf{r})
    -
    \widetilde{\phi}^\ast\_\alpha(\mathbf{r})
    \widetilde{\phi}\_\beta (\mathbf{r})
    )
    \sum\_{n{\mathbf{k}}} f\_{n{\mathbf{k}}}
    \langle\widetilde{\psi}\_{n\mathbf{k}}|\widetilde{p}\_\alpha\rangle
    \langle\widetilde{p}\_\beta| \widetilde{\psi}\_{n\mathbf{k}}\rangle$$

Normally one does not attempt to reconstruct *all-electron* densities explicitly since the second term on the right-hand side varies rapidly near the nuclei and is too costly to expand in-plane waves (see the bit about augmentation and compensation charges). For LAECHG=.TRUE., however, this reconstruction is exactly the thing that is done.

## Related tags and articles

AECCAR0, AECCAR1, AECCAR2

Examples that use this tag

---
