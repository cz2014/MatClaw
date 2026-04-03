# Number of bands NBANDS

Categories: Common Pitfalls

NBANDS must be chosen in such that a considerable number of empty bands is included in the calculation. As a minimum, VASP requires one empty band, otherwise VASP will give a warning. Only for large gap insulators, accurate results can be obtained without empty bands and the warning might be ignored.

Choosing NBANDS large enough is important for the following reason. In iterative matrix-diagonalization schemes, eigenvectors close to the top of the calculated number of states converge much slower than the lowest eigen states. This might result in a significant performance loss, if not sufficiently many empty bands are included in the calculation. Therefore, we recommend to set NBANDS to *NELECT/2 + NIONS/2*. This is also the default setting, which is safe in most cases. In some cases, it is also possible to decrease the number of additional bands to around *NIONS/4* slightly improving the performance. On the other hand, some transition metals and atoms with open f shells might require a much larger number of empty bands (up to *2\*NIONS*).

To check this parameter perform several calculations for a fixed potential (ICHARG=12) with an increasing number of bands (e.g. starting from *NELECT/2 + NIONS/2*). An accuracy of $10^{-6}$ should be obtained in 10-15 iterations. Mind that the RMM-DIIS scheme (ALGO=Fast) is more sensitive to the number of bands than the default Davidson algorithm (ALGO=Normal).

---
