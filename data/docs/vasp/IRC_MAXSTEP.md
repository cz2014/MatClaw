# IRC_MAXSTEP

Categories: INCAR tag, Transition states

IRC\_MAXSTEP = real  
 Default: **IRC\_MAXSTEP** = 3.000

Description: Upper limit for the step size (in fs).

---

The damped-velocity-Verlet algorithm for the IRC calculations uses an adaptively varying size of the time step. It depends on the estimated accuracy of the previous step. IRC\_MAXSTEP defines the upper limit for the step size in fs.

## Related tags and articles

IRC calculations,
IRC\_DIRECTION ,
IRC\_STOP,
IRC\_DELTA0,
IRC\_MINSTEP,
IRC\_VNORM0
