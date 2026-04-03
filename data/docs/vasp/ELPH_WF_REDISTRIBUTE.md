# ELPH_WF_REDISTRIBUTE

Categories: INCAR tag, Electron-phonon interactions

ELPH\_WF\_REDISTRIBUTE = [logical]  
 Default: **ELPH\_WF\_REDISTRIBUTE** = .FALSE.

Description:
After computing the electronic states, they are redistributed among the CPUs such that the workload to compute the electron self-energy is similar among the different CPUs.

> **Mind:** Available as of VASP 6.5.0

---

The computational effort for each Kohn–Sham state is first estimated, and then the states are distributed among MPI ranks to balance the workload as evenly as possible. This redistribution is most relevant when used in combination with `ELPH_SELFEN_IMAG_SKIP = .TRUE.`.
When `ELPH_MODE = TRANDPORT`, the default value is `ELPH_WF_REDISTRIBUTE = .TRUE.`.

## Related tags and articles

ELPH\_MODE,
ELPH\_SELFEN\_IMAG\_SKIP,
ELPH\_RUN,
ELPH\_WF\_COMM\_OPT,
ELPH\_WF\_CACHE\_PREFILL
