# LTEMPER

Categories: INCAR tag, Parallel Tempering

LTEMPER = [logical]  
 Default: **LTEMPER** = .FALSE.

Description: LTEMPER specified whether parallel tempering is used. The flag must be used in combination with IMAGES.

---

VASP supports various modes where simultaneous calculations for different INCAR, KPOINTS, POTCAR, or POSCAR files are performed.
The parallel tempering mode is explained in this section, however, please read the section IMAGES first. Parallel tempering is also known as replica-exchange molecular dynamics.

If the tags IMAGES=nn and LTEMPER=.TRUE. are set in the INCAR file, VASP performs parallel tempering calculations. In this case, it is expedient to supply different INCAR and POSCAR files in each subdirectory 01, 02, 03, ..., nn. For each subdiretory a different simulation temperature should be supplied using the tags TEBEG in the INCAR files 01/INCAR, 02/INCAR ... nn/INCAR.

In the course of the simulations, VASP will attempt to swap the temperatures between the images. Swapping attempts are made every
NTEMPER MD steps and accepted with a likelyhood of

:   $$p = \min \left( 1, \frac{ \exp \left( -\frac{E\_j}{kT\_i} - \frac{E\_i}{kT\_j} \right) }{ \exp \left( -\frac{E\_i}{kT\_i} - \frac{E\_j}{kT\_j} \right) } \right) = \min \left( 1, e^{(E\_i - E\_j) \left( \frac{1}{kT\_i} - \frac{1}{kT\_j} \right)} \right) ,$$

where $E\_i, E\_j$ and $T\_i, T\_j$ are the energies and temperatures of the considered two replicas. Note that VASP swaps the temperatures and not the positions between images. This means that the temperatures in each subdirectory change as the MD progresses. Information on the current temperatures for each image can be found in the OUTCAR files around the lines (all OUTCAR files will show the same information):

```
parallel tempering new
```

The average acceptance ratios are also written to the OUTCAR file. For efficient parallel tempering the acceptance ratio should not fall much below 0.2-0.3. If the acceptance ratio is too small, one usually needs to increase the number of images. However, too many images can also decrease the probability that all images visit all allowed temperatures.

## Related tags and articles

IMAGES,
NTEMPER

Examples that use this tag

## References

---
