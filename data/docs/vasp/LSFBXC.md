# LSFBXC

Categories: INCAR tag, Exchange-correlation functionals, Magnetism

LSFBXC  = .TRUE. | .FALSE.  
 Default:  **LSFBXC**  = .FALSE.

Description: Removes sources and drains from the exchange-correlation B field.

---

With LSFBXC=T, the sources and drains are removed from the exchange-correlation (XC) B field at each step of the electronic minimization. Thus, any XC potential can be constrained to correspond to a Maxwellian magnetic field at the cost of becoming a potential-only XC functional, since there is no correction applied to the XC energy. In other words, it is strictly necessary to optimize the Kohn-Sham orbitals using iterative methods, e.g. ALGO = Normal , and it is *not* possible to use direct optimizers, e.g. ALGO = Conjugate , etc., as they require consistency between XC energy and XC potential.

Moore et al. implemented the same feature in a parallel work and performed more extensive applications. Whether the two implementations are identical has not been tested, and no publication is associated with the present implementation (by Marie-Therese Huebsch) using LSFBXC.

## Related tags and articles

XC, GGA

## References
