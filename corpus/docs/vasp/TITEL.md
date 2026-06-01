# TITEL

Categories: Exchange-correlation functionals, POTCAR tag

TITEL = [string]

Definition: The TITEL tag specifies the title of a specific POTCAR file. It is also the first line of any POTCAR file. It is not possible nor necessary to set this tag in the INCAR file.

---

The POTCAR tag TITEL is a string composed of:

* the type of pseudopotential (either PAW for the projector-augmented-wave formalism or US for ultrasoft pseudopotentials,
* information about the exchange-correlation functional (GGA for PW91, PBE for PBE, missing for LDA),
* the element symbol,
* a suffix specifying the type of potential.
* the date of the pseudopotential creation.

In very early pseudopotentials releases, not all of this information is necessarily present.

## Examples

* TITEL = `PAW Ti_sv 26Sep2005` (Ti potential with the semicore *s* and *p* states added to the valence from the potpaw\_LDA.64 potential set.
* TITEL = `PAW_PBE Ti_sv_GW 05Dec2013` (Ti potential for GW calculations with the semicore *s* and *p* states added to the valence from the potpaw\_PBE.64 potential set
* TITEL = `PAW_GGA Ti_pv 07Sep2000` (Ti potential with the semicore *p* states added to the valence from the PW91 (2010) potential set.
* TITEL = `US Ti` (Ti potential with the semicore *p* states added to the valence from the PW91 USPP (2002) potential set. For this very old pseudopotential, no information on functional, valency, or creation date is available.

## Related tags and articles

POTCAR, pseudopotentials, available pseudopotentials

## References
