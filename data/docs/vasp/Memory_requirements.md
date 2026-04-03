# Memory requirements

Categories: Performance, Howto, Memory

The memory requirements of VASP can easily exceed your computer facilities.
In this case the first step is to estimate where the excessive memory requirements
derive from. There are two possibilities:

* Storage of wave functions: All bands for all k-points must be kept in memory at the same time. The memory requirements for the wave functions are:

```
NKDIM*NBANDS*NRPLWV*16
```

The factor 16 arises from the fact that all quantities are COMPLEX\*16.

* Work arrays for the representation of the charge density, local potentials, structure factor and large work arrays: A total of approximately 10 arrays is allocated on the second finer grid:

```
4*(NGXF/2+1)*NGYF*NGZF*16
```

Once again all quantities are COMPLEX\*16.

Try to reduce the memory requirements by reducing the corresponding parameters.
See section \ref{imp} for a discussion of the minimal requirements for
these parameters.

---
