# Constrained molecular dynamics calculations

Categories: Advanced molecular-dynamics sampling, Howto

Geometric constraints are introduced by defining one or more entries with the STATUS parameter set to 0 in the ICONST-file. Constraints can be used within a standard NVT or NpT MD setting introduced by MDALGO=1|2|3. Note that fixing geometric parameters related to lattice vectors is not allowed within an NVT simulation (VASP would terminate with an error message). Constraints can be combined with restraints, time-dependent bias potentials (Metadynamics), monitored coordinates and other elements available within the context of MD.
