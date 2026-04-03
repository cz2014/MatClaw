# Time-propagation algorithms in molecular dynamics

Categories: Theory, Molecular dynamics, Thermostats

In molecular dynamics simulations, the ionic positions $\mathbf{r}\_{i}(t)$ and velocities $\mathbf{v}\_{i}(t)$ are monitored as functions of time $t$. This time dependence is obtained by integrating Newton's equations of motion. When integrating the equations of motions it is important to use symplectic algorithms which conserve the phase-space volume. To solve the equations of motion under symplectic conditions, various integration algorithms have been developed. The time dependence of a particle can be expressed in a Taylor expansion

:   :   $$\mathbf{r}\_{i}(t+\Delta t) = \mathbf{r}\_{i}(t) + \mathbf{v}\_{i}(t)\Delta t + \frac{\mathbf{F}\_{i}}{2m}(t)\Delta t^{2} + \frac{\partial^{3} \mathbf{r}\_{i}(t)}{\partial t^{3}}\Delta t^{3} + \mathcal{O}(\Delta t^{4})$$

A backward propagation in time by a time step $\Delta t$ can be obtained in a similar way

:   :   $$\mathbf{r}\_{i}(t-\Delta t) = \mathbf{r}\_{i}(t) - \mathbf{v}\_{i}(t)\Delta t + \frac{\mathbf{F}\_{i}}{2m}(t)\Delta t^{2} - \frac{\partial^{3} \mathbf{r}\_{i}(t)}{\partial t^{3}}\Delta t^{3} + \mathcal{O}(\Delta t^{4})$$

Adding these two equation gives and rearrangement gives the Verlet algorithm

:   :   $$\mathbf{r}\_{i}(t+\Delta t) =
        2\mathbf{r}\_{i}(t)-\mathbf{r}\_{i}(t-\Delta t)+\frac{\mathbf{F}\_{i}}{2m}(t)\Delta t^{2}+\mathcal{O}(\Delta t ^{3})$$

The Verlet algorithm can be rearranged to the Velocity-Verlet algorithm by inserting $\mathbf{v}\_{i}(t)=\frac{\mathbf{r}\_{i}(t)-\mathbf{r}\_{i}(t-\Delta t)}{\Delta t}$

:   :   $$\mathbf{r}\_{i}(t+\Delta t) =
        \mathbf{r}\_{i}(t)+ \mathbf{v}\_{i}(t)\Delta t+\frac{\mathbf{F}\_{i}}{2m}(t)\Delta t^{2}.$$

## Velocity-Verlet integration scheme

The Velocity-Verlet algorithm can be decomposed into the following steps:

1. $\mathbf{v}\_{i}(t + \frac{1}{2}\Delta t)=\mathbf{v}\_{i}(t)+\frac{\mathbf{F}\_{i}(t)}{2m\_{i}}\Delta t$
2. $\mathbf{r}\_{i}(t + \Delta t) = \mathbf{r}\_{i}(t) + \mathbf{v}\_{i}(t + \frac{1}{2}\Delta t)\Delta t$
3. compute forces $\mathbf{F}\_{i}(t)$ from density functional theory or machine learning
4. $\mathbf{v}\_{i}(t + \Delta t)=\mathbf{v}\_{i}(t+\frac{1}{2}\Delta t)+\frac{\mathbf{F}\_{i}(t+\Delta t)}{2m\_{i}}\Delta t$

From these equations it can be seen that the velocity and the position vectors are synchronous in time.

## Leap-Frog integration scheme

Another form of the Verlet algorithm can be written in the form of the Leap-Frog algorithm. The Leap-Frog algorithm consists of the following steps:

1. compute forces $\mathbf{F}\_{i}(t)$ from density functional theory or machine learning
2. $\mathbf{v}\_{i}(t + \frac{1}{2}\Delta t)=\mathbf{v}\_{i}(t- \frac{1}{2}\Delta t)+\frac{\mathbf{F}\_{i}(t)}{m\_{i}}\Delta t$
3. $\mathbf{r}\_{i}(t + \Delta t) = \mathbf{r}\_{i}(t) + \mathbf{v}\_{i}(t + \frac{1}{2}\Delta t)\Delta t$

In this form the velocity and the position vectors are asynchronous in time.

## Thermostats and used integrators

| MDALGO | thermostat | integration algorithm |
| --- | --- | --- |
| 0 | Nosé-Hoover | Velocity-Verlet |
| 1 | Andersen | Leap-Frog |
| 2 | Nosé-Hoover | Leap-Frog |
| 3 | Langevin | Velocity-Verlet |
| 4 | Nosé-Hoover chain | Velocity-Verlet |
| 5 | CSVR | Leap-Frog |
| 5 | Multiple Andersen | Leap-Frog |

## Related tags and articles

IBRION, MDALGO, Thermostats
