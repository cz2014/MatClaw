# Plugins

Categories: Howto

Implementing features over VASP carries a significant overhead, both in term of code development and maintenance.
An alternative approach is to use our Python plugin infrastructure. Simply write Python functions in a pre-defined format and VASP will recognize and execute your code while it is running.
This page describes the steps that you will need to write your first Python script and link it with VASP.

## Python scripting

Start by creating a file called `vasp_plugin.py` in the folder in which you are running a VASP calculation.
An alternative route through entry-points is also possible (see below for further instructions).
In `vasp_plugin.py` implement one or all of the following Python functions.

```
def structure(constants, additions):
    """Defines the PLUGINS/STRUCTURE interface"""

def force_and_stress(constants, additions):
    """Defines the PLUGINS/FORCE_AND_STRESS interface"""

def local_potential(constants, additions):
    """Defines the PLUGINS/LOCAL_POTENTIAL interface"""

def machine_learning():
    """Defines the PLUGINS/MACHINE_LEARNING interface"""

def occupancies(constants, additions):
    """Defines the PLUGINS/OCCUPANCIES interface"""
```

As the names of the input variables suggest,

1. `constants` provides a dataclass with quantities computed in VASP that must stay constant through the interface. Typically these include "metadata" such as the lattice vectors, number of grid points, etc. Some interfaces also pass in quantities such as the charge density as `constants`. Please check the page of the specific plugins' tag for more details on which quantities are available as constants. Alternatively, you may print the contents of `constants`.
2. `additions` stores quantities that are allowed to change in the interface. You must use the syntax `additions.<quantity-name> += ...` in order to change additions. That is, quantities must be "added" (or subtracted) to `additions` instead assigning them a new value. We use additions for two reasons. First, it makes sure that you use the memory from VASP; otherwise assigning might create a new array in memory and return zero to VASP. Secondly, adding the values allows multiple compatible plugins running at the same time.

The machine-learning plugin works a bit different. Please refer to its documentation for more details.

Each of the above interfaces may be called by VASP depending on the following INCAR tags

```
   PLUGINS/FORCE_AND_STRESS = T        ! Modifies the force and stress at the end of the SCF loop
   PLUGINS/LOCAL_POTENTIAL = T         ! Modifies the local potential every SCF step
   PLUGINS/MACHINE_LEARNING = T        ! Replaces the VASP force/stress engine with a machine-learned interatomic potential
   PLUGINS/OCCUPANCIES = T             ! Modifies NELECT, EFERMI, SIGMA, ISMEAR, EMIN, EMAX, NUPDOWN at the end of the SCF loop
   PLUGINS/STRUCTURE = T               ! Modifies the structure at the end of the SCF loop
```

Navigate to the relevant INCAR tag pages for further information.

## Exposing interfaces through entry-points (advanced)

Consider using entry points in cases where you do not want to move `vasp_plugin.py` to each new VASP calculation directory. This is also the approach you should take, if you want to distribute your plugin to other users. Within the group "vasp", add the following lines to your `pyproject.toml` file for each interface you would like to introduce new functions. For example, if you wanted to access the `force_and_stress` interface through an entry point, add the following lines to your `pyproject.toml` file,

```
   force_and_stress = "/path/to/python_function:force_and_stress"
```

## Related tags

PLUGINS/FORCE\_AND\_STRESS,
PLUGINS/LOCAL\_POTENTIAL,
PLUGINS/MACHINE\_LEARNING,
PLUGINS/OCCUPANCIES,
PLUGINS/STRUCTURE
