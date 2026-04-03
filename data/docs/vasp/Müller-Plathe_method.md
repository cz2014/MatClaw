# Müller-Plathe method

Categories: Howto, Molecular dynamics, Ensemble properties

There are two components of the thermal conductivity, the  electronic $\kappa\_e$ and the  lattice  $\kappa\_l$, which we call $\lambda$ here. The lattice thermal conductivity $\lambda$ can be obtained by Fourier's law

$\mathbf{J} = -\lambda \nabla T$,

where $\mathbf{J}$ is the heat-flux vector and $\nabla T=\partial T/\partial \mathbf{a}\_i$ is the temperature gradient. In reverse nonequilibrium molecular dynamics proposed by Müller-Plathe, a temperature gradient ($\partial T/\partial \mathbf{a}\_i$) along selected lattice axis $\mathbf{a}\_i$ is created by
splitting the simulation box into 2N slabs of identical thickness orthogonal to $\mathbf{a}\_i$ and swapping the velocity of the coolest particle of type $\mu$ from the slab 1 ($v\_{\mu,c}$) with the velocity of the hottest particle of the same type from the slab N+1 ($v\_{\mu,h}$).
Assuming that $\mathbf{a}\_i$ is orthogonal to the remaining two lattice vectors $\mathbf{a}\_j$ and $\mathbf{a}\_k$, $\lambda$ is computed as

:   $$\lambda = -\frac{\sum\_{transfers} \sum\_{\mu} m\_{\mu} (v\_{\mu,h}^2 - v\_{\mu,c}^2 )}{4\tau |\mathbf{a}\_j \times\mathbf{a}\_k| \langle \partial T/\partial \mathbf{a}\_i \rangle}$$

where the first summation is taken over all swapping events, $m\_{\mu}$ is the mass of a particle of the type $\mu$, $\tau$ is the total simulation time, and $\langle\cdots\rangle$ represents an ensemble average of the quantity enclosed.
The method is invoked by defining the parameter FMP\_ACTIVE (see below). The simulation has to be started from a well-equilibrated POSCAR-file and one of the following thermostats can be utilized in the NVE ensemble:

:   |  |  |
    | --- | --- |
    | thermostats | tags |
    | Langevin thermostat | `MDALGO = 3` and `LANGEVIN_GAMMA = NTYP×0.0` |
    | Andersen thermostat | `MDALGO = 1` and `ANDERSEN_PROB = 0.0` |

> **Mind:**
>
> * For measurements of thermal conductivity $\lambda$, the Langevin thermostat is preferred because it utilizes the velocity Verlet algorithm. The velocity Verlet algorithm computes positions and velocities in a synchronized manner. Nevertheless, setting `MDALGO = 1` can be useful when studying particle redistributions under a temperature gradient.
> * The Müller-Plathe method can be utilized in the canonical ensemble. In the canonical ensemble, the thermal conductivity can not be measured because the energy is not conserved. Still, it can be useful to study a material's properties with a temperature gradient under canonical conditions.

The behavior of the simulation is controlled via the following parameters defined in the INCAR file:

* FMP\_ACTIVE=[logical array] invokes the method and specifies whether or not the atomic type (as defined in POSCAR) is allowed for swapping.
* FMP\_DIRECTION=[integer] index of the lattice vector $\mathbf{a}\_i$ along which the gradient $\partial T/\partial \mathbf{a}\_i$ is created.
* FMP\_SNUMBER=[integer] number of slabs.
* FMP\_SWAPNUM=[integer] number pairs of particles exchanged in a single swapping event.
* FMP\_PERIOD=[integer] number of time steps between two swapping events.

The output needed to evaluate the expression for $\lambda$ is written out to the REPORT file. In particular, lines introduced by the string "tsl>" contain the ID number of the slab (item 2), the number of atoms in the slab (item 3), and the instantaneous temperature of the slab (item 4). This information, is needed to evaluate $\langle \partial T/\partial \mathbf{a}\_i \rangle$ and is written for each MD step:

```
grep "tsl>" REPORT 
tsl>        1     128   348.740
tsl>        2     138   387.874
tsl>        3     136   391.949
tsl>        4     127   380.342
tsl>        5     113   432.304
tsl>        6     122   409.074
tsl>        7     121   406.230
tsl>        8     120   370.238
tsl>        9     118   377.384
tsl>       10     134   383.762
tsl>       11     109   376.807
tsl>       12     146   377.061
tsl>        1     131   374.098
 ...
```

After a swapping event, FMP\_SWAPNUM lines starting with the string "fmp>" are written (only written if NSW>FMP\_PERIOD):

```
grep "fmp>" REPORT
fmp> swapping atoms:     1133    1080     1158.178       15.604
fmp> swapping atoms:     1109    1485     1160.495       56.120
fmp> swapping atoms:     1059    1281     1400.528       18.375
fmp> swapping atoms:     1054    1357     1162.322       21.041
...
```

These lines contain the ID numbers (items 4 and 5) and instantaneous temperatures of hot (item 6) and cold atoms (item 7). Since the instantaneous temperature of a single particle $\mu$ is defined via $\frac{3}{2}k\_B\,T\_{\mu} = \frac{m\_{\mu}}{2} v\_{\mu}^2$,
the instantaneous temperatures of hot and cold atoms can be used, in a straightforward manner, to evaluate the numerator of the equation for $\lambda$ given above:

```
 grep "fmp>" REPORT | awk 'BEGIN {bolkEV=8.6173857e-5; Q=0.} {Q+= $6-$7} END {print 1.5*Q*bolkEV}'
```

> **Mind:**
>
> * The swapping process defined above leaves the total energy unchanged. Thus, for instance, the total energy is a conserved quantity if the simulation with the Müller-Plathe method is realized in the NVE ensemble.
> * The lattice vector along which the gradient of temperature is evaluated must be orthogonal to the remaining two lattice vectors.
> * To obtain meaningful results, a large supercell must be used in this type of simulation. Additionally averaging over several MD runs is recommended.

## Example

INCAR:

```
ML_LMLFF       = .TRUE. # switch on machine learning
ML_MODE        = RUN    # execute in production mode
ML_OUTPUT_MODE = 0      # reduce written output
ML_OUTBLOCK    = 100    # write every 100th step

TEBEG          = 320    # simulation temperature
ISIF           = 2      # compute stress tensor without box update
IBRION         = 0      # run molecular dynamics
MDALGO         = 3      # use Langevin thermostat
LANGEVIN_GAMMA = 2*0    # define microcanonical ensemble
POTIM          = 0.50   # time step 0.5fs
NSW            = 100000 # number of time steps
NBLOCK         = 100    # reduce output writing for speed
NWRITE         = 0      # write only little output
KBLOCK         = 1000   # frequency of pair correlation computation

FMP_SNUMBER   = 12    # number of slabs
FMP_DIRECTION = 3     # heat will be transfered along 3rd lattice vector
FMP_PERIOD    = 400   # swapping will be made every 400 steps
FMP_SWAPNUM   = 1     # one pair will be swapped during every swapping event
FMP_ACTIVE    = .FALSE. .TRUE. # swap only second species defined in POSCAR
```

POSCAR:

**Click to show POSCAR**

```
H2O_liquid                              
   1.00000000000000     
    25.7311637418799997   -0.0000240755320000   -0.0000838822960000
    -0.0000000011150000   25.7309330236340017   -0.0000216116710000
    -0.0000000579360000    0.0000000000980000   25.7338018054700015
   H    O 
  1008   504
Direct
  0.9719536107331490  0.5651793136020415  0.2294052102477605
 -0.0077300499517214  0.2613430995605425  0.1102855192680011
  0.1272929902409080  0.7688976203518609  0.0040420878130920
  0.1840798126749473  0.8151812936619544  0.7436072327230931
  0.5416971697672741 -0.3480209629916928  0.1985352280548357
... [1507 more coordinate lines truncated] ...
 
  0.73530655E-02  0.30065103E-02 -0.13176402E-01
 -0.80071529E-02 -0.13133020E-01  0.49628126E-02
 -0.11384086E-01  0.63397969E-02  0.19808006E-01
 -0.83581773E-02  0.10417810E-01 -0.20805653E-03
  0.18043599E-02  0.22694564E-01  0.19178825E-02
... [1507 more coordinate lines truncated] ...
 
           1
  0.500000000000000     
  0.10000000E+01  0.00000000E+00  0.00000000E+00  0.00000000E+00
  0.97209649E+00  0.56523774E+00  0.22914920E+00
  0.99211436E+00  0.26108790E+00  0.11038194E+00
  0.12707178E+00  0.76902081E+00  0.44269508E-02
  0.18391740E+00  0.81538373E+00  0.74360319E+00
... [4532 more coordinate lines truncated] ...
```

To extract the data from a collection of REPORT files the following analysis script can be used.
AnalysisScript.sh:

**Click to show AnalysisScript.sh**

```
 #!/usr/bin/env bash
 echo "This script will compute the thermal conductivity from VASP output."
 echo "The VASP has to be created with the FMP method."
 echo "First a couple of parameters have to be supplied:"
 echo "FMP_PERIOD"
 echo "POTIM"
 echo "Surface area orthogonal to heat gradient"
 echo "Length of the box along heat gradient"
 echo "FMP_SNUMBER"
 echo "Some wildcard for the file names. For example REPORT.*"
 echo "If only one file should be analyzed just input the file by REPORT.1"
 # FMP_PERIOD:
 echo "Please supply FMP_PERIOD"
 read period
 # POTIM:
 echo "Please enter the time step of your simulation in [fs]"
 read potim
 # area of surface orthogonal to the direction of the heat transfer:
 echo "Please enter surface area orthogonal to the direction of the heat transfer in [Angstroem^2]"
 read A
 # size of the cell along the direction of the heat transfer:
 echo "Please enter the length of the cell along the direction of heat transfer in [Angstroem]"
 read L
 # FMP_SNUMBER:
 echo "Please enter FMP_SNUMBER; Number of slabs perpendicular to the temperature gradient"
 read ns
 echo "Please enter a wildcard for the filenames. For example REPORT.*"
 read wildcard
 files=$(ls ${wildcard} | sort -V)
 # Boltzmann constant in eV
 bolkEV=8.6173857e-5
 # index of the hottest slab (the slab in the middle of the cell)
 let nhot=ns/2+1
 # extract the difference in T between the hottest and coolest atom for each swapping event 
 # and store in the file dT.dat
 rm dT.dat
 for f in ${files}; do
   if test -f ${f}
   then
     grep swapping ${f} | awk '{{print 1.5*($6-$7)*"'${bolkEV}'"}}'  >> dT.dat
    fi
    let i+=1
 done
 # determine the total number of swapping events
 ndat=$(wc -l dT.dat |awk '{print $1}')
 # compute the average heat transferred per unit of time (fs)
 Q=$(awk 'BEGIN {a=0.;c=0} {c+=1;a+=$1} END {printf("%12.16f\n",a/c/"'${period}'"/"'${potim}'")}' dT.dat )
 # Extract data needed to determine the average T of hot and cold slabs
 rm sl?.dat
 for f in ${files}; do
   if test -f ${f}
   then
     grep "tsl>" ${f} | awk '{if (NR%"'${ns}'"==1) {print $4}}'  >> slc.dat
     grep "tsl>" ${f} | awk '{if (NR%"'${ns}'"=="'${nhot}'") {print $4}}'  >> slh.dat
   fi
   let i+=1
 done
 # determine T of cold and hot slabs
 tc=$(awk 'BEGIN {a=0.} {a+=$1} END {printf("%12.16f\n",a/NR)}' slc.dat)
 th=$(awk 'BEGIN {a=0.} {a+=$1} END {printf("%12.16f\n",a/NR)}' slh.dat)
 # compute linear T gradient.
 grad=$(echo print "(" 2 "*("$th "-" $tc ")/" $L ")" |python ) 
 # Finally, compute thermal conductivity
 lambda=$(echo print "(" 0.5 "*" $Q "/" $A "/" $grad "*" 1602177.3299999998 ")" |python)
 echo lambda $lambda
```

## Convergence Analysis for thermal conductivity

In general, a lot of molecular dynamics steps and a large supercell are needed to get converged results for thermal conductivity. Therefore, convergence analysis is a crucial step when measuring thermal conductivities. To measure the convergence of $\lambda$ it is recommended to do several MD runs. The thermal conductivity can then be computed with the help of the provided analysis script. It should be noted that the analysis script assumes a linear temperature gradient. Hence, it is essential to check the linearity of the temperature gradient when using the script.

Convergence of $\lambda$. As the simulation time progresses, the averages of the plot incorporate an increasing amount of data until convergence is achieved

## Related tags and articles

FMP DIRECTION,
FMP\_ACTIVE,
FMP\_SNUMBER,
FMP\_SWAPNUM,
FMP\_PERIOD,
Electronic transport coefficients

## References
