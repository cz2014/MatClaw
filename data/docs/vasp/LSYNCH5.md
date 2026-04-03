# LSYNCH5

Categories: INCAR tag

LSYNCH5 = [logical]  
 Default: **LSYNCH5** = .FALSE.

Description: LSYNCH5 determines whether the output in vaspout.h5 is always synchronized with VASP while the calculation is running.

---

If you set this flag, VASP will enable single-writer-multiple-reader mode for the HDF5 file.
This allows you to monitor the output using py4vasp while the calculation is still running.

> **Mind:** Synchronizing the HDF5 file continuously comes with a computational cost. Please do your own testing whether that is a bottleneck for your calculation.

## Related tags and articles

LH5

Examples that use this tag
