# Band gap renormalization in diamond using one-shot method

Categories: Examples

Overview > Band gap renormalization in diamond using one-shot method > List of tutorials

## Task

Calculating the zero-point renormalization (ZPR) and the temperature dependence of the indirect band gap in diamond using a one-shot method.

## Input

### POSCAR

* Primitive cell (*POSCAR.prim*):

```
C_2_fcc
   1.00000000000000
     0.00000000   1.78349300  1.78349300
     1.78349300   0.00000000  1.78349300
     1.78349300   1.78349300  0.00000000
   C
     2
Direct
  0.00000000  0.00000000  0.00000000
  0.75000000  0.75000000  0.75000000
```

* 4x4x4 super cell used in this calculation (*POSCAR.4x4x4*):

```
C_128_fcc
   1.00000000000000
    0.00000000   7.13397200   7.13397200
    7.13397200   0.00000000   7.13397200
    7.13397200   7.13397200   0.00000000
   C
  128
Direct
   0.00000000   0.00000000   0.00000000
   0.25000000   0.00000000   0.00000000
   0.50000000   0.00000000   0.00000000
   0.75000000   0.00000000   0.00000000
   0.00000000   0.25000000   0.00000000
... [123 more coordinate lines truncated] ...
```

### KPOINTS

```
K-Points
 0
Gamma
 1  1  1
 0  0  0
```

* We only need a single k-point, since the convergence is done via the super-cell size.

### INCAR

```
general:
 System = cd-C
 PREC = Accurate
 ALGO = FAST
 ISMEAR = 0 
 SIGMA = 0.1;
 IBRION = 6
 PHON_LMC = .TRUE.
 PHON_NSTRUCT = 0
 PHON_NTLIST = 1
 PHON_TLIST = 0.0
```

* The tags with "PHON\_" control the electron-phonon related features. PHON\_LMC enables the calculation of structures with random displacements (one shot or Monte Carlo) of the atoms according to the density matrix of a harmonic oscillator. By selecting PHON\_NSTRUCT=0 a one-shot configuration (ZG configuration) is obtained. The tag PHON\_NTLIST selects the number of temperatures for which the structure with the one shot calculation is obtained. This requires also the list of temperatures given by PHON\_TLIST which have exact PHON\_NTLIST number of elements.
* IBRION=6 is selected to obtain the eigenvectors and eigenvalues of the dynamical matrix at the Gamma point.

## Calculation

This example will use a one-shot method, where only a single structure that contains the electron-phonon information is required for a given temperature. The "Gamma" version of VASP is used throughout this example since only a single k point is used in the calculations.

The calculation consists of two steps:

1. Obtain new "distorted" POSCAR file which contains special displacements. This calculation also contains the band gap of the original structure.
2. Execute simple DFT calculation for the structure containing the special displacements to obtain the band gap.
3. Extract ZPR as the difference between the band gaps from the two calculations.

### Obtain structure with special displacements

To run the calculation *POSCAR.4x4x4* needs to be copied to *POSCAR* and *INCAR.init* to *INCAR*.

Execute VASP.

Copy the OUTCAR file to *OUTCAR.init*. It will be later used for the band gap of the "undistorted" structure.

The new POSCAR file containing the special displacements is given as *POSCAR.T=0.*.

### Calculate electronic levels of structure with special displacements

Copy the file *POSCAR.T=0.* to *POSCAR*.

Delete (or comment out with *#*) all the lines in the INCAR file related to "PHON\_" so that it looks like the following:

```
System = cd-C
PREC = Accurate
ALGO = FAST
ISMEAR = 0 
SIGMA = 0.1;
```

Execute VASP.

Copy *OUTCAR* to *OUTCAR.T=0.*.

### Extract ZPR

We extract the band gap renormalization as

$\Delta E\_{\mathrm{rm}} = E\_{\mathrm{SP}}-E$

where $E\_{\mathrm{SP}}$ and $E$ are the band gaps with and without special displacements, respectively.

Since the 4x4x4 cell of cubic diamond has 3 degenerate bands at the valence band maximum and 6 degenerate bands at the conduction band minimum, they are averaged in the calculation of the band gap. This is necessary since the convergence with respect to cell size is drastically improved this way. Also, all perturbation theory calculations in the literature evaluate the band gap the same way, which ensures the compatibility of the different computational methods.

The band gaps are extracted from the previously saved files *OUTCAR.init* and *OUTCAR.T=0.* using the following script:

**Click to show/*extract\_zpr.sh***

```
#!/bin/bash 

i="OUTCAR.T=0."
j="OUTCAR.init"

homo1=`awk '/NELECT/ {print $3/2}' $i`
homo2=`awk '/NELECT/ {print $3/2-1}' $i`
homo3=`awk '/NELECT/ {print $3/2-2}' $i`
lumo1=`awk '/NELECT/ {print $3/2+var+1}' $i`
lumo2=`awk '/NELECT/ {print $3/2+var+2}' $i`
lumo3=`awk '/NELECT/ {print $3/2+var+3}' $i`
lumo4=`awk '/NELECT/ {print $3/2+var+4}' $i`
lumo5=`awk '/NELECT/ {print $3/2+var+5}' $i`
lumo6=`awk '/NELECT/ {print $3/2+var+6}' $i`
e1a=`grep "   $homo1  " $i | head -$nkpt | sort -n -k 2 | tail -1 | awk '{print $2}'`
e1b=`grep "   $homo2  " $i | head -$nkpt | sort -n -k 2 | tail -1 | awk '{print $2}'`
e1c=`grep "   $homo3  " $i | head -$nkpt | sort -n -k 2 | tail -1 | awk '{print $2}'`
e2a=`grep "   $lumo1  " $i | head -$nkpt | sort -n -k 2 | head -1 | awk '{print $2}'`
e2b=`grep "   $lumo2  " $i | head -$nkpt | sort -n -k 2 | head -1 | awk '{print $2}'`
e2c=`grep "   $lumo3  " $i | head -$nkpt | sort -n -k 2 | head -1 | awk '{print $2}'`
e2d=`grep "   $lumo4  " $i | head -$nkpt | sort -n -k 2 | head -1 | awk '{print $2}'`
e2e=`grep "   $lumo5  " $i | head -$nkpt | sort -n -k 2 | head -1 | awk '{print $2}'`
e2f=`grep "   $lumo6  " $i | head -$nkpt | sort -n -k 2 | head -1 | awk '{print $2}'`   
 
homo_ref=`awk '/NELECT/ {print $3/2}' $j`
lumo_ref=`awk '/NELECT/ {print $3/2+var+1}' $j`

h_ref=`grep "   $homo_ref  " $j | head -$nkpt | sort -n -k 2 | tail -1 | awk '{print $2}'`
l_ref=`grep "   $lumo_ref  " $j | head -$nkpt | sort -n -k 2 | head -1 | awk '{print $2}'`  
 
echo "The band gap (in eV) without zero-point vibrations is:"
echo "$h_ref $l_ref" |awk '{print ($2-$1)}'
echo "The band gap (in eV) including zero-point vibrations is:"
echo "$e1a $e1b $e1c $e2a $e2b $e2c $e2d $e2e $e2f" |awk '{print (($4+$5+$6+$7+$8+$9)/6.0-($1+$2+$3)/3.0)}'
echo "The zero-point renormalization of the band gap (in eV) is:" 
echo "$e1a $e1b $e1c $e2a $e2b $e2c $e2d $e2e $e2f $h_ref $l_ref" |awk '{print (($4+$5+$6+$7+$8+$9)/6.0-($1+$2+$3)/3.0)-($11-$10)}'
```

To use the script please type:

```
bash extract_zpr.sh
```

The output of the script should look like the following:

```
The band gap (in eV) without zero-point vibrations is:
4.4049
The band gap (in eV) including zero-point vibrations is:
4.05102
The zero-point renormalization of the band gap (in eV) is:
-0.353883
```

### Better accuracy

The accuracy of the band gap renormalization depends dominantly on the size of the super cell, so this is the quantity that has to be usually converged in this type of calculation.

This example contains a POSCAR file for a 5x5x5 cell (*POSCAR.5x5x5*).
After repeating all above steps with this POSCAR file the following results should be obtained:

```
The band gap (in eV) without zero-point vibrations is:
4.1421
The band gap (in eV) including zero-point vibrations is:
3.83717
The zero-point renormalization of the band gap (in eV) is:
-0.304933
```

The interested user can try to further increase the cell size, by making a super cell from the primitive cell (*POSCAR.prim*) provided by this tutorial (how to build a super cell is for example covered here).

### Temperature dependence of the band gap

Here the temperature dependence of the band gap due to electron-phonon interactions is calculated. The input files are located in the directory  *TEMP\_DEPENDENCE*. Switch to this directory. Copy *POSCAR.4x4x4* to *POSCAR* and *INCAR.init* to *INCAR*. The *INCAR* file contains following lines which are different from the calculation of the ZPR:

```
PHON_NTLIST = 8
PHON_TLIST = 0.0 100.0 200.0 300.0 400.0 500.0 600.0 700.0
```

After running the calculations several new POSCAR files are created.

Before running the calculations copy *INCAR.run\_temp* to *INCAR*.

Run a standard VASP calculation for each of them to obtain the band gap or use the script *run\_temperature.sh* provided with this calculation:

**Click to show/*run\_temperature.sh***

```
#!/bin/bash

# please enter your executable path here
vasp_exec=./vasp_gam

#please enter the number of processors used for VASP here
np=8

for i in 0 100 200 300 400 500 600 700
do
   cp POSCAR.T\=$i. POSCAR
   mpirun -np $np $vasp_exec
   mv OUTCAR OUTCAR.T\=$i
done
```

To run the script please edit the file and set your VASP executable path (*vasp\_exec*) and the number of processors you are going to use (*np*). To run the calculation type:

```
bash ./run_temperature.sh
```

This step produces several OUTCAR files which can be analyzed using the script *extract\_temp.sh*:

**Click to show/*extract\_temp.sh***

```
!/bin/bash 

if [ -f gap_vs_temp.dat ]
then
   rm gap_vs_temp.dat
fi

touch gap_vs_temp.dat
counter=0

for temp in 0 100 200 300 400 500 600 700
do
   i="OUTCAR.T=$temp"

   homo1=`awk '/NELECT/ {print $3/2}' $i`
   homo2=`awk '/NELECT/ {print $3/2-1}' $i`
   homo3=`awk '/NELECT/ {print $3/2-2}' $i`
   lumo1=`awk '/NELECT/ {print $3/2+var+1}' $i`
   lumo2=`awk '/NELECT/ {print $3/2+var+2}' $i`
   lumo3=`awk '/NELECT/ {print $3/2+var+3}' $i`
   lumo4=`awk '/NELECT/ {print $3/2+var+4}' $i`
   lumo5=`awk '/NELECT/ {print $3/2+var+5}' $i`
   lumo6=`awk '/NELECT/ {print $3/2+var+6}' $i`
   e1a=`grep "^    $homo1   " $i | head -$nkpt | sort -n -k 2 | tail -1 | awk '{print $2}'`
   e1b=`grep "^    $homo2   " $i | head -$nkpt | sort -n -k 2 | tail -1 | awk '{print $2}'`
   e1c=`grep "^    $homo3   " $i | head -$nkpt | sort -n -k 2 | tail -1 | awk '{print $2}'`
   e2a=`grep "^    $lumo1   " $i | head -$nkpt | sort -n -k 2 | head -1 | awk '{print $2}'`
   e2b=`grep "^    $lumo2   " $i | head -$nkpt | sort -n -k 2 | head -1 | awk '{print $2}'`
   e2c=`grep "^    $lumo3   " $i | head -$nkpt | sort -n -k 2 | head -1 | awk '{print $2}'`
   e2d=`grep "^    $lumo4   " $i | head -$nkpt | sort -n -k 2 | head -1 | awk '{print $2}'`
   e2e=`grep "^    $lumo5   " $i | head -$nkpt | sort -n -k 2 | head -1 | awk '{print $2}'`
   e2f=`grep "^    $lumo6   " $i | head -$nkpt | sort -n -k 2 | head -1 | awk '{print $2}'`

   if [ $temp -eq "0" ]
   then
      ref=`echo "$e1a $e1b $e1c $e2a $e2b $e2c $e2d $e2e $e2f" |awk '{print (($4+$5+$6+$7+$8+$9)/6.0-($1+$2+$3)/3.0)}'`
   fi

   echo "$e1a $e1b $e1c $e2a $e2b $e2c $e2d $e2e $e2f $temp $ref" |awk '{print $10,(($4+$5+$6+$7+$8+$9)/6.0-($1+$2+$3)/3.0)-$11}' >> gap_vs_temp.dat
done
```

To run the script please type the following:

```
bash ./extract_temp.sh
```

This script calculates the relative change of the band with respect to temperature (that means the offset is shifted to zero). The result is written to *gap\_vs\_temp.dat*. To plot the data please type the following:

```
gnuplot -e "set terminal jpeg;set xlabel 'T (K)'; set ylabel 'band gap'; set style data lines; plot 'gap_vs_temp.dat', 'C_exp_points_offset0.dat' w circles, 'C_exp_fit_offset0.dat'" > gap_vs_temp.jpg
```

The resulting curve should look like the following:

The experimental data (blue lines and circles) are taken from reference .

## Temperature dependence of the band gap including volume effects

In the previous step, we see that the experimental slope of the temperature dependence of the band gap is underestimated. To improve the agreement we will now also consider the volume dependence. The volume dependence is calculated from quasi-harmonic calculations .

First save your obtained band gap vs. temperature curve, since it will be overwritten otherwise. Type the following:

```
mv gap_vs_temp.dat gap_vs_temp_novol.dat
```

Go out of the directory *./TEMP\_DEPENDENCE* and go to the directory *./QUASI\_HARMONIC*. For the purpose of this tutorial, the quasi-harmonic calculations will be performed for the 4x4x4 cell but for exact calculations, one needs to go to larger cell sizes until the results are converged.

There are three scripts in this directory to perform the quasi-harmonic calculations:

1. *quasi\_harm\_4x4x4\_diamond\_create\_pos\_and\_run\_vasp.sh*
2. *quasi\_harm\_4x4x4\_diamond\_make\_energy\_vs\_volume\_plots.sh*
3. *quasi\_harm\_4x4x4\_diamond\_obtain\_fitting.sh*

For a quasi-harmonic fit we need free energy vs. volume curves at different temperatures. Starting from the equilibrium volume we need to create POSCAR files at different volumes. To do this use the script:

**Click to show/*quasi\_harm\_4x4x4\_diamond\_create\_pos\_and\_run\_vasp.sh***

```
#! /bin/bash

# please enter your executable path here
vasp_exec=./vasp_gam

#please enter the number of processors used for VASP here
np=8

cp INCAR.qh INCAR

for i in 6.13521592 6.27789536 6.4205748 6.56325424 6.70593368 6.84861312 6.99129256 7.133972 7.27665144 7.41933088 7.56201032 7.70468976 7.8473692 7.99004864 8.13272808
do
sed "s/7.13397200/${i}/g" POSCAR.4x4x4 > POSCAR_$i
cp POSCAR_$i POSCAR
mpirun -np 8 $vasp_exec

mv OUTCAR OUTCAR_$i
done
```

This script creates 15 POSCAR files where the volume is varied in both directions in steps of 2 percent with respect to the starting volume. It also runs the necessary VASP calculations to obtain the dynamical matrix. To run this script please set your executable path and number of processors in the script and type:

```
bash ./quasi_harm_4x4x4_diamond_create_pos_and_run_vasp.sh
```

This script renames all the OUTCAR files for each volume which are needed in the next step.
In that step the free energy vs. volume curves need to be extracted for each temperature. To do this use the script:

**Click to show/*quasi\_harm\_4x4x4\_diamond\_make\_energy\_vs\_volume\_plots.sh***

```
#!/bin/bash

bandshift=0
gwrun=-1
dgbd=-1
val=-1
con=-1
gwldadiff=-1
test=-1
while [[ $# -gt 0 ]]
do
   key="$1"
   case $key in
   esac
   shift
done

if [ -f "helpscript.perl" ]; then
   rm helpscript.perl
fi

cat > helpscript.perl  <<EOF
#!/bin/perl

use strict;
use warnings;

my \$zahler=0;
my @entropy=0;
my \$ezp=0;
my \$fhelmholtz=0;
my \$uenergy;
my \$kboltzmann=8.6173303*10**(-5.0);
my \$ntemp=8;
my \$tmax=700;
my \$tmin=0;
my \$tstep=100;
for (my \$itemp=1;\$itemp<=\$ntemp;\$itemp++)
{
   \$entropy[\$itemp]=0;
}
while (<>)
{
   chomp;
   \$_=~s/^/ /;
   my @help=split(/[\t,\s]+/);
   \$zahler=\$zahler+1;
   if (\$zahler == 1) {\$uenergy=\$help[1];}
   else 
   {
      my \$homega=\$help[2]/1000;
      \$ezp=\$ezp+\$homega*0.5;
      for (my \$itemp=1;\$itemp<=\$ntemp;\$itemp++)
      {
         my \$temp=(\$itemp-1)*\$tstep+\$tmin;
         my \$kbt=\$kboltzmann*\$temp;
         if (\$temp < 0.0000001) 
         {
         }
         else
         {
              \$entropy[\$itemp]=\$entropy[\$itemp]-\$kboltzmann*log(1-exp(-\$homega/\$kbt));
              \$entropy[\$itemp]=\$entropy[\$itemp]+\$kboltzmann*\$homega/\$kbt*(1/(exp(\$homega/\$kbt)-1));
         }
      }
   }
   last if eof;
}

\$ezp=\$ezp; #/ \$zahler;

for (my \$itemp=1;\$itemp<=\$ntemp;\$itemp++)
{
    my \$temp=(\$itemp-1)*\$tstep+\$tmin;
        
    \$entropy[\$itemp]=\$entropy[\$itemp]; # / \$zahler; 
    \$fhelmholtz=\$uenergy+\$ezp-\$temp*\$entropy[\$itemp];
    printf ("%15.8e %15.8e\n",\$temp,\$fhelmholtz);
}
printf ("#NOTEMP %15.8e\n",\$uenergy);
EOF

rm OUTTEMP*
first=0
for i in OUTCAR_*; do

   echo "Starting $i"
   v2=${i##OUTCAR_}
   if [ -f "helpfile.help" ]; then
      rm helpfile.help
   fi
   touch helpfile.help
   cp OUTCAR_$v2 OUTCAR
   awk '/free energy/' OUTCAR | tail -n 1| awk '{print $5}' >> helpfile.help
   awk '/[0-9]* f .* THz/ {print $1,$10}' OUTCAR >> helpfile.help
   awk '/[0-9]* f.i.*THz/ {print $1,$9}' OUTCAR >> helpfile.help
   volume=`awk '/volume of cell/ {print $5}' OUTCAR | tail -n 1`

   perl helpscript.perl helpfile.help > hhhhelp.txt

   runcount=0
   while read line; do
      runcount=$((runcount+1))
      if [[ $first -eq 0 ]]; then
         echo $line | awk -v var="$volume" '{print var,$2,$1}' > OUTTEMP_$runcount
      else
         echo $line | awk -v var="$volume" '{print var,$2}' >> OUTTEMP_$runcount
      fi
   done < ./hhhhelp.txt

   first=1
done

for i in OUTTEMP_*; do
   v2=${i##OUTTEMP_}
   mv OUTTEMP_$v2 OUTHELP
   sort -n -k 1 OUTHELP > OUTTEMP_$v2
done

rm helpfile.help
rm helpscript.perl
rm hhhhelp.txt
rm OUTHELP
```

To use this script please type:

```
bash ./quasi_harm_4x4x4_diamond_make_energy_vs_volume_plots.sh
```

The free energy curves for each volume are saved to *OUTTEMP\_\**.

Finally to obtain the equilibrium volume at each temperature use the following script:

**Click to show/*quasi\_harm\_4x4x4\_diamond\_obtain\_fitting.sh***

```
#!/bin/bash

for i in OUTTEMP_*
do
   cp $i OUTTEMP.current
   #extract temperature
   temp=`head -n 1 OUTTEMP.current|awk '{print $3}'`
   #do fitting
   gnuplot -e "E(V)=E0+9.0/8.0*B0*V0*((V0/V)**(2.0/3.0)-1)**2 + 9.0/16.0*B0*\
      (B0P-4)*V0*((V0/V)**(2.0/3.0)-1.0)**3.0 + R*((V0/V)**(2.0/3.0)-1.0)**4.0;\
      B0P = 1;B0 = 1;V0 = 720;E0 = -1150;R  = -1.0;fit E(x) 'OUTTEMP.current'  u 1:2 via B0P,B0,V0,E0,R" &> suppress_output
   #extract volume from fit
   a=`grep "V0" fit.log|grep "=" |tail -n 1|awk '{print ($3/2.0)**(1.0/3.0)}'`
   #print temperature and volume to 
   echo "temperature: $temp, a_latt: $a" 
done

rm suppress_output
rm OUTTEMP.current
```

To run this script type:

```
bash ./quasi_harm_4x4x4_diamond_obtain_fitting.sh
```

The output should look like the following:

```
temperature: 0.00000000e+00, a_latt: 7.18012
temperature: 1.00000000e+02, a_latt: 7.18014
temperature: 2.00000000e+02, a_latt: 7.18064
temperature: 3.00000000e+02, a_latt: 7.18267
temperature: 4.00000000e+02, a_latt: 7.18613
temperature: 5.00000000e+02, a_latt: 7.19037
temperature: 6.00000000e+02, a_latt: 7.19493
temperature: 7.00000000e+02, a_latt: 7.19959
temperature: #NOTEMP, a_latt: 7.15218
```

Now switch back to the folder *./TEMP\_DEPENDENCE* and replace the lattice parameters at each temperature in the *POSCAR.T=\** files by the one obtained for the above fit. After that rerun the scripts *run\_temperature.sh* and *extract\_temp.sh*.

To plot the newly obtained curve together with the other curves please type:

```
gnuplot -e "set terminal jpeg;set xlabel 'T (K)'; set ylabel 'band gap'; set style data lines; plot 'gap_vs_temp_novol.dat', 'C_exp_points_offset0.dat' w circles, 'C_exp_fit_offset0.dat', 'gap_vs_temp.dat'" > gap_vs_temp_volume.jpg
```

The resulting plot should look like the following:

Now we see in this plot that by adding volume effects a better agreement with experiment is obtained.
For this tutorial, we only used a 4x4x4 cell since larger cells would be already quite time-consuming, but for the converged 5x5x5 cell both curves should look slightly worse compared to experiment. A discrepancy between experiment and theory is expected, since the electron exchange and correlation are not sufficiently described within PBE which was used in this example. To get a really excellent agreement one needs to use the GW approximation .

Strictly speaking, the correct way to add volume effects to electron-phonon interactions would be to first change the volume for each temperature and then calculate the electron-phonon interaction for that temperature. In this tutorial and also in reference , it is done the other way around. Hence the electron-phonon interactions need to be calculated only once. In reference we observed that the two approaches give very similar results.

## References

## Download

EPC cd-C.tgz

Overview > Band gap renormalization in diamond using one-shot method > List of tutorials
