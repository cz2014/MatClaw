# HILLSPOT

Categories: Advanced molecular-dynamics sampling, Files

During the metadynamics simulation, the time-dependent bias potential (see MDALGO) is written in file HILLSPOT using the same format as for the PENALTYPOT file. If the metadynamics is performed as a sequence of shorter runs (which is recommended), the HILLSPOT file should be copied into PENALTYPOT at the end of each run. The following is an example of script running the sequence of 100 simulations:

```
#!/bin/bash
i=1
while [ $i -le 100 ]
do
  cp POSCAR POSCAR.$i
  ./vasp
  cp CONTCAR POSCAR
  cp REPORT REPORT.$i
  cp HILLSPOT PENALTYPOT
  let i=i+1
done
```

## Related Tags and Sections

HILLS\_BIN,
HILLS\_H,
HILLS\_W,
MDALGO

---
