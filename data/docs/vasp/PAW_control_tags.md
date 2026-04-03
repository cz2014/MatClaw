# PAW control tags

Categories: Projector-augmented-wave method, Howto

There are a few tags that control
the behavior of the PAW implementation.
The first one is LMAXPAW=*l*. This flag sets the maximum *l*-quantum number for
the evaluation of the on-site terms on the
radial support grids in the PAW method. The default for LMAXPAW is
$2\*l\_{max}$, where $l\_{max}$ is the maximum angular
quantum number of the partial waves.
A useful setting for this tag is for instance LMAXPAW=0. In this case, only spherical terms are evaluated on the
radial grid. This does not mean that a-spherical terms
are totally neglected, because the compensation charges
are always expanded up to $2\*l\_{max}$ on the plane wave
grid.

For LMAXPAW=-1, no on-site correction terms are evaluated on the radial
support grid, which effectively means that the
behavior of US-PP's is recovered with PAW input datasets.
Usually this allows very efficient and fast calculations,
and this switch might be of interest for relaxations
and molecular dynamics runs. Energies should be evaluated
with the default setting for LMAXPAW.

An additional tag LMAXMIX=*l* controls up to which *l* quantum number the on-site PAW
charge densities are passed through the charge density mixer and written
to the CHGCAR file.

The default is LMAXMIX}=2. Higher l-quantum numbers are usually **not**
handled by the mixer, i.e. a straight mixing is applied for them
(the PAW on-site charge density for higher l quantum numbers is reset precisely
to the value corresponding to the present orbitals). Usually,
it is not required to increase LMAXMIX, but the following two cases
are exceptions:

* L(S)DA+U calculations require in many cases an increase of LMAXMIX to 4 (or 6 for f-elements) in order to obtain fast convergence to the groundstate.
* The CHGCAR file also contains only information up to LMAXMIX for the on-site PAW occupancy matrices. When the CHGCAR file is read and kept fixed in the course of the calculations (ICHARG=11), the results will be necessarily not identical to a self-consistent run. The deviations can be (or actually are) large for L(S)DA+U calculations. For the calculation of band structures within the L(S)DA+U approach it is strictly required to increase LMAXMIX to 4 (d elements) and 6 (f elements).

The second switch, that is useful in the context of the
PAW method (and US-PP) is ADDGRID.
The default is ADDGRID=*.FALSE.*. If ADDGRID=*.TRUE.* is written in the INCAR file, an additional (third) support grid is
used for the evaluation of the augmentation charges. This
third grid contains 8 times more points than the fine
grid NGXF, NGYF, NGZF.
Whenever terms involving augmentation charges are evaluated, this
third grid is used.
For instance: The augmentation charge is evaluated first
in real space on this fine grid, FFT-transformed to reciprocal space
and then added to the total charge density on the
grid NGXF, NGYF, NGZF.
The additional grid helps to reduce the noise in the forces significantly.
In many cases, it even allows to perform calculations in which
NGXF=NGX etc. This can be achieved by setting
ENAUG = 1 and ADDGRID=*.TRUE.* in the INCAR file. The flag can also be used for US-PPs,
in particular, to reduce the noise in the forces.
