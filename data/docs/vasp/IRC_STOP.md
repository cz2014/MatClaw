# IRC_STOP

Categories: INCAR tag, Transition states

IRC\_STOP = integer  
 Default: **IRC\_STOP** = 20

Description: Sets the number of steps in which the energy must monotonously increase before an IRC calculation terminates.

---

Along the IRC pathway, from a higher energy state, i.e., the transition state or the excited state, towards a lower energy state, i.e., reactants or products, the energy generally decreases. In some cases, the IRC pathway may encounter regions with relatively constant energy (plateaus) or fluctuations due to numerical noise or complex interactions, particularly in the vicinity of transition states.

IRC\_STOP sets the number of time steps with increasing energy, after which the damped-velocity-Verlet algorithm in an IRC calculation terminates. In order to avoid a premature termination, especially close to transition states, IRC\_STOP should always be greater than 1.

## Related tags and articles

IRC calculations,
IRC\_DIRECTION ,
IRC\_DELTA0,
IRC\_MINSTEP,
IRC\_MAXSTEP,
IRC\_VNORM0
