# Calculation of atoms

Categories: Atoms and Molecules, Howto

The following files are needed for the calculation of atoms

* INCAR
* POSCAR
* POTCAR
* KPOINTS

Before using a pseudopotential intensively it is not only necessary to check it in different bulk phases but the pseudopotential should also reproduce exactly the eigenvalues and the total energy of the free atom for which it was created. If energy cutoff and cell size are sufficient, the agreement between the atomic reference calculation and a calculation using VASP is normally better than 1 meV. Calculations for an atom are relatively fast and unproblematic in most cases.

For the calculation only the $\Gamma$ point should be used i.e. the KPOINTS file should have the following contents:

```
Monkhorst Pack
0
Monkhorst Pack
 1  1  1
 0  0  0
```

The size of the cell depends on the element in question. Some values for reliable results are compiled in Tab. 1.

:   |  |  |  |  |  |
    | --- | --- | --- | --- | --- |
    |  | Cellsize | | | |
    | Aluminum | 14 $\AA$ |
    | Potassium | 12 $\AA$ |
    | Copper, Rhodium, Palldium ... | 10 $\AA$ |
    | Nitrogen | 7 $\AA$ |
    | Carbon | 8 $\AA$ |
    *Tab. 1: Typical convenient settings for the cellsize for a calculation of atoms.*

A simple cubic cell can be often enough but it is usually recommended to use nearly cubic cells with minimal orthorombic distortion. This can be important for some atoms due to higher degrees of freedom for relaxation. An example POSCAR file should look like:

```
atom
1
     10.00000    .00000    .00000
       .00000  10.00100    .00000
       .00000    .00000  10.00200
   1
cart
 0    0    0
```

Due to the large cell NGX, NGY, NGZ and NGXF, NGYF, NGZF need to be increased. This can be most easily achieved by setting PREC=*Accurate* or PREC=*High*.

The INCAR file can be very simple:

```
SYSTEM = Pd: atom
#Electronic minimisation
  ENCUT  = 200.00 eV  #energy cut-off for the calculation
  EDIFF  =   1E-04    #stopping-criterion for ELM
  NELMDL =  5

#Ionic parameters
  POMASS = 106.42     #mass (not really used in this case)
  ZVAL   =  10.00     #valence

#DOS related values
  ISMEAR =    0
  SIGMA = 0.1   #use smearing method
```

The only difference to the bulk calculation is that Gaussian smearing must be used now. You might set SIGMA to a very small value; this is necessary if atomic orbitals are almost degenerated. Another important point is spin polarization which can also lead to different energies in many cases. To turn on spin polarization additionally set ISPIN=2 in the INCAR file.

**Mind**: Look at the right value for the energy. It is **not** $F=E+ \sigma S$, which contains a "meaningless" entropy term, but the energy $E$. If SIGMA is very small both values are the same, but for extremely small SIGMA values VASP might have difficulties to converge to the correct atomic ground state.

On the start of an atomic calculation it is useful to delay the charge mixing for a large number of steps (in the example INCAR file above 5 steps by specifying NELMDL=5) because the initial charge density corresponds already to the atomic charge density for which the pseudopotential was generated. It is also convenient to perform a calculation for a fixed atomic charge density (ICHARG=12) as a first test. In some rare cases the real LDA ground state might differ from the configuration for which the pseudopotential was generated. For the atomic all electron reference calculation the occupancies are set by hand (for Pd $s^1d^9$ was chosen to be the reference configuration, which is not the LDA ground state of the atom). In this case it is necessary
to set the occupancies for VASP also by hand. This can be done by including the following lines in the INCAR file:

```
 ISMEAR = -2
 FERWE  =  5*0.9  0.5
```

(5\*0.9 is interpreted as 0.9 0.9 0.9 0.9 0.9). To find out the ordering of the eigenvalues it might be necessary to perform a calculation with ICHARG=12 (i.e. fixed atomic charge density), or have a look on the information supplied with your pseudopotential. After a successful atomic calculation compare the differences between the eigenvalues with those obtained by the pseudopotential generation program. Also check the total energy, the differences should be smaller than 20 meV.

'*Mind*:} We have found that the size of the cell can be reduced if one special point is used instead of the $\Gamma$ point, i.e. if the KPOINTS file has the following contents:

```
Monkhorst Pack
0
Monkhorst Pack
 2  2  2
 0  0  0
```

The reasons for this behaviour are: Due to the finite size of the cell a band dispersion exists i.e. the atomic eigenvalues split and form a band with finite width. To first order the center of the band lies exactly at the position of the atomic eigenvalues. Using the $\Gamma$-point the eigenvalues at the bottom of the band are obtained. If the special point (0.25,0.25,0.25) 2$\pi/a$ is used instead of the $\Gamma$-point, the energy of the center of the band is obtained. Nevertheless we recommend this setting only for absolute experts: in most cases the degeneracy of the p- and d-orbitals is removed and only the mean value of the eigenvalues remains physically significant. In this cases it is also necessary to increase SIGMA or to set the partial occupancies by hand!

## Determining the groundstate energy of atoms

The POTCAR file contains information on the energy of the atom in the reference configuration (i.e. the configuration for which the pseudopotential was generated). Total energies calculated by VASP are with respect to this configuration. The reference calculation, however, did not allow for spin-polarisation or broken symmetry solutions, which usually lower the energy for gradient corrected of hybrid functionals. To include these effects properly, it is required to calculate the lowest energy magnetic groundstate using VASP.

Unfortunately convergence to the symmetry broken spin polarized groundstate can be relatively slow in VASP. The following INCAR file worked reasonably well for most elements:

```
ISYM = 0      # no symmetry
ISPIN = 2     # allow for spin polarisation
VOSKOWN = 1   # this is important, in particular for GGA
                        # but not required for PBE potentials
ISMEAR = 0    # Gaussian smearing, otherwise negative occupancies might come up
SIGMA = 0.002 # tiny smearing width to safely break symmetry
AMIX = 0.2    # mixing set manually
BMIX = 0.0001  
NELM = 100    # often many steps are required
ICHARG = 1
```

Execute VASP twice to three times, consecutively with this input file until energies are converged. Furthermore, we recommend to use large slightly non-cubic cells, i.e. $12.000$ $\AA$ $\times$ $12.001$ $\AA$ $\times$ $12.002$ $\AA$. In some cases, we also found it advantageously to use direct energy minimization instead of charge-density mixing

```
ALGO = D 
LSUBROT = .FALSE. 
NELM = 500 
TIME = 0.2
```

or

```
ALGO = A 
LSUBROT = .FALSE. 
NELM = 500 
TIME = 0.2
```

Always check for convergence, and whether all occupancies are 0 or 1.

---
