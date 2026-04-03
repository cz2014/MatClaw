# Metadynamics calculations

Categories: Advanced molecular-dynamics sampling, Howto

### Anderson thermostat

* For a metadynamics run with Andersen thermostat, one has to:

1. Set the standard MD-related tags: IBRION=0, TEBEG, POTIM, and NSW
2. Set MDALGO=1 (MDALGO=11 in VASP 5.x), and choose an appropriate setting for ANDERSEN\_PROB
3. Set the parameters HILLS\_H, HILLS\_W, and HILLS\_BIN
4. Define collective variables in the ICONST-file, and set the `STATUS` parameter for the collective variables to 5
5. If needed, define the bias potential in the PENALTYPOT-file

The actual time-dependent bias potential is written to the HILLSPOT-file, which is updated after adding a new Gaussian. At the beginning of the simulation, VASP attempts to read the initial bias potential from the PENALTYPOT-file. For the continuation of a metadynamics run, copy HILLSPOT to PENALTYPOT. The values of all collective variables for each MD step are listed in REPORT-file, check the lines after the string Metadynamics.

### Nose-Hoover thermostat

* For a metadynamics run with Nose-Hoover thermostat, one has to:

1. Set the standard MD-related tags: IBRION=0, TEBEG, POTIM, and NSW
2. Set MDALGO=2 (MDALGO=21 in VASP 5.x), and choose an appropriate setting for SMASS
3. Set the parameters HILLS\_H, HILLS\_W, and HILLS\_BIN
4. Define collective variables in the ICONST-file, and set the STATUS parameter for the collective variables to 5
5. If needed, define the bias potential in the PENALTYPOT-file

The actual time-dependent bias potential is written to the HILLSPOT-file, which is updated after adding a new Gaussian. At the beginning of the simulation, VASP attempts to read the initial bias potential from the PENALTYPOT-file. For the continuation of a metadynamics run, copy HILLSPOT to PENALTYPOT. The values of all collective variables for each MD step are listed in REPORT-file, check the lines after the string Metadynamics.

## Related tags and sections

Metadynamics

---
