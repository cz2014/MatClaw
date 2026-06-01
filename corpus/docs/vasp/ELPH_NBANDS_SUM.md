# ELPH_NBANDS_SUM

Categories: INCAR tag, Electron-phonon interactions

ELPH\_NBANDS\_SUM = [integer array]  
 Default: **ELPH\_NBANDS\_SUM** = ELPH\_NBANDS

Description: Number of intermediate states to include in the computation of the phonon-induced electron self-energy.

> **Mind:** Available as of VASP 6.5.0

---

The computation of the self-energy is achieved via a sum over intermediate states $|\Psi\_{m \mathbf{k} + \mathbf{q}}\rangle$.
ELPH\_NBANDS\_SUM specifies the maximum number of bands, $N\_{\text{b}}$, such that $m$ runs from $1 \ldots N\_{\text{b}}$.

Multiple values can be specified for ELPH\_NBANDS\_SUM, in which case the self-energy is computed once for each value.
The results are reported in separate groups inside the vaspout.h5 file:

```
/results/electron_phonon/electrons/self_energy_1
/results/electron_phonon/electrons/self_energy_2
/results/electron_phonon/electrons/self_energy_3
...
```

This tag is useful for studying the convergence of the self-energy with respect to the number of intermediate states.
At a certain point, including more bands in the summation over states should no longer change the result.

> **Mind:** When computing the renormalization of the electronic bandstructure, a large number of intermediate states may be necessary to reach convergence. If the self-energy still changes noticeably around `ELPH_NBANDS_SUM = ELPH_NBANDS`, then you may have to increase ELPH\_NBANDS.

## Related tags and articles

* Bandstructure renormalization
* ELPH\_RUN
* ELPH\_NBANDS
* ELPH\_SELFEN\_FAN
* ELPH\_SELFEN\_DW
