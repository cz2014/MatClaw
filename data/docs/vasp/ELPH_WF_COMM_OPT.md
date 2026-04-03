# ELPH_WF_COMM_OPT

Categories: INCAR tag, Electron-phonon interactions

ELPH\_WF\_COMM\_OPT = [integer]  
 Default: **ELPH\_WF\_COMM\_OPT** = 0

Description:
Selects the MPI communication pattern used to exchange orbitals between different MPI ranks.

> **Mind:** Available as of VASP 6.5.0

---

The available options are:

* **0** — Use two-sided MPI communication (default)
* **1** — Use one-sided MPI communication

Some MPI libraries have shown instability or performance issues when using one-sided communication.
If unexpected behavior occurs, it is recommended to keep the default setting `ELPH_WF_COMM_OPT = 0`.

## Related tags and articles

* ELPH\_WF\_CACHE\_PREFILL
* ELPH\_WF\_REDISTRIBUTE
