# LAMMPS documentation corpus — source & provenance

Complete verbatim mirror of the LAMMPS manual source (`doc/src/`, reStructuredText) from
upstream — the entire command reference (all `pair_style`, `fix`, `compute`, `dump`, `region`,
... pages plus the howto/intro material) for the agent to grep when writing LAMMPS input
scripts + data files. Native `.rst`; figures (images) are omitted.

- **Upstream:** https://github.com/lammps/lammps (`doc/src/`)
- **Commit:** `c46bbef` (pulled 2026-06-19)
- **License:** LAMMPS is GPL-2.0; these docs are redistributed under their original license.
  This is a verbatim mirror, not a derivative work.
- **Re-sync:**
  ```
  git clone --depth 1 --filter=blob:none --sparse https://github.com/lammps/lammps t
  ( cd t && git sparse-checkout set doc/src )
  rsync -am --include='*/' --include='*.rst' --exclude='*' t/doc/src/ corpus/docs/lammps/
  ```

**Entry points:** `Commands_all.rst` (command index); `pair_*.rst` / `fix_*.rst` /
`compute_*.rst` / `dump.rst`; `read_data.rst` / `write_data.rst`; `minimize.rst`; `units.rst`;
`atom_style.rst`. (For the moire tasks: `pair_sw`, `pair_kolmogorov_crespi_full`, `pair_hybrid`.)
