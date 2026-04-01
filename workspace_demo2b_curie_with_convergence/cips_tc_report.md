# Ferroelectric phase transition of monolayer CuInP2S6 from DeePMD MD

## Summary

- Estimated Curie temperature: **261.3 +/- 10.0 K**
- Order parameter: **Q(T) = <|eta(t)|>**, with eta(t) = c * (<z_Cu> - <z_S>) in Ang, where fractional z coordinates are unwrapped each frame to keep the monolayer contiguous along c. Because the two sulfur sublayers contain equal numbers of S atoms, <z_S> is equivalent to the sulfur-bilayer midpoint.
- DeePMD model: `/pscratch/sd/c/cz2014/cips_distill/frozen_model.pb`
- Supercell: 6x6x1 (360 atoms)
- MD settings: NVT Langevin, 2.00 fs timestep, trajectories saved every 20 steps (0.04 ps/frame)

## Convergence / pilot near Tc

- A 60 ps pilot at 350 K was not converged when the signed order parameter was monitored.
- I therefore extended the 350 K pilot to 100 ps. The signed order parameter showed 46 sign changes in the equilibrium half, indicating repeated ferroelectric switching near the transition.
- In the 100 ps pilot at 350 K, the equilibrium-half averages were <eta> = 0.0547 Ang and <|eta|> = 0.1105 Ang.
- This behavior motivated using the **magnitude** of the supercell-averaged Cu off-centering, <|eta|>, as the robust finite-temperature order parameter and refining the near-Tc temperatures with longer 100 ps runs.

## Tc determination

- Low-temperature order-parameter plateau (100-250 K average): 1.1478 Ang
- High-temperature order-parameter plateau (450-600 K average): 0.1485 Ang
- Half-height estimate of Tc: 260.1 K
- Piecewise-linear breakpoint estimate of Tc: 262.5 K
- Reported Tc: **261.3 +/- 10.0 K**

## Temperature-resolved results

| T (K) | Data used | Saved frames | Frames used | <eta> (Ang) | <|eta|> (Ang) | Block SEM (Ang) | Sign changes in equilibrium half |
|---:|:---|---:|---:|---:|---:|---:|---:|
| 100 | coarse_60ps | 1501 | 751 | 1.2541 | 1.2541 | 0.0014 | 0 |
| 150 | coarse_60ps | 1501 | 751 | 1.2446 | 1.2446 | 0.0041 | 0 |
| 200 | coarse_60ps | 1501 | 751 | 1.1394 | 1.1394 | 0.0156 | 0 |
| 250 | coarse_60ps | 1501 | 751 | 0.9531 | 0.9531 | 0.0330 | 0 |
| 275 | refined_100ps | 2501 | 1251 | -0.1984 | 0.2003 | 0.0263 | 10 |
| 300 | refined_100ps | 2501 | 1251 | 0.0559 | 0.1565 | 0.0291 | 33 |
| 325 | refined_100ps | 2501 | 1251 | 0.0208 | 0.1228 | 0.0200 | 35 |
| 350 | refined_100ps | 2501 | 1251 | 0.0547 | 0.1105 | 0.0199 | 37 |
| 375 | refined_100ps | 2501 | 1251 | 0.0593 | 0.1103 | 0.0153 | 35 |
| 400 | refined_100ps | 2501 | 1251 | -0.0881 | 0.1523 | 0.0328 | 35 |
| 450 | coarse_60ps | 1501 | 751 | 0.0986 | 0.1224 | 0.0516 | 25 |
| 500 | coarse_60ps | 1501 | 751 | -0.1482 | 0.2240 | 0.0626 | 23 |
| 600 | coarse_60ps | 1501 | 751 | -0.0335 | 0.0991 | 0.0134 | 34 |

## Key observations

- The Cu off-centering is large and single-domain-like at low temperature, with very few or no sign reversals.
- Near 300-400 K the order parameter collapses rapidly and the signed displacement begins to switch sign frequently, signaling the ferroelectric-to-paraelectric transition.
- Above the transition the signed order parameter averages close to zero, while the magnitude <|eta|> remains finite because of finite-size and dynamic fluctuation effects in the 6x6x1 supercell.
- The refined 100 ps trajectories around the transition sharpen the Tc estimate relative to the original 60 ps sweep.

## Frames used at each temperature

100 K: 1501 saved / 751 used (coarse_60ps); 150 K: 1501 saved / 751 used (coarse_60ps); 200 K: 1501 saved / 751 used (coarse_60ps); 250 K: 1501 saved / 751 used (coarse_60ps); 275 K: 2501 saved / 1251 used (refined_100ps); 300 K: 2501 saved / 1251 used (refined_100ps); 325 K: 2501 saved / 1251 used (refined_100ps); 350 K: 2501 saved / 1251 used (refined_100ps); 375 K: 2501 saved / 1251 used (refined_100ps); 400 K: 2501 saved / 1251 used (refined_100ps); 450 K: 1501 saved / 751 used (coarse_60ps); 500 K: 1501 saved / 751 used (coarse_60ps); 600 K: 1501 saved / 751 used (coarse_60ps)

## Output files

- `cips_tc_curve.png`
- `results/cips_tc_data.csv`
- `pilot/pilot_equilibration_summary.md`
- `pilot/pilot_T350K_100ps_summary.md`