# Profiling

Categories: VASP, Installation, INCAR tag, Performance

In the most recent version of VASP, profiling routines were added to all important routines in VASP. Using profiling will print at the end of the OUTCAR a list of all routines called during the specific run of VASP, its overall execution time, the number of times it was called and the level at which it was called.

## Compilation

To add support for profiling add `-DPROFILING` to the already existing preprocessor flags

```
 CPP = $(CPP_) -DMPI .... -DPROFILING
```

Then you have to entirely recompile VASP by executing

```
 make clean
 make vasp
```

## Support for new routines

If you want to include newly developed routines to the profiling, you have to include the profiling module (if it is not already included in the enclosing module your routine is in) by adding

```
 USE profiling
```

Furthermore you have to put the following statement at the very beginning of the routine with the name `[name]`

```
#ifdef PROFILING
  CALL START_PROFILING('[name]')
#endif
```

and at every possible return to the outer subroutine you have to put

```
#ifdef PROFILING
  CALL STOP_PROFILING('[name]')
#endif
```

Mind that there are sometimes other `#ifdef` constructs, which change the starting or return point of subroutines.
If a subroutine is not started or not stopped appropriately the profiling will get messed up. There is still some room for improvement, but it works so far.

In addition one can also profile certain parts of a routine or calls to LAPACK routines by enclosing this parts with calls to `START_PROFILING` and `STOP_PROFILING`, e.g.:

```
#ifdef PROFILING
  CALL START_PROFILING('dgemvn')
#endif
CALL DGEMVn( 'N' , INDMAX, LMMAXC,  ONE , NONLR_S%RPROJ(1+NLIIND), &
            INDMAX,  TMP(1,1+NP) , 1 , ZERO ,  WORK(1+NONLR_S%IRMAX*NP), 1)
#ifdef PROFILING
  CALL STOP_PROFILING('dgemvn')
#endif
```

## Output

All the timings will be summarized at the end of the OUTCAR file.

```
 PROFILE, used timers:    2017
 =============================
  index                 routine                    time                            calls level                                        
 ----------------------------------------------------------------------------------------------
     1    total_time                         4134.378029                                1   1
     2      initialization                       21.859301                              1   2
     6        init_mpi                              2.456473                            1   3
     7          m_init                                2.312794                          1   4
     .           .                                   .                                  .   .
     .           .                                   .                                  .   .
     .           .                                   .                                  .   .
 
   721      loop+                              4112.458616                              1   2
   727        elmin_all                          3857.453593                            1   3
   734          potlok                                6.538449                         20   4
   735            fft3d_mpi                             2.587358                       80   5
   736              fftbrc_mpi                            2.545392                     80   6
   737                fftbas_plan_mpi                       2.545311                   80   7
   743                  map_forward                           2.228926                120   8
   745                    m_alltoallv_z                         2.208413               80   9
```

In the first row we have just an index number, then the name of the called routine, its total execution time at this place in the program, the number of calls and the nesting level inside VASP (so `total_time` has level `1`, since it includes all other routines. `initialization` is called from inside `total_time` so it has level `2` and so on). After the detailed profile the Flat profile in printed

```
Flat profile
============
            routine name                   CPU           calls
---------------------------------------------------------------
m_sumb_d                              687.598978        6060
fftbas                                550.950960      309943
dllmm_kernel                          438.080414    29933568
rholm_kernel                          371.424660    26191872
racc0_hf                              314.036521      150528
rpro1_hf                              298.218335      172032
m_bcast_z_from                        187.539585       66560
m_alltoall_d                          183.903689       18992
roteta                                134.378198          20
pw_charge_trace                       130.274880      150528
vhamil_trace                          112.664470      143360
linbas                                 92.481414         658
pdssyex_zheevx                         87.056319         289
crrexp_mul_gwave                       75.224447    29933568
orth1                                  50.643717        2632
rs_coulomb_green_func                  50.344199        2822
       .                                   .             .
       .                                   .             .
       .                                   .             .
```

Here all execution times of a routine are summed up and all timings from routines called from inside this routine are subtraced. So we get the real execution time of this routine and can track down the most time consuming routines for this specific run.

## INCAR Flags

In the INCAR the output of the profiling can be controlled by four different flag:

* PTHRESHOLD
* PROUTINE
* PLEVEL
* PFLAT
