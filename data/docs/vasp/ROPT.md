# ROPT

Categories: INCAR tag, Projector-augmented-wave method

ROPT = [real array], one entry for each species on the POTCAR file

|  |  |  |
| --- | --- | --- |
| Default: **ROPT** | = -5E-4 | if LREAL=Auto and PREC=Normal |
|  | = -5E-4 | if LREAL=Auto and PREC=Single or SingleN |
|  | = -2.5E-4 | if LREAL=Auto and PREC=Accurate |
|  | = -0.01 | if LREAL=Auto and PREC=Low |
|  | = -0.002 | if LREAL=Auto and PREC=Medium |
|  | = -4E-4 | if LREAL=Auto and PREC=High |

|  |  |  |
| --- | --- | --- |
| Default: **ROPT** | = 2/3 | if LREAL=On and PREC=Low |
|  | = 1.0 | if LREAL=On and PREC=Medium |
|  | = 1.5 | if LREAL=On and PREC=High |

Description: ROPT determines how accurately the projectors are represented in real space. With LREAL=On, the real space projectors are optimized using an algorithm proposed by King-Smith et al. LREAL=Auto is the recommended scheme since it is considerably more accurate, resulting in more localized projector functions than with the King-Smith et al. method.

---

> **Mind:**
>
> * Whether the user supplies negative or positive values in the INCAR file is irrelevant. With LREAL=Auto and On, ROPT are internally set to negative and positive values, respectively.
> * LREAL=On is outdated and should be only used, if compatibility to old calculations is desired.

Depending on their value, VASP interprets ROPT entries in one of two ways:

* ABS|ROPT| ≥ 0.1: "conventional"-mode:

:   Sets the number of real space points within the cutoff sphere for a particular species to approximately 1000×ROPT. So for instance, the line

```
ROPT = 0.7 1.5
```

:   will set the number of real space points within the cutoff sphere for the first species to approximately 700, and that for the second species to 1500.

* ABS|ROPT| < 0.1 : "precision"-mode:

:   In this case, the real-space operators will be optimized for an accuracy of approximately ROPT eV/atom. So, for instance specifying the following line in the INCAR file

```
ROPT = 1E-3 1E-3
```

:   tells VASP to optimize the real-space projector operators for species 1 and 2 for an accuracy of approximately 1 meV/atom (10-3). The estimate is, however, fairly rough: this means that even if an error of say 0.5 meV/atom is selected, the actual error might well approach 5 meV/atom for transition metals with many electrons. It is recommended to first perform reference calculations using LREAL=.FALSE., then switch to LREAL=Auto and decrease ROPT until the desired accuracy is reached.

The "precision" and "conventional" modes may be intermixed, i.e., it is possible to specify

```
ROPT = 0.7 -1E-3
```

In this case, the number of real space points within the cutoff sphere for the first species will be approximately 700, whereas the real space projector functions for the second species are optimized for an accuracy of approximately 1 meV. We recommend to use the "precision" mode with a target accuracy of around 2x10-4 - 10-3 eV/atom.

If you use the "conventional" mode, in which the number of grid points in the real space projection sphere is specified, you have to select ROPT carefully, especially if a hard species is mixed with a soft species. In that case the following lines in the OUTCAR file must be checked (here is the output for LREAL=Auto, however, the one for LREAL=On is quite similar)

```
Optimization of the real space projectors
maximal supplied QI-value         = 13.98
optimisation between [QCUT,QGAM] = [  8.81, 17.62] = [ 21.73, 86.94] Ry
Optimized for a Real-space Cutoff    1.41 Angstroem
  l    n(q)    QCUT    max X(q) W(low)/X(q) W(high)/X(q)  e(spline)
  2      6     8.810    59.645    0.61E-03    0.18E-02    0.11E-06
  2      6     8.810    58.460    0.65E-03    0.19E-02    0.12E-06
  0      7     8.810    97.683    0.18E-02    0.15E-03    0.13E-06
  0      7     8.810    53.223    0.17E-02    0.15E-03    0.12E-06
  1      7     8.810    13.596    0.47E-02    0.65E-02    0.33E-06
  1      7     8.810     7.885    0.35E-02    0.48E-02    0.25E-06
```

QCUT and QGAM are parameters chosen for the generation of this particular PAW dataset (or ultrasoft pseudopotential). The most important information is given in the columns W(low)/X(q) and W(high)/X(q) for LREAL=Auto). In these columns, the values must be as small as possible. If these values are too large increase the ROPT value from the default value (or decrease it if it smaller than 0.1). As a rule of thumb, the maximum allowed value in this column is 10-3 for PREC=Normal. (For PREC=Low errors might be around 10-2. If W(q)/X(q) is larger than 10-2 the errors introduced by the real space projections can be substantial. In this case ROPT must be specified in the INCAR file to avoid incorrect results.

## Related tags and sections

LREAL,
PREC

Examples that use this tag

## References
