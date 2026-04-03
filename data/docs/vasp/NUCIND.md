# NUCIND

Categories: INCAR tag, NMR

NUCIND = .TRUE. | .FALSE.  
 Default: **NUCIND** = .FALSE.

Description: Allows the nucleus-independent chemical shielding (NICS) to be calculated.

---

```
   Warning: Not yet released!
```

This page contains information about a feature that will be available in a future
release of VASP. In other words, currently you cannot use it even with the latest version of VASP. The information may change significantly until it is released.

In conjunction with `LCHIMAG = True`, NUCIND calculates the chemical shielding tensor $\sigma\_{ij}(\mathbf{R})$ at positions $\textbf{R}$ off-nucleus, hence nucleus-independent chemical shielding (NICS) . VASP calculates only from the plane wave
grid, there is no one-center augmentation.

When `NUCIND = True`, by default these are calculated on the fine FFT grid NGXF x NGYF x NGZF in ppm. The output is written to NICS.

It is also written to vaspout.h5, if compiled with HDF5 support. You can find the data groups:

```
/results/nics            Group
/results/nics/grid       Dataset {3}
/results/nics/structure  Group
/results/nics/structure/position Group
/results/nics/structure/position/direct_coordinates Dataset {SCALAR}
/results/nics/structure/position/ion_sha256 Dataset {2}
/results/nics/structure/position/ion_types Dataset {2}
/results/nics/structure/position/lattice_vectors Dataset {3, 3}
/results/nics/structure/position/number_ion_types Dataset {2}
/results/nics/structure/position/position_ions Dataset {8, 3}
/results/nics/structure/position/scale Dataset {SCALAR}
/results/nics/structure/position/system Dataset {SCALAR}
/results/nics/values     Dataset {9, 108, 108, 108}
```

and use py4vasp to access these, e.g., using

```
import py4vasp as pv
calc = pv.Calculation.from_path(".")
calc.nics.plot()
```

to select the isotropic chemical shielding $\sigma\_{iso}$ in 3D space . It will produce an isosurface of the shielding (positive) and deshielding (negative) over the crystal structure.

Alternatively, produce a 2D contour plot of the NICS in a plane :

```
import py4vasp as pv
calc = pv.Calculation.from_path(".")
calc.nics.to_contour(a=0.5)
```

It will result in a contour plot showing the isotropic chemical shielding $\sigma\_{iso}$ in the selected plane. The plane is selected as a fraction `x` of the lattice vector. Here, `x=0.5` corresponds to half of the primary lattice vector $\mathbf{a}$. For the other lattice vectors use `b=x` or `c=x`.

For both the 2D and 3D plots, the isotropic chemical shielding is used by default. You can alternatively select the other properties (see LCHIMAG for details. Herzfeld-Berger convention is followed ) by inputting them as arguments into the functions, e.g., `calc.nics.plot("anisotropic")` or `calc.nics.to_contour("span", a=0.5)`:

* `"isotropic"` (default) - plot the isotropic chemical shielding $\sigma\_{iso}$
* `"anisotropic"` - plot the anisotropic chemical shielding $\sigma\_{ani}$
* `"span"` - plots the span $\Omega$
* `"skew"` - plot the skew $\kappa$

## POSNICS

Alternatively, if the POSNICS file is present, then the positions defined within that file will be used. The calculation takes longer as each point is calculated in serial and not in parallel as for the grid. However, there is far greater flexibility for defining physically relevant positions, e.g., hydrogen bonds, close to nuclei, or chemical bonds. These chemical shielding tensors are printed in the OUTCAR file as follows, e.g., for the 100th NICS point:

```
 nics 100
          1.187143         -0.003408         -0.000000
         -0.002977         -1.893648         -0.000000
         -0.000000         -0.000000         -0.326272
```

It is also written to vaspout.h5, if compiled with HDF5 support. You can find the data groups:

```
/results/posnics         Group
/results/posnics/label   Dataset {SCALAR}
/results/posnics/positions Dataset {3, 10000}
/results/posnics/values  Dataset {10000, 3, 3}
```

and use py4vasp to access these, e.g., using

```
import py4vasp as pv
calc = pv.Calculation.from_path(".")
calc.nics.read()
```

to read the NICS values for the positions defined in POSNICS. Since the grid is not necessarily regular, you will need to plot these yourself.

## Related tags and articles

LCHIMAG, NICS, LNICSALL, LPOSNICS, POSNICS

## References
