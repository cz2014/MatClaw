# IFC_ASR

Categories: INCAR tag, Electron-phonon interactions

IFC\_ASR = [integer]  
 Default: **IFC\_ASR** = 1

Description: If positive, enforces the acoustic sum rule on the interatomic force constants during an electron-phonon calculation.

> **Mind:** Available as of VASP 6.5.0

---

The matrix of interatomic force constants (IFC) should obey the so-called acoustic sum rule (ASR).
However, due to numerical inaccuracies, it is possible that the ASR is slightly broken in practice.
In such cases, the phonons obtained from the Fourier interpolation of the IFC matrix can become imaginary.

By setting `IFC_ASR > 0`, the ASR is explicitly enforced on the IFC matrix via an iterative scheme.
The number of iterations is also given by IFC\_ASR.

> **Mind:** `IFC_ASR = -2` has a special meaning. Usually, the IFC matrix is forced to be symmetric. However, if `IFC_ASR = -2`, then the IFC matrix is neither forced to be symmetric nor is the ASR applied. We do not recommend to use this setting.

## Related tags and articles

* ELPH\_RUN
* ELPH\_IGNORE\_IMAG\_PHONONS
