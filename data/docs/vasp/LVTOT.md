# LVTOT

Categories: INCAR tag, Electronic ground-state properties, Potential

LVTOT = [logical]  
 Default: **LVTOT** = .FALSE.

Description: Determines whether the total local potential $V\_{\text{LOCPOT}}(\mathbf{r})$ (in eV) is written to the LOCPOT file.

---

$V\_{\text{LOCPOT}}(\mathbf{r}) =
V\_{\text{ionic}}(\mathbf{r}) +
\int \frac{n(\mathbf{r'})}{|\mathbf{r}-\mathbf{r'}|}d\mathbf{r'}+
V\_{\text{xc}}(\mathbf{r})$

where $V\_{\text{ionic}}(\mathbf{r})$ is the ionic potential,
the second term is the Hartree potential, and
$V\_{\text{xc}}(\mathbf{r})$ is the (semi-)local exchange-correlation potential.

If LVTOT=.TRUE., the $V\_{\text{LOCPOT}}(\mathbf{r})$ is written to the LOCPOT file and the POT file. The POT file additionally contains the augmentation part.

> **Warning:** LVHAR=T changes the content of the LOCPOT file.

WRT\_POTENTIAL also gives access to the total local potential and offers more options.

## Related tags and articles

Computing the work function, LVHAR, LOCPOT, WRT\_POTENTIAL, LVACPOTAV, POT

Examples that use this tag

---
