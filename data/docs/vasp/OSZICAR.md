# OSZICAR

Categories: Files, Output files

Information about convergence speed and about the current step is written to stdout and to the OSZICAR file. Always keep a copy of the OSZICAR file, it might give important information.

Typically you will get something similar to the following lines:

```
      N     E                dE          d eps    ncg  rms     rms(c)
CG :  1   -.13238703E+04   -.132E+04   -.934E+02  56  .28E+02
CG :  2   -.13391360E+04   -.152E+02   -.982E+01  82  .54E+01
CG :  3   -.13397892E+04   -.653E+00   -.553E+00  72  .13E+01  .14E+00
CG :  4   -.13400939E+04   -.304E+00   -.287E+00  84  .48E+00  .39E-01
CG :  5   -.13401306E+04   -.366E-01   -.322E-01  69  .35E+00  .17E-01
CG :  6   -.13401489E+04   -.183E-01   -.169E-01  75  .74E-01  .66E-02
CG :  7   -.13401516E+04   -.267E-02   -.250E-02  68  .47E-01  .37E-02
CG :  8   -.13401522E+04   -.567E-03   -.489E-03  53  .15E-01  .90E-03
   1 F= -.13401522E+04 E0= -.13397340E+04  d E = -.13402E+04
 trial: gam=  .00000 g(F)=   .153E+01 g(S)=   .000E+00 ort =  .000E+00
 charge predicted from atoms
 charge from overlapping atoms
      N     E                dE          d eps    ncg   rms    rms(c)
CG :  1   -.13400357E+04   -.134E+04   -.926E+01   56   .97E+01
```

*N* is the number of electronic steps, *E* the current free energy, *dE* the change in the free energy from the last to the current step and *d eps* the change in the bandstructure energy. Furthermore *ncg* is the number of evaluations of the Hamiltonian acting on a wavefunction, *rms* is the norm of the residuum ($R=H - \epsilon S | \phi\rangle$) of the trial wave functions (i.e. their approximate error) and *rms(c)* is the difference between input and output charge density.

The next line (after the *N*+1 lines) gives information about the total energy after obtaining convergence. The first values is the total free energy *F* (at this point the energy of the reference atom has been subtracted), *E0* is the energy for $\sigma \to 0$ (see also Partial occupancies) and *dE* is the change in the total energy between the current and the last step; for a static run *dE* is the entropy multiplied by $sigma$. For a molecular dynamics calculation (IBRION=0) this line looks a little bit different:

```
   1 T= 1873.0 E= -.13382154E+04 F= -.13401522E+04 E0= -.13397340E+04 
    EK=   .19368E+01 SP=  .00E+00 SK=  .00E+00
```

*T* corresponds to the current temperature and *E* to the total free energy (including the kinetic energy of the ions and the energy of the Nosé thermostat). *F* and *E0* are the same as above. *EK* is the kinetic energy, *SP* is the potential energy of the Nosé thermostat and *SK* the corresponding kinetic energy.

Additional technical parameters and some status reports are written to stdout.

The ouput to the OSZICAR file is also written for force-field only steps when machine learning force fields are used. In that case the *E0* entry contains the same as the *F* entry since the entropy cannot be calculated in this method. The rest is analogous to the ab initio output.

---
