# GAMMA

Categories: Files, Input files, Electronic occupancy

The GAMMA file is an input file used when ICHARG=5 is set. It is read by VASP during an electronic minimization to incorporate additional occupation changes per k-point and orbital before calculating a new charge density. The file's format is structured as follows:

```
 567  -1  ! Number of k-points, default number of bands
 1  81  92 ! k-point index, band window of occupations to be added
 -0.88697620213424  -0.00000000000110 0.00952263319978  -0.00013538025816 -0.00003023919061  0.00036153047962 ... ! 1 nbnd row per line
  0.00952263319978   0.00013538025816 -0.90621349117750 -0.00000000000092 -0.00002036611614  0.00020787085249 ...
  ... (10 more lines)
 2  81  92
 -0.89265621432703 -0.00000000000107 -0.00944765243065  -0.00671452451385 -0.00029309275635  -0.00012146585216 
  ... (11 more lines)
 ...
 567  82  91
 -0.89056253498876  -0.00000000000112 -0.00449699353373  0.00290102672201 -0.00014095045304  0.00000787119531 ... 
 …
```

The file contains a small header marking the number of k-points (must be consistent with the current number of k-points in the irreducible Brillouin zone), and if there is a default number of bands to be assumed per k-point. Next, is a line that increments through the k-point indices and the current band window, i.e. the indices of bands for which the occupation changes are read in (indices must be smaller or equal to NBANDS). This is followed by the actual occupation changes as a nband times nband matrix (one row per line), where complex number formatting is used. First number is the real part and the second is the complex part, third is again real part, etc.

While ICHARG=5 is set, VASP will read this file right before the new charge density is calculated. However, VASP will only read the file and continues calculation if an additional file called vasp.lock is present in the current directory. This design allows to interface to an external code that performs between the SCF step some extra computation and updates the KS occupations.

> **Tip:** For VASP 6.5.0 or newer compiled with HDF5 support enabled VASP can also read the occupation update more efficiently from the vaspgamma.h5 instead (the text file will take priority if both files are present).

The procedure to construct a new charge density from the combined occupations (KS occupations + GAMMA file) is as follows: The additional occupation changes from the GAMMA can be a off-diagonal matrix $\Delta N\_{n n'}({\bf k})$, new natural orbitals are found by a transformation matrix $V$. This transformation is found by diagonalizing the total correlated density matrix:

$f'\_{\nu {\bf k}} \delta\_{\nu \nu'} = \sum\_{n n'} V\_{\nu n} \left[ f\_{n {\bf k}} \delta\_{n n'} + \Delta N\_{n n'} \right] V^\*\_{n' \nu'},$

$|\Psi'\_{\nu {\bf k}}\rangle = \sum\_n V\_{\nu n} |\Psi\_{n {\bf k}}\rangle$

The new orbitals $|\Psi'\_{\nu {\bf k}}\rangle$ together with $f'\_{\nu {\bf k}}$ are then used to calculate the new charge density. For more information see Ref. Eq. (30)-(32).

The TRIQS software package makes use of it to perform charge self-consistent DFT plus dynamical mean field theory (DMFT) calculations, and provides tutorials on how to perform such calculations with VASP.

> **Mind:** The text file based reading of occupation updates only works for non spin-polarized calculations when reading from the GAMMA file. Please use the hdf5 interface in VASP 6.5.0 or newer (vaspgamma.h5) for spin polarized calculations.

## Related tags and articles

ICHARG, vasp.lock, vaspgamma.h5,DFT+DMFT

## References
