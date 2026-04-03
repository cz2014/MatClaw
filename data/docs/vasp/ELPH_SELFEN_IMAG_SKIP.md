# ELPH_SELFEN_IMAG_SKIP

Categories: INCAR tag, Electron-phonon interactions

ELPH\_SELFEN\_IMAG\_SKIP = [logical]  
 Default: **ELPH\_SELFEN\_IMAG\_SKIP** = .FALSE.

Description:
Use the tetrahedron method to skip the computation of electron-phonon matrix elements for which the energy-conserving delta functions are zero.

> **Mind:** Available as of VASP 6.5.0

---

It is strongly recommended to enable this option when only the imaginary part of the electron self-energy (linewidths) are required, for instance in transport or scattering rate calculations.
Using this tag can reduce the computational cost by orders of magnitude, depending on the electronic band structure.

When using this option, it is also recommended to set ELPH\_WF\_REDISTRIBUTE = .TRUE.

## Related tags and articles

ELPH\_WF\_REDISTRIBUTE,
ELPH\_SCATTERING\_APPROX,
ELPH\_RUN,
((TAG|ELPH\_SELFEN\_G\_SKIP}}
