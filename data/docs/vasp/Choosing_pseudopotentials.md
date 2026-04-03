# Choosing pseudopotentials

Categories: Pseudopotentials, Howto

Several pseudopotential variants labeled by suffixes exist for many elements. When making a choice, it is necessary to balance computational cost, accuracy, and transferability.

* To set up a minimal working example of your calculation, follow prepare a POTCAR.
* Try to create a smaller test calculation and perform your own tests to confirm if the quantity of interest is sensitive to the choice of the pseudopotential. It might be possible to opt for a computationally cheaper POTCAR and gain performance. On the other hand, it could be necessary to opt for a computationally demanding setup to obtain correct results.
* With the aspects described in the next section in mind, carefully look over the recommendations for each group in the periodic table.

## Aspects to refine the choice of pseudopotentials

**Aspect 1:** The bond lengths and the valency of the ions.

:   Short bonds will require harder potentials, and semicore states might have to be treated as valence for certain chemical bonding. For some elements, variants for specific valency exist; for example, the suffix \_2 or \_3 can be used to describe  fixed divalent or trivalent Lanthanides.

**Aspect 2:** The physical or chemical property of interest.

:   If you are only interested in a rough structure optimization, soft potentials (\_s) with minimal valency may suffice. This approach might also work for phonon calculations that rely on large supercells.
:   On the other hand, when optimizing a magnetic structure, it may be necessary to include semicore states in the valence (\_pv and \_sv).
:   For the computation of optical properties, it is crucial to use GW potentials.

**Aspect 3:** The method or algorithm used in your calculation.

:   For any calculation involving unoccupied states significantly above the Fermi energy, the \_GW variants of potentials are superior and should be used. Particularly, all kinds of calculations within many-body perturbation theory need a high number of empty bands. Therefore, when GW, BSE, etc. is performed, the GW potentials should be used throughout the workflow.

:   Hartree-Fock and hybrid caluclations should *not* be performed with soft potentials (\_s). Moreover, any calculations where you switch the exchange-correlation functional should *not* be performed with soft potentials (\_s).

:   For standard DFT-ground-state calculations, using \_GW or \_h potentials is usually unnecessary unless, e.g., the property of interest or geometry of the structure demands it.

## Recommendations and advice

### Recommended PAW potentials

#### Standard DFT without the need for many unoccupied states

:   The table directly below highlights recommended PAW potentials in **bold**.
:   These potentials are *not ideal* for calculations involving a large number of excited states as needed, e.g., for optical properties or many-body perturbation theory.

:   |  |  |  |  |
    | --- | --- | --- | --- |
    | Standard PBE potentials (potpaw.64) | | | |
    | Potential name | Number of valence electrons | Valence electron configuration | ENAMX [eV] |
    | **H** | **1** | **1*s*1** | **250.0** |
    | H.25 | 0.25 | 1*s*0.25 | 250.0 |
    | H.33 | 0.33 | 1*s*0.33 | 250.0 |
    | H.42 | 0.42 | 1*s*0.42 | 250.0 |
    | H.5 | 0.5 | 1*s*0.5 | 250.0 |
    | H.58 | 0.58 | 1*s*0.58 | 250.0 |
    | H.66 | 0.66 | 1*s*0.66 | 250.0 |
    | H.75 | 0.75 | 1*s*0.75 | 250.0 |
    | H1.25 | 1.25 | 1*s*1.25 | 250.0 |
    | H1.33 | 1.33 | 1*s*1.33 | 250.0 |
    | H1.5 | 1.5 | 1*s*1.5 | 250.0 |
    | H1.66 | 1.66 | 1*s*1.66 | 250.0 |
    | H1.75 | 1.75 | 1*s*1.75 | 250.0 |
    | H\_AE | 1 | 1*s*1 | 1000.0 |
    | H\_h | 1 | 1*s*1 | 700.0 |
    | H\_s | 1 | 1*s*1 | 200.0 |
    | **He** | **2** | **1*s*2** | **478.896** |
    | He\_AE | 2 | 1*s*2 | 2135.871 |
    | Li | 1 | 2*s*1 | 140.0 |
    | **Li\_sv** | **3** | **1*s*2 2*s*1** | **499.034** |
    | **Be** | **2** | **2*s*1.99 2*p*0.01** | **247.543** |
    | Be\_sv | 4 | 1*s*2 2*s*1.99 2*p*0.01 | 308.768 |
    | **B** | **3** | **2*s*2 2*p*1** | **318.614** |
    | B\_h | 3 | 2*s*2 2*p*1 | 700.0 |
    | B\_s | 3 | 2*s*2 2*p*1 | 269.245 |
    | **C** | **4** | **2*s*2 2*p*2** | **400.0** |
    | C\_h | 4 | 2*s*2 2*p*2 | 741.689 |
    | C\_s | 4 | 2*s*2 2*p*2 | 273.911 |
    | **N** | **5** | **2*s*2 2*p*3** | **400.0** |
    | N\_h | 5 | 2*s*2 2*p*3 | 755.582 |
    | N\_s | 5 | 2*s*2 2*p*3 | 279.692 |
    | **O** | **6** | **2*s*2 2*p*4** | **400.0** |
    | O\_h | 6 | 2*s*2 2*p*4 | 765.519 |
    | O\_s | 6 | 2*s*2 2*p*4 | 282.853 |
    | **F** | **7** | **2*s*2 2*p*5** | **400.0** |
    | F\_h | 7 | 2*s*2 2*p*5 | 772.626 |
    | F\_s | 7 | 2*s*2 2*p*5 | 289.837 |
    | **Ne** | **8** | **2*s*2 2*p*6** | **343.606** |
    | Na | 1 | 3*s*1 | 101.968 |
    | **Na\_pv** | **7** | **2*p*6 3*s*1** | **259.561** |
    | Na\_sv | 9 | 2*s*2 2*p*6 3*s*1 | 645.64 |
    | **Mg** | **2** | **3*s*2** | **200.0** |
    | Mg\_pv | 8 | 2*p*6 3*s*2 | 403.929 |
    | Mg\_sv | 10 | 2*s*2 2*p*6 3*s*2 | 495.223 |
    | **Al** | **3** | **3*s*2 3*p*1** | **240.3** |
    | **Si** | **4** | **3*s*2 3*p*2** | **245.345** |
    | **P** | **5** | **3*s*2 3*p*3** | **255.04** |
    | P\_h | 5 | 3*s*2 3*p*3 | 390.202 |
    | **S** | **6** | **3*s*2 3*p*4** | **258.689** |
    | S\_h | 6 | 3*s*2 3*p*4 | 402.436 |
    | **Cl** | **7** | **3*s*2 3*p*5** | **262.472** |
    | Cl\_h | 7 | 3*s*2 3*p*5 | 409.136 |
    | **Ar** | **8** | **3*s*2 3*p*6** | **266.408** |
    | K\_pv | 7 | 3*p*6 4*s*1 | 116.731 |
    | **K\_sv** | **9** | **3*s*2 3*p*6 4*s*1** | **259.264** |
    | Ca\_pv | 8 | 3*p*6 4*s*2 | 119.559 |
    | **Ca\_sv** | **10** | **3*s*2 3*p*6 4*s*2** | **266.622** |
    | Sc | 3 | 3*d*2 4*s*1 | 154.763 |
    | **Sc\_sv** | **11** | **3*s*2 3*p*6 3*d*2 4*s*1** | **222.66** |
    | Ti | 4 | 3*d*3 4*s*1 | 178.33 |
    | Ti\_pv | 10 | 3*p*6 3*d*3 4*s*1 | 222.335 |
    | **Ti\_sv** | **12** | **3*s*2 3*p*6 3*d*3 4*s*1** | **274.61** |
    | V | 5 | 3*d*4 4*s*1 | 192.543 |
    | V\_pv | 11 | 3*p*6 3*d*4 4*s*1 | 263.673 |
    | **V\_sv** | **13** | **3*s*2 3*p*6 3*d*4 4*s*1** | **263.673** |
    | Cr | 6 | 3*d*5 4*s*1 | 227.08 |
    | **Cr\_pv** | **12** | **3*p*6 3*d*5 4*s*1** | **265.681** |
    | Cr\_sv | 14 | 3*s*2 3*p*6 3*d*5 4*s*1 | 395.471 |
    | Mn | 7 | 3*d*6 4*s*1 | 269.864 |
    | **Mn\_pv** | **13** | **3*p*6 3*d*6 4*s*1** | **269.864** |
    | Mn\_sv | 15 | 3*s*2 3*p*6 3*d*6 4*s*1 | 387.187 |
    | **Fe** | **8** | **3*d*7 4*s*1** | **267.882** |
    | Fe\_pv | 14 | 3*p*6 3*d*7 4*s*1 | 293.238 |
    | Fe\_sv | 16 | 3*s*2 3*p*6 3*d*7 4*s*1 | 390.558 |
    | **Co** | **9** | **3*d*8 4*s*1** | **267.968** |
    | Co\_pv | 15 | 3*p*6 3*d*8 4*s*1 | 271.042 |
    | Co\_sv | 17 | 3*s*2 3*p*6 3*d*8 4*s*1 | 390.362 |
    | **Ni** | **10** | **3*d*9 4*s*1** | **269.532** |
    | Ni\_pv | 16 | 3*p*6 3*d*9 4*s*1 | 367.986 |
    | **Cu** | **11** | **3*d*10 4*s*1** | **295.446** |
    | Cu\_pv | 17 | 3*p*6 3*d*10 4*s*1 | 368.648 |
    | **Zn** | **12** | **3*d*10 4*s*2** | **276.723** |
    | Ga | 3 | 4*s*2 4*p*1 | 134.678 |
    | **Ga\_d** | **13** | **3*d*10 4*s*2 4*p*1** | **282.691** |
    | Ga\_h | 13 | 3*d*10 4*s*2 4*p*1 | 404.601 |
    | Ge | 4 | 4*s*2 4*p*2 | 173.807 |
    | **Ge\_d** | **14** | **3*d*10 4*s*2 4*p*2** | **310.294** |
    | Ge\_h | 14 | 3*d*10 4*s*2 4*p*2 | 410.425 |
    | **As** | **5** | **4*s*2 4*p*3** | **208.702** |
    | As\_d | 15 | 3*d*10 4*s*2 4*p*3 | 288.651 |
    | **Se** | **6** | **4*s*2 4*p*4** | **211.555** |
    | **Br** | **7** | **4*s*2 4*p*5** | **216.285** |
    | **Kr** | **8** | **4*s*2 4*p*6** | **185.331** |
    | Rb\_pv | 7 | 4*p*6 4*d*0.001 5*s*0.999 | 121.882 |
    | **Rb\_sv** | **9** | **4*s*2 4*p*6 4*d*0.001 5*s*0.999** | **220.112** |
    | **Sr\_sv** | **10** | **4*s*2 4*p*6 4*d*0.001 5*s*1.999** | **229.353** |
    | **Y\_sv** | **11** | **4*s*2 4*p*6 4*d*2 5*s*1** | **202.626** |
    | **Zr\_sv** | **12** | **4*s*2 4*p*6 4*d*3 5*s*1** | **229.898** |
    | Nb\_pv | 11 | 4*p*6 4*d*4 5*s*1 | 208.608 |
    | **Nb\_sv** | **13** | **4*s*2 4*p*6 4*d*4 5*s*1** | **293.235** |
    | Mo | 6 | 4*d*5 5*s*1 | 224.584 |
    | Mo\_pv | 12 | 4*p*6 4*d*5 5*s*1 | 224.584 |
    | **Mo\_sv** | **14** | **4*s*2 4*p*6 4*d*5 5*s*1** | **242.676** |
    | Tc | 7 | 4*d*6 5*s*1 | 228.694 |
    | **Tc\_pv** | **13** | **4*p*6 4*d*6 5*s*1** | **263.523** |
    | Tc\_sv | 15 | 4*s*2 4*p*6 4*d*6 5*s*1 | 318.703 |
    | Ru | 8 | 4*d*7 5*s*1 | 213.271 |
    | **Ru\_pv** | **14** | **4*p*6 4*d*7 5*s*1** | **240.049** |
    | Ru\_sv | 16 | 4*s*2 4*p*6 4*d*7 5*s*1 | 318.855 |
    | Rh | 9 | 4*d*8 5*s*1 | 228.996 |
    | **Rh\_pv** | **15** | **4*p*6 4*d*8 5*s*1** | **247.408** |
    | **Pd** | **10** | **4*d*9 5*s*1** | **250.925** |
    | Pd\_pv | 16 | 4*p*6 4*d*9 5*s*1 | 250.925 |
    | **Ag** | **11** | **4*d*10 5*s*1** | **249.844** |
    | Ag\_pv | 17 | 4*p*6 4*d*10 5*s*1 | 297.865 |
    | **Cd** | **12** | **4*d*10 5*s*2** | **274.336** |
    | In | 3 | 5*s*2 5*p*1 | 95.934 |
    | **In\_d** | **13** | **4*d*10 5*s*2 5*p*1** | **239.211** |
    | Sn | 4 | 5*s*2 5*p*2 | 103.236 |
    | **Sn\_d** | **14** | **4*d*10 5*s*2 5*p*2** | **241.083** |
    | **Sb** | **5** | **5*s*2 5*p*3** | **172.069** |
    | **Te** | **6** | **5*s*2 5*p*4** | **174.982** |
    | **I** | **7** | **5*s*2 5*p*5** | **175.647** |
    | **Xe** | **8** | **5*s*2 5*p*6** | **153.118** |
    | **Cs\_sv** | **9** | **5*s*2 5*p*6 6*s*1** | **220.318** |
    | **Ba\_sv** | **10** | **5*s*2 5*p*6 5*d*0.01 6*s*1.99** | **187.181** |
    | **La** | **11** | **4*f*0.0001 5*s*2 5*p*6 5*d*0.9999 6*s*2** | **219.292** |
    | La\_s | 9 | 5*p*6 5*d*1 6*s*2 | 136.53 |
    | **Ce** | **12** | **4*f*1 5*s*2 5*p*6 5*d*1 6*s*2** | **273.042** |
    | Ce\_3 | 11 | 5*s*2 5*p*6 5*d*1 6*s*2 | 176.506 |
    | Ce\_h | 12 | 4*f*1 5*s*2 5*p*6 5*d*1 6*s*2 | 299.9 |
    | Pr | 13 | 4*f*2.5 5*s*2 5*p*6 5*d*0.5 6*s*2 | 337.25 |
    | **Pr\_3** | **11** | **5*s*2 5*p*6 5*d*1 6*s*2** | **181.719** |
    | Pr\_h | 13 | 4*f*2.5 5*s*2 5*p*6 5*d*0.5 6*s*2 | 400.742 |
    | Nd | 14 | 4*f*3.5 5*s*2 5*p*6 5*d*0.5 6*s*2 | 338.34 |
    | **Nd\_3** | **11** | **5*s*2 5*p*6 5*d*1 6*s*2** | **182.619** |
    | Nd\_h | 14 | 4*f*3.5 5*s*2 5*p*6 5*d*0.5 6*s*2 | 402.016 |
    | Pm | 15 | 4*f*4.5 5*s*2 5*p*6 5*d*0.5 6*s*2 | 340.358 |
    | **Pm\_3** | **11** | **5*s*2 5*p*6 5*d*1 6*s*2** | **176.959** |
    | Pm\_h | 15 | 4*f*4.5 5*s*2 5*p*6 5*d*0.5 6*s*2 | 404.406 |
    | Sm | 16 | 4*f*5.5 5*s*2 5*p*6 5*d*0.5 6*s*2 | 341.177 |
    | **Sm\_3** | **11** | **5*s*2 5*p*6 5*d*1 6*s*2** | **177.087** |
    | Sm\_h | 16 | 4*f*5.5 5*s*2 5*p*6 5*d*0.5 6*s*2 | 405.382 |
    | Eu | 17 | 4*f*6.5 5*s*2 5*p*6 5*d*0.5 6*s*2 | 344.705 |
    | **Eu\_2** | **8** | **5*p*6 6*s*2** | **99.328** |
    | Eu\_3 | 9 | 5*p*6 5*d*1 6*s*2 | 129.057 |
    | Eu\_h | 17 | 4*f*6.5 5*s*2 5*p*6 5*d*0.5 6*s*2 | 403.212 |
    | Gd | 18 | 4*f*7.5 5*s*2 5*p*6 5*d*0.5 6*s*2 | 342.859 |
    | **Gd\_3** | **9** | **5*p*6 5*d*1 6*s*2** | **154.332** |
    | Gd\_h | 18 | 4*f*7.5 5*s*2 5*p*6 5*d*0.5 6*s*2 | 407.403 |
    | Tb | 19 | 4*f*8.5 5*s*2 5*p*6 5*d*0.5 6*s*2 | 340.855 |
    | **Tb\_3** | **9** | **5*p*6 5*d*1 6*s*2** | **155.613** |
    | Tb\_h | 19 | 4*f*8.5 5*s*2 5*p*6 5*d*0.5 6*s*2 | 405.043 |
    | Dy | 20 | 4*f*9.5 5*s*2 5*p*6 5*d*0.5 6*s*2 | 341.547 |
    | **Dy\_3** | **9** | **5*p*6 5*d*1 6*s*2** | **155.713** |
    | Dy\_h | 20 | 4*f*9.5 5*s*2 5*p*6 5*d*0.5 6*s*2 | 405.886 |
    | Ho | 21 | 4*f*10.5 5*s*2 5*p*6 5*d*0.5 6*s*2 | 343.845 |
    | **Ho\_3** | **9** | **5*p*6 5*d*1 6*s*2** | **154.137** |
    | Ho\_h | 21 | 4*f*10.5 5*s*2 5*p*6 5*d*0.5 6*s*2 | 415.91 |
    | Er | 22 | 4*f*11.5 5*s*2 5*p*6 5*d*0.5 6*s*2 | 346.295 |
    | Er\_2 | 8 | 5*p*6 6*s*2 | 119.75 |
    | **Er\_3** | **9** | **5*p*6 5*d*1 6*s*2** | **155.037** |
    | Er\_h | 22 | 4*f*11.5 5*s*2 5*p*6 5*d*0.5 6*s*2 | 429.583 |
    | Tm | 23 | 4*f*12.5 5*s*2 5*p*6 5*d*0.5 6*s*2 | 344.206 |
    | **Tm\_3** | **9** | **5*p*6 5*d*1 6*s*2** | **149.221** |
    | Tm\_h | 23 | 4*f*12.5 5*s*2 5*p*6 5*d*0.5 6*s*2 | 419.812 |
    | Yb | 24 | 4*f*13.5 5*s*2 5*p*6 5*d*0.5 6*s*2 | 344.312 |
    | **Yb\_2** | **8** | **5*p*6 6*s*2** | **112.578** |
    | Yb\_3 | 9 | 5*p*6 5*d*1 6*s*2 | 188.359 |
    | Yb\_h | 24 | 4*f*13.5 5*s*2 5*p*6 5*d*0.5 6*s*2 | 409.285 |
    | Lu | 25 | 4*f*14 5*s*2 5*p*6 5*d*1 6*s*2 | 255.695 |
    | **Lu\_3** | **9** | **5*p*6 5*d*1 6*s*2** | **154.992** |
    | Hf | 4 | 5*d*3 6*s*1 | 220.334 |
    | **Hf\_pv** | **10** | **5*p*6 5*d*3 6*s*1** | **220.334** |
    | Hf\_sv | 12 | 5*s*2 5*p*6 5*d*4 | 237.444 |
    | Ta | 5 | 5*d*4 6*s*1 | 223.667 |
    | **Ta\_pv** | **11** | **5*p*6 5*d*4 6*s*1** | **223.667** |
    | W | 6 | 5*d*5 6*s*1 | 223.057 |
    | **W\_sv** | **14** | **5*s*2 5*p*6 5*d*5 6*s*1** | **223.057** |
    | **Re** | **7** | **5*d*6 6*s*1** | **226.216** |
    | Re\_pv | 13 | 5*p*6 5*d*6 6*s*1 | 226.216 |
    | **Os** | **8** | **5*d*7 6*s*1** | **228.022** |
    | Os\_pv | 14 | 5*p*6 5*d*7 6*s*1 | 228.022 |
    | **Ir** | **9** | **5*d*8 6*s*1** | **210.864** |
    | **Pt** | **10** | **5*d*9 6*s*1** | **230.283** |
    | Pt\_pv | 16 | 5*p*6 5*d*9 6*s*1 | 294.607 |
    | **Au** | **11** | **5*d*10 6*s*1** | **229.943** |
    | **Hg** | **12** | **5*d*10 6*s*2** | **233.204** |
    | Tl | 3 | 6*s*2 6*p*1 | 90.14 |
    | **Tl\_d** | **13** | **5*d*10 6*s*2 6*p*1** | **237.053** |
    | Pb | 4 | 6*s*2 6*p*2 | 97.973 |
    | **Pb\_d** | **14** | **5*d*10 6*s*2 6*p*2** | **237.835** |
    | Bi | 5 | 6*s*2 6*p*3 | 105.037 |
    | **Bi\_d** | **15** | **5*d*10 6*s*2 6*p*3** | **242.839** |
    | Po | 6 | 6*s*2 6*p*4 | 159.707 |
    | **Po\_d** | **16** | **5*d*10 6*s*2 6*p*4** | **264.565** |
    | **At** | **7** | **6*s*2 6*p*5** | **161.43** |
    | **Rn** | **8** | **6*s*2 6*p*6** | **151.497** |
    | **Fr\_sv** | **9** | **6*s*2 6*p*6 7*s*1** | **214.54** |
    | **Ra\_sv** | **10** | **6*s*2 6*p*6 7*s*2** | **237.367** |
    | **Ac** | **11** | **6*s*2 6*p*6 6*d*1 7*s*2** | **172.351** |
    | **Th** | **12** | **5*f*1 6*s*2 6*p*6 6*d*1 7*s*2** | **247.306** |
    | Th\_s | 10 | 5*f*1 6*p*6 6*d*1 7*s*2 | 169.363 |
    | **Pa** | **13** | **5*f*1 6*s*2 6*p*6 6*d*2 7*s*2** | **252.193** |
    | Pa\_s | 11 | 5*f*1 6*p*6 6*d*2 7*s*2 | 193.466 |
    | **U** | **14** | **5*f*2 6*s*2 6*p*6 6*d*2 7*s*2** | **252.502** |
    | U\_s | 14 | 5*f*2 6*s*2 6*p*6 6*d*2 7*s*2 | 209.23 |
    | **Np** | **15** | **5*f*3 6*s*2 6*p*6 6*d*2 7*s*2** | **254.26** |
    | Np\_s | 15 | 5*f*3 6*s*2 6*p*6 6*d*2 7*s*2 | 207.713 |
    | **Pu** | **16** | **5*f*4 6*s*2 6*p*6 6*d*2 7*s*2** | **254.353** |
    | Pu\_s | 16 | 5*f*4 6*s*2 6*p*6 6*d*2 7*s*2 | 207.83 |
    | **Am** | **17** | **5*f*5 6*s*2 6*p*6 6*d*2 7*s*2** | **255.875** |
    | **Cm** | **18** | **5*f*6 6*s*2 6*p*6 6*d*2 7*s*2** | **257.953** |
    | Cf | 20 | 5*f*8 6*s*2 6*p*6 6*d*2 7*s*2 | 414.614 |

#### Calculation requiring a large number of unoccupied states

:   The following table highlights recommended PAW potentials for calculations involving many states above the Fermi energy in **bold**.
:   They are optimized for scattering properties high above the Fermi level and thus have advantages if many unoccupied states are involved, as for optical properties or many-body perturbation theory.

:   |  |  |  |  |
    | --- | --- | --- | --- |
    | GW potentials (potpaw.64) | | | |
    | Potential name | Number of valence electrons | Valence electron configuration | ENAMX [eV] |
    | **H\_GW** | **1** | **1*s*1** | **300.0** |
    | H\_GW\_new | 1 | 1*s*1 | 536.615 |
    | H\_h\_GW | 1 | 1*s*1 | 700.0 |
    | **He\_GW** | **2** | **1*s*2** | **405.78** |
    | Li\_AE\_GW | 3 | 1*s*2 2*p*1 | 433.699 |
    | Li\_GW | 1 | 2*s*1 | 112.104 |
    | **Li\_sv\_GW** | **3** | **1*s*2 2*p*1** | **433.699** |
    | Be\_GW | 2 | 2*s*1.9999 2*p*0.001 | 247.543 |
    | **Be\_sv\_GW** | **4** | **1*s*2 2*p*2** | **537.454** |
    | **B\_GW** | **3** | **2*s*2 2*p*1** | **318.614** |
    | B\_GW\_new | 3 | 2*s*2 2*p*1 | 318.614 |
    | B\_h\_GW | 3 | 2*s*2 2*p*1 | 731.373 |
    | **C\_GW** | **4** | **2*s*2 2*p*2** | **413.992** |
    | C\_GW\_new | 4 | 2*s*2 2*p*2 | 433.983 |
    | C\_h\_GW | 4 | 2*s*2 2*p*2 | 741.689 |
    | C\_s\_GW | 4 | 2*s*2 2*p*2 | 304.843 |
    | **N\_GW** | **5** | **2*s*2 2*p*3** | **420.902** |
    | N\_GW\_new | 5 | 2*s*2 2*p*3 | 452.633 |
    | N\_h\_GW | 5 | 2*s*2 2*p*3 | 755.582 |
    | N\_s\_GW | 5 | 2*s*2 2*p*3 | 312.986 |
    | **O\_GW** | **6** | **2*s*2 2*p*4** | **414.635** |
    | O\_GW\_new | 6 | 2*s*2 2*p*4 | 466.797 |
    | O\_h\_GW | 6 | 2*s*2 2*p*4 | 765.519 |
    | O\_s\_GW | 6 | 2*s*2 2*p*4 | 334.664 |
    | **F\_GW** | **7** | **2*s*2 2*p*5** | **487.698** |
    | F\_GW\_new | 7 | 2*s*2 2*p*5 | 480.281 |
    | F\_h\_GW | 7 | 2*s*2 2*p*5 | 848.626 |
    | **Ne\_GW** | **8** | **2*s*2 2*p*6** | **432.275** |
    | Ne\_s\_GW | 8 | 2*s*2 2*p*6 | 318.26 |
    | **Na\_sv\_GW** | **9** | **2*s*2 2*p*6 3*p*1** | **372.853** |
    | Mg\_GW | 2 | 3*s*2 | 126.143 |
    | Mg\_pv\_GW | 8 | 2*p*6 3*s*2 | 403.929 |
    | **Mg\_sv\_GW** | **10** | **2*s*2 2*p*6 3*d*2** | **429.893** |
    | **Al\_GW** | **3** | **3*s*2 3*p*1** | **240.3** |
    | Al\_sv\_GW | 11 | 2*s*2 2*p*6 3*s*2 3*p*1 | 411.109 |
    | **Si\_GW** | **4** | **3*s*2 3*p*2** | **245.345** |
    | Si\_sv\_GW | 12 | 2*s*2 2*p*6 3*s*2 3*p*2 | 547.578 |
    | **P\_GW** | **5** | **3*s*2 3*p*3** | **255.04** |
    | **S\_GW** | **6** | **3*s*2 3*p*4** | **258.689** |
    | **Cl\_GW** | **7** | **3*s*2 3*p*5** | **262.472** |
    | **Ar\_GW** | **8** | **3*s*2 3*p*6** | **290.599** |
    | **K\_sv\_GW** | **9** | **3*s*2 3*p*6 3*d*1** | **248.998** |
    | **Ca\_sv\_GW** | **10** | **3*s*2 3*p*6 3*d*2** | **281.43** |
    | **Sc\_sv\_GW** | **11** | **3*s*2 3*p*6 3*d*3** | **378.961** |
    | **Ti\_sv\_GW** | **12** | **3*s*2 3*p*6 3*d*4** | **383.774** |
    | **V\_sv\_GW** | **13** | **3*s*2 3*p*6 3*d*5** | **382.321** |
    | **Cr\_sv\_GW** | **14** | **3*s*2 3*p*6 3*d*6** | **384.932** |
    | Mn\_GW | 7 | 3*d*6 4*s*1 | 278.466 |
    | **Mn\_sv\_GW** | **15** | **3*s*2 3*p*6 3*d*7** | **384.627** |
    | Fe\_GW | 8 | 3*d*7 4*s*1 | 321.007 |
    | **Fe\_sv\_GW** | **16** | **3*s*2 3*p*6 3*d*8** | **387.837** |
    | Co\_GW | 9 | 3*d*8 4*s*1 | 323.4 |
    | **Co\_sv\_GW** | **17** | **3*s*2 3*p*6 3*d*9** | **387.491** |
    | Ni\_GW | 10 | 3*d*9 4*s*1 | 357.323 |
    | **Ni\_sv\_GW** | **18** | **3*s*2 3*p*6 3*d*10** | **389.645** |
    | Cu\_GW | 11 | 3*d*10 4*s*1 | 417.039 |
    | **Cu\_sv\_GW** | **19** | **3*s*2 3*p*6 3*d*10 4*s*1** | **467.331** |
    | Zn\_GW | 12 | 3*d*10 4*s*2 | 328.191 |
    | **Zn\_sv\_GW** | **20** | **3*s*2 3*p*6 3*d*10 4*s*2** | **401.665** |
    | Ga\_GW | 3 | 4*s*2 4*p*1 | 134.678 |
    | **Ga\_d\_GW** | **13** | **3*d*10 4*s*2 4*p*1** | **404.602** |
    | Ga\_sv\_GW | 21 | 3*s*2 3*p*6 3*d*10 4*s*2 4*p*1 | 404.602 |
    | Ge\_GW | 4 | 4*s*2 4*p*2 | 173.807 |
    | **Ge\_d\_GW** | **14** | **3*d*10 4*s*2 4*p*2** | **375.434** |
    | Ge\_sv\_GW | 22 | 3*s*2 3*p*6 3*d*10 4*s*2 4*p*2 | 410.425 |
    | **As\_GW** | **5** | **4*s*2 4*p*3** | **208.702** |
    | As\_sv\_GW | 23 | 3*s*2 3*p*6 3*d*10 4*s*2 4*p*3 | 415.313 |
    | **Se\_GW** | **6** | **4*s*2 4*p*4** | **211.555** |
    | Se\_sv\_GW | 24 | 3*s*2 3*p*6 3*d*10 4*s*2 4*p*4 | 469.344 |
    | **Br\_GW** | **7** | **4*s*2 4*p*5** | **216.285** |
    | Br\_sv\_GW | 25 | 3*s*2 3*p*6 3*d*10 4*s*2 4*p*5 | 475.692 |
    | **Kr\_GW** | **8** | **4*s*2 4*p*6** | **252.232** |
    | **Rb\_sv\_GW** | **9** | **4*s*2 4*p*6 4*d*1** | **221.197** |
    | **Sr\_sv\_GW** | **10** | **4*s*2 4*p*6 4*d*2** | **224.817** |
    | **Y\_sv\_GW** | **11** | **4*s*2 4*p*6 4*d*3** | **339.758** |
    | **Zr\_sv\_GW** | **12** | **4*s*2 4*p*6 4*d*4** | **346.364** |
    | **Nb\_sv\_GW** | **13** | **4*s*2 4*p*6 4*d*5** | **353.872** |
    | **Mo\_sv\_GW** | **14** | **4*s*2 4*p*6 4*d*6** | **344.914** |
    | **Tc\_sv\_GW** | **15** | **4*s*2 4*p*6 4*d*7** | **351.044** |
    | **Ru\_sv\_GW** | **16** | **4*s*2 4*p*6 4*d*8** | **348.106** |
    | Rh\_GW | 9 | 4*d*8 5*s*1 | 247.408 |
    | **Rh\_sv\_GW** | **17** | **4*s*2 4*p*6 4*d*9** | **351.206** |
    | Pd\_GW | 10 | 4*d*9 5*s*1 | 250.925 |
    | **Pd\_sv\_GW** | **18** | **4*s*2 4*p*6 4*d*10** | **356.093** |
    | Ag\_GW | 11 | 4*d*10 5*s*1 | 249.844 |
    | **Ag\_sv\_GW** | **19** | **4*s*2 4*p*6 4*d*11** | **354.43** |
    | Cd\_GW | 12 | 4*d*10 5*s*2 | 254.045 |
    | **Cd\_sv\_GW** | **20** | **4*s*2 4*p*6 4*d*10 5*s*2** | **361.806** |
    | **In\_d\_GW** | **13** | **4*d*10 5*s*2 5*p*1** | **278.624** |
    | In\_sv\_GW | 21 | 4*s*2 4*p*6 4*d*10 5*s*2 5*p*1 | 366.771 |
    | **Sn\_d\_GW** | **14** | **4*d*10 5*s*2 5*p*2** | **260.066** |
    | Sn\_sv\_GW | 22 | 4*s*2 4*p*6 4*d*10 5*s*2 5*p*2 | 368.778 |
    | Sb\_GW | 5 | 5*s*2 5*p*3 | 172.069 |
    | **Sb\_d\_GW** | **15** | **4*d*10 5*s*2 5*p*3** | **263.1** |
    | Sb\_sv\_GW | 23 | 4*s*2 4*p*6 4*d*10 5*s*2 5*p*3 | 372.491 |
    | **Te\_GW** | **6** | **5*s*2 5*p*4** | **174.982** |
    | Te\_sv\_GW | 24 | 4*s*2 4*p*6 4*d*10 5*s*2 5*p*4 | 376.618 |
    | **I\_GW** | **7** | **5*s*2 5*p*5** | **175.647** |
    | I\_sv\_GW | 25 | 4*s*2 4*p*6 4*d*10 5*s*2 5*p*5 | 381.674 |
    | **Xe\_GW** | **8** | **5*s*2 5*p*6** | **179.547** |
    | Xe\_sv\_GW | 26 | 4*s*2 4*p*6 4*d*10 5*s*2 5*p*6 | 400.476 |
    | **Cs\_sv\_GW** | **9** | **5*s*2 5*p*6 5*d*1** | **198.101** |
    | **Ba\_sv\_GW** | **10** | **5*s*2 5*p*6 5*d*1 6*s*1** | **267.02** |
    | **La\_GW** | **11** | **4*f*0.2 5*s*2 5*p*6 5*d*0.8 6*s*2** | **313.688** |
    | **Ce\_GW** | **12** | **4*f*1 5*s*2 5*p*6 5*d*1 6*s*2** | **304.625** |
    | **Hf\_sv\_GW** | **12** | **5*s*2 5*p*6 5*d*4** | **309.037** |
    | **Ta\_sv\_GW** | **13** | **5*s*2 5*p*6 5*d*5** | **286.008** |
    | **W\_sv\_GW** | **14** | **5*s*2 5*p*6 5*d*6** | **317.132** |
    | **Re\_sv\_GW** | **15** | **5*s*2 5*p*6 5*d*7** | **317.012** |
    | **Os\_sv\_GW** | **16** | **5*s*2 5*p*6 5*d*8** | **319.773** |
    | **Ir\_sv\_GW** | **17** | **5*s*2 5*p*6 5*d*9** | **319.843** |
    | Pt\_GW | 10 | 5*d*9 6*s*1 | 248.716 |
    | **Pt\_sv\_GW** | **18** | **5*s*2 5*p*6 5*d*10** | **323.669** |
    | Au\_GW | 11 | 5*d*10 6*s*1 | 248.344 |
    | **Au\_sv\_GW** | **19** | **5*s*2 5*p*6 5*d*11** | **306.658** |
    | **Hg\_sv\_GW** | **20** | **5*s*2 5*p*6 5*d*10 6*s*2** | **312.028** |
    | **Tl\_d\_GW** | **15** | **5*s*2 5*d*10 6*s*2 6*p*1** | **237.053** |
    | Tl\_sv\_GW | 21 | 5*s*2 5*p*6 5*d*10 6*s*2 6*p*1 | 316.583 |
    | **Pb\_d\_GW** | **16** | **5*s*2 5*d*10 6*s*2 6*p*2** | **237.809** |
    | Pb\_sv\_GW | 22 | 5*s*2 5*p*6 5*d*10 6*s*2 6*p*2 | 317.193 |
    | Bi\_GW | 5 | 6*s*2 6*p*3 | 146.53 |
    | **Bi\_d\_GW** | **17** | **5*s*2 5*d*10 6*s*2 6*p*3** | **261.876** |
    | Bi\_sv\_GW | 23 | 5*s*2 5*p*6 5*d*10 6*s*2 6*p*3 | 323.513 |
    | **Po\_d\_GW** | **18** | **5*s*2 5*d*10 6*s*2 6*p*4** | **267.847** |
    | Po\_sv\_GW | 24 | 5*s*2 5*p*6 5*d*10 6*s*2 6*p*4 | 326.618 |
    | **At\_d\_GW** | **17** | **5*d*10 6*s*2 6*p*5** | **266.251** |
    | At\_sv\_GW | 25 | 5*s*2 5*p*6 5*d*10 6*s*2 6*p*5 | 328.529 |
    | **Rn\_d\_GW** | **18** | **5*d*10 6*s*2 6*p*6** | **267.347** |
    | Rn\_sv\_GW | 26 | 5*s*2 5*p*6 5*d*10 6*s*2 6*p*6 | 329.758 |

#### Reference calculation; extremely high accuracy

:   For reference calculations, i.e., calculations where the utmost accuracy is needed, and computational effort is of no concern, we recommend the following set of potentials. These are mostly hard pseudopotentials (\_h) of the GW variant, which were used with a 1000 eV plane-wave cutoff in a recent comparison study of DFT codes to reproduce all-electron results as accurately as possible. However, in most cases, the results should be comparable with the standard potentials, while the computational effort will increase significantly.

:   > **Mind:** Unless the utmost accuracy is required, it is usually not worth paying the extra computational cost required for the hard GW potentials recommended in the following list, compared to their standard counterparts at the beginning of this section for DFT calculations.

:   |  |  |  |  |  |
    | --- | --- | --- | --- | --- |
    | Reference potentials (potpaw.64) | | | | |
    | Element | Potential name | Number of valence electrons | Valence electron configuration | ENAMX [eV] |
    | H | H\_GW | 1 | 1*s*1 | 300.0 |
    | He | He\_GW | 2 | 1*s*2 | 405.78 |
    | Li | Li\_sv\_GW | 3 | 1*s*2 2*p*1 | 433.699 |
    | Be | Be\_sv\_GW | 4 | 1*s*2 2*p*2 | 537.454 |
    | B | B\_GW | 3 | 2*s*2 2*p*1 | 318.614 |
    | C | C\_GW | 4 | 2*s*2 2*p*2 | 413.992 |
    | N | N\_GW | 5 | 2*s*2 2*p*3 | 420.902 |
    | O | O\_h\_GW | 6 | 2*s*2 2*p*4 | 765.519 |
    | F | F\_GW | 7 | 2*s*2 2*p*5 | 487.698 |
    | Ne | Ne\_GW | 8 | 2*s*2 2*p*6 | 432.275 |
    | Na | Na\_sv\_GW | 9 | 2*s*2 2*p*6 3*p*1 | 372.853 |
    | Mg | Mg\_sv\_GW | 10 | 2*s*2 2*p*6 3*d*2 | 429.893 |
    | Al | Al\_GW | 3 | 3*s*2 3*p*1 | 240.3 |
    | Si | Si\_GW | 4 | 3*s*2 3*p*2 | 245.345 |
    | P | P\_GW | 5 | 3*s*2 3*p*3 | 255.04 |
    | S | S\_GW | 6 | 3*s*2 3*p*4 | 258.689 |
    | Cl | Cl\_GW | 7 | 3*s*2 3*p*5 | 262.472 |
    | Ar | Ar\_GW | 8 | 3*s*2 3*p*6 | 290.599 |
    | K | K\_sv\_GW | 9 | 3*s*2 3*p*6 3*d*1 | 248.998 |
    | Ca | Ca\_sv\_GW | 10 | 3*s*2 3*p*6 3*d*2 | 281.43 |
    | Sc | Sc\_sv\_GW | 11 | 3*s*2 3*p*6 3*d*3 | 378.961 |
    | Ti | Ti\_sv\_GW | 12 | 3*s*2 3*p*6 3*d*4 | 383.774 |
    | V | V\_sv\_GW | 13 | 3*s*2 3*p*6 3*d*5 | 382.321 |
    | Cr | Cr\_sv\_GW | 14 | 3*s*2 3*p*6 3*d*6 | 384.932 |
    | Mn | Mn\_sv\_GW | 15 | 3*s*2 3*p*6 3*d*7 | 384.627 |
    | Fe | Fe\_sv\_GW | 16 | 3*s*2 3*p*6 3*d*8 | 387.837 |
    | Co | Co\_sv\_GW | 17 | 3*s*2 3*p*6 3*d*9 | 387.491 |
    | Ni | Ni\_sv\_GW | 18 | 3*s*2 3*p*6 3*d*10 | 389.645 |
    | Cu | Cu\_sv\_GW | 19 | 3*s*2 3*p*6 3*d*10 4*s*1 | 467.331 |
    | Zn | Zn\_sv\_GW | 20 | 3*s*2 3*p*6 3*d*10 4*s*2 | 401.665 |
    | Ga | Ga\_d\_GW | 13 | 3*d*10 4*s*2 4*p*1 | 404.602 |
    | Ge | Ge\_d\_GW | 14 | 3*d*10 4*s*2 4*p*2 | 375.434 |
    | As | As\_GW | 5 | 4*s*2 4*p*3 | 208.702 |
    | Se | Se\_GW | 6 | 4*s*2 4*p*4 | 211.555 |
    | Br | Br\_GW | 7 | 4*s*2 4*p*5 | 216.285 |
    | Kr | Kr\_GW | 8 | 4*s*2 4*p*6 | 252.232 |
    | Rb | Rb\_sv\_GW | 9 | 4*s*2 4*p*6 4*d*1 | 221.197 |
    | Sr | Sr\_sv\_GW | 10 | 4*s*2 4*p*6 4*d*2 | 224.817 |
    | Y | Y\_sv\_GW | 11 | 4*s*2 4*p*6 4*d*3 | 339.758 |
    | Zr | Zr\_sv\_GW | 12 | 4*s*2 4*p*6 4*d*4 | 346.364 |
    | Nb | Nb\_sv\_GW | 13 | 4*s*2 4*p*6 4*d*5 | 353.872 |
    | Mo | Mo\_sv\_GW | 14 | 4*s*2 4*p*6 4*d*6 | 344.914 |
    | Tc | Tc\_sv\_GW | 15 | 4*s*2 4*p*6 4*d*7 | 351.044 |
    | Ru | Ru\_sv\_GW | 16 | 4*s*2 4*p*6 4*d*8 | 348.106 |
    | Rh | Rh\_sv\_GW | 17 | 4*s*2 4*p*6 4*d*9 | 351.206 |
    | Pd | Pd\_sv\_GW | 18 | 4*s*2 4*p*6 4*d*10 | 356.093 |
    | Ag | Ag\_sv\_GW | 19 | 4*s*2 4*p*6 4*d*11 | 354.43 |
    | Cd | Cd\_sv\_GW | 20 | 4*s*2 4*p*6 4*d*10 5*s*2 | 361.806 |
    | In | In\_d\_GW | 13 | 4*d*10 5*s*2 5*p*1 | 278.624 |
    | Sn | Sn\_d\_GW | 14 | 4*d*10 5*s*2 5*p*2 | 260.066 |
    | Sb | Sb\_d\_GW | 15 | 4*d*10 5*s*2 5*p*3 | 263.1 |
    | Te | Te\_GW | 6 | 5*s*2 5*p*4 | 174.982 |
    | I | I\_GW | 7 | 5*s*2 5*p*5 | 175.647 |
    | Xe | Xe\_GW | 8 | 5*s*2 5*p*6 | 179.547 |
    | Cs | Cs\_sv\_GW | 9 | 5*s*2 5*p*6 5*d*1 | 198.101 |
    | Ba | Ba\_sv\_GW | 10 | 5*s*2 5*p*6 5*d*1 6*s*1 | 267.02 |
    | La | La\_GW | 11 | 4*f*0.2 5*s*2 5*p*6 5*d*0.8 6*s*2 | 313.688 |
    | Ce | Ce\_GW | 12 | 4*f*1 5*s*2 5*p*6 5*d*1 6*s*2 | 304.625 |
    | Pr | Pr\_h | 13 | 4*f*2.5 5*s*2 5*p*6 5*d*0.5 6*s*2 | 400.742 |
    | Nd | Nd\_h | 14 | 4*f*3.5 5*s*2 5*p*6 5*d*0.5 6*s*2 | 402.016 |
    | Pm | Pm\_h | 15 | 4*f*4.5 5*s*2 5*p*6 5*d*0.5 6*s*2 | 404.406 |
    | Sm | Sm\_h | 16 | 4*f*5.5 5*s*2 5*p*6 5*d*0.5 6*s*2 | 405.382 |
    | Eu | Eu\_h | 17 | 4*f*6.5 5*s*2 5*p*6 5*d*0.5 6*s*2 | 403.212 |
    | Gd | Gd\_h | 18 | 4*f*7.5 5*s*2 5*p*6 5*d*0.5 6*s*2 | 407.403 |
    | Tb | Tb\_h | 19 | 4*f*8.5 5*s*2 5*p*6 5*d*0.5 6*s*2 | 405.043 |
    | Dy | Dy\_h | 20 | 4*f*9.5 5*s*2 5*p*6 5*d*0.5 6*s*2 | 405.886 |
    | Ho | Ho\_h | 21 | 4*f*10.5 5*s*2 5*p*6 5*d*0.5 6*s*2 | 415.91 |
    | Er | Er\_h | 22 | 4*f*11.5 5*s*2 5*p*6 5*d*0.5 6*s*2 | 429.583 |
    | Tm | Tm\_h | 23 | 4*f*12.5 5*s*2 5*p*6 5*d*0.5 6*s*2 | 419.812 |
    | Yb | Yb\_h | 24 | 4*f*13.5 5*s*2 5*p*6 5*d*0.5 6*s*2 | 409.285 |
    | Lu | Lu | 25 | 4*f*14 5*s*2 5*p*6 5*d*1 6*s*2 | 255.695 |
    | Hf | Hf\_sv\_GW | 12 | 5*s*2 5*p*6 5*d*4 | 309.037 |
    | Ta | Ta\_sv\_GW | 13 | 5*s*2 5*p*6 5*d*5 | 286.008 |
    | W | W\_sv\_GW | 14 | 5*s*2 5*p*6 5*d*6 | 317.132 |
    | Re | Re\_sv\_GW | 15 | 5*s*2 5*p*6 5*d*7 | 317.012 |
    | Os | Os\_sv\_GW | 16 | 5*s*2 5*p*6 5*d*8 | 319.773 |
    | Ir | Ir\_sv\_GW | 17 | 5*s*2 5*p*6 5*d*9 | 319.843 |
    | Pt | Pt\_sv\_GW | 18 | 5*s*2 5*p*6 5*d*10 | 323.669 |
    | Au | Au\_sv\_GW | 19 | 5*s*2 5*p*6 5*d*11 | 306.658 |
    | Hg | Hg\_sv\_GW | 20 | 5*s*2 5*p*6 5*d*10 6*s*2 | 312.028 |
    | Tl | Tl\_d\_GW | 15 | 5*s*2 5*d*10 6*s*2 6*p*1 | 237.053 |
    | Pb | Pb\_d\_GW | 16 | 5*s*2 5*d*10 6*s*2 6*p*2 | 237.809 |
    | Bi | Bi\_d\_GW | 17 | 5*s*2 5*d*10 6*s*2 6*p*3 | 261.876 |
    | Po | Po\_d\_GW | 18 | 5*s*2 5*d*10 6*s*2 6*p*4 | 267.847 |
    | At | At\_d\_GW | 17 | 5*d*10 6*s*2 6*p*5 | 266.251 |
    | Rn | Rn\_d\_GW | 18 | 5*d*10 6*s*2 6*p*6 | 267.347 |
    | Fr | Fr\_sv | 9 | 6*s*2 6*p*6 7*s*1 | 214.54 |
    | Ra | Ra\_sv | 10 | 6*s*2 6*p*6 7*s*2 | 237.367 |
    | Ac | Ac | 11 | 6*s*2 6*p*6 6*d*1 7*s*2 | 172.351 |
    | Th | Th | 12 | 5*f*1 6*s*2 6*p*6 6*d*1 7*s*2 | 247.306 |
    | Pa | Pa | 13 | 5*f*1 6*s*2 6*p*6 6*d*2 7*s*2 | 252.193 |
    | U | U | 14 | 5*f*2 6*s*2 6*p*6 6*d*2 7*s*2 | 252.502 |
    | Np | Np | 15 | 5*f*3 6*s*2 6*p*6 6*d*2 7*s*2 | 254.26 |
    | Pu | Pu | 16 | 5*f*4 6*s*2 6*p*6 6*d*2 7*s*2 | 254.353 |
    | Am | Am | 17 | 5*f*5 6*s*2 6*p*6 6*d*2 7*s*2 | 255.875 |
    | Cm | Cm | 18 | 5*f*6 6*s*2 6*p*6 6*d*2 7*s*2 | 257.953 |

### Selecting a pseudopotential set

:   Generally, we recommend using the latest release of pseudopotentials.

:   > **Tip:** For compatibility reasons or to accurately reproduce another calculation, you might need to use another (older) pseudopotential release. Consult the list of available pseudopotentials.

### Hydrogen-like atoms with fractional valence

:   Twelve hydrogen-like potentials are supplied for a valency between 0.25 and 1.75. Further potentials might become available, c.f. available pseudopotentials. These are useful, e.g., to passivate dangling surface bonds.

:   > **Mind:** The POTCAR files restrict the number of digits for the valency (typically 2, at most 3 digits). Therefor, using three H.33 potentials does yield 0.99 electrons and not 1.00 electron. This can cause undesirable hole- or electron-like states. Set the NELECT tag in the INCAR file to correct the total number of electrons.

### First-row elements

:   For the 1st row elements B, C, N, O, and F, three potential versions exist, the plain one, a hard version, and a soft version. For most purposes, the standard version of PAW potentials is most appropriate. They yield reliable results for energy cutoffs between 325 and 400 eV, where 370-400 eV are required to predict vibrational properties accurately. Binding geometries and energy differences are already well reproduced at 325 eV. The typical bond-length errors for first row dimers (N2, CO, O2) are about 1% compared to more accurate DFT calculations. The hard pseudopotentials (\_h) give results that are essentially identical to the best DFT calculations presently available (FLAPW, or Gaussian with very large basis sets). The soft potentials (\_s) are optimized to work around 250-280 eV. They yield reliable description for most oxides, such as VxOy, TiO2, CeO2, but fail to describe some structural details in zeolites, i.e., cell parameters, and volume.

:   For Hartree-Fock (HF) and hybrid-functional calculations, we strictly recommend using the standard, standard GW, or hard potentials. For instance, the O\_s potential can cause unacceptably large errors even in transition metal oxides. Generally, the soft potentials are less transferable from one exchange-correlation functional to another and often fail when the exact exchange needs to be calculated.

:   > **Tip:** If dimers with short bonds are present in the system (H2O, O2, CO, N2, F2, P2, S2, Cl2), we recommend using the \_h potentials. Specifically, C\_h, O\_h, N\_h, F\_h, P\_h, S\_h, Cl\_h, or their \_GW counterparts. Otherwise, the standard version is often the best choice for first-row elements.

### Alkali and alkali-earth elements (simple metals)

:   For Li (and Be), a standard potential and a potential that treats the 1*s* shell as valence states are available (Li\_sv, Be\_sv). One should use the \_sv potentials for many applications since their transferability is much higher than the standard potentials.

:   For the other alkali and alkali-earth elements, the semi-core *s* and *p* states should be treated as valence states as well. For lighter elements (Na-Ca), it is usually sufficient to treat the 2*p* and 3*p* states as valence states (\_pv), respectively. For Rb-Sr, the 4*s*, 4*p*, and 5*s*, 5*p* states, must be treated as valence states (\_sv).

:   > **Tip:** For alkali and alkali-earth metals, the \_sv variants should be chosen, other than for very light elements Na, Mg, K, and Ca, where \_pv is usually sufficient.

### p-elements

:   For Ga, Ge, In, Sn, Tl-At, the lower-lying *d* states should be treated as valence states (\_d potential). For these elements, alternative potentials that treat the *d* states as core states are also available but should be used with great care.

### d-elements

:   For the *d* elements, applies the same as for the alkali and earth-alkali metals: the semi-core *p* states and possibly the semi-core *s* states should be treated as valence states. In most cases, however, reliable results can be obtained even if the semi-core states are kept frozen.

:   When to switch from X\_pv potentials to the X potentials depends on the required accuracy and the row for the 3*d* elements, even the Ti, V, and Cr potentials give reasonable results but should be used with uttermost care. 4*d* elements are the most problematic, and we advise using the X\_pv potentials up to Tc\_pv. For 5*d* elements the 5*p* states are rather strongly localized (below 3 Ry), since the 4*f* shell becomes filled. One can use the standard potentials starting from Hf, but we recommend performing test calculations. For some elements, X\_sv potentials are available (,e.g., Nb\_sv, Mo\_sv, Hf\_sv). These potentials usually have very similar energy cutoffs as the \_pv potentials and can also be used. For HF-type and hybrid-functional calculations, we strongly recommend using the \_sv and \_pv potentials whenever possible.

:   > **Tip:** As a rule of thumb the *p* states should be treated as valence states for d-elements, if their eigenenergy $\epsilon$ lies above 3 Ry.

### f-elements

:   Due to self-interaction errors, *f* electrons are not handled well by the presently available density functionals. In particular, partially filled *f* states are often incorrectly described. For instance, all *f* states are pinned at the Fermi-level, leading to large overbinding for Pr-Eu and Tb-Yb. The errors are largest at quarter and three-quarter filling, e.g., Gd is handled reasonably well since 7 electrons occupy the majority *f* shell. These errors are DFT and not VASP related.
:   Particularly problematic is the description of the transition from an itinerant (band-like) behavior observed at the beginning of each period to localized states towards the end of the period. For the 4*f* elements, this transition occurs already in La and Ce, whereas the transition sets in for Pu and Am for the 5*f* elements. A routine way to cope with the inabilities of present DFT functionals to describe the localized 4*f* electrons is to place the 4*f* electrons in the core. Such potentials are available and described below; however, they are expected to fail to describe magnetic properties arising *f* orbitals. Furthermore, PAW potentials in which the *f* states are treated as valence states are available, but these potentials are expected to fail to describe electronic properties when *f* electrons are localized. In this case, one might treat electronic correlation effects more carefully, e.g., by employing hybrid functionals or introducing on-site Coulomb interaction.

:   For some elements, soft versions (\_s) are available as well. The semi-core *p* states are always treated as valence states, whereas the semi-core *s* states are treated as valence states only in the standard potentials. For most applications (oxides, sulfides), the standard version should be used since the soft versions might result in *s* ghost-states close to the Fermi-level (,e.g., Ce\_s in ceria). The soft versions are, however, expected to be sufficiently accurate for calculations on intermetallic compounds.

#### Lanthanides with fixed valence

:   In addition, special GGA potentials are supplied for Ce-Lu, in which *f* electrons are kept frozen in the core, which is an attempt to treat the localized nature of *f* electrons. The number of f electrons in the core equals the total number of valence electrons minus the formal valency. For instance, according to the periodic table, Sm has a total of 8 valence electrons, i.e., 6 *f* electrons and 2 *s* electrons. In most compounds, Sm adopts a valency of 3; hence 5 *f* electrons are placed in the core when the pseudopotential is generated. The corresponding potential can be found in the directory Sm\_3. The formal valency n is indicted by \_n, where n is either 3 or 2. Ce\_3 is, for instance, a Ce potential for trivalent Ce (for tetravalent Ce, the standard potential should be used).

:   > **Warning:** *f*-elements are notoriously hard to describe with DFT due to self-interaction errors in the strongly localized orbitals. Placing some, or all, 4*f* electrons in the core can rectify this issue, but then the description of magnetism will fail and transferability will suffer.

:   > **Tip:** If you are not interested in 4*f*-magnetism, and know the valency of your lanthanide, use the \_2 or \_3 potentials.

### Test your setup

:   Even if you have taken a lot of care to optimize your pseudopotential choice, it is always good to perform some test calculations with other potentials, if necessary on a small prototype system. You might realize that you need extra accuracy, or that you are leaving performance on the table by using unnecessarily hard POTCARs for your problem.

### Example: NiO equilibrium volume

Antiferromagnetic NiO in the rocksalt structure is a prototype system for a correlated material. It is a Mott insulator and not well described with standard DFT. To get correct material properties, methods beyond DFT are required. DFT+DMFT calculations are an option, but the much cheaper DFT+U approach is often used with satisfactory results.

Fig 1. LSDA+U Energy vs. volume plot for AFM NiO. Different Ni potentials were used to create the data. All other inputs are equivalent. The all-electron (AE) reference was calculated with Wien2K.

The computational setup and how to interpret the results of a DFT+U calculation for NiO are given in the section on NiO LSDA+U. Here, we will focus on the effect of the choice of the Ni pseudopotential on the equation of state (EOS). We compare the results to reference Wien2K calculations, which do not use pseudopotentials, as Wien2K is an all-electron (AE) code.

The Ni, Ni\_pv, and Ni\_sv\_GW pseudopotentials of the potpaw\_PBE.64 set were combined with the O pseudopotential for all calculations. The plane-wave cutoff energy ENCUT was set to 1000 eV to avoid any influence of basis set convergence.

Fig. 1 shows the data for all three Ni POTCAR options and the AE reference as a black line. The standard Ni potential, which is the one usually recommended for calculations that do not need a high number of unoccupied bands, is underestimating the equilibrium volume by 6%, which translates to a lattice parameter of 4.04 Å. Taking the semi-core 3*p*-states into account with the Ni\_pv potential improves the results significantly, with the volume underestimation reduced to 1.7% and increasing the lattice parameter to 4.10 Å. If we want to also take the semicore 3*s*-states into account, we need to choose a \_GW potential, Ni\_sv\_GW. The inclusion of the *s*-states improves the EOS further, with the underestimation of the volume now being only 0.2% and the lattice parameter matching the AE reference to two significant digits at 4.12 Å.

It is worth noting that the semicore 3*p*-, and the 3*s*-states, are only important for the equilibrium volume if the L(S)DA+U method is used. If no Hubbard corrections are used, all three tested Ni pseudopotentials give a lattice parameter of 4.06 Å, which is very close to the 4.07 Å of the AE reference.

However, the large value of U=8 eV applied to the Ni 4*d*-states in our calculations pushes the *d*-states away from the Fermi level and compresses them. If the *p* (or, better, the *sp*) orbitals are in the valence, they can hybridize with the *d*-states and expand, increasing the lattice parameter. (This process happens equivalently in a DFT+DMFT calculation of NiO.) In fact, the expected linear increase of the lattice parameter with increasing U value is only observed correctly if the Ni\_sv\_GW potential is used. Note that the lattice parameter predicted by the Ni PAW potential for U=8 eV, at 4.04 Å, is actually lower than the 4.06 Å predicted without the U, because the *d*-states are still compressed, but the frozen *s*- and *p*-states cannot expand accordingly.

## Related tags and sections

POTCAR, Prepare a POTCAR, Available pseudopotentials

Theoretical background: Pseudopotentials, Projector-augmented-wave formalism

## References
