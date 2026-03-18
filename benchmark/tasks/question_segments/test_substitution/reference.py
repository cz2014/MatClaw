"""Reference solution for test_substitution.
Source: test_core.py, lines 32-114
"""

from pathlib import Path

from pymatgen.analysis.defects.core import (
    Adsorbate,
    DefectComplex,
    Interstitial,
    NamedDefect,
    PeriodicSite,
    Substitution,
    Vacancy,
)
from pymatgen.analysis.defects.finder import DefectSiteFinder
from pymatgen.core import Structure
from pymatgen.core.periodic_table import Element, Specie
import numpy as np

# --- Fixture setup ---

# test_dir
test_dir = Path("/Users/cz/Work/MatTools_temp/src/tool_source_code/pymatgen-analysis-defects/tests/test_files")

# gan_struct
gan_struct = Structure.from_file(test_dir / "GaN.vasp")

# --- Reference test code ---

s = gan_struct.copy()
n_site = s.sites[3]
assert n_site.specie.symbol == "N"
o_site = PeriodicSite(Specie("O"), n_site.frac_coords, s.lattice)
o_site2 = PeriodicSite(Specie("O"), s.sites[2].frac_coords, s.lattice)
sub = Substitution(s, o_site)
sub2 = Substitution(s, o_site2)
assert sub == sub2  # symmetry equivalent sites
assert str(sub) == "O subsitituted on the N site at at site #3"
assert sub.oxi_state == 1
assert sub.get_charge_states() == [-1, 0, 1, 2]
assert sub.get_multiplicity() == 2
sc, site_ = sub.get_supercell_structure(return_site=True)
assert site_.specie.symbol == "O"
assert sc.formula == "Ga64 N63 O1"
assert sub.name == "O_N"
assert sub.latex_name == r"O$_{\rm N}$"
assert sub == sub
assert sub.element_changes == {Element("N"): -1, Element("O"): 1}
assert sub.latex_name == r"O$_{\rm N}$"

# test supercell with locking
sc_locked = sub.get_supercell_structure(relax_radius=5.0)
free_sites = [
    i
    for i, site in enumerate(sc_locked)
    if site.properties["selective_dynamics"][0]
]

finder = DefectSiteFinder()
fpos = finder.get_defect_fpos(sc_locked, sub.structure)
cpos = sc_locked.lattice.get_cartesian_coords(fpos)
free_sites_ref = sc_locked.get_sites_in_sphere(cpos, 5.0, include_index=True)
free_sites_ref = [site.index for site in free_sites_ref]
free_sites_union = set(free_sites_ref) | set(free_sites)
free_sites_intersection = set(free_sites_ref) & set(free_sites)
assert len(free_sites_intersection) / len(free_sites_union) == 1.0

# test perturbation
sc_locked = sub.get_supercell_structure(relax_radius=5.0, perturb=0.0)
free_sites_ref2 = sc_locked.get_sites_in_sphere(cpos, 5.0, include_index=True)
free_sites_ref2 = [site.index for site in free_sites_ref2]
assert set(free_sites_ref2) == set(free_sites_ref)

# test for user defined charge
dd = sub.as_dict()
dd["user_charges"] = [-100, 102]
sub_ = Substitution.from_dict(dd)
assert sub_.get_charge_states() == [-100, 102]

dd["user_charges"] = []  # empty list == None => use oxidation state info
sub_ = Substitution.from_dict(dd)
assert sub_.get_charge_states() == [-1, 0, 1, 2]

# test target_frac_coords with get_supercell_structure
sub_sc_struct = sub.get_supercell_structure()
finder = DefectSiteFinder()
fpos = finder.get_defect_fpos(sub_sc_struct, sub.structure)
assert np.allclose(fpos, [0.1250, 0.0833335, 0.18794])
# change target coords:
sub_sc_struct = sub.get_supercell_structure(target_frac_coords=[0.3, 0.5, 0.9])
fpos = finder.get_defect_fpos(sub_sc_struct, sub.structure)
assert np.allclose(fpos, [0.375, 0.5833335, 0.68794])  # closest equivalent site

# test oxidation state setting for substitutional defects when substitution is an antisite:
# from pymatgen.analysis.defects.generators import AntiSiteGenerator
ga_site = s.sites[0]
assert ga_site.specie.symbol == "Ga"
n_site = PeriodicSite(Specie("N"), ga_site.frac_coords, s.lattice)
n_ga = Substitution(s, n_site)
assert n_ga.get_charge_states() == [-7, -6, -5, -4, -3, -2, -1, 0, 1]

# test also works fine when input structure does not have oxidation states:
s.remove_oxidation_states()
ga_site = s.sites[0]
assert ga_site.specie.symbol == "Ga"
n_site = PeriodicSite(Element("N"), ga_site.frac_coords, s.lattice)
n_ga = Substitution(s, n_site)
assert n_ga.get_charge_states() == [-7, -6, -5, -4, -3, -2, -1, 0, 1]

n_ga.user_charges = [-100, 102]
assert n_ga.get_charge_states() == [-100, 102]
