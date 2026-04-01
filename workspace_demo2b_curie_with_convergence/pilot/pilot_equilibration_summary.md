# CIPS pilot MD equilibration check

- Temperature: 350 K
- Supercell: 6x6x1 (360 atoms)
- Time step: 2.0 fs
- Steps: 30000
- Total time: 60.0 ps
- Saved frames: 1501
- Equilibrium frames used (second half): 751
- Signed per-frame order parameter: eta = c * (<z_Cu> - <z_S>) in Ang, after unwrapping fractional z coordinates to keep the monolayer contiguous along c.
- Because the top and bottom sulfur sublayers contain equal numbers of S atoms, <z_S> is equivalent to the sulfur-bilayer midpoint.
- Mean eta over the second half: 0.2917 Ang
- Mean |eta| over the second half: 0.2917 Ang
- Std(eta) over the second half: 0.0858 Ang
- SEM(eta) over the second half: 0.0031 Ang
- Drift between the third and fourth quarter of the trajectory: 0.0455 Ang
- Equilibration threshold: 0.0200 Ang
- Sign changes in eta(t): 0
- Equilibrated: False

## 5-ps block averages

-   0.00-  4.96 ps : mean=  1.1589 Ang, mean|eta|=  1.1589 Ang, std= 0.0791 Ang
-   5.00-  9.96 ps : mean=  0.8874 Ang, mean|eta|=  0.8874 Ang, std= 0.1197 Ang
-  10.00- 14.96 ps : mean=  0.6927 Ang, mean|eta|=  0.6927 Ang, std= 0.0761 Ang
-  15.00- 19.96 ps : mean=  0.5245 Ang, mean|eta|=  0.5245 Ang, std= 0.1199 Ang
-  20.00- 24.96 ps : mean=  0.2681 Ang, mean|eta|=  0.2681 Ang, std= 0.0541 Ang
-  25.00- 29.96 ps : mean=  0.3588 Ang, mean|eta|=  0.3588 Ang, std= 0.0472 Ang
-  30.00- 34.96 ps : mean=  0.3417 Ang, mean|eta|=  0.3417 Ang, std= 0.0528 Ang
-  35.00- 39.96 ps : mean=  0.1909 Ang, mean|eta|=  0.1909 Ang, std= 0.0479 Ang
-  40.00- 44.96 ps : mean=  0.2741 Ang, mean|eta|=  0.2741 Ang, std= 0.0932 Ang
-  45.00- 49.96 ps : mean=  0.3653 Ang, mean|eta|=  0.3653 Ang, std= 0.0450 Ang
-  50.00- 54.96 ps : mean=  0.3258 Ang, mean|eta|=  0.3258 Ang, std= 0.0537 Ang
-  55.00- 59.96 ps : mean=  0.2530 Ang, mean|eta|=  0.2530 Ang, std= 0.0677 Ang
-  60.00- 60.00 ps : mean=  0.1992 Ang, mean|eta|=  0.1992 Ang, std= 0.0000 Ang