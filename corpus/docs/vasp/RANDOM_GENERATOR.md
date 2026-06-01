# RANDOM_GENERATOR

Categories: INCAR tag, Calculation setup

RANDOM\_GENERATOR = default | pcg\_32

Description: Specifies the random-number generator used to initialize the wavefunction (see INIWAV) for electronic minimization, initialize atomic velocities for molecular dynamics, etc.

---

The random-number generator (RNG) generates a sequence of random numbers, which is initialized by the tag RANDOM\_SEED. By default the random number generator uses a very stable, compiler and platform independent algorithm. It is based on the work: "Toward a Universal Random Number Generator" by George Marsaglia and Arif Zaman. Florida State University Report: FSU-SCRI-87-50 (1987) and was later modified by F. James and publisheed . This algorithm is programmed in serial, not utilizing any threading or parallelism. For normal system the time to initialize wave functions is negligible, but for large systems with many bands `NBANDS > 1000`, and plane wave coefficients this can take several seconds to minutes.

For such systems it can be advantageous to switch `RANDOM_GENERATOR = pcg_32`, which is threaded (need to enable OpenMP threading at compile time) over the number of OpenMP threads. The algorithm is also guaranteed to produce the same random numbers in each call, but might depend on the compiler and library used. Compared to the default generator it is thus not platform independent. Hence, use `RANDOM_GENERATOR = default` for strictly reproducible numbers across different machines at all steps during the calculation or comparison of VASP versions.

## Related tags and articles

RANDOM\_SEED, INIWAV

Workflows that use this tag

## References
