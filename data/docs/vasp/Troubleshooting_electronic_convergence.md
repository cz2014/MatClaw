# Troubleshooting electronic convergence

Categories: Howto, Electronic minimization

There can be many reasons why convergence to the electronic ground state fails. Below you find some general strategies to overcome convergence issues in the electronic minimization and some recommendations for specific cases, e.g., charged systems or magnetic systems. This lecture goes over electronic convergence in VASP.

## Step-by-step instructions

**Step 1:** Simplify the calculation and reduce time-to-solution. Try to create a minimal INCAR file with as few tags as possible. If the calculation converges, then gradually add them back until you find which one was causing the problem. Try to reduce the time-to-solution as much as possible by lowering the **k**-point sampling (or using gamma-only calculations if applicable), lower ENCUT, use PREC=Normal.

**Step 2:** Check the value of ISMEAR. If you have partially occupied states set ISMEAR=-1 or 1.

**Step 3:** Fixing the charge density (for cases where density mixing is used)

**Step 4:** Increase NBANDS. Check if you have enough bands. You can do this by looking at the OUTCAR file and checking that there are enough empty states, i.e., states with zero occupation. When using an iterative solver, the last states might not be accurately described, if these are occupied, then convergence is likely to fail. Often, the VASP default setting for NBANDS is insufficient for systems with f-orbitals or calculations with meta-GGA's.

**Step 5:** Switch ALGO.

**Step 6:** For IALGO=5X or 4X change TIME.

> **Tip:** You can get information at each electronic step using `NWRITE = 2,3`.

## Method-specific recommendations

In the following, we will describe a few recipes that work for particular systems.
Some of these recipes might be transferable even to other methods.

### Magnetic calculation with LDA+U

Magnetic calculations present a lot of challenges, in particular when the energy differences between different magnetic configurations are small.
Our recommendation is to split the calculation into multiple steps:

1. give initial magnetization only to the magnetic atoms
2. use spin-polarized calculation
3. perform the calculation in 3 steps (always starting from the previous WAVECAR):
   1. step 1 with ICHARG=12 and ALGO=Normal without any LDA+U tags
   2. step 2 with ALGO=All (Conjugate gradient) and a small TIME step 0.05 instead of the default 0.4 (this is crucial)
   3. step 3 add LDA+U tags keeping ALGO=All and small TIME

It might be helpful to split step 1. in two by first running with a smaller ENCUT and then restarting the calculation from the WAVECAR with the desired ENCUT.

### MBJ calculation

This exchange-correlation functional is not particularly easy to converge in some systems.
For these systems, we recommend that you split the calculation into multiple steps that successively bring you closer to the solution (always restarting from the WAVECAR of the previous step):

1. Converge with the PBE functional
2. Converge with the METAGGA=MBJ functional with the CMBJ parameter set to some value and ALGO=All and TIME=0.1
3. Converge with the METAGGA=MBJ functional without CMBJ parameter set and ALGO=All and TIME=0.1

Similar to the recipe for magnetic calculation with LDA+U, it might be helpful to run steps 1. to 3. with a low ENCUT and then perform step 3. again with the desired ENCUT.

### Dipole Correction

1. First, converge the calculation with LDIPOL=.FALSE. Store the WAVECAR in the same folder.
2. Use the WAVECAR to restart the calculation with LDIPOL=.TRUE.

### Magnetic calculations

What can one do when convergence is bad:

* Start from charge density of non-spin-polarized calculation using ISTART=0 (or remove the WAVECAR file) and ICHARG=1.
* Use linear mixing by setting BMIX=0.0001 and BMIX\_MAG=0.0001.
* Mix slowly, i.e., reduce AMIX and AMIX\_MAG.
* REDUCE MAXMIX, the number of steps stored in the Broyden mixer (default MAXMIX=45).
* Restart from partially converged results (stop a calculation after say 20 steps and restart from the WAVECAR file).
* Use constraints to stabilize the magnetic configuration.

## Related tags and articles

NWRITE
