# LPARDH5

Categories: INCAR tag, Charge density

LPARDH5 = [logical]  
 Default: **LPARDH5** = .FALSE.

Description: LPARDH5 determines whether the partial charges are written to PARCHG or vaspout.h5.

> **Mind:** Available as of VASP 6.5.0

---

Partial charges can be calculated as a postprocessing step when LPARD = .TRUE.. The output is written to one or several PARCHG files if LPARDH5=.FALSE., and to vaspout.h5 if LPARDH5=.TRUE.. If NBMOD = -1, the setting of LPARD is irrelevant. Instead of a PARCHG file, or a partial\_charges group in the vaspout.h5 hdf5 file, a CHGCAR file *without* augmentation charges will be written.

If the output is redirected to vaspout.h5, py4vasp can be used to analyze the partial charge density and to simulate STM pictures.

For example, the following Python code would create a dictionary with the partial charge output and plot an STM simulation.

```
  import py4vasp as pv
  calc = pv.Calculation.from_path(".")
  part_charge_dict = calc.partial_density.to_dict()
  calc.partial_density.to_stm()
```

The command below prints the table of contents of the vaspout.h5 file.

```
 h5ls -r vaspout.h5
```

The section relevant to partial charges will look similar to this:

```
 /results/partial_charges Group
 /results/partial_charges/bands Dataset {1}
 /results/partial_charges/grid Dataset {3}
 /results/partial_charges/kpoints Dataset {1}
 /results/partial_charges/parchg Dataset {1, 1, 2, 480, 48, 48}
```

LPARD,
LWAVEH5,
LCHARGH5,
IBAND,
EINT,
NBMOD,
KPUSE,
LSEPB,
LSEPK,
PARCHG,
band-decomposed charge densities

Examples that use this tag

---
