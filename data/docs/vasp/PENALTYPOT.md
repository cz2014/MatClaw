# PENALTYPOT

Categories: Files, Input files, Advanced molecular-dynamics sampling

File that defines the bias potential for a biased molecular-dynamics run.

At the beginning of each metadynamics simulation, VASP attempts to read the file PENALTYPOT containing the bias potential acting on the geometric parameters with `STATUS=5` defined in the ICONST file. In analogy to the time-dependent bias potential generated in metadynamics, the bias potential is defined as a superposition of Gaussian hills. Each line in the PENALTYPOT file represents one (multidimensional) Gaussian:

:   :   $x\_1 x\_2 ... x\_m h w$,

where $x\_1$ to $x\_m$ stand for the position in the space of active coordinates, and $h$ and $w$ are the height and width of the Gaussian, respectively. Note that both positive and negative values are allowed for the parameter $h$.

For example, if two active coordinates with `STATUS=5` are defined in the ICONST file:

```
R 1 5 5
R 1 6 5
```

then each line in the PENALTYPOT must contain four items. The bias potential is defined in the following lines:

```
1.6 0.8 1.0 0.2
1.6 1.0 1.0 0.2
1.6 1.2 1.0 0.2
1.6 1.4 1.0 0.2
1.6 1.6 1.0 0.2
1.6 1.8 1.0 0.2
1.6 2.0 1.0 0.2
```

## Related tags and articles

MDALGO, ICONST

---
