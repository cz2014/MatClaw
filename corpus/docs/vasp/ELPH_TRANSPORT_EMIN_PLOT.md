# ELPH_TRANSPORT_EMIN_PLOT

Categories: INCAR tag, Electron-phonon interactions

ELPH\_TRANSPORT\_EMIN\_PLOT = [real]  
 Default: **ELPH\_TRANSPORT\_EMIN\_PLOT** = $\min(\varepsilon\_{n\mathbf{k}})$-5

Description:
Specifies the minimum energy (in eV) to be considered when computing the  transport distribution function for plotting.

> **Mind:** Available as of VASP 6.5.0

---

By default, the lower energy limit is set to $\min(\varepsilon\_{n\mathbf{k}})$ − 5 eV, where $\varepsilon\_{n\mathbf{k}}$ are the electronic eigenvalues computed in the k-point mesh defined by the KPOINTS\_ELPH file.
The transport function for plotting is evaluated on a linear energy grid of energies between ELPH\_TRANSPORT\_EMIN\_PLOT and ELPH\_TRANSPORT\_EMAX\_PLOT and with ELPH\_TRANSPORT\_NEDOS\_PLOT points.
The transport function for plotting is computed additionally to the one that is used to evaluate the  Onsager coefficients but allows choosing a different energy range, thus not compromising the accuracy of the transport calculations.

The transport function and corresponding energy grids are written to vaspout.h5.

```
 $ h5ls -r vaspout.h5 | grep plot
 /results/electron_phonon/electrons/transport_1/energy_plot Dataset {501}
 /results/electron_phonon/electrons/transport_1/transport_function_plot Dataset {7, 1, 3, 3, 501}
```

## Related tags and articles

* ELPH\_TRANSPORT
* ELPH\_TRANSPORT\_EMAX\_PLOT
* ELPH\_TRANSPORT\_NEDOS\_PLOT
* ELPH\_RUN
* ELPH\_SCATTERING\_APPROX
* TRANSPORT\_RELAXATION\_TIME
