# Energy cutoff and FFT meshes

Categories: Howto, Calculation setup

The plane-wave expansion of the Kohn-Sham (KS) orbitals are associated to a mesh to perform FFTs from real space coordinates $\mathbf{r}$ to reciprocal coordinates $\mathbf{G}$ and vice versa. These have a very large impact on the accuracy of any ab-initio calculation particularly including basic electronic minimization calculations.
The so-called FFT mesh and thus basis-set truncation is a result of the selected energy cutoff (ENCUT). It is one of the most important parameters for the accuracy. Some indications and illustrations on how to choose ENCUT or other related tags like PREC are provided below.

# Aspects to refine the choice of the cutoff energy, FFT mesh and related parameters

## Energy cutoff

The energy cutoff (ENCUT) should be chosen according to the pseudopotential (POTCAR)
and required accuracy. The default value for ENCUT is the largest among the **ENMAX** values found
in the POTCAR file. Values smaller than the default should never be used, since
it leads to very large errors. The default minimal value
should usually result in an error in the cohesive energy which is less than 10 meV.

> **Tip:** The recommended procedure for choosing ENCUT is to perform a series of calculations with different ENCUT values (larger than the default one) and to monitor the results for the property of interest.

Regarding the convergence of the total energy with respect to ENCUT,
the distinction between the **total energy** and the **total energy difference**
(e.g., between different geometries during a structure relaxation or of two polymorphs) should be made.
Usually, the total energy difference converges much faster than the total energies.
This is especially true if both geometries are rather similar (e.g., structure relaxation),
and in this case the errors due to the finite energy cutoff should to some extent cancel each other when
calculating the energies difference. However, if two configurations differ strongly from each other,
e.g. for the calculation of the cohesive energy (bulk versus atom), the convergence of the energies difference with
respect to ENCUT may be quite slow.

> **Important:** We strongly recommend specifying the energy cutoff (ENCUT) always manually in the INCAR file to ensure the same accuracy between calculations. Otherwise, the default ENCUT may differ among the different calculations if other atomic species are present, with the consequence that the total energies can not be compared.

## FFT mesh

There are a number of quantities, e.g., the Kohn-Sham orbitals, the charge density, magnetization, XC potential, etc. that are described on a real-space mesh in the unit cell. Depending on the relation of the specific quantity to the KS orbitals the real-space mesh and associated FFT mesh must be choosen denser.

### Mesh for the KS orbitals (soft mesh or coarse mesh)

The FFT mesh for the KS orbitals is the so-called coarse or soft mesh. The size of the coarse FFT mesh (NGX,NGY,NGZ) is determined by ENCUT and PREC. NGX, NGY and NGZ can also be set manually.

In order to avoid wrap-around errors the FFT mesh should contain all wave vectors up to $2G\_{\rm cut}$, where $G\_{\rm cut}$ is defined by

:   $$E\_{\rm cut}=\frac{\hbar^2}{2m\_e}G\_{\rm cut}^2$$

with $E\_{\rm cut}$=ENCUT.
It is not always possible or necessary to use such a large FFT mesh for the KS orbitals, particularly during the test phase where a lower accuracy may surfize while other parameters of the calculation are varied and adjusted.
Usually, only high-quality calculations require a mesh that avoids
any wrap-around error. Such calculations can be done with `PREC = Accurate`.

For most calculations, and in particular with standard pseudopotentials with their default cutoff energies,
it is sufficient to choose NGX, NGY and NGZ to $3/4$ of the required values to
avoid most wrap-around errors, i.e., to include only the wave vectors up to $(3/2)G\_{\rm cut}$.
This is the case when PREC=Normal, which is the default.

If NGX, NGY and NGZ are set manually to values that may lead to sizeable wrap-around errors,
a warning will be printed in OUTCAR (search for the string 'wrap').

A hint that the wrap-around errors may be too large is given by the forces.
If there is a considerable drift in the forces, the FFT mesh should be increased.
Search for the string 'total drift' in the OUTCAR file that is located beneath the line *TOTAL-FORCE*:

```
    total drift:                               -0.002730      0.010480      0.038560
```

The drift should definitely not exceed the magnitude of the forces,
in general it should be smaller than the size of the
forces you are interested in (usually 0.1 eV/Å).

### Mesh for the densities (fine mesh)

For the representation of the charge density, which contains the KS orbitals to the power of 2, and other quantities like the augmentation charges a second finer FFT mesh
(NGXF,NGYF,NGZF) is used.
With PREC=Normal and Accurate, this fine grid has a size
(NGXF,NGYF,NGZF)=$2\times$(NGX,NGY,NGZ),
twice larger than the coarse grid.
NGX, NGY and NGZ can also be set manually.

The drift in the forces, for instance, may also be reduced by increasing the number of points
of the fine mesh.

Note that the ENAUG tag can also be used to set the size of the fine mesh,
however this tag is **deprecated** and should not be used anymore.
Furthermore, it is active only with the **deprecated** settings `PREC = Low, Medium or High`; otherwise it is ignored.

### Support grid

For `ADDGRID = True`, an additional 'support' grid is used for the evaluation of the augmentation charges.
This grid has a size of $2\times$(NGXF,NGYF,NGZF), i.e., it has twice more points that the fine grid along each lattice vector. The support grid often helps to reduce the noise in the forces, however as explained in more detail in the documentation of ADDGRID it should be used with caution.

# Example: volume relaxation and pressure

An illustration of the effect of the energy cutoff (ENCUT) on the results is given for the equilibrium volume and pressure of diamond. It clearly shows the noise induced by using an unconverged value for ENCUT. See the how-to pages on volume relaxation and avoiding Pulay stress.

## Related tags and articles

ENCUT,
PREC,
ADDGRID,
ENAUG,
NGX,
NGY,
NGZ,
NGXF,
NGYF,
NGZF

Projector-augmented-wave formalism, wrap-around errors, volume relaxation, Pulay stress
