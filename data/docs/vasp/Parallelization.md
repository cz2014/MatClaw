# Category:Parallelization

Categories: VASP, Performance

VASP makes use of parallel machines splitting the calculation into many tasks, that communicate with each other using MPI.
Since a single core cannot perform enough operations, for many complex problems, this parallelization is necessary to finish the calculation in a reasonable time.

## Theory

### Basic parallelization

By default, VASP distributes the number of bands (NBANDS) over the available MPI ranks. But it is often beneficial to add parallelization of the FFTs (NCORE), parallelization over **k** points (KPAR), and parallelization over separate calculations (IMAGES). All these tags default to 1 and divide the number of MPI ranks among the parallelization options. Additionally, there are some parallelization options for specific algorithms in VASP, e.g., NOMEGAPAR. In summary, VASP parallelizes with

:   :   $$\text{total ranks} = \text{ranks parallelizing bands} \times \text{NCORE} \times \text{KPAR} \times \text{IMAGES} \times \text{other algorithm-dependent tags}.$$

In addition to the parallelization using MPI, VASP can make use of OpenMP threading and/or OpenACC (for the GPU port). Note that running on multiple OpenMP threads and/or GPUs switches off the NCORE parallelization.

### Communication patterns

The aforementioned parallelization levels directly map onto MPI communicators. Initially, VASP divides all available ranks into IMAGES equally-sized images. Setting KPAR splits each of these images further into groups of **k** points. Properties involving all **k** points (e.g. density, Fermi energy) require then a communication over these **k**-point groups. VASP divides the **k**-point group into band groups of size NCORE. The band group parallelizes the FFTs and triggers the most frequent communications. To evaluate properties involving multiple bands (e.g. Hamiltonian, orthonormalization) communication between the band groups occurs.

### MPI setup

The MPI setup determines the placement of the ranks onto the nodes. VASP assumes the ranks first fill up a node before the next node is occupied. As an example when running with 20 ranks on two nodes, VASP expects rank 1–10 on node 1 and rank 11–20 on node 2. If the ranks are placed differently, communication between the nodes occurs for every parallel FFT. Because FFTs are essential to VASP's speed, this deteriorates the performance of the calculation. A manifestation is an increase in computing time when the number of nodes is increased from 1 to 2. If NCORE is not used this issue is less severe but will still reduce the performance.

To address this issue, please check the setup of the MPI library and the submitted job script. It is usually possible to overwrite the placement by setting environment variables or command-line arguments. When in doubt, contact the HPC administration of your machine to investigate the behavior.

### File handling

When VASP is started it reads the file INCAR in the root directory.
Because the MPI setup needs to happen early in the general setup of the calculation the following tags are processed before any of the other settings:
NCORE\_IN\_IMAGE1, IMAGES, KPAR, NCORE, NPAR, NCSHMEM, LUSENCCL.
When IMAGES are used, subsequently any input given in the root directory is superseded by the same file in subdirectories 01, 02, ...
Any file not present in these subdirectories will be read from the root directory.
The output files are always written to the subdirectories.

### Terminology in high-performance computing (HPC)

CPU
:   The central processing unit of a computer. A CPU may consist of multiple *cores*. One or more CPUs can be combined with accelerators like *GPUs* to form a *node*. Desktop computers typically contain a single CPU.

GPU
:   The graphical processing unit. A GPU is very efficient at matrix and vector operations and may accelerate a program by transferring particularly suitable tasks from the *CPU* to the GPU.

Core
:   When a *CPU* has the option to execute multiple tasks in parallel, we refer to this as a multi-core CPU. Because these computational cores are physically close, they typically exhibit a fast communication between them.

Node
:   The node constitutes a physical entity consisting of one or more *CPUs* potentially accelerated by *GPUs*. The communication between nodes is much slower compared to the communication within a single node.

NUMA (Non-Uniform Memory Access) domain
:   these are distinct regions within a computer system where each core or group of cores has its own local memory that can be accessed faster than memory connected to other cores. In a NUMA architecture, memory access times vary depending on the proximity of the memory to the CPU core requesting it — local memory access is quicker, while remote access across domains incurs latency.

Socket
:   *Processes* communicate via sockets. Each socket corresponds to an endpoint in this communication.

Process
:   A process is a program executing on one or more *cores*. Multiple processes may distribute work via communication. Each process may spawn multiple *threads* to execute their task.

OpenMP thread
:   These threads live on a single *node*. *Processes* can instantiate these threads for loops or other parallel tasks.

Message Passing Interface (MPI)
:   A communication protocol to facilitate parallel execution of multiple *processes*. The *processes* send messages among them to synchronize parallel tasks when necessary.

Rank
:   Each rank corresponds to one *process* participating in the *MPI* communication. These ranks determine which particular task a *process* works on and identify senders and receivers of messages.

Memory
:   *Processes* store the data they work on in the dynamic random access memory (DRAM) or random access memory (RAM). From there it propagates to the execution *cores* via the *cache*.

Cache
:   The cache is physically much closer to the *CPU* than the *memory*. Therefore, data is moved from the *memory* to the cache before processing.

> **Warning:** The terminology of nodes, cores, CPUs, threads, etc. is not universal. For instance, some refer to a single core as a CPU, others refer to an entire node as a CPU.

> **Tip:** There is a lecture on high-performance computing (HPC) in VASP available on our YouTube channel.

## How to

### Optimizing the parallelization

The performance of a specific parallelization depends on the system, i.e., the number of ions, the elements, the size of the cell, etc.
Different algorithms (density-functional theory, many-body perturbation theory, or molecular dynamics) require a separate optimization of the parallel setup.
To obtain publishable results, many projects require performing many similar calculations, i.e., calculations with similar input and using the same algorithms.
Therefore, we recommend optimizing the parallelization to make the most of the available compute time. This optimization process depends greatly on the hardware and compiler toolchain on which you run your calculation. Hence, make sure to verify your setup when switching one of these.

> **Tip:** Run a few test calculations varying the parallel setup and use the optimal choice of parameters for the rest of the calculations.

For more detailed advice, check the following:

* How to optimize the parallelization in a nutshell

### OpenMP/OpenACC

Both OpenMP and OpenACC parallelize the FFTs and therefore disregard any conflicting specification of NCORE.
When combining these methods OpenACC takes precedence but any code not ported to OpenACC benefits from the additional OpenMP threads.
This approach is relevant because the recommended NVIDIA Collective Communications Library requires a single MPI rank per GPU.
Learn more about the OpenMP and OpenACC parallelization in these sections

* How to parallelize with multiple OpenMP threads per MPI rank
* How to run on GPUs

## Additional parallelization options

KPAR
:   For Laplace transformed MP2 this tag has a different meaning.

NCORE\_IN\_IMAGE1
:   Defines how many ranks work on the first image in the thermodynamic coupling constant integration (VCAIMAGES).

NOMEGAPAR
:   Parallelize over imaginary frequency points in $GW$ and RPA calculations.

NTAUPAR
:   Parallelize over imaginary time points in $GW$ and RPA calculations.
