# Downsampling of the Hartree-Fock operator

Categories: Exchange-correlation functionals, Hybrid functionals

### Downsampling

Consider the description of a certain bulk system, using a supercell made up
of $N$ primitive cells, in such a way that, {**A** i' }, the lattice vectors
of the supercell are given by **A** i' =*n* i**A** i (i=1,2,3),
where {**A** i} are the lattice vectors of the primitive cell.
Let $R\_{\rm max}=2/\mu$ be the distance for which

:   $$\frac{\mathrm{erfc}\left(\mu|\mathbf{r}-\mathbf{r}'|\right)}{|\mathbf{r}-\mathbf{r}'|} \approx 0
    \quad \mathrm{for}\quad {|\mathbf{r}-\mathbf{r}'|}\gt R\_\mathrm{max}.$$

When the nearest neighbour distance between the periodically repeated images
of the supercell $R\_{NN}\gt 2R\_{\rm max}$ (i.e. $R\_{NN}\gt 4/\mu$), the
short-range Hartree-Fock potential can be represented exactly, sampling the BZ at the $\Gamma$-point only, i.e.,

:   $$V^{\mathrm{SR}}\_x\left(\mathbf{r},\mathbf{r}'\right)=
    -\frac{e^2}{2}\sum\_m f\_{m{\Gamma}}
    u\_{m{\Gamma}}^{\*}(\mathbf{r}')u\_{m{\Gamma}}(\mathbf{r})
    \frac{\mathrm{ erfc}(\mu|\mathbf{r}-\mathbf{r}'|)}
    {\vert \mathbf{r}-\mathbf{r}' \vert}.$$

This is equivalent to a representation of the bulk system using the
primitive cell and a $n\_{1}\times n\_{2}\times n\_{3}$ sampling of the BZ,

:   $$V^{\mathrm{SR}}\_x\left(\mathbf{r},\mathbf{r}'\right)=
    -\frac{e^2}{2}\sum\_{m'\mathbf{q}}f\_{m'\mathbf{q}}
    e^{-i\mathbf{q}\cdot\mathbf{r}'}u\_{m'\mathbf{q}}^{\*}(\mathbf{r}')
    u\_{m'\mathbf{q}}(\mathbf{r})e^{i\mathbf{q}\cdot\mathbf{r}}
    \times\frac{\mathrm{ erfc}(\mu|\mathbf{r}-\mathbf{r}'|)}
    {\vert \mathbf{r}-\mathbf{r}' \vert}$$

where the set of ${\mathbf{q}}$ vectors is given by

:   $$\{\mathbf{q}\}=\{i\mathbf{G}\_1+j\mathbf{G}\_2+k\mathbf{G}\_3\},$$

for *i* =1,..,*n* 1, *j* =1,..,n 2, and *k* =1,..,n 3, with **G**1,2,3 being the reciprocal lattice vectors of the supercell.

In light of the above it is clear that the number of ${\mathbf{q}}$-points needed to represent
the short-range Hartree-Fock potential decreases with decreasing $R\_{\rm max}$
(i.e., with increasing $\mu$).
Furthermore, one should realize that the maximal range of the exchange interactions
is not only limited by the ${\rm erfc}(\mu|{\bf r}-{\bf r}'|)/|{\bf r}-{\bf r}'|$
kernel, but depends on the extent of the spatial overlap of the orbitals as well
(this can easily be shown for the Hartree-Fock exchange energy when one adopts a Wannier
representation of the orbitals);
$R\_{\rm max}=2/\mu$; (as defined above), therefore, provides an upper limit
for the range of the exchange interactions, consistent with maximal spatial
overlap of the orbitals.

It is thus well conceivable that the situation arises where the short-range Hartree-Fock
potential may be represented on a considerably coarser mesh of points in the BZ than
the other contributions to the Hamiltonian.
To take advantage of this situation one may, for instance, restrict the sum over
${\bf q}$ in the short range exchange potential to a subset, {${\bf q\_{k}}$}, of the full $N\_{1}\times N\_{2}\times N\_{3}$ ${\bf k}$-point set, {${\bf k}$}, for which the following holds

:   $$\mathbf{q\_k} = \mathbf{b}\_1 \frac{n\_1 C\_1}{N\_1} + \mathbf{b}\_2 \frac{n\_2 C\_2}{N\_2}
    + \mathbf{b}\_3 \frac{n\_3 C\_3}{N\_3},\quad(n\_i=0,..,N\_i-1)$$

where **b**1,2,3 are the reciprocal lattice vectors of the primitive cell,
and $C\_{i}$ is the integer grid reduction factor along reciprocal lattice direction
**b** i. This leads to a reduction in the computational workload by a factor:

:   $$\frac{1}{C\_1 C\_2 C\_3}$$

**Note**: From the above, one should not get the impression that the grid reduction can only be used (or is useful) only in conjunction with range-separated functionals (e.g., HSE03/HSE06). It can be applied, for instance, in the PBE0 and pure HF cases as well, although from the above it might be clear that the range-separated functionals, in general, will allow for a larger reduction of the grid.

#### Caveat: when one should not use downsampling

In metallic systems, downsampling the exact exchange potential (NKRED, NKREDX, NKREDY, and/or NKREDZ ≠ 1) must be used with great care, and results might be wrong, if downsampling is applied. Problematic cases include electron or hole doped semiconductors or insulators. If two electrons are added to a bulk TiO2 cell containing 72 atoms, and calculations are performed using $2\times2\times2$ ${\bf k}$-points, the following results are obtained for the one-electron energies and occupancies with and without NKRED=2 (LHFCALC=.TRUE. ; AEXX=0.2 ; HFSCREEN = 0.2):

```
k-point   1: 0.0000    0.0000    0.0000
            DOPED NKRED = 2           DOPED NKRED = 1              UNDOPED CASE
 band No.  band energies occupation   band energies occupation   band energies occupation
valence bands
   262       2.4107      2.00000        2.4339      2.00000        2.4082      2.00000
   263       2.4107      2.00000        2.4339      2.00000        2.4082      2.00000
   264       2.8522      2.00000        2.8597      2.00000        2.8566      2.00000
conduction bands						 
   265       5.4046      2.00000        5.8240      1.87262        5.8126      0.00000
   266       5.4908      2.00000        5.8695      1.62151        5.8424      0.00000
   267       5.4894      2.00000        5.8695      1.62192        5.8424      0.00000
```

```
k-point   2: 0.5000    0.0000    0.0000
            DOPED NKRED = 2           DOPED NKRED = 1              UNDOPED CASE
 band No.  band energies occupation   band energies occupation  band energies occupation
valence bands
   262       2.0015      2.00000        2.0144      2.00000       2.0160      2.00000       
   263       2.5961      2.00000        2.6072      2.00000       2.6046      2.00000
   264       2.5961      2.00000        2.6072      2.00000       2.6045      2.00000
conduction bands					                              
   265       6.1904      0.00000        6.1335      0.00435       6.0300      0.00000
   266       6.1904      0.00000        6.1335      0.00435       6.0300      0.00000
   267       6.1907      0.00000        6.1340      0.00426       6.0305      0.00000
```

```
k-point   3 :  0.5000    0.5000    0.0000
            DOPED NKRED = 2           DOPED NKRED = 1              UNDOPED CASE
 band No.  band energies occupation   band energies occupation  band energies occupation
 valence bands
   262       2.4237      2.00000        2.4433      2.00000       2.4287      2.00000
   263       2.4238      2.00000        2.4432      2.00000       2.4287      2.00000
   264       2.4239      2.00000        2.4433      2.00000       2.4287      2.00000
conduction bands						                      
   265       5.8966      0.42674        5.9100      1.24121       5.8817      0.00000
   266       5.8780      0.54128        5.9100      1.24143       5.8817      0.00000
   267       5.8826      0.50661        5.9100      1.24261       5.8817      0.00000
```

Without NKRED, the one electron energies are pretty similar to the one electron energies in the undoped system (last two columns), whereas using NKRED a strong reduction of the "gap" between the valence and conduction band is observed, in particular, close to the conduction band minimum (in this case the point). This result is an artifact of the approximation used for NKRED=2. The nonlocal exchange operator cancels the self-interaction present in the Hartree-potential. For NKRED=2 and $2\times2\times2$ ${\bf k}$-points, the nonlocal exchange operator at each ${\bf k}$-point is evaluated using the one-electron orbitals at this ${\bf k}$-point only, e.g.:

:   $$V\_{\mathbf{k}}\left( \mathbf{G},\mathbf{G}'\right)=
    \langle \mathbf{k}+\mathbf{G} | V\_x | \mathbf{k}+\mathbf{G}'\rangle =
    -\frac{4\pi e^2}{\Omega} f\_{m\mathbf{k}}\sum\_{\mathbf{G}''}
    \frac{C^\*\_{m\mathbf{k}}(\mathbf{G}'-\mathbf{G}'') C\_{m\mathbf{k}}(\mathbf{G}-\mathbf{G}'')}
    {|\mathbf{G}''|^2}$$

The sum over ${\bf q}$ in the Hartree-Fock exchange potential reduces to a single ${\bf k}$-point. This reduces the self-interaction for states that originally have an occupancy larger than one, concomitantly pulling those states to lower energies. Initially, empty states (occupancy smaller one) are pushed up slightly. Since this is an artifact, NKRED must be used with utmost care for large supercells with coarse ${\bf k}$-point sampling. Please always check whether occupancies are similar at all ${\bf k}$ points if this
is not the case. The calculations should be double-checked without downsampling.

Since HF type calculations using $2\times2\times2$ ${\bf k}$ points without NKRED, are roughly 64 times more expensive than those using the $\Gamma$-point only, it might seem impossible to do anything but $\Gamma$-point only calculations. However, VASP allows to generate special ${\bf k}$ points using generating lattices.

The following ${\bf k}$-point sets are particularly useful for HF-type calculations:

```
k-point set generating a bcc like lattice in the BZ ->  2 k points in BZ
0
direct
 0.5 0.5 0.5
 -.5 -.5 0.5
 0.5 -.5 -.5
 0 0 0
```

This KPOINTS file generates two 2 ${\bf k}$ points, one at the $\Gamma$-point and one along the space diagonal at the BZ boundary (*R* point).

The following KPOINTS file generates 4 ${\bf k}$ points, one at the $\Gamma$ point
and three at the *S* points (the latter ones might be symmetry equivalent for cubic cells).

```
k-point set generating an fcc lattice ->  4 k points in BZ
0
direct
 0.5 0.5 0.0
 0.0 0.5 0.5
 0.5 0.0 0.5
 0 0 0
```

Using such grids, sensible and fairly rapidly converging results are obtained, e.g., for electron and hole doped materials, even if the conduction or valence band is partially occupied or depleted. For instance, the following energies are obtained for TiO2:

```
Gamma only     TOTEN  =      -837.759900 eV
2 k-points     TOTEN  =      -838.039157 eV
4 k-points     TOTEN  =      -838.129712 eV
2x2x2          TOTEN  =      -838.104787 eV
2x2x2 NKRED=2  TOTEN  =      -838.418681 eV
```

## Related tags and articles

NKRED,
NKREDX,
NKREDY,
NKREDZ,
Hybrid functionals: formalism

## References

---
