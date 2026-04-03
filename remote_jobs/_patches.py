"""Monkey-patches for upstream bugs in atomate2/ASE.

These patches run on the remote HPC worker at import time.
Each patch is idempotent (safe to apply multiple times).
"""

import logging

logger = logging.getLogger(__name__)

_PATCHED: set[str] = set()


def patch_ase_relaxer_stale_arrays():
    """Fix KeyError in AseRelaxer.relax() when input structure has site properties.

    Bug: When a pymatgen Structure with forces/energies site properties is
    converted to ASE Atoms, the site properties become atoms.arrays entries.
    When the calculator produces its own results, ASE's save_calc_results()
    finds the keys already exist and raises KeyError.

    Fix: Wrap AseRelaxer.relax() to strip pre-existing calculator-result keys
    from write_atoms before the ase_write call.

    See atomate2_err.md for full analysis.
    Upstream: https://gitlab.com/ase/ase/-/issues/1464
    """
    if "ase_relaxer_stale_arrays" in _PATCHED:
        return
    _PATCHED.add("ase_relaxer_stale_arrays")

    try:
        from atomate2.ase.utils import AseRelaxer
    except ImportError:
        logger.debug("atomate2 not installed, skipping AseRelaxer patch")
        return

    _original_relax = AseRelaxer.relax

    def _patched_relax(self, atoms, *args, **kwargs):
        # Temporarily replace ase_write in the module namespace with a wrapper
        # that clears stale calculator-result keys before delegating to the
        # real write function.
        from ase import Atoms as _AtomsClass
        from ase.io import write as _real_ase_write

        import atomate2.ase.utils as _utils_module

        def _safe_ase_write(filename, images, *a, **kw):
            atoms_list = [images] if isinstance(images, _AtomsClass) else images
            for atom_obj in atoms_list:
                if atom_obj.calc is not None and hasattr(atom_obj.calc, "results"):
                    calc_keys = set(atom_obj.calc.results)
                    for key in list(atom_obj.arrays):
                        if key in calc_keys and key not in ("numbers", "positions"):
                            del atom_obj.arrays[key]
                    for key in list(atom_obj.info):
                        if key in calc_keys:
                            del atom_obj.info[key]
            return _real_ase_write(filename, images, *a, **kw)

        original_write = _utils_module.ase_write
        _utils_module.ase_write = _safe_ase_write
        try:
            return _original_relax(self, atoms, *args, **kwargs)
        finally:
            _utils_module.ase_write = original_write

    AseRelaxer.relax = _patched_relax
    logger.info("Patched AseRelaxer.relax() to strip stale site-property arrays")
