# Optimizing the parallelization

Categories: Parallelization, Howto

To find the optimal parallelization setup of a VASP calculation, it is necessary to run tests for each system, algorithm and computer architecture. Below, we offer general advice on how to optimize the parallelization.

## Optimizing the parallelization

For repetitive tasks, **a few iterations estimate the performance** of the full calculation very well.
For example, run only a few electronic or ionic self-consistency steps (without reaching full convergence).
Compare the time various parallelization setups need to perform these few iterations.

Try to **get as close as possible to the actual system**.
Specifically, use the same or a very similar physical system (atoms, cell size, cutoff, ...);
run on the target computational hardware (CPUs, interconnect, number of nodes, ...).
If too many parameters are different, the parallel configuration may not be transferable to the production calculation.

In our experience, the best performance is achieved by **combining multiple parallelization options** because the parallel efficiency of each level drops near its limit.
By default, the number of bands (NBANDS) are distributed over the available MPI ranks.
But it is often beneficial to add parallelization of the FFTs (NCORE), parallelization over **k** points (KPAR), and parallelization over separate calculations (IMAGES).
Additionally, there are some parallelization options for specific algorithms in VASP, e.g., NOMEGAPAR for parallelization over imaginary frequency points in $GW$ and RPA calculations. In summary, **VASP parallelizes with**

:   :   $$\text{total ranks} = \text{ranks parallelizing bands} \times \text{NCORE} \times \text{KPAR} \times \text{IMAGES} \times \text{other algorithm-dependent tags}.$$

To optimize the parallelization, follow this recipe:

### Step 1: list of the relevant parallelization INCAR tags

:   **Create a list of the relevant parallelization INCAR tags** for the specific calculation. **Read the documentation for each of the relevant tags** to understand the limits and reasonable choices.

### Step 2: Dry run

:   For any calculation involving electronic minimization, it can be useful to first **run VASP with ALGO=*None*** set in the INCAR file or with the command-line argument --dry-run. With ALGO=*None* the computational setup for the electronic minimization is done without actually performing the minimization. For instance, the FFTs are planned, and the irreducible **k** points of the first Brillouin zone are constructed. Therefore, some parameters, e.g., the default number of Kohn-Sham orbitals (NBANDS) and the total number of plane waves, are written to the OUTCAR file while using barely any computational time.

### Step 3: Test candidate parallelization

:   Combine the information from the documentation and the dry run into a few possible candidates for a reasonable setup. **Run test calculations** on a subset of the production run e.g. by reducing the number of steps.

### Step 4: Use best performing parallelization

:   Run the production calculation with the best performing setup.

## Tips to parallelize electronic minimization

For the common case of electronic minimization calculations, the following rules of thumb apply:

* Aim to set the number of ranks to the default value of NBANDS divided by a small integer. Note that the number of bands (NBANDS) is increased to accommodate the number of ranks.
* Choose NCORE as a factor of the cores per node to avoid communicating between nodes for the FFTs. Mind that NCORE cannot be set with OpenMP threading and/or the OpenACC GPU port. Use the number of OpenMP threads in this case to for fine grained control over parallelization.
* The **k**-point parallelization is efficient but requires additional memory. Given sufficient memory, increase KPAR up to the number of irreducible **k** points. Keep in mind that KPAR should factorize the number of **k** points. This is especially important to reduce MPI communication between NUMA domains and compute nodes. Read also KPAR for more information.

> **Tip:** If the number of **k** points is a prime number (or does not factorize well), copy the IBZKPT file to KPOINTS and add zero-weigthed points.

* For bulk systems with small unit cells (NBANDS is small, NKPTS=no of k points is large), `NCORE = 1` and `KPAR = NKPTS` is optimal.
* Lookout for the **LOOP** timer for each electronic minimization step, and the overall **LOOP+** timer that includes all electronic minimization steps plus post-processing like forces.
* For running on GPUs:
  + MPI ranks = no of GPUs
  + `KPAR = no of GPUs` if memory allows
  + OpenMP threading can be quite important for the parts that still run on the host, because usually no of GPUs is rather small.
  + NSIM controls how many orbitals are worked on in parallel. For GPUs the default value of 4 is way too small. Increase the value. Values as large as `NSIM = 32` might be beneficial.
  + small systems might perform very poorly in standard DFT (this is different for hybrid, GW, or BSE calculations). GPUs show their benefit when there are many bands or ions over which the code is parallelized.
* Finally, use the IMAGES tag to split several VASP runs into separate calculations. The limit is dictated by the number of desired calculations.

## Understanding the hardware

Optimizing the parallel execution depends greatly on the hardware architecture, network topology for MPI communication, and compiler / library toolchain. Hence, it is a good start to first get familiar with the computer system you are working with, i.e., look out for specific documentation of your high-performance computing (HPC) center for submitting jobs. Keywords to look out for might be: *submitting jobs*, *distribution and binding*, *MPI rank and thread binding*, *rank / thread affinity*, *hybrid MPI and OpenMP* etc. Usually, HPC facilities put great work in optimizing the computer system in a very special way and one has to follow their recommendations to get the most out of the compute resources.

Each hardware setup is unique since nowadays CPUs and GPUs alike consists not of a single monolithic core anymore. Each processor might consist of multiple tiles or domains that each are connected to their own memory. To leverage the full potential of the hardware one has to reduce communication between cores that are "far away" from each other. To understand this better the concept of NUMA (Non-Uniform Memory Access) domains is useful. In NUMA architecture, memory access times vary depending on the proximity of the memory to the CPU core requesting it — local memory access is quicker, while remote access across domains incurs latency. Modern multi-socket and multi-core systems use NUMA to improve scalability and performance by keeping data close to the cores that use it most often. Understanding and managing NUMA domains is essential for optimizing memory placement and parallel performance in HPC.

Fig. 1: Example output of `lstopo` command for an AMD Epyc 7543 processor. The processor consists of multiple hardware tiles that display as 4 distinct NUMA domains. Disclaimer: This is an example and not a general hardware recommentation.

Fig. 1 displays the NUMA architecture of an AMD Epyc 7543 processor. In total this processor has 512 GB of system memory available. However, this memory is spread across 4 NUMA nodes (pink bars). Each NUMA domain consists of 8 physical CPU cores (each able to work on 2 threads, i.e. P#0/P#32 belong to the same physical core). These domains share not only a chunk of the system memory, but also their own L3 cache. Hence, it is important for this specific processor that not more than 8 cores work on a specific task. If more cores work on the same memory they have to communicate to the other NUMA domains with some latency. This is important for choosing parallelization tags. Hence, we know now that 8 cores is a good work-group size for VASP on this processor, and that up to 32 cores can work on the same memory with a small penalty. If we use more than 32 cores, we have to communicate between two different processors (nodes / sockets) via a different protocol (MPI); much higher latency. If the tool `lstopo` is not available on your system, you can use the command `numactl --hardware` to get text output of the same information:

```
# numactl --hardware
available: 4 nodes (0-3)
node 0 cpus: 0 1 2 3 4 5 6 7 32 33 34 35 36 37 38 39
node 0 size: 128262 MB
node 1 cpus: 8 9 10 11 12 13 14 15 40 41 42 43 44 45 46 47
node 1 size: 129018 MB
node 2 cpus: 16 17 18 19 20 21 22 23 48 49 50 51 52 53 54 55
node 2 size: 129018 MB
node 3 cpus: 24 25 26 27 28 29 30 31 56 57 58 59 60 61 62 63
node 3 size: 129003 MB
node distances:
node   0   1   2   3 
 0:  10  12  12  12 
 1:  12  10  12  12 
 2:  12  12  10  12 
 3:  12  12  12  10
```

Another point that immediately follows from the concept of NUMA domains is that MPI ranks should not jump between NUMA domains. They would loose access to their previous cache. To avoid this one uses *pinning* or *binding* of MPI ranks. This becomes also important for combining MPI with OpenMP threading. Threads should live close to their parent rank and also not move to share the same caches, i.e. live in the same NUMA domain. Binding ranks and threads to specific cores or regions depends on the software setup. For example in the popular SLURM jobscript submission system this is done via the flag `--cpu-bind=cores` , for openmpi this is done via `--bind-to=core`, and for intel MPI via `-genv I_MPI_PIN=ON`. To bind threads use the environment variable `OMP_PROC_BIND` and set it to `true` or `close`. For threads it is also important to tell them where they should run via `OMP_PLACES`, which best is set to `cores`.

In summary, to leverage the potential of this hardware in the best way, we want to have groups of 8 cores work as independent as possible. Hence, we should choose NBANDS, and the number of **k**-points in the IBZ such that they can be divided by 8. Then, we will find a good setting with `NCORE = 8` and `KPAR = 4` (or 4 times the number of compute nodes with this processor you have).

For benchmarking, start with this settings. Then, try to change the parallelization tags and observe how performance changes.

## Related tags an articles

Parallelization

NCORE, KPAR, IMAGES
