# Stochastic boundary conditions

Categories: Molecular dynamics, Advanced molecular-dynamics sampling

In some cases, it is desirable to study the approach of an initially non-equilibrium system to equilibrium. Examples of such simulations include the impact problems when a particle with large kinetic energy hits a surface or calculation of friction force between two surfaces sliding with respect to each other. As shown by Toton *et al.*, this type of problems can be studied using the stochastic boundary conditions (SBC) derived from the generalized Langevin equation by Kantorovich and Rompotis. In this approach, the system of interest is divided into three regions: (a) fixed atoms, (b) the internal (Newtonian) atoms moving according to Newtonian dynamics, and (c) a buffer region of Langevin atoms (*i.e.*, atoms governed by Langevin equations of motion) located between (a) and (b).

The role of the Langevin atoms is to dissipate heat, while the fixed atoms are needed solely to create the correct potential well for the Langevin atoms to move in. The Newtonian region should include all atoms relevant to the process under study: in the case of the impact problem, for instance, the Newtonian region should contain atoms of the molecule hitting the surface and several uppermost layers of the material forming the surface. Performing molecular dynamics with such a setup guarantees that the system (possibly out of equilibrium initially) arrives at the appropriate canonical distribution.

* To run a simulation with stochastic boundary conditions, one has to:

1. Set the standard MD-related tags: IBRION=0, TEBEG, POTIM, and NSW
2. Set ISIF=2
3. Set MDALGO=3 to invoke the Langevin thermostat
4. Prepare the POSCAR file in such a way that the Newtonian and Langevin atoms are treated as different species (even if they are chemically identical). In your POSCAR, use "selective dynamics" and the corresponding logical flags to define the frozen and moveable atoms.
5. Specify friction coefficients γ, for all species in the POSCAR file, by means of the LANGEVIN\_GAMMA-tag: set the friction coefficients to 0 for all fixed and Newtonian atoms, and choose a proper γ for the Langevin atoms.

#### Practical example

Consider a system consisting of 16 hydrogen and 48 silicon atoms. Suppose that eight silicon atoms are considered to be Langevin atoms and the remaining 32 Si atoms are either fixed or Newtonian atoms. The Langevin and Newtonian (or fixed) atoms should be considered as different species, *i.e.*, the POSCAR-file should contain the line like this:

```
Si H Si
40 16 8
```

As only the final eight Si atoms are considered to be Langevin atoms, the INCAR-file should contain the following line defining the friction coefficients:

```
LANGEVIN_GAMMA = 0.0   0.0   10.0
```

*i.e.*, for all non-Langevin atoms, γ should be set to zero.

## References
