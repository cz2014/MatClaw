# Wxxxx.tmp

Categories: Files, Input files, Output files

These files store only the diagonal elements of the screened exchange $W$ needed for BSE calculations and are therefore fairly small compared to the WFULLxxxx.tmp files which store the full matrix. The *xxxx* in the name corresponds to integer values labeling the k-point index. During the BSE calculations, VASP will first try to read the WFULLxxxx.tmp files, and then, if these are missing, the Wxxxx.tmp files. For small isotropic (jellium-like) bulk systems, results with the Wxxxx.tmp might be similar to the results obtained using the WFULLxxxx.tmp files. However, for molecules and atoms as well as surfaces it is strictly required to use the full-screened Coulomb kernel $W$.

---
