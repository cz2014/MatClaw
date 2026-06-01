# ESF_SPLINES

ESF\_SPLINES = .FALSE. | .TRUE.  
 Default: **ESF\_SPLINES** = .FALSE.

Description: Enable k-point interpolation of the electronic structure factor using tricubic splines in ACFDT/RPA calculations.

---

With ESF\_SPLINES =T, the electronic structure factor (ESF) is interpolated using tricubic splines to accelerate k-point convergence of the RPA-correlation energy in ACFDT/RPA calculations. The default settings of the maximum number of iteration steps (ESF\_NINTER) and convergence threshold (ESF\_CONV) typically yield similar k-point convergence compared to the k-p perturbation theory approach.

> **Tip:** By means of ESF interpolation, one can obtain the RPA-correlation energy for metals and insulators, in contrast to the k-p method that fails for metals.

## Algorithm

This feature follows the same idea as in coupled cluster calculations.
To compute the RPA-correlation energy, the electronic structure factor in the RPA

$S({\bf q}+{\bf G}) =\int {\rm d}\omega
\left\{(\mathrm{ln}[1-\tilde\chi^0({\mathbf{q}},\mathrm{i}\omega)V({\mathbf{q}})])\_{{\mathbf{G,G}}} +V\_{{\mathbf{G,G}}}({\mathbf{q}})\tilde\chi^0({\mathbf{q}},{\mathrm{i}}\omega) \right\}$

is evaluated on the k-point grid defined in KPOINTS and the correlation energy (as its trace) is stored.
To obtain the correlation energy on a finer k-point grid, more q-points are added using tricubic spline interpolation. The resulting energy is compared to the previous correlation energy.
This procedure is repeated ESF\_NINTER times or until the difference in energy between the interpolation steps is less than ESF\_CONV.

## ESF-interpolation method vs k-p perturbation theory

> **Warning:** Remove WAVEDER and avoid setting LOPTICS=T when running a job with ESF\_SPLINES=T.

Note that the ESF-interpolation method is incompatible with k-p perturbation theory, where the largest q-point integration error

:   $$\lim\_{\bf q\to 0} \tilde\chi^0\_{{\bf G G}'}({\bf q},{\rm i}\omega) \cdot {\bf V}\_{\bf G G'}({\bf q})$$

is added explicitly to the RPA integral. The long-wave limit is ill-defined for metallic systems; hence, the k-p method fails for metals. For the k-p method, the long-wave contribution is stored in the WAVEDER file, and VASP assumes you want to add this term if the file is present in the working directory.

## Output

The result of the ESF interpolation is reported to the OUTCAR file in the following format

```
     cutoff energy     smooth cutoff   RPA   correlation   Hartree contr. to MP2  RPA spline-interp.
-----------------------------------------------------------------------------------------------------
           166.667           133.333      -12.9738715106      -19.7255874374      -13.4968000908
           158.730           126.984      -12.8840657072      -19.6294580403      -13.4017404001
           151.172           120.937      -12.7775593388      -19.5151822998      -13.3005326847
           143.973           115.178      -12.6604147404      -19.3892142669      -13.1868498210
           137.117           109.694      -12.5530911576      -19.2733151174      -13.0861120393
           130.588           104.470      -12.4659186304      -19.1786165194      -12.9778587892
           124.369            99.495      -12.3690601643      -19.0725742983      -12.8709666989
           118.447            94.758      -12.2461267475      -18.9372318755      -12.7590723870
 linear regression    
 converged value                          -14.0340307585      -20.8751715586      -14.5828037654
```

The last column contains the result from the spline interpolation for the selected energy cutoffs reported in the first column.

> **Mind:** Available as of VASP.6.5.0

## Related tags and articles

ESF\_CONV,
ESF\_NINTER,
LOPTICS

Examples that use this tag

## References
