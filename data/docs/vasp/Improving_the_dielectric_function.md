# Improving the dielectric function

Categories: Examples

Overview > Dielectric properties of Si using BSE > Improving the dielectric function  > Plotting the BSE fatband structure of Si > List of tutorials

## Task

Calculate the dielectric function of Si using an averaging over multiple grids or a model-BSE to improve k-sampling in BSE calculations.

## Input

```
Si
 5.4300
0.5 0.5 0.0
0.0 0.5 0.5
0.5 0.0 0.5
2
cart
0.00 0.00 0.00 
0.25 0.25 0.25
```

### INCAR

* This is the INCAR file for the basic DFT calculation:

```
System  = Si
PREC = Normal ; ENCUT = 250.0
ISMEAR = 0 ; SIGMA = 0.01
KPAR = 2
EDIFF = 1.E-8
```

### KPOINTS

```
Automatic
 0
Gamma
 4 4 4 
 0 0 0
```

## Calculation

The calculated spectra can be improved in two ways:

* Averaging over multiple grids:

:   Compute *N* independent dielectric functions using BSE (or any other method), using *shifted* grids of **k**-points, and take the average over the results.

* Model-BSE:

:   Use a parametrized model for the dielectric screening, and DFT eigenenergies moved with a *scissor* operator, instead of RPA screening and GW quasiparticle energies.

### Averaging over multiple grids

* Construct shifted k-point grid with the same density.
* $n\times n\times n$ k-point grid $\rightarrow$ $X\_{n}$ irreducible k-points ${K\_{n}}$ with weights $W\_{n}$. We do $x\_{n}$ calculations on a $m\times m\times m$ grid, shifted of Gamma by $K\_{n}$.
* Extract the dielectric function of each calculation and average over them with respect to the weights $W\_{n}$:

We have now effectively constructed the result for a $(n\times m) \times (n\times m) \times (n\times m)$ grid. But interactions of range longer than $m$ times the supercell size have been ignored.

* In our example we use $n=4$ and $m=4$: Effectively we use $16\times 16\times 16$ k-points.

* In the script *doall-average.sh* the scheme is written for $n=4$ and $n=\textrm{\$NKPT}$. At the end the dielectric functions are extracted and averaged accordingly. You can choose up to which level of theory (DFT, RPA, BSE) the dielectric function is computed by commenting out the corresponding lines in the script (default is all the way up to BSE).
* Because of the shifted grids we have to use density functional perturbation theory to calculate the derivatives of the wave functions with respect to $\mathbf{k}$ and not the finite difference scheme. We also have to switch off all k-points symmetry in all INCAR files. These two important parameters look like the following in the INCAR file:

```
PREC = Normal ; ENCUT = 250.0
 
ALGO = EXACT ; NELM = 1
ISMEAR = 0 ; SIGMA = 0.01
KPAR = 2

NBANDS = 32 # The number of bands in the consecutive BSE calculation should be the same!  
LOPTICS = .TRUE.; LPEAD = .FALSE.
ISYM = -1
OMEGAMAX = 40
```

* Finally the averaging over multiple grids should should give spectra that are in much closer agreement than the calculations using $4\times 4\times 4$ k-points:

### Model-BSE

The dielectric function $\epsilon^{-1}\_{\mathbf{G},\mathbf{G'}} (\mathbf{q})$ is replaced by the local model function:

:   ${\varepsilon}\_{\mathbf{G},\mathbf{G}}^{-1}(\mathbf{q})=1-(1-{{\varepsilon}\_{\infty}^{-1}})\text{exp}(-\frac{|\mathbf{q+G}|^2}{4{\lambda}^2})$.

This makes the screened Coulomb kernel diagonal $(\mathbf{G}=\mathbf{G'})$ in the screened Coulomb potential:

:   $W^{cv\mathbf{k}}\_{c'v'\mathbf{k}} = \frac{4\pi e^{2}}{\Omega} \sum\limits\_{\mathbf{G}} \frac{\epsilon^{-1}\_{\mathbf{G},\mathbf{G}}(\mathbf{0})}{|\mathbf{G}|^{2}}B^{c\mathbf{k}}\_{c'\mathbf{k}}(\mathbf{G}) [B^{v\mathbf{k}}\_{v'\mathbf{k}}(\mathbf{G})]^\*$,

where $B^{n\mathbf{k}}\_{n'\mathbf{k}}(\mathbf{G})$ denote Bloch integrals of the cell-periodic part of the Bloch waves.

* In addition to a model dielectric function we need approximate quasiparticle energies and wave functions.

:   Approximation:

    * Use DFT single particle eigenvalues + SCISSOR (SCISSOR=GW band gap - DFT band gap).
    * Use DFT single particle orbitals.

* Extract $\mathbf{G}=\mathbf{G'}$ dielectric function from the vasprun.xml file from the previous GW calculation using the script *./extract\_die\_G.sh vasprun.xml > dieG\_g6x6x6-GW0.dat'* or view the attached file *dieG\_g6x6x6-GW0.dat*. Use AEXX=0.088 for $\epsilon^{-1}\_{\infty}$ and HFSCREEN=1.26 for $\lambda$.Then fit the model to get:

* Check the GW+BSE and DFT+mBSE calculations for constistency:

* The sequence of calculations as given in the script *doall-model.sh* consists of two steps:

:   * Step 1: standard DFT calculation. The INCAR file (INCAR.DFT) for this step looks as follows:

```
PREC = Normal ; ENCUT = 250.0
ISMEAR = 0 ; SIGMA = 0.01
EDIFF = 1.E-8
NBANDS = 16
PRECFOCK = Normal
 
#WAVEDER file must be made:
LOPTICS = .TRUE.
LPEAD = .TRUE.
OMEGAMAX = 40
```

:   * Step2: model BSE calculation. The INCAR file (INCAR.mBSE) for this step looks as follows:

```
PREC = Normal ; ENCUT = 250.0
 
ALGO = TDHF
ANTIRES = 0 ; SIGMA = 0.01
ENCUTGW = 150
 
EDIFF = 1.E-8
NBANDS = 16
NBANDSO = 4
NBANDSV = 8
OMEGAMAX = 20

PRECFOCK = Normal

LMODELHF = .TRUE.
HFSCREEN = 1.26
AEXX = 0.088
SCISSOR = 0.69
```

* Finally the result of the DFT+mBSE should be of similar accuracy as the GW+BSE calculations when compared to experiment:

## Download

Si\_improve\_eps.tgz

## References

Overview > Dielectric properties of Si using BSE > Improving the dielectric function  > Plotting the BSE fatband structure of Si > List of tutorials
