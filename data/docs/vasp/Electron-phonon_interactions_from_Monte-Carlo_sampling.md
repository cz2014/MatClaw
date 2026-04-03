# Electron-phonon interactions from Monte-Carlo sampling

Categories: Phonons, Electron-phonon interactions, Howto

> **Mind:** This feature is only available from VASP 6.0 or higher.

For the theory on electron-phonon interactions from Monte-Carlo (MC) sampling, see the theory page.

First of all this method needs a sufficiently large supercell.
It also involves phonon calculations for the $\Gamma$ point (see Phonons from finite differences). So many tags in the INCAR will be used from the phonon calculations.

The first implementation of electron-phonon interactions from MC sampling in VASP is found in Ref. .

The original publication of the ZG configuration (one-shot method) is found in Ref. .

## Step-by-step instructions

**Step 1**: Run a single calculation to create the POSCAR file(s) with special positions either belonging to the ZG configuration method or MC sampling. To enable electron-phonon interactions from MC methods PHON\_LMC=*.TRUE.* has to be set in the INCAR file. Also, IBRION=6 has to be selected (the sampling methods are currently only implemented for IBRION=6). The description of the remaining required INCAR tags for each method is given below. Both methods produce POSCAR files with different distorted Wycoff positions but unchanged Brillouin matrix. The ZG configuration method produces one structure for each temperature defined in PHON\_TLIST. The files are labeled as

```
POSCAR.T=TEMP.
```

The MC sampling code produces many POSCAR files at a given temperature defined by TEBEG. The files are labeled as

```
POSCAR.T=TEBEG.NUMBER
```

where NUMBER runs from 1 to PHON\_NSTRUCT.

**Step 2**: Run calculation for the previously created POSCAR files on the desired observable. These calculations can be anything that is suitable for an MC sum $\langle O(T)\rangle = \frac{1}{n} \sum\limits\_{i=1}^{n} O(x\_{T}^{\textrm{MC,i}})$, for example, band gap calculations, absorption spectra calculations, etc.

**Step 3 (optional)**: Calculate the desired observable for the original "pristine" supercell. This step can be necessary when changes to an observable due to electron-phonon interactions are required. An example of such a calculation is the calculation of the band-gap renormalization due to electron-phonon interactions.

**Step 4 (optional)**: If MC sampling was used, average the results over the number of structures created in step 1 (PHON\_NSTRUCT).

## ZG configuration (one-shot sampling)

M. Zacharias and F. Giustino introduced a one-shot method (named ZG configuration after the authors). This method is an approximation to full MC sampling. It only uses a single distorted structure and hence it is computationally much cheaper than the full MC sampling. It retains an accuracy very close to the full MC sampling for converged supercell sizes. For example, we showed that for the zero-point renormalization of the band gap, the accuracy is within 5 meV between the ZG configurations and the full MC sampling. Hence we suggest using this method preferably, when convergence of the supercell size is hard to achieve or the 5 meV accuracy is enough.

To select the ZG configuration PHON\_NSTRUCT=0 has to be set in the INCAR file.

The number of different temperatures and the list of temperatures (in K) have to be provided using the tags PHON\_NTLIST and PHON\_TLIST, respectively, in the INCAR file. An example would look like:

```
PHON_NTLIST = 4
PHON_TLIST = 0.0 100.0 200.0 350.0
```

This makes the simultaneous calculation of the ZG configuration at several temperatures possible.

An example INCAR file for a temperature range from 0-700 K (with step size of 100 K) is given as:

```
System = DEFAULT
PREC = Accurate
ISMEAR = 0; SIGMA = 0.1;
IBRION = 6
PHON_NTLIST = 8
PHON_TLIST = 0.0 100.0 200.0 300.0 400.0 500.0 600.0 700.0
PHON_NSTRUCT = 0
PHON_LMC = .TRUE.
```

## Full MC sampling

The tag PHON\_NSTRUCT sets the number of structures generated due to the MC sampling. Convergence of the observable with respect to this number should be monitored.

The tag TEBEG=0 is also needed to choose the temperature at which the sampling is run.

Additionally, the PHON\_LBOSE can be set *.TRUE.* or *.FALSE.* (default PHON\_LBOSE=*.TRUE.*), which selects Bose-Einstein or Maxwell-Boltzmann statistics, respectively.

A sample INCAR file for 0 K looks like the following:

```
System = DEFAULT
PREC = Accurate
ISMEAR = 0; SIGMA = 0.1;
IBRION = 6

PHON_LMC = .TRUE.
PHON_NSTRUCT = 100
TEBEG = 0.0
```

## Related tags and articles

* PHON\_LBOSE
* PHON\_LMC
* PHON\_NSTRUCT
* PHON\_NTLIST
* PHON\_TLIST
* Electron-phonon interactions from statistical sampling
* Band-structure renormalization
* Transport calculations

## References

---
