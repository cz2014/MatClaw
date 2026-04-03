# Slow-growth approach

Categories: Advanced molecular-dynamics sampling, Theory

The free-energy profile along a geometric parameter $\xi$ can be scanned by an approximate slow-growth
approach.
In this method, the value of $\xi$ is linearly changed
from the value characteristic for the initial state (1) to that for
the final state (2) with a velocity of transformation
$\dot{\xi}$.
The resulting work needed to perform a transformation $1 \rightarrow 2$
can be computed as:

:   :   $$w^{irrev}\_{1 \rightarrow 2}=\int\_{{\xi(1)}}^{{\xi(2)}} \left ( \frac{\partial {V(q)}} {\partial \xi} \right ) \cdot \dot{\xi}\, dt.$$

In the limit of infinitesimally small $\dot{\xi}$, the work $w^{irrev}\_{1 \rightarrow 2}$
corresponds to the free-energy difference between the the final and initial state.
In the general case, $w^{irrev}\_{1 \rightarrow 2}$ is the irreversible work related
to the free energy via Jarzynski's identity:

:   :   $$exp^{-\frac{\Delta A\_{1 \rightarrow 2}}{k\_B\,T}}=
        \bigg \langle exp^{-\frac{w^{irrev}\_{1 \rightarrow 2}}{k\_B\,T}} \bigg\rangle.$$

Note that calculation of the free-energy via this equation requires
averaging of the term ${\rm exp} \left \{-\frac{w^{irrev}\_{1 \rightarrow 2}}{k\_B\,T} \right \}$
over many realizations of the $1 \rightarrow 2$
transformation.
Detailed description of the simulation protocol that employs Jarzynski's identity
can be found in reference .

## How to

* For a slow-growth simulation, one has to perform a calcualtion very similar to Constrained molecular dynamics but additionally the transformation velocity-related INCREM tag for each geometric parameter with STATUS=0 has to be specified:

1. Set the standard MD-related tags: IBRION=0, TEBEG, POTIM, and NSW
2. Choose a thermostat:
   1. Set MDALGO=1, and choose an appropriate setting for ANDERSEN\_PROB
   2. Set MDALGO=2, and choose an appropriate setting for SMASS
3. Define geometric constraints in the ICONST file, and set the STATUS parameter for the constrained coordinates to 0
4. When the free-energy gradient is to be computed, set LBLUEOUT=.TRUE.

5. Specify the transformation velocity-related INCREM-tag for each geometric parameter with STATUS=0.

## References

---
