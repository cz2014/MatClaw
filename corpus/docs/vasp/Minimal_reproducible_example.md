# Minimal reproducible example

Categories: Calculation setup, Howto

A **minimal reproducible example** is a set of input and output files that allow a bug, problem, or result to be demonstrated and reproduced. A crucial point is that the **minimal reproducible example** should be as small and simple as possible.

It is helpful to create a **minimal reproducible example** when reporting an issue to a colleague, supervisor, or on the VASP forum, but also as a starting point to explore more options and features based on a known system.

## How to create a minimal reproducible example

### Step 1

To reduce the complexity of a calculation, remove all preparatory and unnecessary post-processing steps from the workflow and any INCAR tags that are unnecessary to reproduce the issue. This may mean using a different structure (POSCAR) with fewer atoms. Or, for a magnetic calculation that may imply switching off projections (LORBIT), the use of spin-orbit coupling (LSORBIT) or perhaps an on-site Coulomb interaction (LDAU) if this is not essential to what is demonstrated. For a molecular-dynamics run, reducing the complexity may imply starting from an intermediate time step with a random seed (RANDOM\_SEED) and choosing a smaller supercell.

### Step 2

Select parameters that reproduce the result with minimal computational effort, even though it may reduce the accuracy of the calculation. For instance, this often implies reducing (ENCUT), choosing a coarser k mesh (KPOINTS), lowering PREC, etc.

### Step 3

Finally, ensure to include

1. all files to run the calculation (execution commands/submission script and input files that may include INCAR, POSCAR, POTCAR, KPOINTS, ICONST, etc.),
2. the main output files (stdout, OUTCAR, REPORT for molecular-dynamics runs, ML\_LOGFILE for machine-learning force fields, etc.)
3. and any problem-specific files that, e.g., include the specific data in focus or that extract and plot the data from the output files.

If the problem only occurs for specific hardware, versions of VASP, or toolchains, it is also essential to include that information.

## Related tags and articles

Input files,  Output files, Troubleshooting electronic convergence
