# WRT_NMRCUR

Categories: INCAR tag, NMR

WRT\_NMRCUR = 0 | 1 | 2 | 3 | 4  
 Default: **WRT\_NMRCUR** = 0

Description: Allows to write the NMR current response in atomic units to file.

---

```
   Warning: Not yet released!
```

This page contains information about a feature that will be available in a future
release of VASP. In other words, currently you cannot use it even with the latest version of VASP. The information may change significantly until it is released.

In conjunction with `LCHIMAG = True`, WRT\_NMRCUR allows to write the current response on the fine grid NGXF x NGYF x NGZF in atomic units (hartree bohr$^{-2}$) to an external magnetic field within linear response NMR. The output is written to NMRCURBX, NMRCURBY, and/or NMRCURBZ depending on the selected direction of the perturbing $\mathbf{B}$ field:

* `WRT_NMRCUR = 0`: no current response written to file (default)
* `WRT_NMRCUR = 1`: $B\_x$
* `WRT_NMRCUR = 2`: $B\_y$
* `WRT_NMRCUR = 3`: $B\_z$
* `WRT_NMRCUR = 4`: all three directions of $\mathbf{B}=(B\_x,B\_y,B\_z)^T$

It is also written to vaspout.h5, if compiled with HDF5 support. You can find the data groups

```
 /results/nmrcurbx        Group
 /results/nmrcurbx/grid   Dataset {3}
 /results/nmrcurbx/structure Group
 /results/nmrcurbx/structure/position Group
 /results/nmrcurbx/structure/position/direct_coordinates Dataset {SCALAR} 
 /results/nmrcurbx/structure/position/ion_sha256 Dataset {1}
 /results/nmrcurbx/structure/position/ion_types Dataset {1}
 /results/nmrcurbx/structure/position/lattice_vectors Dataset {3, 3}
 /results/nmrcurbx/structure/position/number_ion_types Dataset {1}
 /results/nmrcurbx/structure/position/position_ions Dataset {2, 3}
 /results/nmrcurbx/structure/position/scale Dataset {SCALAR}
 /results/nmrcurbx/structure/position/system Dataset {SCALAR}
 /results/nmrcurbx/values Dataset {3, 24, 24, 24}
```

and use py4vasp to access these, e.g., using

```
import py4vasp as pv
calc = pv.Calculation.from_path(".")
calc.current_density.to_contour("NMR(x)", a=0.5) + calc.current_density.to_quiver("NMR(x)", a=0.5)
```

to select the current response triggered by $B\_x$. It will result in a contour plot showing the magnitude of the current density and a quiver plot with the projected current in the selected plane. The plane is selected as a fraction $x$ of the lattice vector. Here, `x=0.5` along $\mathbf{a}$. For the other lattice vectors use `b=x` or `c=x`.

> **Warning:** For bulk calculations you must switch off the use of symmetry. In other words, set `ISYM <= 0` if there is more than a single k point at zero (the Γ point).

> **Tip:** Consider switching on current augmentation (`LLRAUG = True`).

## Related tags and articles

LCHIMAG, LLRAUG, NMRCURBX
