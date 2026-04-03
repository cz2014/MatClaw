# LREAL

Categories: INCAR tag, Projector-augmented-wave method

LREAL = .FALSE. | Auto (or A) | On (or O) | .TRUE.  
 Default: **LREAL** = .FALSE.

Description: LREAL determines whether the projection operators are evaluated in real-space or in reciprocal space.

---

|  |  |
| --- | --- |
| LREAL=.FALSE. | projection done in reciprocal space |
| LREAL=Auto or A | projection done in real space, fully automatic optimization of projection operators (little to no user interference required) |
| LREAL=On or O | projection done in real space, projection operators are re-optimized (not recommended) |
| LREAL=.TRUE. | projection done in real space, use projectors on file (not recommended) |

The nonlocal part of the pseudopotential requires the evaluation of an expression:

:   :   $\sum\_{ij}D\_{ij}|\beta\_j\rangle\langle\beta\_i|\tilde{\psi}\_{n\mathbf{k}}\rangle$.

where the "projected wavefunction character" is defined as:

:   :   $$\begin{align}C\_{in\mathbf{k}}=\langle\beta\_i|\tilde{\psi}\_{n\mathbf{k}}\rangle &=\frac{\Omega}{N\_{\rm FFT}}\sum\_{\mathbf{r}}\langle\beta\_i|\mathbf{r}\rangle\langle\mathbf{r}|\tilde{\psi}\_{n\mathbf{k}}\rangle=\frac{\Omega}{N\_{\rm FFT}}\sum\_{\mathbf{r}}\beta(\mathbf{r})\tilde{\psi}\_{n\mathbf{k}}(\mathbf{r}) \\ &=\sum\_{\mathbf{G}}\langle\beta\_i|\mathbf{k}+\mathbf{G}\rangle\langle\mathbf{k}+\mathbf{G}|\tilde{\psi}\_{n\mathbf{k}}\rangle=\sum\_\mathbf{G}\bar\beta(\mathbf{k}+\mathbf{G}) C\_{\mathbf{G}n\mathbf{k}}\end{align}$$

This expression can be evaluated in reciprocal or real space: In reciprocal space (second line), the number of operations scales with the size of the basis set, i.e., number of plane waves. In real space (first line), the projection operators are confined to spheres around each atom. Therefore, the number of operations necessary to evaluate one Cin**k** does not increase with the system size (usually, the number of grid points within the cutoff sphere is between 500 and 2000). One of the major obstacles to the method working in real space is that the projection operators must be optimized, i.e., all high Fourier components must be removed from the projection operators. If this is not done, aliasing can happen, i.e., the high Fourier components of the projection operators are downfolded to low Fourier components, and random noise is introduced).

Currently, VASP supports three different schemes to remove the high Fourier components from the projectors. LREAL=.TRUE. is the simplest one. For LREAL=.TRUE., the real-space projectors that the pseudopotential generation code has generated are used. This requires no user interference but is potentially very inaccurate. For the outdated LREAL=On, the real space projectors are optimized by VASP using an algorithm proposed by King-Smith et al. For the recommended LREAL=Auto, an unpublished scheme is used which results in simultaneously more accurate and localized projector functions than for the King-Smith et al. method. To fine-tune the optimization procedure, the tag ROPT can and should be used, if LREAL=Auto (or LREAL=On) is used. Specifically, perform first reference calculations using LREAL=.False. and decrease ROPT until an acceptable accuracy, e.g., 1 meV/atom, is attained. Please also check carefully the documentation for ROPT.

We recommend using the real-space projection scheme for systems containing more than about 30 atoms. We also strongly recommend using only LREAL=Auto.

For LREAL=A (and LREAL=O) the projection operators are optimized by VASP on the fly (i.e. on startup). Several tags influence the optimization:

* ENCUT (i.e., the energy cutoff), components beyond the energy cutoff are 'removed' from the projection operators.

* PREC tag specifies how precise the real-space projectors should be and sets the variables ROPT accordingly to the following values:

:   For LREAL=Auto

:   :   |  |  |
        | --- | --- |
        | ROPT=-5E-4 | if PREC=Normal |
        | ROPT=-5E-4 | if PREC=Single or SingleN |
        | ROPT=-2.5E-4 | if PREC=Accurate |
        | ROPT=-0.01 | if PREC=Low |
        | ROPT=-0.002 | if PREC=Medium |
        | ROPT=-4E-4 | if PREC=High |

:   For LREAL=On

:   :   |  |  |
        | --- | --- |
        | ROPT=2/3 | if PREC=Low |
        | ROPT=1.0 | if PREC=Medium |
        | ROPT=1.5 | if PREC=High |

:   These defaults can be superseded by specifying the ROPT tag in the INCAR file.

> **Mind:**
>
> * Real-space optimization (LREAL=Auto) always results in a small (not necessarily negligible) error. The error is usually a constant energy shift for each atom. If you are interested in energy differences, use only calculations with the same setup (i.e., same ENCUT, PREC, LREAL and ROPT setting) for all calculations. For example, if you want to calculate surface or defect energies, recalculate the bulk ground-state energy with exactly the same setting you are using for the surface. Another possibility is to relax the structure using real-space projection and to perform one final total-energy calculation using LREAL=.FALSE. to get exact energies. For PREC=Normal, the errors introduced by the real-space projection are usually of the same order of magnitude as those introduced by the wrap-around errors. For PREC=Accurate errors are usually less than 1 meV/atom. PREC=Low should be used only for, say, fast molecular-dynamics calculations, if compute resources are really an issue.
> * When the energy cutoff ENCUT is increased significantly w.r.t. their defaults, the real-space projection scheme sometimes becomes unreliable, and it might be necessary to decrease ROPT to values as small as ROPT=1E-4.

## Related tags and articles

ROPT,
PREC

Examples that use this tag

## References

---
