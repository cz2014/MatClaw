# vaspgamma.h5

Categories: Files, Input files, Electronic occupancy

The vaspgamma.h5 file is an input file used when ICHARG=5 is set. It is read by VASP during an electronic minimization to incorporate additional occupation changes per k-point and orbital before calculating a new charge density. The file is only read when VASP is compiled with HDF5 support enabled and the text based GAMMA is not present.

> **Mind:** Available as of VASP 6.5.0

## Contents of the file

The vaspgamma.h5 contains the same information as the GAMMA file. The hdf5 archive should contain two groups:

1. band\_window - band window for each k point, i.e. the indices of bands for which the occupation changes are read in
2. deltaN - contains two groups (up and down) for each spin channel. Each group contains one dataset per k point with size given by the band window.

## Usage

> **Mind:** When reading and writing from and to hdf5 archives with VASP while it is running the tag LSYNCH5 should be set to True.

While ICHARG=5 is set, VASP will read this file right before the new charge density is calculated. However, VASP will only read the file and continues calculation if an additional file called vasp.lock is present in the current directory. This design allows to interface to an external code that performs between the SCF step some extra computation and updates the KS occupations.

For non spin-polarized calculations only the `up` group is read and used in VASP. Averaging over spin channels has to be done prior handing over the file to VASP.

See also GAMMA for further information.

## Related tags and articles

ICHARG, vasp.lock, GAMMA,DFT+DMFT

## References
