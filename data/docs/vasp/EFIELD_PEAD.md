# EFIELD_PEAD

Categories: INCAR tag, Linear response, Dielectric properties, Berry phases

EFIELD\_PEAD = [real array]

|  |  |  |
| --- | --- | --- |
| Default: **EFIELD\_PEAD** | = 3\*0.01 | if LCALCEPS=.TRUE. |
|  | = 3\*0.0 | else |

Description: EFIELD\_PEAD specifies the homogeneous electric force field in the electric enthalpy functional used to compute the self-consistent response to finite electric fields. EFIELD\_PEAD is specified in units of eV/Å.

> **Mind:** If EFIELD\_PEAD is used in combination with LCALCEPS=.TRUE., electric field values below 1E-5 will be reset to the default value.

---

If

```
EFIELD_PEAD=εx εy εz
```

is set, with |*ε*|>0, VASP will first determine the zero-field groundstate of the system, and subsequently switch on the electric field and compute the field-polarized groundstate orbitals.

Additionally, from the change in the macroscopic electronic polarization due to the applied electric field, VASP calculates (part of) the components on the diagonal of the ion-clamped static dielectric tensor (ε∞), in accordance with:

:   $$\epsilon^\infty\_{ii}=1+
    \frac{4\pi}{\epsilon\_0}\frac{\partial P\_i}{\partial \mathcal{E}\_i},
    \qquad
    {i=x,y,z}$$

Beware: this option is only useful if one is interested in selected components on the diagonal of the ion-clamped dielectric tensor (for instance, in cubic systems). To calculate the full ion-clamped dielectric tensor of a system

:   $$\epsilon^\infty\_{ij}=\delta\_{ij}+
    \frac{4\pi}{\epsilon\_0}\frac{\partial P\_i}{\partial \mathcal{E}\_j},
    \qquad
    {i,j=x,y,z}$$

from field-polarized calculations, use LCALCEPS=.TRUE..

**Note**: One should be aware that when the electric field is chosen to be too large, the electric enthalpy functional will lose its minima, and VASP will not be able to find a stationary solution for the field-polarized orbitals.
This is discussed in some detail by Souza *et al.*.
VASP will produce a warning if:

:   $$e|\mathcal{E}\cdot \mathbf{a}\_i|\gt \frac{1}{10}E\_{\mathrm{gap}}/N\_i,$$

where *E*gap is the bandgap, **a**i are the lattice vectors, and *N*i is the number of **k**-points along the reciprocal lattice vector *i*, in the regular (*N*1×*N*2×*N*3) **k**-mesh. The factor 1/10 is chosen to be on the safe side. If one does not include unoccupied bands, VASP is obviously not able to determine the bandgap and can not check whether the electric field might be too large. This will also produce a warning message.

### An example: ε∞ in NaF

* Using the following INCAR file:

```
PREC = Med
EDIFF= 1E-6

ISMEAR = 0

EFIELD_PEAD = 0.0 0.0 0.01
```

:   The computation of the static dielectric properties from the field-polarized groundstate orbitals requires a very tight convergence of the solutions. The EDIFF-tag specifies the usual convergence criterium for the zero-field solution. As a default VASP will try for an even tighter convergence of the field-polarized groundstate: EDIFF/100! Reaching this level of convergence may be very costly and in rare cases even impossible.

* KPOINTS file:

```
6x6x6
 0
Gamma
 6 6 6
 0 0 0
```

:   **Note**: The *PEAD* related routines only work for regular meshes of **k**-points that include the Γ-point, i.e.~either uneven meshes (not recommended) or Γ-centered meshes (like the one above).

* POSCAR file:

```
NaF
 4.5102
 0.0 0.5 0.5
 0.5 0.0 0.5
 0.5 0.5 0.0
1 1
Direct
  0.0000000000000000  0.0000000000000000  0.0000000000000000
  0.5000000000000000  0.5000000000000000  0.5000000000000000
```

* and LDA Na\_sv and F PAW datasets.

With the input above, running VASP should produce something akin to:

```
 entering main loop
       N       E                     dE             d eps       ncg     rms          rms(c)
DAV:   1    -0.121171874254E+03   -0.12117E+03   -0.11093E+04   392   0.169E+03
DAV:   2    -0.290944564657E+03   -0.16977E+03   -0.15372E+03   412   0.454E+02
DAV:   3    -0.296448270211E+03   -0.55037E+01   -0.54726E+01   516   0.857E+01
DAV:   4    -0.296558918897E+03   -0.11065E+00   -0.11062E+00   432   0.122E+01
DAV:   5    -0.296564115002E+03   -0.51961E-02   -0.51960E-02   568   0.177E+00    0.512E+00
      ...         ...                ...
      ...         ...                ...
DAV:  11    -0.295718441201E+03    0.31316E-05   -0.40516E-06   436   0.471E-02    0.256E-03
DAV:  12    -0.295718441337E+03   -0.13610E-06   -0.13352E-06   276   0.146E-02
       N       E                     dE             d eps       ncg     rms          rms(c)
 gam= 0.000 g(H,U,f)=  0.142E-07 0.000E+00 0.322E-02 ort(H,U,f) = 0.000E+00 0.000E+00 0.000E+00
SDA:   1    -0.295718441659E+03   -0.29572E+03   -0.12885E-02   360   0.322E-02 0.000E+00
      ...         ...                ...
 gam= 0.382 g(H,U,f)=  0.220E-07 0.167E-07 0.186E-10 ort(H,U,f) =-0.260E-08-0.389E-08 0.523E-10
DMP:   4    -0.295718441597E+03    0.43565E-09   -0.14510E-07   360   0.387E-07-0.644E-08
 gam= 0.382 g(H,U,f)=  0.232E-08 0.318E-09 0.166E-11 ort(H,U,f) =-0.471E-08-0.181E-08 0.590E-11
DMP:   5    -0.295718441603E+03   -0.59431E-08   -0.61690E-10   360   0.264E-08-0.651E-08
 final diagonalization
 p_tot=(  0.875E-06  0.875E-06  0.875E-06 )
       N       E                     dE             d eps       ncg     rms          rms(c)
 p_tot=(  0.875E-06  0.875E-06  0.875E-06 )
dp_tot=(  0.000E+00  0.000E+00  0.000E+00 )  diag[e(oo)]=(    ---      ---    1.00000 )
 gam= 0.000 g(H,U,f)=  0.149E-04 0.000E+00 0.000E+00 ort(H,U,f) = 0.000E+00 0.000E+00 0.000E+00
SDA:   1    -0.295718441612E+03   -0.14804E-07   -0.59582E-05   360   0.149E-04 0.000E+00
      ...         ...                ...
      ...         ...                ...
 gam= 0.519 g(H,U,f)=  0.392E-07 0.000E+00 0.000E+00 ort(H,U,f) = 0.919E-08 0.000E+00 0.000E+00
DMP:   9    -0.295718447444E+03   -0.21085E-07   -0.17608E-07   360   0.392E-07 0.919E-08
 p_tot=(  0.868E-06  0.868E-06  0.116E-02 )
dp_tot=( -0.721E-08 -0.723E-08  0.116E-02 )  diag[e(oo)]=(    ---      ---    1.91593 )
 gam= 0.519 g(H,U,f)=  0.210E-07 0.000E+00 0.000E+00 ort(H,U,f) =-0.164E-08 0.000E+00 0.000E+00
DMP:  10    -0.295718447453E+03   -0.83301E-08   -0.80481E-08   360   0.210E-07-0.164E-08
 final diagonalization
 p_tot=(  0.860E-06  0.860E-06  0.118E-02 )
dp_tot=( -0.154E-07 -0.155E-07  0.118E-02 )  diag[e(oo)]=(    ---      ---    1.92723 )
   1 F= -.29571845E+03 E0= -.29571845E+03  d E =-.223452E-12
```

where one can discern three distinct blocks of SCF iterations. The first one (steps marked with DAV) corresponds to the calculation of the zero-field groundstate. After this groundstate has been reached, the **k**-point mesh is regenerated using a set of symmetry operations, which takes into account that the symmetry of the system is possibly reduced by the applied electric field. In most cases the new set of **k**-points is larger than the original one. The orbitals at the additional **k**-points are generated from their symmetry equivalent counterparts in the zero-field case. This expanded set of orbitals is now reoptimized until convergence is better than EDIFF/100 (the second block, marked DMP), and the initial electronic polarization is computed.

Then the electric field is switched on, and the field-polarized groundstate is calculated. This is the last block of steps marked with DMP. From the change in the electronic dipole moment due to the electric field VASP computes (part of) the components on the diagonal of the ion-clamped static dielectric tensor.

This information is found both in the OUTCAR file and on stdout:

```
   diag[e(oo)]=(       ----        ----      1.92723 )
```

---

To speed up the computation of the field-polarized groundstate one may set SKIP\_EDOTP=.TRUE. to avoid the recalculation of the electronic polarization at each iteration during the SCF procedure.
However, the additional term in Hamiltonian (second term on the right-hand-side of the electric enthalpy functional) has to be correctly included and can not be kept fixed.
Basically this means one does not minimize the total energy but optimizes the orbitals until a stationary point is reached. A stationary point is considered to be reached as soon as the norm of the gradient on the orbitals is smaller than EDIFF/100, and the SCF procedure will stop.
In the case of the previous example this will lead to:

```
       N       E                     dE             d eps       ncg     rms          rms(c)
 gam= 0.000 g(H,U,f)=  0.149E-04 0.000E+00 0.000E+00 ort(H,U,f) = 0.000E+00 0.000E+00 0.000E+00
SDA:   1    -0.295718441603E+03   -0.60750E-08   -0.59581E-05   360   0.149E-04 0.000E+00
 gam= 0.519 g(H,U,f)=  0.332E-05 0.000E+00 0.000E+00 ort(H,U,f) = 0.629E-05 0.000E+00 0.000E+00
      ...         ...                ...
      ...         ...                ...
 gam= 0.519 g(H,U,f)=  0.124E-07 0.000E+00 0.000E+00 ort(H,U,f) =-0.141E-08 0.000E+00 0.000E+00
DMP:  11    -0.295718435607E+03    0.13956E-06   -0.46725E-08   360   0.124E-07-0.141E-08
 gam= 0.519 g(H,U,f)=  0.637E-08 0.000E+00 0.000E+00 ort(H,U,f) = 0.218E-10 0.000E+00 0.000E+00
DMP:  12    -0.295718435599E+03    0.78403E-08   -0.25522E-08   360   0.637E-08 0.218E-10
 final diagonalization
 p_tot=(  0.844E-06  0.844E-06  0.117E-02 )
dp_tot=( -0.313E-07 -0.313E-07  0.117E-02 )  diag[e(oo)]=(    ---      ---    1.92478 )
   1 F= -.29571844E+03 E0= -.29571844E+03  d E =-.223448E-12
```

## Related tags and articles

SKIP\_EDOTP,
LCALCPOL,
LCALCEPS,
LPEAD,
IPEAD,
LBERRY,
IGPAR,
NPPSTR,
DIPOL,
Berry phases and finite electric fields

Examples that use this tag

## References

---
