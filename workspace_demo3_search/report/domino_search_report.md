
# Domain Wall (Domino) Switching Search in CuInP₂S₆
## E-field MD Simulations on 1×25×1 Monolayer Supercell (500 atoms, 50 Cu sites)

## Summary

We performed a heuristic search through (E-field, Temperature) parameter space
to identify conditions where Cu polarization switching in monolayer CuInP₂S₆
proceeds via sequential domain wall propagation ("domino switching") rather than
random/simultaneous flipping.

**Best condition found: E_z = −0.16 eV/Å/e, T = 50 K**
- Domino metric slope = **0.321 ps/site** (above the 0.3 threshold)
- 42/50 Cu sites flipped within the 38 ps simulation
- Flip time spread: 35.0 ps (min=2.0, max=37.0 ps)
- No Cu desorption (max |dz| = 2.42 Å < 5 Å)

## Methodology

### System Setup
- Unit cell: CuInP₂S₆ monolayer (20 atoms)
- Supercell: 1×25×1 (500 atoms, 50 Cu sites along the b-axis chain)
- DeePMD model: /pscratch/sd/c/cz2014/cips_distill/frozen_model.pb
- Born effective charges: Cu = +0.765, In = P = S = −0.085
- MD settings: 19,000 steps × 2 fs = 38 ps, NVT ensemble, trajectory saved every 10 steps

### Domino Detection Metric
1. Cu atoms sorted by b-fractional coordinate along the chain
2. Cu z-displacement from non-Cu midplane computed per frame
3. Gaussian smoothing (σ = 0.5 ps) applied in time
4. First-flip time: first zero-crossing of smoothed dz (positive → negative)
5. Mean absolute flip-time delay <|dt(d)|> computed for site separations d = 1..10
6. Linear fit slope of <|dt(d)|> vs d:
   - slope > 0.3 ps/site → domain wall propagation
   - slope ~ 0 → random/simultaneous flipping

## Search Path and Results

| Iter | E_z (eV/Å/e) | T (K) | Flipped | Slope (ps/site) | Assessment |
|------|---------------|-------|---------|-----------------|------------|
| 1    | −0.01         | 200   | 12/50   | N/A             | Too weak   |
| 1    | −0.05         | 200   | 39/50   | −0.064          | Random     |
| 2    | −0.05         | 100   | 0/50    | N/A             | No flipping|
| 2    | −0.03         | 150   | 8/50    | N/A             | Too weak   |
| 3    | −0.10         | 100   | 26/50   | 0.232           | Moderate   |
| 3    | −0.08         | 150   | 42/50   | 0.054           | Random     |
| 4    | −0.15         | 50    | 23/50   | 0.146           | Weak       |
| 4    | −0.12         | 80    | 19/50   | 0.272           | Near-domino|
| 5    | −0.14         | 80    | 44/50   | 0.274           | Near-domino|
| 5    | −0.18         | 50    | 50/50   | 0.054           | Random     |
| 6    | −0.15         | 10    | 0/50    | N/A             | No flipping|
| 6    | −0.20         | 30    | 50/50   | 0.066           | Random     |
| **7**| **−0.16**     |**50** | **42/50**|**0.321**       |**DOMINO**  |
| 7    | −0.13         | 60    | 1/50    | N/A             | Too weak   |

## Search Strategy

1. **Iteration 1** (E_z=−0.01, −0.05 at T=200K): Established that near Tc,
   flipping is either too sparse or random. At T=200K, thermal fluctuations
   nucleate flips independently at multiple sites.

2. **Iteration 2** (T=100K, 150K): Explored lower temperatures. At T=100K/E_z=−0.05,
   nothing flipped — field too weak below Tc. At T=150K/E_z=−0.03, barely any flipping.

3. **Iteration 3** (E_z=−0.10/T=100K, E_z=−0.08/T=150K): Stronger fields at lower T.
   E_z=−0.10/T=100K showed moderate sequential tendency (slope=0.232). Higher T
   still gave random behavior.

4. **Iteration 4** (E_z=−0.15/T=50K, E_z=−0.12/T=80K): Pushed to very low T.
   E_z=−0.12/T=80K gave slope=0.272 (near threshold). At T=50K, field barely above
   coercive threshold — only 23/50 flipped.

5. **Iteration 5** (E_z=−0.14/T=80K, E_z=−0.18/T=50K): Refined. E_z=−0.14/T=80K
   confirmed slope~0.274 with more sites flipping. E_z=−0.18/T=50K: all sites
   flipped fast (~10 ps) with slope~0.054 — field too strong, effectively simultaneous.

6. **Iteration 6** (E_z=−0.15/T=10K, E_z=−0.20/T=30K): Explored extreme conditions.
   At T=10K, E_z=−0.15 couldn't overcome the barrier at all. E_z=−0.20/T=30K:
   all flipped in ~10 ps, random.

7. **Iteration 7** (E_z=−0.16/T=50K, E_z=−0.13/T=60K): Fine-tuned near the coercive
   field at T=50K. **E_z=−0.16/T=50K achieved slope=0.321 ps/site — first clear
   detection of domain wall propagation!** The space-time heatmap shows the flipping
   front propagating along the chain over 35 ps.

## Physical Interpretation

Domain wall propagation requires:
1. **Low temperature** (T << Tc ≈ 230 K): Suppresses independent thermal nucleation
   at random sites along the chain
2. **E-field just above coercive threshold**: Strong enough to initiate and sustain
   propagation, but not so strong that all sites flip simultaneously

The sweet spot is a narrow window near the coercive field at low T:
- Below coercive field: no flipping (E_z=−0.13/T=60K, E_z=−0.15/T=10K)
- Just above coercive: sequential propagation (E_z=−0.16/T=50K ✓)
- Well above coercive: simultaneous flipping (E_z=−0.18/T=50K, E_z=−0.20/T=30K)

The best condition (E_z=−0.16/T=50K) shows the domain wall sweeping through
~42 sites over 35 ps, corresponding to a wall velocity of approximately
42 sites × 5.3 Å/site / 35 ps ≈ 6.4 Å/ps = 640 m/s.

## Deliverables

1. **figures/search_space.png**: All 14 explored (E, T) points colored by domino slope
2. **figures/best_spacetime_heatmap.png**: Space-time heatmap + flip-time plot for best condition
3. **figures/domino_metric_best.png**: <|dt(d)|> vs d with linear fit for best condition
4. **report/domino_search_report.md**: This report

## Computational Cost
- 14 E-field MD jobs × ~15 min each (debug queue) = ~3.5 hours wall time
- All jobs used the perlmutter_debug queue (2 concurrent slots)
- No Cu desorption observed in any simulation (all max |dz| < 5 Å)
