# HESSEMAT

Categories: Advanced molecular-dynamics sampling, Files

HESSEMAT defines the Hesse matrix in Cartesian coordinates ($\underline{\mathbf{H}}^\mathbf{x}$ ) for the use in Thermodynamic integration with harmonic reference.
For a system containing $N$ atoms, HESSEMAT has $(3N+1)(N+1)$ lines.
The first line specifies potential energy $V\_{0,\mathbf{x}}(\mathbf{x}\_0)$ (in eV) of the relaxed system for which $\underline{\mathbf{H}}^\mathbf{x}$ is computed.
The following $3N$ lines are reserved for positions in fractional coordinates of all atoms constituting the system, whereby each line should contain three components of position vector of a single atom. The remaining part of HESSEMAT consist of $3N$ block of $N+1$ lines each.
Each block contains information related to a single eigenmode of $\underline{\mathbf{H}}^\mathbf{x}$: the first line specified the eigenvalue (in eV/${\AA}^2$) and remaining and $N$ lines the corresponding eigenvector (in Cartesian coordinates) in a 3-column format.

How to run thermodynamic integration calculations is given here.

## Related tags and articles

TILAMBDA, REPORT
