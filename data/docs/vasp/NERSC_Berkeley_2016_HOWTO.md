# NERSC Berkeley 2016 HOWTO

* **The examples**:

:   * can be copied from:

```
/project/projectdirs/training/www/VASPWorkshop2016/exercises
```

:   * or may be downloaded from the workshop wiki page.

* **Running the examples**:

:   Almost all examples come with a bash-script that runs them. These scripts are called *job.sh*, *doall.sh*, *loop.sh*, *run.sh* or something original like that.
:   To submit these jobscripts to the Haswell nodes on Cori you may do the following:

    * Copy the files hsw.sl and sub.sh to the directory where you want to run the example:

```
cd path-to-your-directory
cp /project/projectdirs/training/www/VASPWorkshop2016/exercises/hsw.sl .
cp /project/projectdirs/training/www/VASPWorkshop2016/exercises/sub.sh .
```

:   * To submit for instance the jobscripts *run.sh*, you specify:

```
./sub.sh run.sh
```

* **hsw.sl**

:   The file hsw.sl contains the slurm-preamble, loads the relevant environment modules, and sets the command with which VASP will be called by the jobscript:

```
#!/bin/bash -l
#SBATCH -N 1
#SBATCH -p regular
#SBATCH -t 30:00
#SBATCH -C haswell

export OMP_NUM_THREADS=4
export OMP_PROC_BIND=spread
export OMP_PLACES=threads

module use ~usgsw/modulefiles
module load vasp/20161102-hsw

export vasp_std="srun -n 4 -c 16 --cpu_bind=cores /global/homes/u/usgsw/vasp/20161102/hsw/intel/bin/vasp_std"
```

:   In this case hsw.sl requests 1 Haswell node (32 cores), and the vasp\_std command will run VASP using 4 MPI-ranks, that each will be able to start 4 openMP-threads.

* **sub.sh**

:   The bash-script sub.sh does very little but concatenate hsw.sl and a call to the jobscript specified as its argument, and submits the result (sub.sl):

```
#!/bin/bash -l

cat ./hsw.sl > sub.sl
echo ./$1   >> sub.sl

sbatch sub.sl
```

:   To be specific, the command

```
./sub.sh run.sh
```

:   will submit the following sub.sl file:

```
#!/bin/bash -l
#SBATCH -N 1
#SBATCH -p regular
#SBATCH -t 30:00
#SBATCH -C haswell

export OMP_NUM_THREADS=4
export OMP_PROC_BIND=spread
export OMP_PLACES=threads

module use ~usgsw/modulefiles
module load vasp/20161102-hsw

export vasp_std="srun -n 4 -c 16 --cpu_bind=cores /global/homes/u/usgsw/vasp/20161102/hsw/intel/bin/vasp_std"
./run.sh
```
