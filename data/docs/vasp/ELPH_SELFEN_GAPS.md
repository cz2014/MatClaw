# ELPH_SELFEN_GAPS

Categories: INCAR tag, Electron-phonon interactions

ELPH\_SELFEN\_GAPS = [logical]  
 Default: **ELPH\_SELFEN\_GAPS** = .false.

Description: Find the direct and indirect gaps and the valence and conduction Kohn-Sham states that form it and select to compute their self-energy due to electron-phonon coupling.

> **Mind:** Available as of VASP 6.5.0

---

This tag additionally activates the reporting of the value of the band-gap renormalization to the standard output, the OUTCAR file

```
 $ grep -A7 'KS-QP gap (meV)' OUTCAR
```

and the vaspout.h5 file under

```
 $ h5ls -r vaspout.h5 | grep gap_renorm
 /results/electron_phonon/electrons/self_energy_1/direct_gap_renorm
 /results/electron_phonon/electrons/self_energy_1/fundamental_gap_renorm`
```

This output is reported once for each  electron-phonon accumulator.

If instead, the computation of the self-energy for a particular set of states is desired, those can be manually specified using a combination of ELPH\_SELFEN\_KPTS, ELPH\_SELFEN\_IKPT, ELPH\_SELFEN\_BAND\_START and ELPH\_SELFEN\_BAND\_STOP.

## Related tags and articles

* Bandstructure renormalization
* Electron-phonon accumulators
* ELPH\_RUN
* ELPH\_SELFEN\_BAND\_START
* ELPH\_SELFEN\_BAND\_STOP
