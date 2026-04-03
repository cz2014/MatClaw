# Nudged elastic bands

Categories: Ionic minimization, Transition states, Howto

The nudged elastic band (NEB) method is a computational technique used for studying energy landscapes and reaction pathways in chemical reactions or phase transitions.
It entails creating an initial path connecting the system's initial and final states, employing a series of *images* to represent intermediate configurations.
These images are linked by springs, forming an elastic band.
The method then iteratively adjusts the image positions along the band, minimizing energy until a minimum energy pathway, known as the 'nudged' path, is achieved.

## How to set up an NEB calculation

#### Step 1

Carefully optimize the structure of the fixed structures of your elastic band, i.e., the initial and the final state.
Remember that in the subsequent steps, the elastic band will be attached to these fixed structures, so any error will affect the transition path you obtain.

#### Step 2

Create a parent directory with enumerated subdirectories. For $n$ images, create $(n + 2)$ subdirectories and label them with their index starting from `0`. The foldername must always have 2 characters, pad with 0 if necessary. E.g. in case of 3 images

```
mycalc -- 00
       |_ 01
       |_ 02
       |_ 03
       |_ 04
```

Place the POSCAR file of the initial state in `00` and POSCAR file of the final state in the last directory (`04` in the example).

#### Step 3

Construct an initial guess for the intermediate structures.
You may use a script like in the tutorial on self-diffusion of a Si atom to a vacancy site or develop your own method.
The intermediate images should be somewhat close to the real transition path; otherwise, the optimization of the elastic band may fail.
Place the POSCAR files corresponding to these intermediate structures in subdirectories `01`, `02`, etc.

> **Mind:** Make sure that the POSCAR contains the same ordering of elements for initial, final, and intermediate states. It is highly recommended to minimize the number of images used to an absolute minimum. Convergence to the ground state is faster with fewer images. Starting with a single image between the two endpoints and increasing the number of images after the initial run has converged is often a prudent approach.

#### Step 4

Create an INCAR file in the parent directory (e.g. `mycalc`) and set the tag IMAGES to the number of intermediate structures.
This will introduce tangential springs to maintain equidistance among images during the relaxation process.
Control the strength with the SPRING tag, where negative values (like the default of -5) activate the NEB method.
It is important not to use excessively large values for SPRING, as it can hinder convergence.
The default value generally provides reliable results.
You should also set IBRION, ISIF, NSW, and other.

#### Step 5

Create the remaining input files KPOINTS and POTCAR.
For the NEB method, we recommend that all input files, except the POSCAR, WAVECAR and CHGCAR file, reside in the parent directory.
Then, run VASP by executing it in the parent directory (e.g. `mycalc`) to optimize the reaction path.

## Possible issues and advice on how to address it

One challenge with the NEB method arises from its non-linear constraint, which restricts movements to a hyper-plane perpendicular to the current tangent.
This characteristic can lead to convergence issues with the conjugate-gradient (CG) algorithm (IBRION=2).
In such cases, it is advisable to use alternative algorithms like the RMM-DIIS algorithm (IBRION=1) or the quick-min algorithm (IBRION=3).
Additionally, the equidistant images tend to deviate from this constraint in the initial steps.
To address this, applying a low dimensionality parameter (IBRION=1, NFREE=2) in the initial steps or using steepest descent minimization without line optimization (IBRION=3, SMASS=2) can help pre-converge the images.

If all degrees of freedom are allowed to relax, (e.g., in isolated molecules or surfaces), it is crucial to ensure that the sum of all positions remains consistent across all cells.
Failing to do so introduces artificial forces, causing the images to drift apart.
While this does not affect the VASP calculations, it can complicate result visualization.

> **Warning:** The NEB feature presented here cannot be applied to structural transitions. Changing the lattice would require a different algorithm referred to as variable-cell NEB that is not available within VASP.

> **Tip:** For more advanced calculations, consider using the Transition State Tools for VASP.

## Related tags and articles

IMAGES, SPRING, IBRION

Tutorial on self-diffusion of a Si atom to a vacancy site

Lecture on modeling chemical reactions (and transition states) using static approaches

Collective jumps of a Pt adatom on fcc-Pt (001): Nudged Elastic Band Calculation

TS search using the NEB Method

## References
