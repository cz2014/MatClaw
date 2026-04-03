# Hellmann-Feynman forces

Categories: Ionic minimization, Forces, Theory

Within the finite temperature, LDA forces are defined as the derivative
of the generalized *free energy*.
This quantity can be evaluated easily. The functional $F$ depends on the
wavefunctions $\phi$, the partial occupancies $f$, and the positions of the
ions $R$. In this section, we will shortly discuss the variational
properties of the free energy and we will explain why we calculate the
forces as a derivative of the free energy. The formulas given are
very symbolic and we do not take into account any constraints on the
occupation numbers or the wavefunctions. We denote the whole set
of wavefunctions as $\phi$ and the set of partial occupancies as $f$.

The electronic groundstate is determined by the variational property of the
free energy i.e.

$0 = \delta F(\phi,f,R)$

for arbitrary variations of $\phi$ and $f$. We can rewrite the right hand side of
this equation as

$\frac{\partial F}{\partial \phi} \delta \phi +
\frac{\partial F}{\partial f} \delta f.$

For arbitrary variations this quantity is zero only if $\frac{\partial F}{\partial \phi}=0$
and $\frac{\partial F}{\partial f}=0$, leading to a system of
equations which determines $\phi$ and $f$ at the electronic groundstate.
We define the forces as derivatives of the free energy
with respect to the ionic positions i.e.

$\mbox{force} = \frac{d F(\phi,f,R)} {d R} =
\frac{\partial F}{\partial \phi} \frac{\partial \phi}{\partial R} +
\frac{\partial F}{\partial f} \frac{\partial f}{\partial R} +
\frac{\partial F}{\partial R} .$

At the groundstate the first two terms are zero and we can write

$\mbox{force}= \frac{d F(\phi,f,R)} {d R} = \frac{\partial F}{\partial R}$

i.e. we can keep $\phi$ and $f$ fixed at their respective groundstate
values and we have to calculate the partial derivative of the free
energy with respect to the ionic positions only. This is relatively
easy task.

Previously we have mentioned that the only physical quantity
is the energy for $\sigma \to 0$. It is in principle possible to evaluate
the derivatives of $E(\sigma \to 0)$ with respect to the ionic
coordinates but this is not easy and requires additional computer time.

---
