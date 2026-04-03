# LPLANE

Categories: INCAR tag, Performance, Parallelization

LPLANE = [logical]  
 Default: **LPLANE** = .TRUE.

Description: LPLANE switches on the plane-wise data distribution in real space.

---

For LPLANE=.TRUE., the data distribution in real space is done plane wise.
Any combination of NPAR and LPLANE can be used.

Generally, LPLANE=.TRUE. reduces the communication band width during the FFT's, but at the same time it unfortunately worsens the load balancing on massively parallel machines.
LPLANE=.TRUE. should only be used if NGZ is at least 3×(number of nodes)/NPAR, and optimal load balancing is achieved if NGZ=*n*×NPAR, where *n* is an arbitrary integer.

If LPLANE=.TRUE. and if the real space projector functions (LREAL=.TRUE. or ON or AUTO) are used, it might be necessary to check the lines following

```
real space projector functions
 total allocation   :
 max/ min on nodes  :
```

The max/ min values should not differ too much, otherwise the load balancing might worsen as well.

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

:   If very many nodes are used, it might be necessary to set LPLANE=.FALSE., but usually this offers very little advantage. For long runs (*e.g.* molecular dynamics), we recommend to optimize NPAR by trying short runs for different settings.

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

NPAR,
NCORE,
LSCALU,
NSIM,
KPAR,
LSCALAPACK,
LSCAAWARE

Examples that use this tag

---
