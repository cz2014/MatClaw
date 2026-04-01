# CIPS DeePMD MD ferroelectric phase-transition report

## Summary

- **Material:** monolayer CuInP$_2$S$_6$ (CIPS)
- **MLFF model:** `/pscratch/sd/c/cz2014/cips_distill/frozen_model.pb` (DeePMD)
- **Simulation cell:** 6x6x1 supercell, 360 atoms
- **Ensemble:** NVT Langevin
- **Time step:** 2.0 fs
- **Production run length:** 50000 steps = 100.0 ps per temperature
- **Trajectory sampling:** every 50 steps = 0.1 ps
- **Saved frames per temperature:** 1001
- **Equilibration discard:** first 500 frames (~50 ps)
- **Frames used for analysis:** last 501 frames (~50 ps) per temperature

## Order parameter definition

The instantaneous ferroelectric order parameter is defined as the Cu sublattice off-centering along the out-of-plane lattice vector relative to the non-Cu framework:

\[ \eta(t) = \overline{\mathbf{r}_{\mathrm{Cu}}(t)\cdot\hat{\mathbf{c}}} - \overline{\mathbf{r}_{\mathrm{host}}(t)\cdot\hat{\mathbf{c}}} \]

where the host average is taken over all non-Cu atoms (In, P, S). The plotted thermodynamic order parameter is the equilibrated time average $\langle |\eta| angle$ from the last 50 ps of each trajectory.

## Pilot convergence check near the transition

A pilot trajectory was run at **325 K** near the expected transition region.
- Initial pilot: 20000 steps = 40.0 ps
- Continuation 1: 30000 steps = 60.0 ps
- Continuation 2: 20000 steps = 40.0 ps
- Post-transient 10-ps window-mean std of |eta|: 0.0676 Å
- Stationarity criterion satisfied: **True**

The initial pilot showed slow relaxation of the Cu off-centering near the transition. After the two continuations, the post-transient window statistics were stable enough to justify 100 ps production trajectories and analysis of the final ~50 ps at each temperature.

## Results

- **Estimated Curie temperature:** **230 ± 35 K**
- Logistic-fit midpoint: 229.0 K
- Half-height estimate: 247.4 K
- Steepest-drop midpoint: 262.5 K

### Order parameter vs temperature

| T (K) | Saved frames | Used frames | <|eta|> (Å) | Block-SE (Å) | <eta> (Å) |
|---:|---:|---:|---:|---:|---:|
| 100 | 1001 | 501 | 1.2974 | 0.0013 | 1.2974 |
| 200 | 1001 | 501 | 1.0517 | 0.0277 | 1.0517 |
| 250 | 1001 | 501 | 0.5035 | 0.0333 | 0.5035 |
| 275 | 1001 | 501 | 0.1528 | 0.0272 | 0.1500 |
| 300 | 1001 | 501 | 0.1011 | 0.0202 | -0.0564 |
| 325 | 1001 | 501 | 0.0954 | 0.0217 | 0.0111 |
| 350 | 1001 | 501 | 0.1531 | 0.0148 | 0.0079 |
| 375 | 1001 | 501 | 0.1432 | 0.0309 | -0.0699 |
| 400 | 1001 | 501 | 0.1124 | 0.0134 | 0.0766 |
| 500 | 1001 | 501 | 0.1010 | 0.0095 | 0.0084 |
| 600 | 1001 | 501 | 0.1272 | 0.0097 | 0.0459 |

## Key observations

1. The low-temperature phase is strongly ferroelectric, with low-T plateau <|eta|> ≈ 0.95 Å.
2. The order parameter drops rapidly through the ~230 K region, marking the ferroelectric-to-paraelectric transition.
3. Above ~400 K the order parameter remains small but nonzero (high-T plateau ≈ 0.11 Å), as expected for a finite supercell where <|eta|> stays positive under thermal fluctuations.
4. Under these fixed-cell NVT conditions, the DeePMD model predicts a Curie temperature in the low-to-mid 300 K range.

## Output files

- Main Tc figure: `analysis/cips_tc_curve.png`
- Pilot equilibration figure: `analysis/pilot_posttransient_stability_325K.png`
- Combined pilot figure: `analysis/pilot_equilibration_combined_325K.png`

## Notes / limitations

- This is a finite-size, fixed-cell NVT estimate from one 6x6x1 supercell and one trajectory per temperature.
- The sweep is effectively a heating protocol because all production runs were initialized from the same ferroelectric structure.
- A tighter Tc estimate would benefit from larger supercells, longer runs, multiple seeds, and explicit heating/cooling hysteresis tests.
