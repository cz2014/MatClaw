# SAXIS

Categories: INCAR tag, Magnetism, Noncollinear magnetism

SAXIS = [real array]  
 Default: **SAXIS** = (0, 0, 1)

Description: Set the global spin-quantization axis w.r.t. Cartesian coordinates.

---

SAXIS specifies the relative orientation of spinor space spanned by the Pauli matrices $\{\sigma\_1$, $\sigma\_2$, $\mathbf{\sigma}\_3\}$ with respect to Cartesian coordinates $\{\hat x, \hat y, \hat z\}$. The default is $\sigma\_1=\hat x$, $\sigma\_2 =\hat y$, $\sigma\_3 = \hat z$.
The direction of the spin-quantization axis $\sigma\_3$ with respect to Cartesian coordinates is set

```
 SAXIS =   sx sy sz    ! global spin-quantization axis
```

such that $\sigma\_3=\mathbf{s}/|\mathbf{s}|$, i.e., $\sigma\_3$ points along $\mathbf{s}=(s\_x,s\_y,s\_z)^T$. The directions of $\sigma\_1$ and $\sigma\_2$ are a consequence of rotating $\sigma\_3$ to point along $\mathbf{s}$ as described below.

The relative orientation of spinor space with respect to real space becomes important in case spin-orbit coupling is included (LSORBIT=True). All magnetic moments and spinor-like quantities written or read by VASP are given in the basis of the spinor space $\{\sigma\_1$, $\sigma\_2$, $\mathbf{\sigma}\_3\}$. This includes the MAGMOM tag in the INCAR file, the total and local magnetizations in the OUTCAR and PROCAR file, the spinor-like orbitals in the WAVECAR file, and the magnetization density in the CHGCAR file.

## Coordinate system

Fig 1. Euler angles $\alpha$ and $\beta$ defined by $\mathbf{s}=(s\_x,s\_y,s\_z)^T$.

The default orientation is $\sigma\_1=\hat x$, $\sigma\_2 =\hat y$, $\sigma\_3 = \hat z$.
To set $\hat{\sigma}\_3=s/|s|$, VASP applies two rotations with Euler angles

:   $$\begin{align}
    \alpha&=\arctan2\left(\frac{s\_y}{s\_x}\right) \in [-\pi,\pi]\\
    \beta&=\arctan2\left(\frac{\sqrt{s\_x^2+s\_y^2}}{s\_z}\right) \in [0,\pi].
    \end{align}$$

Here, $\alpha$ is the angle between the projection of SAXIS onto the *xy* plane (sx,sy,0) and the Cartesian vector $\hat x$, and $\beta$ is the angle between the vector SAXIS and the Cartesian vector $\hat z$, see Fig. 1. Search for `Euler angles` in the OUTCAR file to see what VASP uses. For the default $\mathbf{s}=(0,0,1)$, $\alpha=0$ and $\beta=0$.

The transformation of a vector $\mathbf{m}=(m\_1,m\_2,m\_3)^T$ given in the basis $\{\sigma\_1$, $\sigma\_2$, $\mathbf{\sigma}\_3\}$ into $\mathbf{m}'=(m\_x,m\_y,m\_z)^T$ in Cartesian coordinates and its inverse transformation read

:   $$\begin{align}
    \mathbf{m}&= m\_1 \sigma\_1 + m\_2 \sigma\_2 + m\_3 \sigma\_3 \\
    \mathbf{m}'&= m\_x \hat x + m\_y \hat y + m\_z \hat z \\
    \mathbf{m}'&= R\_z^\alpha R\_y^\beta \mathbf{m} \\
    \mathbf{m} &= R\_y^{-\beta} R\_z^{-\alpha} \mathbf{m}' \\
    \end{align}$$

where the rotation matrices are

:   $$R\_z^\alpha = \left(\begin{matrix}
    \cos(\alpha) & -\sin(\alpha) & 0 \\
    \sin(\alpha) & \cos(\alpha) & 0 \\
    0 & 0 & 1 \\
    \end{matrix}\right), \quad
    R\_y^\beta = \left(\begin{matrix}
    \cos(\beta) & 0 & \sin(\beta) \\
    0 & 1 & 0 \\
    -\sin(\beta) & 0 & \cos(\beta) \\
    \end{matrix}\right).$$

> **Mind:** Apply the proper basis transformation when comparing vector-like quantities and spinor-like quantities.

For instance, when LORBMOM=True the orbital angular momentum is written to the OUTCAR file in Cartesian coordinates. Thus, when comparing the orbital angular momentum (vector-like quantity) and the magnetization (spinor-like quantity), one has to perform a basis transformation on one of the quantities unless the bases agree (default).

## Example

* In case the bases have the same orientation, i.e., $\sigma\_1=\hat x$, $\sigma\_2 =\hat y$, $\sigma\_3 = \hat z$ (default)

:   $$\begin{align}
    m\_x & = & m\_1, \\
    m\_y & = & m\_2, \\
    m\_z & = & m\_3.
    \end{align}$$
:   For a single site this implies setting

```
MAGMOM = mx my mz ! magnetic moment in Cartesian coordinates
SAXIS =  0 0 1   ! default
```

Fig 2. Example with $\mathbf{s}=(1,1,0)^T$ and Euler angles $\alpha=\pi/4$ and $\beta=\pi/2$.

* Another good choice is setting $\mathbf{s}$ to point along the direction of the on-site magnetic moment such that

:   $$\begin{align}
    m\_x & = & \sin(\beta)\cos(\alpha) m &= m\, s\_x / \sqrt{s\_x^2+s\_y^2+s\_z^2} \\
    m\_y & = & \sin(\beta)\sin(\alpha) m &= m\, s\_y / \sqrt{s\_x^2+s\_y^2+s\_z^2} \\
    m\_z & = & \cos(\beta) m &= m\, s\_z / \sqrt{s\_x^2+s\_y^2+s\_z^2},
    \end{align}$$
:   where $m$ is the total on-site magnetic moment.
:   For a single site, this case implies setting

```
MAGMOM = 0 0 m   ! magnetic moment along sigma3
SAXIS =  sx sy sz ! direction of sigma3
```

:   Thus, there are two methods to rotate the initial magnetization in an arbitrary direction: either by changing the initial magnetic moments MAGMOM or by changing SAXIS. Both methods should, in principle, yield exactly the same energy, but for implementation reasons, the second method might be more precise.

* In case

```
SAXIS =  1 1 0   ! alpha=pi/4, beta=pi/2
```

:   the spinor space $\{\sigma\_1$, $\sigma\_2$, $\mathbf{\sigma}\_3\}$ will be rotated with respect to real space $\{\hat x, \hat y, \hat z\}$ as shown in Fig. 2.

## Related tags and articles

LNONCOLLINEAR,
MAGMOM,
LSORBIT

Examples that use this tag

---
