# vasp.lock

Categories: Files, Input files

The vasp.lock file is only used in combination with ICHARG=5. In each SCF step before constructing the new charge density VASP checks if the vasp.lock file is present, and if not waits before continuing. The file is empty, and its content is not considered in any way by VASP.

## Related tags and articles

ICHARG, GAMMA
