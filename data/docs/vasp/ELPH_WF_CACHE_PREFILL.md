# ELPH_WF_CACHE_PREFILL

Categories: INCAR tag, Electron-phonon interactions

ELPH\_WF\_CACHE\_PREFILL = [logical]  
 Default: **ELPH\_WF\_CACHE\_PREFILL** = .TRUE.

Description:
Determines whether to pre-fill the wavefunction (WF) cache before starting the calculation.

> **Mind:** Available as of VASP 6.5.0

---

When enabled, the cache is populated in advance, avoiding one-sided MPI communication during the main computation loop.
This can significantly improve performance and scalability, especially for large parallel runs.

## Related tags and articles

* ELPH\_WF\_REDISTRIBUTE
* ELPH\_WF\_COMM\_OPT
* ELPH\_TRANSPORT
