# PROCAR

Categories: Files, Output files

For static calculations, the file PROCAR contains the spd- and site projected wave function character of each orbital. Various schemes for determining the projected wave function character are implemented in VASP. They are usually controlled by the tags LORBIT and RWIGS. The tag RWIGS must be specified in the INCAR file whenever LORBIT<10 and in this case the orbitals are projected onto spherical harmonics that are non-zero within the region determined by RWIGS.
For LORBIT>=10, the tag RWIGS is not needed and the projection is done onto the projector functions.

* Format for LORBIT=11

```
# of k-points:    5         # of bands:   26         # of ions:    3

k-point     1 :    0.00000000 0.00000000 0.00000000     weight = 0.06250000

band     1 # energy  -17.37867948 # occ.  1.00000000

ion      s     py     pz     px    dxy    dyz    dz2    dxz  x2-y2    tot  
    1  0.144  0.000  0.000  0.000  0.000  0.000  0.000  0.000  0.000  0.145
    2  0.291  0.000  0.006  0.000  0.000  0.000  0.000  0.000  0.000  0.298
    3  0.291  0.000  0.006  0.000  0.000  0.000  0.000  0.000  0.000  0.298
tot    0.727  0.000  0.013  0.000  0.000  0.000  0.000  0.000  0.000  0.740
```

The header contains the information about the number of k-points, bands and how many ions are considered. The next line prints the k-point with the three coordinates in the first Brillouin zone and the corresponding k-point weight for the numerical integration followed by the band number and the energy and occupancy of the state. Each (k-point,band) pair contains the projections for every ion
$|\langle Y\_{lm}^{\alpha}|\phi\_{n\mathbf{k}}\rangle|^2$,
where $Y^\alpha\_{lm}$ is the spherical harmonic centered at ion index $\alpha$, $l,m$ the angular moment and magnetic quantum and $\phi\_{n\mathbf{k}}$ the wavefunction. The line and column with "tot" is the corresponding sum of the line and column, respectively.

For ISPIN=2 PROCAR contains a second set of projections for the spin down channel.

For LNONCOLLINEAR=.TRUE. three additional projections for each ion are printed and the output is similar to

```
ion      s     py     pz     px    dxy    dyz    dz2    dxz  x2-y2    tot  
    1  0.144  0.000  0.000  0.000  0.000  0.000  0.000  0.000  0.000  0.145
    2  0.291  0.000  0.006  0.000  0.000  0.000  0.000  0.000  0.000  0.298
    3  0.291  0.000  0.006  0.000  0.000  0.000  0.000  0.000  0.000  0.298
tot    0.727  0.000  0.013  0.000  0.000  0.000  0.000  0.000  0.000  0.740
    1 -0.011 -0.000 -0.000 -0.000 -0.000 -0.000 -0.000  0.000 -0.000 -0.011
    2 -0.023 -0.000 -0.000  0.000  0.000 -0.000 -0.000  0.000 -0.000 -0.023
    3 -0.023 -0.000 -0.000  0.000  0.000 -0.000 -0.000  0.000 -0.000 -0.023
tot   -0.057 -0.000 -0.001  0.000  0.000 -0.000 -0.000  0.000 -0.000 -0.058 
    1 -0.142 -0.000  0.000  0.000  0.000  0.000 -0.000 -0.000 -0.000 -0.142
    2 -0.286  0.000 -0.006 -0.000 -0.000  0.000 -0.000 -0.000  0.000 -0.293
    3 -0.286  0.000 -0.006 -0.000 -0.000  0.000 -0.000 -0.000  0.000 -0.293
tot   -0.715  0.000 -0.012 -0.000 -0.000  0.000 -0.000 -0.000  0.000 -0.727
    1 -0.024 -0.000  0.000 -0.000 -0.000  0.000 -0.000  0.000 -0.000 -0.024
    2 -0.048  0.000 -0.001  0.000  0.000  0.000 -0.000  0.000  0.000 -0.049
    3 -0.048  0.000 -0.001  0.000  0.000  0.000 -0.000  0.000  0.000 -0.049
tot   -0.119  0.000 -0.002  0.000  0.000  0.000 -0.000  0.000  0.000 -0.121
```

Here the entries correspond to the projected magnetizations
$1/2\sum\_{\mu,\nu=1}^2\sigma\_{\mu\nu}^j
\langle \chi\_{n {\bf k}}^\mu | Y\_{lm}^\alpha \rangle
\langle Y\_{lm}^\alpha | \chi\_{n {\bf k}}^\nu \rangle$ and are calculated for the spinor
of the spinor $|\Psi\_{n{\bf k}}\rangle=\left(\begin{matrix}\chi\_{n{\bf k}}^\uparrow \\\chi\_{n{\bf k}}^\downarrow \end{matrix}\right)$ and the Pauli matrices:

$\sigma^x = \left(\begin{matrix}
0 & 1 \\
1 & 0 \\
\end{matrix}\right), \quad
\sigma^y = \left(\begin{matrix}
0 & -i \\
i & 0 \\
\end{matrix}\right), \quad
\sigma^z = \left(\begin{matrix}
1 & 0 \\
0 & -1 \\
\end{matrix}\right)$

The first set is the total (absolute) magnetization, while the remaining three sets of entries correspond to the three directions $j=1,2,3$.

---
