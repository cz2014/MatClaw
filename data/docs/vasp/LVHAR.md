# LVHAR

Categories: INCAR tag, Electrostatics, Potential

LVHAR = [logical]  
 Default: **LVHAR** = .FALSE.

Description: Determines whether the local potential $V\_{\text{ionic}}(\mathbf{r}) +V\_{\text{hartree}}(\mathbf{r})$ (in eV) is written to the LOCPOT file.

---

$V\_{\text{ionic}}(\mathbf{r})+V\_{\text{hartree}}(\mathbf{r}) =
V\_{\text{ionic}}(\mathbf{r}) +
\int \frac{n(\mathbf{r'})}{|\mathbf{r}-\mathbf{r'}|}d\mathbf{r'}$

where $V\_{\text{ionic}}(\mathbf{r})$ is the ionic potential as mimicked by the pseudopotentials and $V\_{\text{hartree}}(\mathbf{r})$ is the Hartree potential.

The local potential is written to the LOCPOT file and hence to the same file as the local potential for LVTOT=T. Carefully check that the LOCPOT file contains the potential you expect.
WRT\_POTENTIAL also gives access to the ionic and Hartree potentials and offers more options.

> **Warning:** Setting LVHAR=True will set LVTOT=False.

See LOCPOT to find out how to write $V\_{\text{ionic}}(\mathbf{r}) +V\_{\text{hartree}}(\mathbf{r})$ in VASP < 5.2.12.

## Related tags and articles

Computing the work function, LVTOT, LOCPOT, WRT\_POTENTIAL, LVACPOTAV

Examples that use this tag
