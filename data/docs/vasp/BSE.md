# Category:Bethe-Salpeter equations

Categories: VASP, Many-body perturbation theory

The formalism of the Bethe-Salpeter equation (BSE) allows for calculating the polarizability with the electron-hole interaction and constitutes the state of the art for calculating absorption spectra in solids.

## Theory

As discussed in detail in the theory page, the Bethe-Salpeter equation is a non-hermitian eigenvalue problem

:   :   $$\left(\begin{array}{cc}
        \mathbf{A} & \mathbf{B} \\
        \mathbf{B}^\* & \mathbf{A}^\*
        \end{array}\right)\left(\begin{array}{l}
        \mathbf{X}\_\lambda \\
        \mathbf{Y}\_\lambda
        \end{array}\right)=\omega\_\lambda\left(\begin{array}{cc}
        \mathbf{1} & \mathbf{0} \\
        \mathbf{0} & -\mathbf{1}
        \end{array}\right)\left(\begin{array}{l}
        \mathbf{X}\_\lambda \\
        \mathbf{Y}\_\lambda
        \end{array}\right)~.$$

Using the eigenvectors $\mathbf{X}\_\lambda, \mathbf{Y}\_\lambda$ and eigenvalues $\omega\_\lambda$ of this equation we can find the dielectric function including the excitonic effects.

## Scaling

The steep scaling of BSE with the system size can be a limiting factor for its application in large systems. This should be considered when performing BSE calculations.

### Building matrix

The `ALGO = BSE/TDHF` algorithm as a first step, requires building the Hamiltonian of rank

:   $N\_{\rm rank} = N\_k\times N\_c\times N\_v$,

where $N\_k$ is the number of k-points in the full Brillouin zone and $N\_c$ and $N\_v$ are the number of conduction and valence bands, respectively. This computation scales as

:   $N\_k\times N\_q\times (N\_v\times N\_v\times N\_G\times N\_c\times N\_c)$,

where $N\_q$ is the number of q-points and $N\_G$ number of G-vectors. To simplify it, we can estimate this computation as $N^4-N^5$ with the system size.

### Solving equation

In the second step, the equation has to be solved. VASP provides different methods for doing that.

#### Exact diagonalization

The exact diagonalization algorithm (`IBSE = 2`) scales cubically with the matrix rank $N\_{\rm rank}^3$
or as $N^6$ with the system size.

#### Iterative solution

The iterative solution, as in the time-evolution (`IBSE = 1`) or Lanczos
(`IBSE = 3`) algorithms, do not
require diagonalizaing the full matrix but instead, require computing the matrix-vector multiplication for a number of steps or iterations $m$. Thus, solving the equation via the time-evolution or Lanczos algorithms scales as $N\_{\rm rank}^2\times m$ or $N^4$ with the system size. The number of iterations depends on the algorithm and the required precision, which can be selected via BSEPREC .

## Exact diagonalization

The diagonalization of the BSE Hamiltonian can be perform using various eigensolvers provided in ScaLAPACK, ELPA, and cuSolver libraries. The advantage of this approach is that the eigenvectors can be directly obtained and used for the analysis of the excitons.
Using the eigenvalues $\omega\_\lambda$ and eigenvectors $X\_\lambda$ of the BSE Hamiltonian, the macroscopic dielectric which accounts for the excitonic effects can be found

:   :   $$\epsilon\_M(\mathbf{q},\omega)=
        1+2\lim\_{\mathbf{q}\rightarrow 0}v(q)\sum\_{\lambda}
        \left|\sum\_{c,v,k}\langle c\mathbf{k}|e^{i\mathbf{qr}}|v\mathbf{k}\rangle X\_\lambda^{cv\mathbf{k}}\right|^2
        \times
        \left(\frac{1}{\omega\_\lambda - \omega - i\delta}\right)~.$$

The following features are currently supported:

* Calculating the dielectric function and eigenvectors
* Calculations beyond Tamm-Dancoff approximation
* Calculations of $\varepsilon(\mathbf{q},\omega)$ for $\mathbf{q}\neq0$
* Fatband plot

## Time evolution

Alternatively, it is possible to use the time-evolution algorithm which applies a short Dirac delta pulse of electric field and then follows the evolution of the dipole moments.
The dielectric function is found via a Fourier transform

:   :   $\epsilon\_M(\omega)=1-\frac{4\pi}{\Omega}\int\_0^{\infty} \mathrm{d} t
        \sum\_{c,v,\mathbf{k}}\left(\langle\mu\_{cv\mathbf{k}}| \xi\_{cv\mathbf{k}}(t)\rangle+c . c .\right) e^{-i(\omega-i \delta) t}$,

where $\mu$ and $\xi(t)$ are the dipole moments.

The solution found this way is strictly equivalent to the same solution as the exact diagonalization and can be used for obtaining the absorption spectrum, but does not yield the eigenvectors, which can be limiting for the analysis of the excitons. The advantage of this approach is the quadratic scaling with the size of the BSE Hamiltonian $N\_{rank}^2$.

The time-evolution algorithm can be selected by setting IBSE = 1 in a BSE calculation. The required number of steps in the time-evolution calculation depends on the broadening CSHIFT and the maximum energy OMEGAMAX. The precision can be selected via tag BSEPREC.

> **Mind:** The required number of steps does not depend on the size of the Hamiltonian

The following features are currently supported:

* Calculating the dielectric function
* Calculations beyond the Tamm-Dancoff approximation

## Lanczos algorithm

The expression for the dielectric function can be re-written as a continued fraction

:   :   $$\epsilon\_{\alpha\beta}(\omega) = \delta\_{\alpha\beta} - \frac{4\pi}{\Omega}\cfrac{|u\_0|^2}{(\omega - a\_1 + \mathrm i\eta) - \cfrac{b\_1^2}{(\omega -a\_2 + \mathrm i\eta)
        - \cfrac{b\_2^2}{...}}},$$

where $|u\_0\rangle$ is an initial guess vector computed from the dipole moments, $|u\_0\rangle = \sum\_{cv\mathbf{k}} \langle c\mathbf{k}|r\_\alpha|v\mathbf{k}\rangle \langle v\mathbf{k}|r\_\beta|c\mathbf{k}\rangle$. The $a$ and $b$ coefficients are evaluated iteratively, with the iterative algorithm stopping once the difference between $\epsilon(\omega)$ from two consecutive iterations is below a certain threshold selected by BSEPREC.

Using the dipole moments as the starting point means that the iterative algorithm is sensitive only to optically active transitions, i.e. $v\to c$ transitions with non-zero dipole moment. As such, the algorithm will ignore optically inactive transitions and can reach convergence faster than other methods for larger matrices.

The following features are currently supported:

* Calculating the dielectric function

## X-ray absorption spectra

The BSE/TDHF algorithm can also be used to model the X-ray absorption spectra (XAS), i.e., excitations from the core states into conduction bands. The detailed documentation of this method can be found in Category:XAS.

## Performing BSE calculations on GPU

As of VASP 6.5, the BSE/TDHF calculations with `IBSE = 1` or `IBSE = 2` can be fully run on NVIDIA GPUs.
To be able to offload the BSE calculations to GPUs one has to compile VASP with the cuSOLVERMp and cuBLASMp libraries provided with NVHPC-SDK 24.7 or newer.
To be able to use these libraries VASP has to be compiled with HPC-X (MPI shipped with NVHPC-SDK), which can be loaded via

```
module load nvhpc-hpcx-cuda12/24.7
```

To enable these libraries in VASP, make sure to include the following lines in your `makefile.include`

```
CPP_OPTIONS+= -DCUSOLVERMP -DCUBLASMP
LLIBS      += -cudalib=cusolvermp,cublasmp -lnvhpcwrapcal
```

To be able to perform the BSE calculation on GPUs, VASP needs to store the full BSE Hamiltonian in the GPU memory, which is often the limiting factor. The memory required to store the BSE Hamiltonian can be estimated as $N\_{\rm rank}^2\times 16\cdot 10^{-9}$ in Gb for `ANTIRES = 0`. In the case of exact diagonalization `IBSE = 2`, the eigensolver requires an additional scratch space.

> **Mind:** When running BSE calculations on GPUs, we recommend not setting OMEGAMAX or setting it to a larger value so that all the bands selected in NBANDSV and NBANDSO are included in the kernel. Otherwise, additional data transfers between CPU and GPU might be required, which leads to a serious performance degradation on GPUs.

## How to

* Practical guide for solving the Bethe-Salpeter equation via diagonalization BSE calculations
* Practical guide for solving the Casida equation via diagonalization TDDFT calculations
* Practical guide for using the Bethe-Salpeter equation for core excitations
* Practical guide for optimizing the BSE calculations

## Tutorials

* Tutorial for calculating the frequency-dependent dielectric function with excitonic effects based on the Bethe-Salpeter equation.

## References
