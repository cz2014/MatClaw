# WEIMIN

Categories: INCAR tag, Electronic minimization

WEIMIN = [real]

|  |  |  |
| --- | --- | --- |
| Default: **WEIMIN** | = 0.001 | for IBRION≥0 |
|  | = 0 | for IBRION=−1 |

Description: WEIMIN specifies the maximum weight for a band to be considered empty.

---

The tags WEIMIN, EBREAK, and DEPER allow fine-tuning of the iterative matrix diagonalization and are best not changed. They are optimized for a large variety of systems, and changing one of the parameters usually decreases performance or can even screw up the iterative matrix diagonalization totally.
In general, these tags control when the optimization of a single band is stopped within the iterative matrix diagonalization schemes:

Within all implemented iterative schemes a distinction between empty and occupied bands is made to speed up calculations. Unoccupied bands are optimized only twice, whereas occupied bands are optimized up to four times till another break criterion is met. Eigenvalue/eigenvector pairs for which the partial occupancies are smaller than WEIMIN are treated as unoccupied states (and are thus only optimized twice).

## Related tags and articles

EBREAK,
DEPER,
IBRION

Examples that use this tag
