# ELPH_TRANSPORT_NEDOS_PLOT

Categories: INCAR tag, Electron-phonon interactions

ELPH\_TRANSPORT\_NEDOS\_PLOT = [integer]  
 Default: **ELPH\_TRANSPORT\_NEDOS\_PLOT** = -1

Description:
Specifies the number of energy points used to sample the  transport distribution function for plotting.

> **Mind:** Available as of VASP 6.5.0

---

This parameter defines the resolution of the energy grid used to compute and store the transport distribution function in vaspout.h5.
The transport function for plotting is evaluated on a linear energy grid of energies between ELPH\_TRANSPORT\_EMIN\_PLOT and ELPH\_TRANSPORT\_EMAX\_PLOT and with ELPH\_TRANSPORT\_NEDOS\_PLOT points.
A higher value increases the energy resolution of the plotted transport quantities but also slightly increases the post-processing time.

The default value of -1 means that the transport function for plotting is not computed by default. If the number if positive (for example 501) then it corresponds to the number of points in the dataset:

```
 $ h5ls -r vaspout.h5 | grep plot
 /results/electron_phonon/electrons/transport_1/energy_plot Dataset {501}
 /results/electron_phonon/electrons/transport_1/transport_function_plot Dataset {7, 1, 3, 3, 501}
```

## Related tags and articles

* ELPH\_TRANSPORT
* ELPH\_TRANSPORT\_EMIN\_PLOT
* ELPH\_TRANSPORT\_EMAX\_PLOT
* ELPH\_RUN
* TRANSPORT\_RELAXATION\_TIME
