# STOP_ON

Categories: INCAR tag, Performance

STOP\_ON = Error|Alert  
 Default: **STOP\_ON** = Error

Description: STOP\_ON defines if the code should stop on errors only or also on alerts.

---

There are two instances, why one might want a more conservative choice when running calculations.

First, VASP will overwrite user provided input, if the input does not make sense. You may want to
make sure that VASP does not continue in this case by setting the stricter STOP\_ON = Alert

Secondly, VASP will continue if it encounters issues during the calculation if there is a chance
that these disappear during the self consistency. However, if you are at a stage where you still
explore what parameters to use, being more conservative makes the calculation fail faster so
that you can try different parameters.
