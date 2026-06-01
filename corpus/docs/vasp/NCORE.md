# NCORE

Categories: INCAR tag, Performance, Parallelization

NCORE = [integer]  
 Default: **NCORE** = 1

Description: NCORE determines the number of compute cores that work on an individual orbital (available as of VASP.5.2.13).

---

VASP currently offers parallelization and data distribution over bands and/or over plane wave coefficients, and as of VASP.5.3.2, parallelization over **k**-points (no data distribution, see KPAR).
To achieve high efficiency on massively parallel systems or modern multi-core machines, it is strongly recommended to use all parallelization options available. Most algorithms work with any data distribution (except for the single band conjugated gradient, which is obsolete).

NCORE is available from VASP.5.2.13 on, and is more handy than the previous parameter NPAR. The user should either specify NCORE or NPAR, where NPAR takes a higher preference. The relation between both parameters is

NCORE =number-of-cores /KPAR / NPAR

NCORE determines how many cores share the work on an individual orbital. The current default is NCORE=1, meaning that one orbital is treated by one core. NPAR is then set to the total number of cores (divided by KPAR). If NCORE equals the total number of cores, NPAR is set to 1. This implies data distribution over plane wave coefficients only: all cores will work together on every individual band, i.e., the plane wave coefficients of each band are distributed over all cores. This is usually very slow and should be avoided.

NCORE=1 is the optimal setting for small unit cells, and platforms with a small communication bandwidth. It is also a good choice for up to 8 cores. However, this mode substantially increases the memory requirements, because the non-local projector functions must be stored entirely on each core. In addition, substantial all-to-all communications are required to orthogonalize the bands.

On massively parallel systems and modern multi-core machines we strongly recommend to set

```
NCORE = 2 up to number-of-cores-per-socket (or number-of-cores-per-node)
```

For large unit cells, we found that this can improve the performance by up to a factor four compared to the default, and it also significantly improves the stability of the code due to reduced memory requirements. Ideally, NCORE should be a factor of the number-of-cores-per-socket (or number-of-cores-per-node), since this reduces communication between the sockets or nodes. The best value NCORE depends somewhat on the number of atoms in the unit cell. Values around 4 are usually ideal for 100 atoms in the unit cell. For very large unit cells (more than 400 atoms) values around 12-16 are often optimal. If you run extensive simulations for similar systems, make your own tests.

Finally, the optimal settings for NCORE and LPLANE depend strongly on the type of machine you are using.
Some recommended setups:

* LINUX cluster linked by Infiniband, modern multicore machines:

:   On a LINUX cluster with multicore machines linked by a fast network we recommend to set

```
LPLANE = .TRUE.
NCORE  = 2 up to number-of-cores-per-node
LSCALU = .FALSE.
NSIM   = 4
```

:   If very many nodes are used, it might be necessary to set LPLANE = .FALSE., but usually this offers only a very modest performance boost (if at all).

* LINUX cluster linked by 1 Gbit Ethernet, and LINUX clusters with single cores:

:   On a LINUX cluster linked by a relatively slow network, LPLANE must be set to .TRUE., and the NCORE should be equal to 1:

```
LPLANE = .TRUE.
NCORE  = 1
LSCALU = .FALSE.
NSIM   = 4
```

:   Mind that you need at least a 100 Mbit full duplex network, with a fast switch offering at least 2 Gbit switch capacity to find useful speedups. Multi-core machines should be always linked by an Infiniband, since Gbit is too slow for multi-core machines.

* Massively parallel machines with dedicated network (maybe Cray):

:   On massively parallel machines one is sometimes forced to use a large number of cores. In this case load balancing problems and problems with the communication bandwidth are likely to be experienced. In addition the local memory is fairly small on some massively parallel machines (too small keep the real space projectors in the cache using any reasonable VASP setting). Therefore, we recommend to set NCORE on these machines to √*# of cores* (explicit timing can be helpful to find the optimum value). The use of LPLANE=.TRUE. is only recommended if the number of nodes is significantly smaller than NGX, NGY and NGZ.

:   In summary, the following setting is recommended

```
LPLANE = .FALSE.
NPAR   = sqrt(number of cores)
NSIM   = 1
```

## Related tags and articles

NPAR,
LPLANE,
LSCALU,
NSIM,
KPAR,
LSCALAPACK,
LSCAAWARE,
OpenACC GPU Port of VASP,
Combining MPI and OpenMP

Examples that use this tag

---
