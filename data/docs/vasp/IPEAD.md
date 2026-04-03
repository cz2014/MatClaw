# IPEAD

Categories: INCAR tag, Linear response, Dielectric properties, Berry phases

IPEAD = 1 | 2 | 3 | 4  
 Default: **IPEAD** = 4

Description: IPEAD specifies the order of the finite difference stencil used to compute the derivative of the cell-periodic part of the orbitals w.r.t. **k**, |∇**k**un**k**⟩ (LPEAD=.TRUE.), and the derivative of the polarization w.r.t. the orbitals, δ**P**/δ⟨ψn**k**| for (LCALCEPS=.TRUE., or EFIELD\_PEAD≠**0**).

---

A central finite differences formula or order IPEAD is used to compute the first-order derivative of the cell-periodic part of the orbitals w.r.t. **k**.
The coefficients for the different orders can be found here.

## Related tags and articles

LPEAD,
LCALCEPS,
EFIELD\_PEAD,
Berry phases and finite electric fields

Examples that use this tag

---
