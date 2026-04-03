# Self-Consistent Potential Correction

Categories: Electrostatics

SCPC (self-consistent potential correction) is an external package (developed in the Bremen Center for Computational Materials Science and in the MPI-Hamburg) that can be linked to VASP.
For more information about this package see https://github.com/aradi/SCPC-Method.
In supercell calculations for a charged system, a jellium counter charge is applied to maintain overall neutrality,
but the interaction of the artificially repeated charges has to be corrected for, both in the total energy and in the one-electron eigenvalues and eigenstates.
This becomes paramount in slab calculations, where the jellium counter charge may induce spurious states in the vacuum.
SCPC corrects for the spurious effects of the repeated charges automatically, without any post-processing.

SCPC considers the deviation (Δρ) in the electron distribution between the charged and a reference neutral system (provided by VASP in the corresponding CHGCAR files),
and calculates the corresponding periodic electrostatic potential, Vper, aligned to the potential of the reference system (provided in LOCPOT).
Also the potential, Viso, for the same but isolated charge distribution, Δρ, is determined by using open (Dirichlet) boundary conditions. The difference Vcor = Viso - Vper is added to the total electronic potential in each step of the iterative solution of the Kohn-Sham equation. For more information regarding the method, please refer to the SCPC paper.

## Usage

SCPC needs the following keywords in the INCAR file:

```
SCPC { 
    USE   = T    ; turns on the SCPC procedure 
    IN    = 1    ; first SCF cycle when SCPC is switched on. 
    QTOT  = 1.00 ; formal defect charge  
    ZLOW  = 0.22 ; for slabs only: lower interface in fractional coordinate 
    ZHIG  = 0.53 ; for slabs only: upper interface in fractional coordinate 
    DIEL  = 2.46 ; macroscopic dielectric constant,e 
    BROAD = 0.40 ; broadening parameter for e at the interface 
    PRTX(Y,Z)  = T   ; printing the averages in the X(Y,Z) direction  
    RX(Y,Z)CUT = 0.1 ; damping region at the boundary in the X(Y,Z) direction 
}
```

The CHGCAR and LOCPOT files of the reference system have to be provided under the names REFCHG and REFPOT, respectively.

At present, only orthorhombic cells can be corrected.
In case of slabs, the slab normal must be the z direction and the center of the charge should be close to the lateral center.

The reference system is ideally the neutral defect, at the equilibrium geometry of the charged defect,
but using the pristine system as reference instead causes usually only a small error.
The correction is not yet implemented into the calculation of the forces.
For more information see https://github.com/aradi/SCPC-Method .

## References
