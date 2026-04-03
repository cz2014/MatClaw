# RANDOM_SEED

Categories: INCAR tag, Molecular dynamics

RANDOM\_SEED = [integer][integer][integer]  
 Default: **RANDOM\_SEED** = based on the system clock

Description: RANDOM\_SEED specifies the seed of the random-number generator (compile VASP with -Dtbdyn).

---

The random-number generator (RNG) generates a sequence of random numbers, which is initialized by the tag RANDOM\_SEED.
For example, in molecular dynamics simulations, the RNG can be used to initialize atomic velocities. Hence, the seed for the RNG influences the trajectory of a molecular dynamics simulation.
The three integers of RANDOM\_SEED must fulfill these conditions:

```
0 <= RANDOM_SEED(1) < 900000000
0 <= RANDOM_SEED(2) < 1000000
0 <= RANDOM_SEED(3)
```

A typical input for the RANDOM\_SEED looks like this:

```
RANDOM_SEED =         248489752                0                0
```

The initial value of RANDOM\_SEED and the value after each MD step are written to the REPORT file.

> **Tip:** If multiple molecular dynamics runs with different random seeds result in inconsistent time averages, then not enough configurations were sampled. Hence, longer or more trajectories are required to get converged ensemble averages.

> **Mind:** If no RANDOM\_SEED is set in the INCAR then the used value will depend on the system time. For example, in molecular dynamics simulations, initial velocities will be different each time VASP is executed (if TEBEG is used and no velocities are provided in the POSCAR file). Hence, the trajectories will diverge. If reproducibility is desired the RANDOM\_SEED has to be set manually.

## Related tags and articles

IBRION, MDALGO

Examples that use this tag

---
