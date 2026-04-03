# NPAR

Categories: INCAR tag, Parallelization

NPAR = [integer]  
 Default: **NPAR** = number of cores

Description: NPAR determines the number of bands that are treated in parallel.

---

VASP currently offers parallelization and data distribution over bands and/or over plane wave coefficients, and as of VASP.5.3.2, parallelization over **k**-points (no data distribution, see KPAR).
To obtain high efficiency on massively parallel systems or modern multi-core machines, it is strongly recommended to use all at the same time. Most algorithms work with any data distribution (except for the single band conjugated gradient, which is considered to be obsolete).

NPAR determines how many bands are treated in parallel. The current default is NPAR=*number of cores*, meaning that one orbital is treated by one core. NCORE is then set to 1. If NPAR=1, NCORE is set to the number of cores. This implies data distribution over plane wave coefficients only: all cores will work together on every individual band, i.e., the plane wave coefficients of each band are distributed over all cores. This is usually very slow and should be avoided.

NPAR=*number of cores* is the optimal setting for platforms with a small communication bandwidth and is a good choice for up to 8 cores, as well as for machines with a single core per node and a Gigabit network. However, this mode substantially increases the memory requirements, because the non-local projector functions must be stored entirely on each core. In addition, substantial all-to-all communications are required to orthogonalize the bands. On massively parallel systems and modern multi-core machines we strongly urge to set

:   $$\textrm{NPAR}\approx\sqrt{\textrm{\#of}\; \textrm{cores}}$$

or

:   $$\textrm{NCORE}=\textrm{\#of}\;\textrm{cores}\;\textrm{per}\;\textrm{compute}\;\textrm{node}$$

In selected cases, we found that this improves the performance by a factor of up to four compared to the default, and it also significantly improves the stability of the code due to reduced memory requirements.

NCORE is available from VASP.5.2.13 on, and is more handy than the previous parameter NPAR.
The user should either specify NCORE or NPAR, where NPAR takes a higher preference.
The relation between both parameters is

:   $$\textrm{NCORE}=\textrm{\#of}\; \textrm{cores}/\textrm{NPAR}$$

The optimum settings for NPAR and LPLANE depend strongly on the type of machine you are using.
Some recommended setups:

* LINUX cluster linked by Infiniband, modern multicore machines:

:   On a LINUX cluster with multicore machines linked by a fast network we recommend to set

```
LPLANE = .TRUE.
NCORE  = number of cores per node (e.g. 4 or 8)
LSCALU = .FALSE.
NSIM   = 4
```

:   If very many nodes are used, it might be necessary to set LPLANE=.FALSE., but usually this offers very little advantage. For long (e.g. molecular dynamics runs), we recommend to optimize NPAR by trying short runs for different settings.

* LINUX cluster linked by 1 Gbit Ethernet, and LINUX clusters with single cores:

:   On a LINUX cluster linked by a relatively slow network, LPLANE must be set to .TRUE., and the NPAR flag should be equal to the number of cores:

```
LPLANE = .TRUE.
NCORE  = 1
LSCALU = .FALSE.
NSIM   = 4
```

:   Mind that you need at least a 100 Mbit full duplex network, with a fast switch offering at least 2 Gbit switch capacity to find usefull speedups. Multi-core machines should be always linked by an Infiniband, since Gbit is too slow for multi-core machines.

* Massively parallel machines (Cray, Blue Gene):

:   On many massively parallel machines one is forced to use a huge number of cores. In this case load balancing problems and problems with the communication bandwidth are likely to be experienced. In addition the local memory is fairly small on some massively parallel machines; too small keep the real space projectors in the cache with any setting. Therefore, we recommend to set NPAR on these machines to √*# of cores* (explicit timing can be helpful to find the optimum value). The use of LPLANE=.TRUE. is only recommended if the number of nodes is significantly smaller than NGX, NGY and NGZ.

:   In summary, the following setting is recommended

```
LPLANE = .FALSE.
NPAR   = sqrt(number of cores)
NSIM   = 1
```

## Related tags and articles

NCORE,
LPLANE,
LSCALU,
NSIM,
KPAR,
LSCALAPACK,
LSCAAWARE

Examples that use this tag

---
