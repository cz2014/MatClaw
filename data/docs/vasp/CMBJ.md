# CMBJ

Categories: INCAR tag, Exchange-correlation functionals

CMBJ = [real (array)]  
 Default: **CMBJ** = calculated self-consistently

Description: defines the $c$ parameter in the MBJ potential.

---

The CMBJ tag can be set in the following ways:

* Specify a constant that is used at every point of space $\mathbf{r}$

  ```
  CMBJ = c
  ```

* Specify one entry per atomic type

  ```
  CMBJ = c_1 c_2 .. c_n
  ```

  where the order and number $n$ is in accordance with atomic types in your POSCAR file. The MBJ exchange potential at a point $\mathbf{r}$ will then be calculated using the parameter $c\_{i}$ belonging to the atomic species of the atomic site nearest to $\mathbf{r}$.

If CMBJ is not set, $c$ is calculated at each electronic step as the average of $\left\vert\nabla n\right\vert/n$ in the unit cell, as explained in the description of the METAGGA tag.

## Related tags and articles

METAGGA,
CMBJA,
CMBJB,
CMBJE,
SMBJ,
RSMBJ,
LASPH,
LMAXTAU,
LMIXTAU

Examples that use this tag

## References

---
