# I_CONSTRAINED_M

Categories: INCAR tag, Magnetism

I\_CONSTRAINED\_M = 1 | 2 | 4  
 Default: **I\_CONSTRAINED\_M** = none

Description: I\_CONSTRAINED\_M switches on the constrained local moments approach.

---

VASP offers the possibility to add a penalty contribution to the total energy expression (and consequently a penalty functional to the Hamiltonian) that drives the local magnetic moment (integral of the magnetization in a site centered sphere of radius RWIGS) into a direction given by the M\_CONSTR-tag.

* I\_CONSTRAINED\_M=1: Constrain the *direction* of the magnetic moments.

:   The total energy is given by

:   :   $$E=E\_0+ \sum\_I\lambda \left[ \vec{M}\_I-\hat{M}^0\_I \left( \hat{M}^0\_I \cdot \vec{M}\_I\right)\right]^2$$

:   where *E*0 is the usual DFT energy, and the second term on the right-hand-side represents the penalty. The sum is taken over all atomic sites *I*, $\hat{M}^0\_I$ is the desired direction (unit vector) of the magnetic moment at site *I* (as specified using M\_CONSTR), and $\vec{M}\_I$ is the integrated magnetic moment inside a sphere Ω*I* (the radius **must** be specified by means of RWIGS) around the position of atom *I*,

:   :   $$\vec{M}\_I=\int\_{\Omega\_I} \vec{m}(\mathbf{r}) F\_I(|\mathbf{r}|) d\mathbf{r}$$

:   where *F**I*(|**r**|) is a function of norm 1 inside Ω*I*, that smoothly goes to zero towards the boundary of Ω*I*.

:   The penalty term in the total energy introduces an additional potential inside the aforementioned spheres centered at the atomic sites *I*, given by

:   :   $$V\_I (\mathbf{r})=2\lambda \left[ \vec{M}\_I-\hat{M}^0\_I \left( \hat{M}^0\_I \cdot \vec{M\_I}\right)\right]
        \cdot \vec{\sigma} F\_I(|\mathbf{r}|)$$

:   where $\vec{\sigma}=(\sigma\_x,\sigma\_y,\sigma\_z)$ are the Pauli spin-matrices.

* I\_CONSTRAINED\_M=2: Constrain the *size and direction* of the magnetic moments.

:   The total energy is given by

:   :   $$E=E\_0+ \sum\_I\lambda \left( \vec{M}\_I-\vec{M}^0\_I \right)^2$$

:   where $\vec{M}^0\_I$ is the desired magnetic moment at site *I* (as specified using M\_CONSTR).
:   The additional potential that arises from the penalty contribution to the total energy is given by

    :   $$V\_I (\mathbf{r})=2\lambda \left( \vec{M}\_I-\vec{M}^0\_I \right)\cdot \vec{\sigma} F\_I(|\mathbf{r}|)$$

* I\_CONSTRAINED\_M=4: Constrain the *direction and sign* of the magnetic moments, available since VASP.6.4.0.

:   The total energy is given by

:   :   $$E=E\_0+ \sum\_I\lambda \left( |\vec{M}\_I| - \hat{M}^0\_I \cdot \vec{M}\_I\right)$$

:   where $\hat{M}^0\_I$ is the desired magnetic moment at site *I* (as specified using M\_CONSTR).
:   The additional potential that arises from the penalty contribution to the total energy is given by

    :   $$V\_I (\mathbf{r})=\lambda \left( \hat{M}\_I-\hat{M}^0\_I \right)\cdot \vec{\sigma} F\_I(|\mathbf{r}|)$$
:   where $\hat{M}\_I$ denotes the unit vector in $\vec{M}\_I$ direction.

The weight λ, with which the penalty terms enter into the total energy expression and the Hamiltonian in the above is specified through the LAMBDA tag.

As is probably clear from the above, applying constraints by means of a penalty functional contributes to the total energy. This contribution, however, decreases with increasing LAMBDA and can in principle be made vanishingly small . Increasing LAMBDA stepwise, from one run to another (slowly so the solution remains stable) one thus converges towards the DFT total energy for a given magnetic configuration.

---

When one uses the constrained moment approach, additional information pertaining to the effect of the constraints is written into the OSZICAR file:

```
 E_p =  0.36856E-07  lambda =  0.500E+02
<lVp>=  0.30680E-02
 DBL = -0.30680E-02
 ion        MW_int                 M_int
  1 -0.565  0.000  0.000   -0.770  0.000  0.000
  2  0.565  0.000  0.000    0.770  0.000  0.000
  3 -0.565  0.000  0.000   -0.770  0.000  0.000
  4  0.565  0.000  0.000    0.770  0.000  0.000
DAV:   8    -0.133293620177E+03    0.15284E-05   -0.29410E-08  4188   0.144E-03    0.119E-04
```

E\_p is the contribution to the total energy arising from the penalty functional. Under M\_int VASP lists the integrated magnetic moment at each atomic site. The column labeled MW\_int shows the result of the integration of magnetization density which has been smoothed towards the boundary of the sphere. It is actually the smoothed integrated moment which enters in the penalty terms (the smoothing ensures that the total local potential remains continuous at the sphere boundary). One should look at the latter numbers to check whether enough of the magnetization density around each atomic site is contained within the integration sphere and increase RWIGS accordingly. What exactly constitutes "enough" in this context is hard to say. It is best to set RWIGS in such a manner that the integration spheres do not overlap and are otherwise as large as possible.

```
DAV:   9    -0.133293621087E+03   -0.91037E-06   -0.18419E-08  4188   0.104E-03
   1 F= -.13329362E+03 E0= -.13329362E+03  d E =0.000000E+00  mag=     0.0000     0.0000     0.0000

 E_p =  0.36600E-07  lambda =  0.500E+02
 ion             lambda*MW_perp
  1  -0.67580E-03  -0.12424E-22  -0.88276E-23
  2   0.67580E-03   0.14700E-22  -0.24744E-22
  3  -0.67790E-03  -0.82481E-23  -0.19834E-22
  4   0.67790E-03   0.15710E-23   0.34505E-22
```

Under lambda\*MW\_perp the constraining "magnetic field" at each atomic site is listed. It shows which magnetic field is added to the DFT Hamiltonian to stabilize the magnetic configuration.

## Related tags and articles

M\_CONSTR,
LAMBDA,
RWIGS,
LNONCOLLINEAR

Examples that use this tag

---

## References
