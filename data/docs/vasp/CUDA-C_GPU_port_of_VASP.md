# CUDA-C GPU port of VASP

Categories: VASP, Performance, GPU, Installation

> **Warning:** As of VASP.6.3.0, the CUDA-C GPU port of VASP is deprecated. Switch to the OpenACC GPU port of VASP.

Several core algorithms of VASP have been ported to run on GPU-accelerated hardware (as of VASP.5.4.1.05Feb16).

Explicity ported to run on GPU-accelerated hardware

* Electronic minimisation: the blocked-Davidson and RMM-DIIS algorithms (ALGO= Normal, Fast, and VeryFast).
* Hybrid functionals: the action of the Fock-exchange potential on the wave functions (LHFCALC=.TRUE.).

Unsuported (for now)

* LREAL=.FALSE. is currently unsuported . The GPU port of VASP requires the use of real-space-projection operators (i.e., LREAL= Auto | .TRUE.).
* LCALCEPS=.TRUE.
* NCORE ≠ 1 (or equivalently: NPAR ≠ *#of-MPI-ranks* / KPAR) is not supported at the moment. The GPU port of VASP requires NCORE=1 (default).
* Using scaLAPACK for the orthonormalization of the wave functions is not supported by the GPU port of VASP. Actually, this particular operation has been ported to the GPU (just not by means of scaLAPACK). If you have compiled your code with `-DscaLAPACK` you have to set:

```
LSCAAWARE = .FALSE.
```

:   in your INCAR to avoid the use of scaLAPACK for the orthonormalization of the wave functions.

* The gamma-only version of VASP has not been ported to GPU (yet).

**N.B.**: The GPU port of VASP is freely available to VASP5-licensees.

## Hardware/Software requirements

### Hardware requirements

Required GPU Architecture is Kepler or newer:

* Tesla K40 or Tesla K80, with 12 and 24 GB memory respectively, are strongly recommended
* Tesla K20 and Tesla K20X, with 5 GB and 6 GB respectively, may run out of memory on larger problems

### Recommended software stack

* CUDA toolkit, newer is better but anything >=6.5 should work

## Usage

### Building

* See Installing VASP and do not forget the patch(es).

### Running

## People

The GPU port of VASP only exist because of the excellent work of the following people:

* Maxwell Hutchinson (University of Chicago) and Mike Widom (Carnegie Mellon)
* Xavier Rozanska and Paul Fleurat-Lessard (ENS-Lyon)
* Mohamed Hacene, Ani Anciaux-Sedrakian, Diego Klahr, and Thomas Guignon (IFPEN)
* Jeroen Bedorf, Przemyslaw Tredak, Dusan Stosic, Arash Ashari, Paul Springer, Darko Stosic, Christoph Angerer, and Sarah Tariq (NVIDIA)

## Publications

* *Accelerating VASP Electronic Structure Calculations Using Graphic Processing Units*, M. Hacene *et al.*, J. Comput. Chem. 33, 2581 (2012).
* *VASP on a GPU: Application to exact-exchange calculations of the stability of elemental boron*, M. Hutchinson and W. Widom, Comput. Phys. Comm. 183, 1422 (2012).
* *Electronic Structure Calculations on Graphics Processing Units: From Quantum Chemistry to Condensed Matter Physics*, Ross Walker and Andreas Goetz (Editors), John Wiley & Sons, Inc., UK.
* *Speeding up plane-wave electronic-structure calculations using graphics-processing units*, S. Mainz *et al.*, Comput. Phys. Comm. 182, 1421 (2011).

## Additional information

* The presentation at SC15 by GPU developer Max Hutchinson.
* GTC 2013 audio & video presentation on the development of GPU-accelerated VASP.
* Dr. Peter Larsson's blog (National Supercomputer Centre at Linköping University, Sweden).

## Related Tags and Sections

ALGO,
LHFCALC,
LREAL,
LCALCEPS,
Installing VASP

---
