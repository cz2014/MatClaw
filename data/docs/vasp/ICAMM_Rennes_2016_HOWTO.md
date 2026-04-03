# ICAMM Rennes 2016 HOWTO

Here is a brief tutorial on how to run a calculation and how to run post-treatment tools during the VASP training school in Rennes.

* **First thing to do**:

:   - launch terminal:
:   go to **openSUSE** booklet (down left of the screen), select **Système** and choose **Terminal**
:   - source the environment via the following command:
:   `source /etc/bash.bashrc`
:   - export the proper LC\_NUMERIC environment using the following command:
:   `export LC_NUMERIC="en_US.UTF-8"`
:   - execute to following command:
:   `/bin/bash`

* **VASP calculations**:

:   :   3 versions of the VASP code are available:

:   - the so-called *standard* version which allows you to make *standard* calculation with several K-points
:   To use it, enter the following command on a terminal

:   `vasp_std`

:   - the so-called *non-colinear* version which allows you to make *non-colinear* calculation with several K-points
:   To use it, enter the following command on a terminal

:   `vasp_ncl`

:   - the so-called *gamma* version which allows you to make *gamma* calculation but with only 1 K-point
:   To use it, enter the following command on a terminal

:   `vasp_gam`

:   **Please always keep in mind that our local workstation are quite limited so please avoid to run two VASP calculations simultaneously.**

* **wannier90**

:   To use wannier90, use the following command:
:   `/ICAMM/wannier/wannier90-1.2/wannier90.x`

* **phonopy**

:   To use phonopy, use the following command:
:   `phonopy`

* **Gnuplot**:

:   Gnuplot is a portable command-line driven graphing utility.
:   To use it, enter the following command on a terminal

:   `gnuplot`

:   For more infos about gnuplot, visit the following website

* **p4vasp**:

To use the p4vasp visualization software, use the following command:

:   `p4v`

* **vmd**:

To use the vmd visualization software, use the following command:

:   `vmd`
