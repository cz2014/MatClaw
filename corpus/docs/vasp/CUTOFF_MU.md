# CUTOFF_MU

Categories: INCAR tag, Wannier functions

CUTOFF\_MU = [real] ( [real] )

|  |  |  |
| --- | --- | --- |
| Default: **CUTOFF\_MU** | = 0.8 \* Fermi level of a system with NUM\_WANN orbitals occupied |  |

Description: CUTOFF\_MU specifies the energy cutoff $\mu$ in eV for the function specified by CUTOFF\_MU.

---

The value $\mu$ of CUTOFF\_MU corresponds to the energy cutoff of the cutoff function used to obtain Wannier functions with the
 one-shot method.
The meaning of $\mu$ depends on the CUTOFF\_TYPE tag.

For spin-polarized calculations (`ISPIN = 2`), two values can be specified for CUTOFF\_MU, one for each spin channel.
If only a single value is specified, it will be used for both spin channels.

The default value is computed by first determining the Fermi level
of the system if it had NUM\_WANN orbitals occupied and multiplying by 0.8. This gives reasonable freedom to determine the unitary transformation $U\_{mn\mathbf{k}}$ from Bloch states to Wannier functions.

> **Tip:** Careful tuning of this parameter is required to obtain a good Wannierization.

## Related tags and articles

CUTOFF\_TYPE,
CUTOFF\_SIGMA,
LSCDM,
LOCPROJ

Examples that use this tag
