# Practical considerations for transition state finding calculations

Categories: Howto, Transition states

This page details a few practical considerations for obtaining accurate and reliable transition state energies using the Nudged Elastic Band (NEB) and  Intrinsic Reaction Coordinate (IRC) methods implemented in VASP.
We list a few common issues encountered when running calculations with the NEB and IRC methods and identify possible solutions.

## NEB calculations

### Restart with a better guess for the initial and final state configurations

An example band which shows intermediate structures with lower energy than the initial and final configurations.

**Problem**: While performing an NEB calculation, there might be points on the band which have lower energy than that of the initial and final state configurations (corresponding to the structures that were placed in the 00 and 0x, where x is the number of IMAGES plus one). The figure on the right shows an example where the red (computed) points of the intermediate images are more stable than the initial and final configurations. The presence of these intermediate states is not an issue for the NEB methodology. However, if we are seeking to understand elementary reaction steps of one reaction event each, then we would like to have a band consisting of only one maxima and two minima (consisting of the initial and final states).

**Possible solutions**

* Relax the configurations with lower energy. These structures would then correspond to new initial and final configurations. Restart the NEB with these new configurations as the endpoints of the band.
* Make sure that the NEB was run with sufficient (and commensurate to the initial and final structures) accuracy. An important requirement is a small enough EDIFF, which governs the accuracy of the forces used in the NEB method.

### Band becomes "floppy"

**Problem** The band between the IMAGES of the NEB calculation is non-monotonic and appears "floppy".
In such a scenario the interpolated band is likely to oscillate between the computed points.
This problem typically appears when one or more images are added to an already computed band.

**Possible solutions**

* This problem is likely caused by the value of SPRING being too small.
* Check if EDIFF is accurate enough for computation of the forces.
* Check the interpolation algorithm that you use to determine the interpolated band. A cubic spline might suffice in most cases.

### Band does not converge

**Problem** The calculation does not converge, i.e., the NEB method does not find a reasonable path between an initial and final state configuration.
Sometimes a completely different path is found than the desired path.

**Possible solutions**

* Choose a different interpolation strategy to generate your initial guessed path
* Try the Improved dimer method instead
* Check if the numbering of the atoms is the initial and final configurations. Different ordering of atoms will lead to an unexpected path. Visualizing the initial interpolated path should help with diagnosing any issues related to incorrectly ordered atoms.

### Checking convergence

**Problem** Unsure if the highest energy point in the NEB is the first order saddle point between the initial and final state configurations

**Possible solutions**

* Check if there is exactly one imaginary mode by computing the second derivatives of the energy as implemented in IBRION.

## IRC calculations

**Problem** Unrealistic structures are generated along the IRC path

**Possible solution**

* Make sure that a very tight force convergence criteria has been used to determine the transition state; EDIFFG must be at most -0.025.
* Choose a smaller value of IRC\_VNORM0 so that the path conforms with the intrinsic reaction coordinate more closely.

## Related articles

Nudged elastic bands,
IRC calculations

## References
