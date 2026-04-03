# Born effective charges

Categories: Dielectric properties, Howto

The change in polarization from the displacement of an atom is not uniquely defined in periodic systems, where atoms are repeated in different cells and the charge can be generalized. Born effective charges are one way of defining this dynamical charge.

# Introduction

The dynamical charge is defined as the cell volume **Ω**, multiplied by the partial derivative of the macroscopic polarization **P** in the direction *i* with respect to a rigid displacement of the sublattice of atoms *κ* in the direction *j*.

However, the polarization is not uniquely defined in periodic systems and depends on the macroscopic electric field $\mathcal{E}\_i$ fixed by the periodic boundary conditions. The Born effective charge **Z\*** is the partial derivative of the polarization with respect to position *u* for zero macroscopic electric field. As polarization is the first derivative of the total energy with respect to the macroscopic electric field, **Z\*** may be rearranged in terms of the partial derivative of the force **F** in direction *j* on atom *κ* with respect to $\mathcal{E}\_i$:

:   :   $$Z\_{\kappa,ij}^\*
        =\frac{\Omega}{e} \frac{\partial \mathcal{P}\_i} {\partial u\_{\kappa,j}(\textbf{q=0})}
        =\frac{1}{e} \frac{\partial F\_{\kappa,j}}{\partial \mathcal{E}\_i},
        \qquad
        {i,j=x,y,z}$$

> **Mind:**
>
> * The **\*** does not denote a complex conjugate, **Z\*** is always a real quantity.
> * **Z\*** is given in units of $\vert e \vert$ in VASP.
> * VASP outputs **Z***ij*⋆ with *i* for the macroscopic electric field, and *j* for the direction of the force. In literature, **Z***ji*⋆ is commonly seen, with the force direction *j* followed by the electric field direction *i*. Note, py4vasp follows the latter notation **Z***ji*⋆ for historic reasons.

# How to calculate

There are two ways of computing Born effective charges in VASP. The first is done using LCALCEPS, where a finite electric field is applied along the three cartesian directions and the resultant forces on the atoms are calculated:

```
LCALCEPS = .TRUE.
```

The other approach is done using LEPSILON, where the derivative of the wavefunction with respect to an electric field is calculated using density functional perturbation theory (DFPT):

```
LEPSILON = .TRUE.
```

These may be used in combination with IBRION to obtain additional dielectric properties:

```
IBRION = 5 or 6 ! Calculated using finite differences.
IBRION = 7 or 8 ! Calculated using DFPT
```

For more details, see the pages for each tag. The Born effective charges including local field effects will be given in the OUTCAR file:

```
BORN EFFECTIVE CHARGES (including local field effects) (in |e|, cummulative output)
```

# Excluding local field effects

Previously, the local field effects have been included, that is changes in the orbitals due to the electric field induce changes in the Hartree- and exchange-correlation potentials. This may be limited to changes in the Hartree potential, by specifying:

```
LRPA = .TRUE.
LCALCEPS = .TRUE. ! N.B. LEPSILON does not output the final Born effective charges.
```

This prints out the Born effective charges excluding local field effects:

```
BORN EFFECTIVE CHARGES (excluding local field effects) (in |e|, cummulative output)
```

These are calculated normally but remain hidden unless explicitly specified.

## Related tags and articles

LEPSILON,
LCALCEPS,
IBRION,
LRPA,
Berry phases and finite electric fields

## References
