# STOPCAR

Categories: Files

Using the STOPCAR file it is possible to stop VASP during the program execution. If the STOPCAR file contains the line

```
LSTOP = .TRUE.
```

then VASP stops at the next ionic step. On the other hand, if the STOPCAR file contains the line

```
 LABORT = .TRUE.
```

VASP stops at the next electronic step, i.e. WAVECAR and CHGCAR might contain non converged results.

If possible use the first option.

---
