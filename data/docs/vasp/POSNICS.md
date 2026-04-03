# POSNICS

Categories: INCAR tag, NMR

```
   Warning: Not yet released!
```

This page contains information about a feature that will be available in a future
release of VASP. In other words, currently you cannot use it even with the latest version of VASP. The information may change significantly until it is released.

The POSNICS file is an input file that defines the positions to calculate the NMR nucleus-independent chemical shielding (NICS). If it is present in the directory running the job, it will be used by default, though it can be made explicit using `LPOSNICS = True`. The first line defines the number of NICS positions, followed by the positions of the NICS in direct coordinates, i.e., as fractions of the lattice parameters ${\vec a}\_1, {\vec a}\_2$ and ${\vec a}\_3$:

```
10000
0.0 0.0 0.5
0.0 0.01 0.5
0.0 0.02 0.5
...
0.99 0.97 0.5
0.99 0.98 0.5
0.99 0.99 0.5
```

## Related tags and articles

LCHIMAG, NUCIND, LPOSNICS
