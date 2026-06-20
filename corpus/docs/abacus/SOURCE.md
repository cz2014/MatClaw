# ABACUS documentation corpus — source & provenance

Complete verbatim mirror of the ABACUS documentation tree (`docs/`) from upstream, for the
agent to grep when writing ABACUS `INPUT`/`STRU`/`KPT` decks or using any ABACUS feature.

- **Upstream:** https://github.com/deepmodeling/abacus-develop (`docs/`)
- **Commit:** `30db3a4` (pulled 2026-06-19)
- **License:** ABACUS is LGPL-3.0; these docs are redistributed under their original license.
  This is a verbatim mirror, not a derivative work.
- **Re-sync:**
  ```
  git clone --depth 1 --filter=blob:none --sparse https://github.com/deepmodeling/abacus-develop t
  ( cd t && git sparse-checkout set docs )
  rsync -am --include='*/' --include='*.md' --include='*.rst' --exclude='*' t/docs/ corpus/docs/abacus/
  ```

**Entry points:** `index.rst` (doc tree); `advanced/input_files/input-main.md` (full INPUT
keyword reference); `advanced/input_files/{stru,kpt}.md`; `advanced/scf/spin.md` (magnetism);
`advanced/elec_properties/Mulliken.md` (`out_mul`); `advanced/pp_orb.md` (pseudo+orbital, LCAO).
