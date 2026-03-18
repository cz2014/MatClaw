"""Extract reference code from pymatgen-analysis-defects tests.

Generates a self-contained reference.py for each of the 49 benchmark tasks
by extracting the relevant test function and inlining fixture setup code.

Usage:
    python benchmark/tasks/extract_reference.py                  # all tasks
    python benchmark/tasks/extract_reference.py --task test_vacancy  # one task
    python benchmark/tasks/extract_reference.py --dry-run        # preview only
"""

import argparse
import ast
import textwrap
from pathlib import Path

MATTOOLS_TESTS = Path("/Users/cz/Work/MatTools_temp/src/tool_source_code/pymatgen-analysis-defects/tests")
DEST_DIR = Path(__file__).parent / "question_segments"
TEST_DIR_PATH = str(MATTOOLS_TESTS / "test_files")

# --- Task -> source file + function mapping ---

TASK_SOURCE_MAP = {
    # test_core.py
    "test_adsorbate": ("test_core.py", "test_adsorbate"),
    "test_vacancy": ("test_core.py", "test_vacancy"),
    "test_substitution": ("test_core.py", "test_substitution"),
    "test_interstitial": ("test_core.py", "test_interstitial"),
    "test_complex": ("test_core.py", "test_complex"),
    "test_parsing_and_grouping_NamedDefects": ("test_core.py", "test_parsing_and_grouping_NamedDefects"),
    # test_generators.py
    "test_vacancy_generators": ("test_generators.py", "test_vacancy_generators"),
    "test_substitution_generators": ("test_generators.py", "test_substitution_generators"),
    "test_antisite_generator": ("test_generators.py", "test_antisite_generator"),
    "test_interstitial_generator": ("test_generators.py", "test_interstitial_generator"),
    "test_charge_interstitial_generator": ("test_generators.py", "test_charge_interstitial_generator"),
    "test_voronoi_interstitial_generator": ("test_generators.py", "test_voronoi_interstitial_generator"),
    "test_generate_all_native_defects": ("test_generators.py", "test_generate_all_native_defects"),
    # test_supercells.py
    "test_supercells": ("test_supercells.py", "test_supercells"),
    "test_ase_supercells": ("test_supercells.py", "test_ase_supercells"),
    "test_closest_sc_mat": ("test_supercells.py", "test_closest_sc_mat"),
    # test_corrections.py
    "test_freysoldt": ("test_corrections.py", "test_freysoldt"),
    "test_kumagai": ("test_corrections.py", "test_kumagai"),
    # test_thermo.py
    "test_lower_envelope": ("test_thermo.py", "test_lower_envelope"),
    "test_defect_entry": ("test_thermo.py", "test_defect_entry"),
    "test_formation_energy_diagram_using_bulk_entry": ("test_thermo.py", "test_formation_energy_diagram_using_bulk_entry"),
    "test_formation_energy_diagram_shape_fixed": ("test_thermo.py", "test_formation_energy_diagram_shape_fixed"),
    "test_formation_energy_diagram_using_atomic_entries": ("test_thermo.py", "test_formation_energy_diagram_using_atomic_entries"),
    "test_formation_energy_diagram_numerical": ("test_thermo.py", "test_formation_energy_diagram_numerical"),
    "test_competing_phases": ("test_thermo.py", "test_competing_phases"),
    "test_multi": ("test_thermo.py", "test_multi"),
    "test_formation_from_directory": ("test_thermo.py", "test_formation_from_directory"),
    "test_ensure_stable_bulk": ("test_thermo.py", "test_ensure_stable_bulk"),
    "test_defect_entry_grouping": ("test_thermo.py", "test_defect_entry_grouping"),
    # test_finder.py
    "test_defect_finder": ("test_finder.py", "test_defect_finder"),
    # test_utils.py
    "test_get_local_extrema": ("test_utils.py", "test_get_local_extrema"),
    "test_cluster_nodes": ("test_utils.py", "test_cluster_nodes"),
    "test_get_avg_chg": ("test_utils.py", "test_get_avg_chg"),
    "test_chgcar_insertion": ("test_utils.py", "test_chgcar_insertion"),
    "test_topography_analyzer": ("test_utils.py", "test_topography_analyzer"),
    "test_get_localized_states": ("test_utils.py", "test_get_localized_states"),
    "test_group_docs": ("test_utils.py", "test_group_docs"),
    "test_plane_spacing": ("test_utils.py", "test_plane_spacing"),
    # test_recombination.py
    "test_boltzmann": ("test_recombination.py", "test_boltzmann"),
    "test_get_vibronic_matrix_elements": ("test_recombination.py", "test_get_vibronic_matrix_elements"),
    "test_pchip_eval": ("test_recombination.py", "test_pchip_eval"),
    "test_get_SRH_coef": ("test_recombination.py", "test_get_SRH_coef"),
    "test_get_Rad_coef": ("test_recombination.py", "test_get_Rad_coef"),
    # test_ccd.py
    "test_defect_band_raises": ("test_ccd.py", "test_defect_band_raises"),
    "test_HarmonicDefect": ("test_ccd.py", "test_HarmonicDefect"),
    "test_wswq_slope": ("test_ccd.py", "test_wswq_slope"),
    "test_SRHCapture": ("test_ccd.py", "test_SRHCapture"),
    "test_dielectric_func": ("test_ccd.py", "test_dielectric_func"),
    # plotting/test_thermo.py
    "test_fed_plot": ("plotting/test_thermo.py", "test_fed_plot"),
}

# --- Fixture setup code (inlined) ---
# Each fixture is a block of code that produces the named variable.
# Dependencies are listed so we can topologically sort.

FIXTURE_DEPS = {
    "test_dir": [],
    "gan_struct": ["test_dir"],
    "stable_entries_Mg_Ga_N": ["test_dir"],
    "defect_Mg_Ga": ["gan_struct"],
    "data_Mg_Ga": ["test_dir"],
    "defect_entries_and_plot_data_Mg_Ga": ["data_Mg_Ga", "defect_Mg_Ga"],
    "chgcar_fe3o4": ["test_dir"],
    "v_ga": ["test_dir"],
    "v_N_GaN": ["test_dir"],
    "basic_fed": ["data_Mg_Ga", "defect_entries_and_plot_data_Mg_Ga", "stable_entries_Mg_Ga_N"],
    # Local fixtures in test_ccd.py
    "hd0": ["v_ga"],
    "hd1": ["v_ga"],
    # Local fixture in test_thermo.py
    "formation_energy_diagram": ["data_Mg_Ga", "defect_entries_and_plot_data_Mg_Ga", "stable_entries_Mg_Ga_N"],
}

FIXTURE_CODE = {
    "test_dir": f'test_dir = Path("{TEST_DIR_PATH}")',

    "gan_struct": 'gan_struct = Structure.from_file(test_dir / "GaN.vasp")',

    "stable_entries_Mg_Ga_N": 'stable_entries_Mg_Ga_N = loadfn(test_dir / "stable_entries_Mg_Ga_N.json")',

    "defect_Mg_Ga": textwrap.dedent("""\
        ga_site = gan_struct[0]
        mg_site = PeriodicSite(Specie("Mg"), ga_site.frac_coords, gan_struct.lattice)
        defect_Mg_Ga = Substitution(gan_struct, mg_site)"""),

    "data_Mg_Ga": textwrap.dedent("""\
        root_dir = test_dir / "Mg_Ga"
        data_Mg_Ga = defaultdict(dict)
        for fold in root_dir.glob("./*"):
            if not fold.is_dir():
                continue
            data_Mg_Ga[fold.name] = {
                "vasprun": Vasprun(fold / "vasprun.xml.gz"),
                "locpot": Locpot.from_file(fold / "LOCPOT.gz"),
            }"""),

    "defect_entries_and_plot_data_Mg_Ga": textwrap.dedent("""\
        bulk_locpot = data_Mg_Ga["bulk_sc"]["locpot"]
        def _get_defect_entry_data(q):
            computed_entry = data_Mg_Ga[f"q={q}"]["vasprun"].get_computed_entry(inc_structure=True)
            defect_locpot = data_Mg_Ga[f"q={q}"]["locpot"]
            def_entry = DefectEntry(defect=defect_Mg_Ga, charge_state=q, sc_entry=computed_entry)
            frey_summary = def_entry.get_freysoldt_correction(
                defect_locpot=defect_locpot, bulk_locpot=bulk_locpot, dielectric=14
            )
            return def_entry, frey_summary
        defect_entries = dict()
        plot_data = dict()
        for qq in [-2, -1, 0, 1]:
            defect_entry, frey_summary = _get_defect_entry_data(qq)
            defect_entries[qq] = defect_entry
            plot_data[qq] = frey_summary.metadata["plot_data"]
        defect_entries_and_plot_data_Mg_Ga = (defect_entries, plot_data)"""),

    "chgcar_fe3o4": 'chgcar_fe3o4 = Chgcar.from_file(test_dir / "CHGCAR.Fe3O4.vasp")',

    "v_ga": textwrap.dedent("""\
        v_ga = dict()
        for q1, q2 in [(0, -1), (-1, 0)]:
            ccd_dir = test_dir / f"v_Ga/ccd_{q1}_{q2}"
            vaspruns = [Vasprun(ccd_dir / f"{i}/vasprun.xml") for i in [0, 1, 2]]
            wswq_dir = ccd_dir / "wswqs"
            wswq_files = sorted(
                [f for f in wswq_dir.glob("WSWQ*")],
                key=lambda x: int(x.name.split(".")[1])
            )
            wswqs = [WSWQ.from_file(f) for f in wswq_files]
            v_ga[(q1, q2)] = {
                "vaspruns": vaspruns,
                "procar": Procar(ccd_dir / "1/PROCAR"),
                "wswqs": wswqs,
            }"""),

    "v_N_GaN": textwrap.dedent("""\
        bulk_locpot_v_N = Locpot.from_file(test_dir / "v_N_GaN/bulk/LOCPOT.gz")
        v_N_GaN = {
            "bulk_locpot": bulk_locpot_v_N,
            "defect_locpots": {
                -1: Locpot.from_file(test_dir / "v_N_GaN/q=-1/LOCPOT.gz"),
                0: Locpot.from_file(test_dir / "v_N_GaN/q=0/LOCPOT.gz"),
                1: Locpot.from_file(test_dir / "v_N_GaN/q=1/LOCPOT.gz"),
                2: Locpot.from_file(test_dir / "v_N_GaN/q=2/LOCPOT.gz"),
            },
        }"""),

    "basic_fed": textwrap.dedent("""\
        bulk_vasprun_fed = data_Mg_Ga["bulk_sc"]["vasprun"]
        bulk_bs_fed = bulk_vasprun_fed.get_band_structure()
        vbm_fed = bulk_bs_fed.get_vbm()["energy"]
        bulk_entry_fed = bulk_vasprun_fed.get_computed_entry(inc_structure=False)
        defect_entries_fed, _ = defect_entries_and_plot_data_Mg_Ga
        def_ent_list_fed = list(defect_entries_fed.values())
        atomic_entries_fed = list(
            filter(lambda x: len(x.composition.elements) == 1, stable_entries_Mg_Ga_N)
        )
        pd_fed = PhaseDiagram(stable_entries_Mg_Ga_N)
        basic_fed = FormationEnergyDiagram.with_atomic_entries(
            defect_entries=def_ent_list_fed,
            atomic_entries=atomic_entries_fed,
            vbm=vbm_fed,
            inc_inf_values=False,
            phase_diagram=pd_fed,
            bulk_entry=bulk_entry_fed,
        )
        basic_fed.band_gap = 2"""),

    "hd0": textwrap.dedent("""\
        _vaspruns_hd0 = v_ga[(0, -1)]["vaspruns"]
        _procar_hd0 = v_ga[(0, -1)]["procar"]
        hd0 = HarmonicDefect.from_vaspruns(
            _vaspruns_hd0,
            charge_state=0,
            procar=_procar_hd0,
            store_bandstructure=True,
        )"""),

    "hd1": textwrap.dedent("""\
        _vaspruns_hd1 = v_ga[(-1, 0)]["vaspruns"]
        _procar_hd1 = v_ga[(-1, 0)]["procar"]
        hd1 = HarmonicDefect.from_vaspruns(
            _vaspruns_hd1,
            charge_state=1,
            procar=_procar_hd1,
            store_bandstructure=True,
        )"""),

    "formation_energy_diagram": textwrap.dedent("""\
        bulk_vasprun_fed = data_Mg_Ga["bulk_sc"]["vasprun"]
        bulk_bs_fed = bulk_vasprun_fed.get_band_structure()
        vbm_fed = bulk_bs_fed.get_vbm()["energy"]
        bulk_entry_fed = bulk_vasprun_fed.get_computed_entry(inc_structure=False)
        defect_entries_fed, _ = defect_entries_and_plot_data_Mg_Ga
        def_ent_list_fed = list(defect_entries_fed.values())
        atomic_entries_fed = list(
            filter(lambda x: len(x.composition.elements) == 1, stable_entries_Mg_Ga_N)
        )
        pd_fed = PhaseDiagram(stable_entries_Mg_Ga_N)
        # basic constructor with inc_inf_values=True
        fed_ = FormationEnergyDiagram(
            bulk_entry=bulk_entry_fed,
            defect_entries=def_ent_list_fed,
            vbm=vbm_fed,
            pd_entries=stable_entries_Mg_Ga_N,
            inc_inf_values=True,
        )
        # constructor with atomic entries (used for the rest of the tests)
        formation_energy_diagram = FormationEnergyDiagram.with_atomic_entries(
            defect_entries=def_ent_list_fed,
            atomic_entries=atomic_entries_fed,
            vbm=vbm_fed,
            inc_inf_values=False,
            phase_diagram=pd_fed,
            bulk_entry=bulk_entry_fed,
        )"""),
}

# --- Imports needed by each fixture ---

FIXTURE_IMPORTS = {
    "test_dir": {"from pathlib import Path"},
    "gan_struct": {"from pymatgen.core import Structure"},
    "stable_entries_Mg_Ga_N": {"from monty.serialization import loadfn"},
    "defect_Mg_Ga": {
        "from pymatgen.analysis.defects.core import PeriodicSite, Substitution",
        "from pymatgen.core.periodic_table import Specie",
    },
    "data_Mg_Ga": {
        "from collections import defaultdict",
        "from pymatgen.io.vasp.outputs import Vasprun, Locpot",
    },
    "defect_entries_and_plot_data_Mg_Ga": {
        "from pymatgen.analysis.defects.thermo import DefectEntry",
    },
    "chgcar_fe3o4": {"from pymatgen.io.vasp.outputs import Chgcar"},
    "v_ga": {"from pymatgen.io.vasp.outputs import WSWQ, Vasprun, Procar"},
    "v_N_GaN": {"from pymatgen.io.vasp.outputs import Locpot"},
    "basic_fed": {
        "from pymatgen.analysis.defects.thermo import FormationEnergyDiagram",
        "from pymatgen.analysis.phase_diagram import PhaseDiagram",
    },
    "hd0": {"from pymatgen.analysis.defects.ccd import HarmonicDefect"},
    "hd1": {"from pymatgen.analysis.defects.ccd import HarmonicDefect"},
    "formation_energy_diagram": {
        "from pymatgen.analysis.defects.thermo import FormationEnergyDiagram",
        "from pymatgen.analysis.phase_diagram import PhaseDiagram",
    },
}


def extract_functions(source_path):
    """Parse a test file with ast and return function info.

    Returns:
        dict: {func_name: {"source": str, "start": int, "end": int, "params": list[str]}}
    """
    source_text = source_path.read_text()
    source_lines = source_text.splitlines()
    tree = ast.parse(source_text, filename=str(source_path))

    functions = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name.startswith("test_"):
            start = node.lineno  # 1-indexed
            end = node.end_lineno
            # Extract parameter names (fixture dependencies)
            params = [arg.arg for arg in node.args.args if arg.arg != "self"]
            # Get source lines (body only, skip the def line)
            body_lines = source_lines[start:end]  # start is 1-indexed, so start:end gets body
            # Actually get the full function including def line for the source
            full_lines = source_lines[start - 1:end]
            # Extract just the body (indented code after def)
            body_only = []
            for line in full_lines[1:]:  # skip def line
                # Remove one level of indentation (4 spaces)
                if line.startswith("    "):
                    body_only.append(line[4:])
                else:
                    body_only.append(line)

            functions[node.name] = {
                "source": "\n".join(body_only),
                "full_source": "\n".join(full_lines),
                "start": start,
                "end": end,
                "params": params,
            }
    return functions


def _collect_imports(source_path):
    """Extract top-level import statements from a source file."""
    source_text = source_path.read_text()
    tree = ast.parse(source_text, filename=str(source_path))
    imports = []
    for node in ast.iter_child_nodes(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            line_start = node.lineno
            line_end = node.end_lineno
            lines = source_text.splitlines()[line_start - 1:line_end]
            imports.append("\n".join(lines))
    return imports


def resolve_fixtures(params):
    """Topologically sort fixture dependencies and return ordered list of fixtures needed.

    Returns list of fixture names in dependency order (leaves first).
    """
    needed = set()

    def _collect(name):
        if name in needed:
            return
        needed.add(name)
        for dep in FIXTURE_DEPS.get(name, []):
            _collect(dep)

    for p in params:
        if p in FIXTURE_DEPS:
            _collect(p)

    # Topological sort
    ordered = []
    visited = set()

    def _visit(name):
        if name in visited:
            return
        visited.add(name)
        for dep in FIXTURE_DEPS.get(name, []):
            if dep in needed:
                _visit(dep)
        ordered.append(name)

    for name in sorted(needed):
        _visit(name)

    return ordered


def build_reference(task_name, source_file, func_info):
    """Assemble self-contained reference.py content."""
    params = func_info["params"]
    fixture_order = resolve_fixtures(params)

    # Collect all needed imports
    all_imports = set()

    # Add fixture imports
    for fixture_name in fixture_order:
        for imp in FIXTURE_IMPORTS.get(fixture_name, set()):
            all_imports.add(imp)

    # Add source file imports (skip bare pytest imports, but keep if body uses pytest)
    source_path = MATTOOLS_TESTS / source_file
    file_imports = _collect_imports(source_path)
    body_uses_pytest = "pytest" in func_info["source"]
    for imp in file_imports:
        if "import pytest" in imp and not body_uses_pytest:
            continue
        all_imports.add(imp)

    # If body uses pytest but no pytest import was added, add it
    if body_uses_pytest and not any("import pytest" in imp for imp in all_imports):
        all_imports.add("import pytest")

    # Deduplicate imports: parse into (module, names) to merge overlapping imports
    # Simple dedup: just use the raw set (each unique import line is kept)
    # Group: stdlib, third-party
    STDLIB_PREFIXES = (
        "from collections", "from pathlib", "import itertools",
        "import os", "import copy", "from collections import",
    )
    stdlib_imports = []
    third_party_imports = []
    for imp in sorted(all_imports):
        if any(imp.startswith(p) for p in STDLIB_PREFIXES):
            stdlib_imports.append(imp)
        else:
            third_party_imports.append(imp)

    # Build the file
    parts = []

    # Header
    parts.append(f'"""Reference solution for {task_name}.')
    parts.append(f"Source: {source_file}, lines {func_info['start']}-{func_info['end']}")
    parts.append('"""')
    parts.append("")

    # Imports
    if stdlib_imports:
        for imp in sorted(stdlib_imports):
            parts.append(imp)
        parts.append("")
    if third_party_imports:
        for imp in sorted(third_party_imports):
            parts.append(imp)
        parts.append("")

    # Fixture setup
    if fixture_order:
        parts.append("# --- Fixture setup ---")
        parts.append("")
        for fixture_name in fixture_order:
            code = FIXTURE_CODE.get(fixture_name)
            if code:
                parts.append(f"# {fixture_name}")
                parts.append(code)
                parts.append("")

    # Reference test code
    parts.append("# --- Reference test code ---")
    parts.append("")
    parts.append(func_info["source"])
    parts.append("")

    return "\n".join(parts)


def main():
    parser = argparse.ArgumentParser(description="Extract reference code from pymatgen-analysis-defects tests")
    parser.add_argument("--task", type=str, help="Extract for a single task")
    parser.add_argument("--dry-run", action="store_true", help="Print to stdout instead of writing files")
    args = parser.parse_args()

    if args.task:
        tasks = {args.task: TASK_SOURCE_MAP[args.task]}
    else:
        tasks = TASK_SOURCE_MAP

    # Parse all needed source files
    source_cache = {}
    for task_name, (source_file, func_name) in tasks.items():
        if source_file not in source_cache:
            source_path = MATTOOLS_TESTS / source_file
            source_cache[source_file] = extract_functions(source_path)

    # Generate reference.py for each task
    generated = 0
    for task_name, (source_file, func_name) in sorted(tasks.items()):
        functions = source_cache[source_file]
        if func_name not in functions:
            print(f"WARNING: {func_name} not found in {source_file}")
            continue

        func_info = functions[func_name]
        content = build_reference(task_name, source_file, func_info)

        dest_path = DEST_DIR / task_name / "reference.py"
        if args.dry_run:
            print(f"=== {dest_path} ===")
            print(content)
            print()
        else:
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            dest_path.write_text(content)
            print(f"  wrote {dest_path}")
            generated += 1

    if not args.dry_run:
        print(f"\nGenerated {generated} reference.py files")


if __name__ == "__main__":
    main()
