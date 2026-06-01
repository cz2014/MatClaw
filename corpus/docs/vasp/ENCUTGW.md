# ENCUTGW

Categories: INCAR tag, Many-body perturbation theory, GW

ENCUTGW = [real]  
 Default: **ENCUTGW** = 2/3 ENCUT

Description: The tag ENCUTGW sets the energy cutoff for the response function. It controls the basis set for the response functions
in exactly the same manner as ENCUT does for the orbitals.

---

In GW and random-phase-approximation (RPA) calculations, storing and manipulating the response function dominates the computational work load:

$\chi\_{{\mathbf{q}}}^0 ({\mathbf{G}}, {\mathbf{G}}', \omega)=\frac{1}{\Omega} \sum\_{n,n',{\mathbf{k}}}2 w\_{{\mathbf{k}}}
(f\_{n'{\mathbf{k}}+{\mathbf{q}}} - f\_{n{\mathbf{k}}})
\times \frac{\langle \psi\_{n{\mathbf{k}}}| e^{-i ({\mathbf{q}}+{\mathbf{G}}){\mathbf{r}}} | \psi\_{n'{\mathbf{k}}+{\mathbf{q}}}\rangle
\langle \psi\_{n'{\mathbf{k}}+{\mathbf{q}}}| e^{i ({\mathbf{q}}+{\mathbf{G}}'){\mathbf{r'}}} | \psi\_{n{\mathbf{k}}}\rangle}
{ \epsilon\_{n'{\mathbf{k}}+{\mathbf{q}}}-\epsilon\_{n{\mathbf{k}}} - \omega - i \eta }.$

ENCUTGW controls how many $\mathbf{G}$ vectors are included in the
the response function $\chi\_{{\mathbf{q}}}^0 ({\mathbf{G}}, {\mathbf{G}}', \omega)$.

Our experience suggests that choosing ENCUTGW= 2/3 ENCUT yields reasonable results at fairly modest computational cost, although, the response function contains contributions up to twice the plane wave cutoff $G\_{\rm cut}$, see ALGO tag. Furthermore, RPA correlation energies are reported using an internal extrapolation of the correlation energy by varying the value of ENCUTGW inside VASP between the largest value given in the INCAR file and smaller values . Mind: The extrapolated value is only reliable, if ENCUTGW is smaller then ENCUT. The cutoff extrapolation with respect to ENCUTGW would be precise if the plane wave basis for the orbitals were infinite. Again, the VASP defaults yield very reasonable values for the extrapolated correlation energy. In fact, it is unwise to increase ENCUTGW only, without increasing ENCUT. To converge RPA correlation energies, simply increase ENCUT and the number of orbitals, and use the VASP default for ENCUTGW.

> **Mind:** More details on how the infinite basis set limit is extrapolated in RPA/ACFDT can be found here.

For quasiparticle (QP) bandgaps, it is sometimes possible to set ENCUTGW to values between 150 to 200 eV, and even 100 eV can yield
gaps that are accurate to within a few tens of an eV for main group elements. Be aware, however, that the absolute values of the QP energies depend inverse proportionally on the number of plane waves. Thus, the convergence of absolute QP energies is very slow, although QP gaps might seem converged.

The recommended procedure to obtain accurate QP energies is discussed in the reference below. Specifically, for reference type calculations we recommend the following procedure:

* Use the default for ENCUTGW, or even decrease ENCUTGW to half the value of ENCUT.
* Calculate all orbitals that the plane-wave basis set allows to calculate. This number can be determined by searching for "maximum number of plane-waves" in the ground-state DFT OUTCAR file, and setting NBANDS to this value.
* Increase ENCUT systematically and plot the QP energies versus the number of plane-wave coefficients, which equals the number of orbitals. This means ENCUTGW and NBANDS increase as ENCUT increases.

This procedure can be carried out using few k points. Other commonly applied methods can yield less accurate results and are not considered to be reliable.

## FFT grid and PRECFOCK

The PRECFOCK tag determines the fast Fourier transformation (FFT) grid in all GW (and Hartree-Fock) related routines. For small systems, the computational time is often dominated by FFT operations. Therefore, the PRECFOCK tag can have a significant impact on the compute time for QP calculations. For large systems, the FFT's usually do not dominate the computational workload, and savings are expected to be small for PRECFOCK = *fast*.
QP shifts are usually not very sensitive to the setting of PRECFOCK and therefore there is no harm in setting PRECFOCK = *fast*), whereas for RPA calculations we recommend to set PRECFOCK = *normal* to avoid numerical errors.

## Related tags and articles

PRECFOCK,
ENCUT,
ENCUTGWSOFT,
GW calculations,
Basis set convergence

Examples that use this tag

## Further reading

* Generally, QP energies converge like one over the number of orbitals and one over the number of plane waves in the response function. For basis set converged calculations, we recommend using the strategies outlined in Ref. , which contains a comprehensive study of the performance of the convergence of GW calculations.

## References

---
