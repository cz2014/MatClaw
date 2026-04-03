# INIWAV

Categories: INCAR tag, Electronic minimization

INIWAV = 0 | 1

|  |  |  |
| --- | --- | --- |
| Default: **INIWAV** | = 1 |  |

Description: Specifies how to set up the initial orbitals in case `ISTART = 0`.

---

* `INIWAV = 0`

:   Take 'jellium orbitals', i.e., fill the Kohn-Sham–orbital arrays with plane waves of lowest kinetic energy = lowest eigenvectors for a constant potential ('jellium').

:   > **Important:** 'jellium' calculations require a specific POTCAR file, not included in the standard potential database.

* `INIWAV = 1`

:   Fill the Kohn-Sham–orbital arrays with random numbers. It is definitely the safest fool-proof switch. If you see long times for the wave function initialization, i.e. between the two messages "WAVECAR not read" and "entering main loop", in large systems consider using the parallel random number generator `RANDOM_GENERATOR = pcg_32`.

:   > **Tip:** Use `INIWAV = 1` whenever possible.

> **Mind:** The INIWAV tag is only used for jobs that start from scratch (`ISTART = 0`) and has no meaning otherwise.

## Related tags and sections

ISTART RANDOM\_GENERATOR
