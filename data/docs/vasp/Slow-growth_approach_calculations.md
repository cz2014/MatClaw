# Slow-growth approach calculations

Categories: Advanced molecular-dynamics sampling, Howto

## Anderson thermostat

* For a slow-growth simulation, one has to perform a calcualtion very similar to Constrained molecular dynamics but additionally the transformation velocity-related INCREM-tag for each geometric parameter with STATUS=0 has to be specified. For a slow-growth approach run with Andersen thermostat, one has to:

1. Set the standard MD-related tags: IBRION=0, TEBEG, POTIM, and NSW
2. Set MDALGO=1, and choose an appropriate setting for ANDERSEN\_PROB
3. Define geometric constraints in the ICONST file, and set the **STATUS** parameter for the constrained coordinates to 0
4. When the free-energy gradient is to be computed, set LBLUEOUT=.TRUE.

5. Specify the transformation velocity-related INCREM-tag for each geometric parameter with STATUS=0.

## Nose-Hoover thermostat

* For a slow-growth approach run with Nose-Hoover thermostat, one has to:

1. Set the standard MD-related tags: IBRION=0, TEBEG, POTIM, and NSW
2. Set MDALGO=2, and choose an appropriate setting for SMASS
3. Define geometric constraints in the ICONST-file, and set the STATUS parameter for the constrained coordinates to 0
4. When the free-energy gradient is to be computed, set LBLUEOUT=.TRUE.

5. Specify the transformation velocity-related INCREM-tag for each geometric parameter with STATUS=0

VASP can handle multiple (even redundant) constraints. Note, however, that a too large number of constraints can cause problems with the stability of the SHAKE algorithm. In problematic cases, it is recommended to use a looser convergence criterion (see SHAKETOL) and to allow a larger number of iterations (see SHAKEMAXITER) in the SHAKE algorithm. Hard constraints may also be used in metadynamics simulations (see MDALGO=11 | 21). Information about the constraints is written onto the REPORT-file: check the lines following the string: Const\_coord
