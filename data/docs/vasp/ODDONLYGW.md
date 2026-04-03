# ODDONLYGW

Categories: INCAR tag, Many-body perturbation theory, GW

ODDONLYGW = [logical]  
 Default: **ODDONLYGW** = .FALSE.

Description: ODDONLYGW allows to avoid the inclusion of the $\Gamma$ point in the evaluation of response functions (in GW calculations).

---

The independent particle polarizability $\chi\_{{\mathbf{q}}}^0 ({\mathbf{G}}, {\mathbf{G}}', \omega)$ is given by:

$\chi\_{{\mathbf{q}}}^0 ({\mathbf{G}}, {\mathbf{G}}', \omega) =
\frac{1}{\Omega} \sum\_{n,n',{\mathbf{k}}}2 w\_{{\mathbf{k}}} (f\_{n'{\mathbf{k}}+{\mathbf{q}}} - f\_{n{\mathbf{k}}})
\times \frac{\langle \psi\_{n{\mathbf{k}}}| e^{-i ({\mathbf{q}}+{\mathbf{G}}){\mathbf{r}}} | \psi\_{n'{\mathbf{k}}+{\mathbf{q}}}\rangle
\langle \psi\_{n'{\mathbf{k}}+{\mathbf{q}}}| e^{i ({\mathbf{q}}+{\mathbf{G}}'){\mathbf{r'}}} | \psi\_{n{\mathbf{k}}}\rangle}
{ \epsilon\_{n'{\mathbf{k}}+{\mathbf{q}}}-\epsilon\_{n{\mathbf{k}}} - \omega - i \eta }$

If the $\Gamma$ point is included in the summation over $\mathbf{k}$, convergence is very slow for some materials (e.g. GaAs).

To deal with this problem the flag ODDONLYGW has been included.
In the automatic mode, the $\mathbf{k}$-grid is given by (see Sec. \ref{sec:autok}):

```
[math]\displaystyle{  \vec{k} = \vec{b}_{1} \frac{n_{1}}{N_{1}} + \vec{b}_{2} \frac{n_{2}}{N_{2}}  + \vec{b}_{3} \frac{n_{3}}{N_{3}} ,\qquad  n_1=0...,N_1-1 \quad  n_2=0...,N_2-1 \quad  n_3=0...,N_3-1.  }[/math]
```

## Related tags and articles

EVENONLYGW,
GW calculations

Examples that use this tag

---
