# Tkatchenko-Scheffler method with iterative Hirshfeld partitioning

Categories: Exchange-correlation functionals, Van der Waals functionals, Theory

The Tkatchenko-Scheffler method, which uses fixed neutral atoms as a reference to estimate the effective volumes of atoms-in-molecule (AIM) and to calibrate their polarizabilities and dispersion coefficients, fails to describe the structure and the energetics of ionic solids. As shown in references and , this problem can be solved by replacing
the conventional Hirshfeld partitioning used to compute properties of interacting atoms by the iterative scheme proposed by Bultinck. In this iterative Hirshfeld algorithm (HI), the neutral reference atoms are replaced with ions with fractional charges determined together with the AIM charge densities in a single iterative procedure. The algorithm is initialized with a promolecular density defined by non-interacting neutral atoms. The iterative procedure then runs in the following steps:

* The Hirshfeld weight function for the step $i$ is computed as

:   $$w\_A^{i}({\mathbf{r}}) = {n^{i}\_A({\mathbf{r}})}/\left({\sum\_B n^{i}\_B({\mathbf{r}})}\right)$$

where the sum extends over all atoms in the system.

* The number of electrons per atom is determined using

:   $$N\_{A}^{i+1} = N\_{A}^{i} + \int \left[ n\_{A}^{i}(\mathbf{r}) - w\_{A}^i(\mathbf{r})\,n(\mathbf{r}) \right]\,d^{3}\mathbf{r}.$$

* New reference charge densities are computed using

:   $$n^{i+1}\_A(\mathbf{r}) = n^{\text{lint}(N^i\_A)}(\mathbf{r})\left [ \text{uint}(N^i\_A)-N^i\_A\right ] + n^{\text{uint}(N\_A^i)}({\mathbf{r}})\left [ N^i\_A - \text{lint}(N^i\_A)\right ]$$

where $\text{lint}(x)$ expresses the integer part of $x$ and $\text{uint}(x)=\text{lint}(x)+1$.

Steps (1) to (3) are iterated until the difference in the electronic populations between two subsequent steps ($\Delta\_{A}^{i} = \vert N\_{A}^{i}-N\_{A}^{i+1}\vert$) is less than a predefined threshold for all atoms. The converged iterative Hirshfeld weights ($w\_{A}^{i}$) are then used to define the AIM properties needed to evaluate the dispersion energy (see Tkatchenko-Scheffler method).

The TS-HI method is described in detail in reference and its performance in optimization of various crystalline systems is examined in reference .

## Usage

The Tkatchenko-Scheffler method with iterative Hirshfeld partitioning (TS-HI) is invoked by setting IVDW=21. The convergence criterion for iterative Hirshfeld partitioning (in e) can optionally be defined via the parameter HITOLER (the default value is 5e-5). Other optional parameters controlling the input for the calculation are as in the conventional Tkatchenko-Scheffler method. The default value of the adjustable parameter VDW\_SR is 0.95 and corresponds to the PBE functional.

> **Mind:**
>
> * This method requires the use of POTCAR files from the PAW dataset version 52 or later.
> * The input reference data for non-interacting atoms are available only for elements of the first six rows of the periodic table except of the lanthanides. If the system contains other elements, the user must provide the free-atomic parameters for all atoms in the system via VDW\_ALPHA, VDW\_C6, VDW\_R0 (see Tkatchenko-Scheffler method defined in the INCAR file.
> * The charge-density dependence of gradients is neglected.
> * The DFT-TS/HI method is incompatible with the setting ADDGRID=*.TRUE.*.
> * It is essential that a sufficiently dense FFT grid (controlled via NGXF, NGYF and NGZF) is used in the DFT-TS/HI - we strongly recommend to use PREC=*Accurate*} for this type of calculations (in any case, avoid using PREC=*Low*).
> * Defaults for the parameters controlling the damping function (VDW\_S6, VDW\_SR, VDW\_D) are available only for the PBE functional. If a functional other than PBE is used, the value of VDW\_SR must be specified in the INCAR file.
> * Ewald's summation in the calculation of $E\_{disp}$ (controlled via LVDW\_EWALD) implemented according to reference is available as of VASP.5.3.4.
> * Hirshfeld charges for all configurations generated in a calculation are written out in the OUTCAR file. The corresponding table is introduced by the expression *Hirshfeld charges:*.

## Related tags and articles

HITOLER,
VDW\_SR,
VDW\_ALPHA,
VDW\_C6,
VDW\_R0,
VDW\_S6,
VDW\_D,
LVDW\_EWALD,
IVDW,
Tkatchenko-Scheffler method,
Self-consistent screening in Tkatchenko-Scheffler method,
Many-body dispersion energy,
Many-body dispersion energy with fractionally ionic model for polarizability

## References

---
