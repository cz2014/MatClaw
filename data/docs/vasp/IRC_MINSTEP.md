# IRC_MINSTEP

Categories: INCAR tag, Transition states

IRC\_MINSTEP = real  
 Default: **IRC\_MINSTEP** = 0.0250

Description: Lower limit for the step size (in fs).

---

The damped-velocity-Verlet algorithm for the IRC calculations uses an adaptively varying size of the time step. It depends on the estimated accuracy of the previous step. IRC\_MINSTEP defines the lower limit for the step size in fs.

## Related tags and articles

IRC calculations,
IRC\_DIRECTION ,
IRC\_STOP,
IRC\_DELTA0,
IRC\_MAXSTEP,
IRC\_VNORM0
