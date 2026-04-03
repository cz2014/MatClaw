# Nonlocal vdW-DF functionals

Categories: Exchange-correlation functionals, Van der Waals functionals, Howto

The vdW-DF method originally proposed by Dion *et al.* consists of a semilocal or hybrid exchange-correlation functional $E\_{\text{xc}}^{\text{SL/hybrid}}$ that is augmented with a nonlocal correlation functional $E\_{\text{c,disp}}$ that approximately accounts for dispersion interactions:

:   $$E\_{\text{xc}}^{\text{vdW}} = E\_{\text{xc}}^{\text{SL/hybrid}} + E\_{\text{c,disp}},$$

where

:   $$E\_{\text{c,disp}} = \frac{1}{2}\int\int n(\textbf{r})
    \Phi\left(\textbf{r},\textbf{r}'\right) n(\textbf{r}')
    d^{3}rd^{3}r',$$

with a kernel $\Phi$ that depends on the electronic density $n$, its derivative $\nabla n$ as well as on the interelectronic distance $\left\vert\bf{r}-\bf{r}'\right\vert$. In VASP, the calculation of $E\_{\text{c,disp}}$ is done using the algorithm of Román-Pérez and Soler that is based on FFTs and the convolution theorem to calculate efficiently the double real-space integral. Several versions of the vdW-DF functionals proposed in the literature can be used (see list below).

The vdW-DF functionals are available since the 5.2.12.26May2011 version of VASP for the calculation of total energies and forces. The stress tensor calculation for the cell optimization (ISIF=3) is available since the VASP 5.2.12.11Nov2011 version for spin-unpolarized systems and VASP 5.3.1 for spin-polarized systems. They have been implemented by J. Klimeš. If you make use of the vdW-DF functionals presented in this section, we ask you to cite Ref. . Please also cite the original vdW-DF paper of Dion *et al.* and the paper of Román-Pérez and Soler.

In versions of VASP prior to 6.4.0, a meta-GGA functional (e.g., SCAN) could be combined only with the rVV10 nonlocal functional. Conversely, a GGA functional could be combined only with the original nonlocal functional of Dion *et al.*. This restriction is lifted since VASP.6.4.0 thanks to the introduction of the IVDW\_NL tag. Since VASP.6.4.0, the spin-polarized formulation of the nonlocal vdW correlation term is available. It can be switched on with the logical tag LSPIN\_VDW (.FALSE. by default), however its use is limited to the the functional of Dion *et al.* (not available for rVV10) and only when the nonlocal term is combined with a GGA functional. In other cases (and in prior versions of VASP), the nonlocal correlation functional is evaluated with the sum of the spin-up and spin-down electron densities.

An overview of the performance of the vdW-DF functionals can be found for instance in Ref. .

> **Important:** Some nonlocal vdW-DF result in very noisy energies, which can degrade the convergence to the electronic groundstate. Conjugate-gradient algorithms are particularly prone to show issues, such as a sudden increase in the energy. If ALGO = all (conjugate gradient algorithm) fails to converge, try to use denser FFT grids, for instance by setting PREC = Accurate.

> **Mind:**
>
> * For **VASP.6.4.2** and prior versions it was necessary to copy the vdw\_kernel.bindat file into the working directory for calculations with the van der Waals kernel corresponding to IVDW\_NL=1. Otherwise, vdw\_kernel.bindat was generated at the beginning of the calculation, which took several hours. However, since **VASP.6.4.3** it is not really necessary to copy vdw\_kernel.bindat into the directory, since its calculation has been considerably accelerated (about 2 minutes with 8 MPI ranks). More details are given below. Note that no vdw\_kernel.bindat file is needed for calculations with the rVV10 kernel (IVDW\_NL=2).
> * In VASP.6.2 (and prior versions) the stress tensor is broken for rVV10 (it is correct for other vdW-DF though). From VASP.6.3.0 onwards, the stress tensor for rVV10 is correct.

## List of nonlocal vdW-DF functionals

* To add a nonlocal correlation energy $E\_{\text{c,disp}}$ to the semilocal or hybrid exchange-correlation energy (selected with the GGA, METAGGA or XC tag) one needs to set LUSE\_VDW=.TRUE. (and optionally IVDW\_NL) in the INCAR file.

* Since vdW-DF functionals tend to yield less spherical densities than standard GGA functionals, it is recommended to set LASPH=.TRUE. to get reasonably accurate contributions from the spheres around the atoms.

Examples of INCAR files are shown below.

* **vdW-DF** of Dion *et al.*:

```
GGA       = RE
AGGAC     = 0.0
LUSE_VDW  = .TRUE.
LASPH     = .TRUE.
```

* **vdW-DF2** of Lee *et al.* (2nd version of vdW-DF):

```
GGA       = ML
AGGAC     = 0.0
LUSE_VDW  = .TRUE.
ZAB_VDW   = -1.8867 # the default is -0.8491
LASPH     = .TRUE.
```

* **optPBE-vdW** of Klimeš *et al.*:

```
GGA       = OR
AGGAC     = 0.0
LUSE_VDW  = .TRUE.
LASPH     = .TRUE.
```

* **optB88-vdW** of Klimeš *et al.*:

```
GGA       = BO
PARAM1    = 0.1833333333
PARAM2    = 0.22
AGGAC     = 0.0
LUSE_VDW  = .TRUE.
LASPH     = .TRUE.
```

* **optB86b-vdW** of Klimeš *et al.*:

```
GGA       = MK
PARAM1    = 0.1234 
PARAM2    = 1.0
AGGAC     = 0.0
LUSE_VDW  = .TRUE.
LASPH     = .TRUE.
```

* **BEEF-vdW** of Wellendorff *et al.*:

```
GGA       = BF
LUSE_VDW  = .TRUE.
ZAB_VDW   = -1.8867 # the default is -0.8491
LASPH     = .TRUE.
```

or

```
GGA       = LIBXC
LIBXC1    = GGA_XC_BEEFVDW
LUSE_VDW  = .TRUE.
ZAB_VDW   = -1.8867 # the default is -0.8491
LASPH     = .TRUE.
```

Note that the GGA functional BEEF is available only via an external library, either libbeef (-Dlibbeef) or Libxc (-DUSELIBXC).

* **rev-vdW-DF2** (also known as vdW-DF2-B86R) of Hamada:

```
GGA       = MK
PARAM1    = 0.1234568 # =10/81
PARAM2    = 0.7114
AGGAC     = 0.0
LUSE_VDW  = .TRUE.
ZAB_VDW   = -1.8867 # the default is -0.8491
LASPH     = .TRUE.
```

In the vdW-DF2, BEEF-vdW and rev-vdW-DF2 functionals, the nonlocal correlation consists of the Dion *et al.* functional, but with the parameter $Z\_{ab}$ that is changed from -0.8491 (the default value in VASP) to -1.8867 by setting ZAB\_VDW=-1.8867.

* **vdW-DF-cx** of Berland and Hyldgaard:

```
GGA       = CX
AGGAC     = 0.0
LUSE_VDW  = .TRUE.
LASPH     = .TRUE.
```

* **vdW-DF3-opt1** of Chakraborty *et al.* :

```
GGA       = BO
PARAM1    = 0.1122334456
PARAM2    = 0.1234568 # =10/81
AGGAC     = 0.0
LUSE_VDW  = .TRUE.
IVDW_NL   = 3
ALPHA_VDW = 0.94950 # default for IVDW_NL=3 but can be overwritten by this tag
GAMMA_VDW = 1.12    # default for IVDW_NL=3 but can be overwritten by this tag
LASPH     = .TRUE.
```

* **vdW-DF3-opt2** of Chakraborty *et al.* :

```
GGA       = MK
PARAM1    = 0.1234568 # =10/81
PARAM2    = 0.58
AGGAC     = 0.0
LUSE_VDW  = .TRUE.
IVDW_NL   = 4
ZAB_VDW   = -1.8867 # the default is -0.8491
ALPHA_VDW = 0.28248 # default for IVDW_NL=4 but can be overwritten by this tag
GAMMA_VDW = 1.29    # default for IVDW_NL=4 but can be overwritten by this tag
LASPH     = .TRUE.
```

* **rVV10** of Sabatini *et al.* :

```
GGA       = ML
LUSE_VDW  = .TRUE.
IVDW_NL   = 2
BPARAM    = 6.3     # default but can be overwritten by this tag
CPARAM    = 0.0093  # default but can be overwritten by this tag
LASPH     = .TRUE.
```

* **SCAN+rVV10** of Peng *et al.* :

```
METAGGA   = SCAN
LUSE_VDW  = .TRUE.
BPARAM    = 15.7    # the default value is 6.3
CPARAM    = 0.0093  # default but can be overwritten by this tag
LASPH     = .TRUE.
```

* **PBE+rVV10L** of Peng and Perdew :

```
GGA       = PE
LUSE_VDW  = .TRUE.
BPARAM    = 10      # the default value is 6.3
CPARAM    = 0.0093  # default but can be overwritten by this tag
LASPH     = .TRUE.
```

* **r$^2$SCAN+rVV10** of Ning *et al.* :

```
METAGGA   = R2SCAN
LUSE_VDW  = .TRUE.
BPARAM    = 11.95   # the default value is 6.3
CPARAM    = 0.0093  # default but can be overwritten by this tag
LASPH     = .TRUE.
```

## Important technical remarks

### Kernel file vdw\_kernel.bindat

* **Until VASP.6.4.2**: The calculation of the nonlocal correlation functional of Dion *et al.* (used when IVDW\_NL=1, which means for all functionals listed above except rVV10, SCAN+rVV10 and r$^2$SCAN+rVV10) requires a precalculated kernel which is distributed via the VASP download portal (vdw\_kernel.bindat.gz has to be decompressed). If VASP does not find this file, the kernel is calculated, which is however extremely demanding (several hours!). Thus, the kernel needs to be either copied to the VASP run directory for each calculation or can be stored in a central location and read from there. The location needs to be set in routine *PHI\_GENERATE*. This does not work on some clusters and the kernel needs to be copied into the working directory in such cases. The distributed file uses little endian convention and can not be read on big endian machines. The big endian version of the file is available also from the VASP portal. In the case of the rVV10 nonlocal correlation functional, no precalculated kernel is required and it is calculated on the fly, which is however much less demanding than in the case of the functional of Dion *et al.*.
* **Since VASP.6.4.3**: The calculation of the kernel for the functional of Dion *et al.* (IVDW\_NL=1), as well as for IVDW\_NL=3 and 4, is tremendously faster: the default value of a parameter has been reduced (with basically no loss of accuracy) and the calculation has been parallelized (with MPI and OpenACC for GPUs). Therefore, starting a calculation without vdw\_kernel.bindat file present in the directory should be no problem for the computational time, and a vdw\_kernel.bindat file will be generated rather efficiently during the first iteration. Note that a file vdw\_kernel.bindat that was generated for a given kernel (IVDW\_NL=1, 3 or 4) can not be used for a calculation using another kernel, and in such a case the incompatibility of the vdw\_kernel.bindat file will be detected and a new vdw\_kernel.bindat file automatically generated to replace the incompatible one.

### POTCAR file

* There are no special POTCAR files for the vdW-DF functionals and the PBE or LDA POTCAR files can be used. Currently the evaluation of the nonlocal correlation functional is not done fully within the PAW method, but the sum of the pseudo-valence density and partial core density is used. This approximation works rather well, as is discussed in , and the accuracy generally increases when the number of valence electrons is increased or when harder PAW datasets are used. For example, for adsorption it is recommended to compare the adsorption energy obtained with standard PAW datasets and more-electron POTCAR files for both PBE calculations and vdW-DF calculations to assess the quality of the results.

### Computational time

* The evaluation of the nonlocal correlation energy requires some additional time. Most of it is spent on performing FFTs to evaluate the energy and potential. Thus the additional time is determined by the number of FFT grid points, basically the size of the simulation cell. It is almost independent on the number of the atoms in the cell, but increases with the amount of vacuum in the cell. The relative increase is high for isolated molecules in large cells, but small for solids in smaller cells with many k-points.

## Related Tags and Sections

LUSE\_VDW, IVDW\_NL, LSPIN\_VDW, ZAB\_VDW, ALPHA\_VDW, GAMMA\_VDW, BPARAM, CPARAM, GGA, AGGAC, PARAM1, PARAM2, METAGGA

See also the alternative atom-pairwise and many-body dispersion methods: IVDW

## References

---
