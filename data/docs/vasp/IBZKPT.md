# IBZKPT

Categories: Files, Output files

The IBZKPT file is compatible with the KPOINTS file and is generated if the automatic k-mesh generation is selected in the KPOINTS file. IBZKPT contains the k-point coordinates and weights (and if the tetrahedron method was selected additional tetrahedron connection tables are used) in the "Entering all k-points explicitly" format used for providing k-points "by hand". This file can also be generated with the external tool, *kpoints*.

IBZKPT maybe copied to KPOINTS to save time, if one KPOINTS set is used several times.

---
