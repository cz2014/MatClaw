# Interface pinning calculations

Categories: Advanced molecular-dynamics sampling, Howto

**Interface pinning** uses the $Np\_zT$ ensemble where the barostat only acts along the $z$ direction.
This ensemble uses a Langevin thermostat and a Parrinello-Rahman barostat with lattice constraints in the remaining two dimensions.
The solid-liquid interface must be in the $x$-$y$ plane perpendicular to the action of the barostat.

Set the following tags for the **interface pinning** method:

OFIELD\_Q6\_NEAR
:   Defines the near-fading distance $n$.

OFIELD\_Q6\_FAR
:   Defines the far-fading distance $f$.

OFIELD\_KAPPA
:   Defines the coupling strength $\kappa$ of the bias potential.

OFIELD\_A
:   Defines the desired value of the order parameter $A$.

The following example INCAR file calculates the interface pinning in sodium:

```
TEBEG = 400                   # temperature in K
POTIM = 4                     # timestep in fs
IBRION = 0                    # run molecular dynamics
ISIF = 3                      # use Parrinello-Rahman barostat for the lattice
MDALGO = 3                    # use Langevin thermostat
LANGEVIN_GAMMA_L = 3.0        # friction coefficient for the lattice degree of freedoms (DoF)
LANGEVIN_GAMMA = 1.0          # friction coefficient for atomic DoFs for each species
PMASS = 100                   # mass for lattice DoFs
LATTICE_CONSTRAINTS = F F T   # fix x-y plane, release z lattice dynamics
OFIELD_Q6_NEAR = 3.22         # near fading distance for function w(r) in Angstrom
OFIELD_Q6_FAR = 4.384         # far fading distance for function w(r) in Angstrom
OFIELD_KAPPA = 500            # strength of bias potential in eV/(unit of Q)^2
OFIELD_A = 0.15               # desired value of the Q6 order parameter
```

## References

---
