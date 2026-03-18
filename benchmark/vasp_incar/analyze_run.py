"""Analyze a backed-up absorptionE1_Ir run workspace.

Usage:
    python benchmark/vasp_incar/analyze_run.py benchmark/vasp_incar/workspace/absorptionE1_Ir_run1

Reads steps.jsonl and INCAR files, reports:
1. INCAR correctness (config_check against properties.json)
2. Whether the agent used rag_search
3. Retrieved chunk sources and snippets (if RAG was used)
"""

import json
import re
import sys
from pathlib import Path

# Add project root for imports
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from pymatgen.io.vasp.inputs import Incar
from benchmark.vasp_incar.evaluate import config_check, syntax_check


def load_properties():
    props_path = Path(__file__).parent / "question_segments" / "absorptionE1_Ir" / "properties.json"
    return json.loads(props_path.read_text())


def parse_steps(workspace: Path) -> list[dict]:
    """Parse steps.jsonl, extracting key fields from the repr string."""
    steps_path = workspace / "steps.jsonl"
    if not steps_path.exists():
        print(f"  ERROR: {steps_path} not found")
        return []

    steps = []
    for line in steps_path.read_text().splitlines():
        if not line.strip():
            continue
        record = json.loads(line)
        step_repr = record.get("step", "")

        # Extract step_number
        m = re.search(r"step_number=(\d+)", step_repr)
        step_num = int(m.group(1)) if m else -1

        # Extract code_action (between code_action=' and ', observations=)
        # The code_action field uses escaped single quotes
        code_action = ""
        m = re.search(r"code_action='(.*?)', observations=", step_repr, re.DOTALL)
        if m:
            code_action = m.group(1).replace("\\'", "'").replace("\\n", "\n")
        else:
            m = re.search(r'code_action="(.*?)", observations=', step_repr, re.DOTALL)
            if m:
                code_action = m.group(1).replace('\\"', '"').replace("\\n", "\n")

        # Extract error (non-None)
        has_error = "error=None" not in step_repr.split("model_output_message=")[0] if "model_output_message=" in step_repr else False
        error_msg = ""
        if has_error:
            m2 = re.search(r"error=Agent\w+Error\('(.*?)'\)", step_repr)
            if m2:
                error_msg = m2.group(1)[:200]

        # Extract is_final_answer
        is_final = "is_final_answer=True" in step_repr

        # Extract observations
        observations = ""
        m = re.search(r"observations='(.*?)', observations_images=", step_repr, re.DOTALL)
        if m:
            observations = m.group(1).replace("\\'", "'").replace("\\n", "\n")

        # Check for rag_search in code_action
        has_rag = "rag_search(" in code_action

        steps.append({
            "step_number": step_num,
            "code_action": code_action,
            "has_error": has_error,
            "error_msg": error_msg,
            "is_final": is_final,
            "has_rag": has_rag,
            "observations": observations,
        })

    return steps


def check_incars(workspace: Path, properties: dict) -> dict:
    """Check each step's INCAR against config constraints."""
    results = {}
    for prop_name, step_spec in properties["properties"].items():
        # Map step1_incar -> step1/INCAR
        step_dir = prop_name.replace("_incar", "")
        incar_path = workspace / step_dir / "INCAR"

        if not incar_path.exists():
            results[prop_name] = {"exists": False, "errors": ["INCAR file not found"]}
            continue

        incar_text = incar_path.read_text()
        incar, syntax_warns = syntax_check(incar_text)
        if incar is None:
            results[prop_name] = {"exists": True, "errors": [f"Parse failed: {syntax_warns}"]}
            continue

        config_errs = config_check(incar, step_spec["config_constraints"])
        results[prop_name] = {
            "exists": True,
            "errors": config_errs,
            "n_tags": len(incar),
            "key_tags": {k: incar.get(k) for k in ["ISIF", "IBRION", "ISMEAR", "SIGMA", "ENCUT", "NSW", "EDIFFG", "ISPIN"]},
        }

    return results


def extract_rag_chunks(steps: list[dict]) -> list[dict]:
    """Extract RAG search queries and returned chunks from steps."""
    rag_calls = []
    for s in steps:
        if not s["has_rag"]:
            continue

        # Extract queries from code_action
        queries = []
        m = re.search(r'queries=\[(.*?)\]', s["code_action"], re.DOTALL)
        if m:
            queries = re.findall(r'"([^"]+)"', m.group(1))
            if not queries:
                queries = re.findall(r"'([^']+)'", m.group(1))

        # Extract software filter
        software = []
        m = re.search(r'software=\[(.*?)\]', s["code_action"])
        if m:
            software = re.findall(r'"([^"]+)"', m.group(1))
            if not software:
                software = re.findall(r"'([^']+)'", m.group(1))

        # Extract chunk sources from observations
        sources = re.findall(r"'source': '([^']+)'", s["observations"])
        # Extract snippet previews (first 120 chars each)
        snippets = re.findall(r"'snippet': '((?:[^'\\]|\\.){0,200})", s["observations"])

        rag_calls.append({
            "step": s["step_number"],
            "queries": queries,
            "software": software,
            "n_chunks": len(sources),
            "sources": sources,
            "snippet_previews": [sn[:120].replace("\\n", " ") for sn in snippets],
        })

    return rag_calls


def analyze(workspace_path: str):
    workspace = Path(workspace_path)
    properties = load_properties()

    print(f"\n{'='*70}")
    print(f"ANALYSIS: {workspace.name}")
    print(f"{'='*70}")

    # 1. Parse steps
    steps = parse_steps(workspace)
    if not steps:
        return

    print(f"\nTotal steps: {len(steps)}")
    for s in steps:
        status = "FINAL" if s["is_final"] else ("ERROR" if s["has_error"] else "OK")
        rag_tag = " [RAG]" if s["has_rag"] else ""
        print(f"  Step {s['step_number']}: {status}{rag_tag}")
        if s["has_error"]:
            print(f"    Error: {s['error_msg'][:120]}")

    # 2. Check INCARs
    print(f"\n--- INCAR Correctness ---")
    incar_results = check_incars(workspace, properties)
    all_pass = True
    for prop_name, result in incar_results.items():
        if not result["exists"]:
            print(f"  {prop_name}: MISSING")
            all_pass = False
        elif result["errors"]:
            print(f"  {prop_name}: FAIL - {result['errors']}")
            all_pass = False
        else:
            tags = result.get("key_tags", {})
            tag_str = ", ".join(f"{k}={v}" for k, v in tags.items() if v is not None)
            print(f"  {prop_name}: PASS ({tag_str})")

    if all_pass:
        print("  OVERALL: ALL PASS")
    else:
        print("  OVERALL: SOME FAILURES")

    # 3. RAG usage
    print(f"\n--- RAG Usage ---")
    rag_steps = [s for s in steps if s["has_rag"]]
    if not rag_steps:
        print("  No rag_search calls detected.")
    else:
        print(f"  rag_search called in {len(rag_steps)} step(s): {[s['step_number'] for s in rag_steps]}")

    # 4. Chunk analysis
    rag_calls = extract_rag_chunks(steps)
    if rag_calls:
        print(f"\n--- Retrieved Chunks ---")
        for rc in rag_calls:
            print(f"  Step {rc['step']}:")
            print(f"    Queries: {rc['queries']}")
            print(f"    Software filter: {rc['software']}")
            print(f"    Chunks returned: {rc['n_chunks']}")
            for i, src in enumerate(rc["sources"]):
                preview = rc["snippet_previews"][i] if i < len(rc["snippet_previews"]) else ""
                print(f"      [{i+1}] {src}")
                if preview:
                    print(f"          {preview[:100]}...")

    print()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python analyze_run.py <workspace_path>")
        sys.exit(1)
    analyze(sys.argv[1])
