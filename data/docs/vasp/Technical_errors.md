# Technical errors

Categories: Common Pitfalls

Technical errors fall into four categories:

* Errors due to k-point sampling. This will be discussed in Number of k points and method for smearing. Mind that the errors due to the k-point mesh are not transferable i.e. a $9\times 9\times 9$ k-points grid leads to a completely different error for fcc, bcc and sc. It is therefore absolutely essential to be very careful with respect to the k-point sampling.
* Errors due to the cut-off ENCUT. This error is highly transferable, i.e. the default cutoff ENCUT (read from the POTCAR file) is in most cases safe, and one can expect that energy differences will be accurate within a few meV (see Energy cut off and FFT mesh). An exception is the stress tensor which converges notoriously slow with respect to the size of the plane wave basis set (see Energy vs volume Volume relaxations and Pulay stress).
* Wrap around errors (see Wrap-around errors): These errors are due to an insufficient FFT mesh and they are not as well behaved as the errors due to the energy cut off (see Energy cut off and FFT mesh). But once again, if one uses the default cut off (read from the POTCAR file) the wrap around errors are usually very small (a few meV per atom) even if the FFT mesh is not sufficient. The reason is that the default cut offs in VASP are rather large, and therefore the charge density and the potentials contain only small components in the region where the wrap around error occurs.
* Errors due to the real space projection: Real space projection always introduces additional (small) errors. These errors are also quite well behaved i.e. if one uses the same real space projection operators all the time, the errors are almost constants. Anyway, one should try to avoid the evaluation of energy differences between calculations with LREAL=*.FALSE.* and LREAL=*.TRUE.* (see LREAL). Mind that for LREAL=*Auto* (the recommended setting) the real space operators are optimized by VASP according to ENCUT and PREC i.e. one gets different real space projection operators if ENCUT or PREC is changed.

In conclusion, to minimize errors one should use the same setting for ENCUT, ENAUG, PREC, LREAL and ROPT throughout all calculations, and these flags should be specified explicitly in the INCAR file. In addition it is also preferable to use the same supercell for all calculations whenever possible.

---
