"""Three-layer INCAR evaluation: syntax check, config constraints, LLM-as-judge.

Each INCAR file path from the agent is evaluated through:
1. Syntax: Parse via pymatgen Incar and check for unknown/invalid tags.
2. Config constraints: Verify tag values against properties.json rules.
3. LLM judge (optional): Holistic assessment of INCAR quality by an LLM.

The evaluate_incar_task() function aggregates results in the same format
as benchmark/tasks/evaluate.py: returns "ok" or [errors..., n_err, n_total].
"""

import json
import warnings
from pathlib import Path

import litellm
import yaml
from pymatgen.io.vasp.inputs import Incar

BENCHMARK_DIR = Path(__file__).parent
QUESTIONS_DIR = BENCHMARK_DIR / "question_segments"

# VASP boolean string -> Python bool mapping
_VASP_BOOLS = {
    ".TRUE.": True, ".FALSE.": False,
    ".true.": True, ".false.": False,
    "T": True, "F": False,
}

# Safe universal VASP defaults (from vasp.at/wiki).
# Only includes tags with context-independent defaults.
# Excludes: ENCUT (POTCAR-dependent), EDIFFG (EDIFF-dependent),
# NSW (default 0 = no ionic steps), IMAGES (default 0 = no NEB),
# IBRION (default 0 = MD, context-dependent).
_VASP_DEFAULTS = {
    "ISPIN": 1,
    "ISIF": 2,
    "ISMEAR": 1,
    "SIGMA": 0.2,
    "POTIM": 0.5,
    "SPRING": -5.0,
}


def _load_properties(task_name: str) -> dict:
    """Load properties.json for a task."""
    path = QUESTIONS_DIR / task_name / "properties.json"
    return json.loads(path.read_text(encoding="utf-8"))


def _load_judge_model() -> str:
    """Load judge model from config, falling back to agent model."""
    config_path = BENCHMARK_DIR / "config" / "llm_config.yaml"
    cfg = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    if "judge_model" in cfg:
        return cfg["judge_model"]
    provider = cfg["default_provider"]
    return cfg["providers"][provider]["model_id"]


def _load_judge_api_key() -> str | None:
    """Load API key for the judge model."""
    import os
    config_path = BENCHMARK_DIR / "config" / "llm_config.yaml"
    cfg = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    provider = cfg["default_provider"]
    api_key_tpl = cfg["providers"][provider].get("api_key", "")
    if api_key_tpl.startswith("${") and api_key_tpl.endswith("}"):
        env_var = api_key_tpl[2:-1]
        return os.environ.get(env_var)
    return api_key_tpl or None


def _read_incar_from_path(file_path: str) -> str | None:
    """Read INCAR content from a file path returned by the agent.

    Returns the file content string, or None if the path is invalid.
    """
    p = Path(file_path)
    if not p.exists():
        return None
    return p.read_text(encoding="utf-8")


def syntax_check(incar_text: str) -> tuple[Incar | None, list[str]]:
    """Parse INCAR text and check for parameter warnings.

    Returns:
        (parsed Incar object or None, list of warning strings)
    """
    try:
        incar = Incar.from_str(incar_text)
    except Exception as e:
        return None, [f"Failed to parse INCAR: {e}"]

    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        incar.check_params()

    return incar, [str(x.message) for x in w]


def _coerce(val, rule: dict):
    """Coerce parsed INCAR value for comparison against a constraint rule.

    Handles:
    - VASP boolean strings (.TRUE./.FALSE.) compared to Python bools
    - String expected values that are VASP booleans
    - Numeric type normalization
    """
    expected = rule.get("value")

    # If expected is a VASP boolean string like ".TRUE.", compare as bool
    if isinstance(expected, str) and expected in _VASP_BOOLS:
        if isinstance(val, bool):
            return val
        if isinstance(val, str) and val in _VASP_BOOLS:
            return _VASP_BOOLS[val]

    # Numeric coercion for range/gt checks
    if rule["match"] in ("range", "gt"):
        try:
            return float(val)
        except (ValueError, TypeError):
            return val

    # Int coercion for exact/in_set with int expected values
    if rule["match"] in ("exact", "in_set"):
        if isinstance(expected, int) and isinstance(val, float) and val == int(val):
            return int(val)
        if isinstance(expected, list) and all(isinstance(v, int) for v in expected):
            if isinstance(val, float) and val == int(val):
                return int(val)

    return val


def _expected_coerce(expected):
    """Coerce expected value for comparison (e.g., VASP bool strings)."""
    if isinstance(expected, str) and expected in _VASP_BOOLS:
        return _VASP_BOOLS[expected]
    return expected


def _check_value(val, rule: dict) -> bool:
    """Check whether *val* satisfies a constraint rule.

    Returns True if the value passes the constraint, False otherwise.
    """
    val = _coerce(val, rule)
    expected = _expected_coerce(rule.get("value"))

    match rule["match"]:
        case "exact":
            return val == expected
        case "in_set":
            return val in rule["value"]
        case "range":
            fval = float(val) if not isinstance(val, (int, float)) else val
            return rule["min"] <= fval <= rule["max"]
        case "gt":
            fval = float(val) if not isinstance(val, (int, float)) else val
            return fval > rule["min"]
        case _:
            return False


def _format_error(tag: str, val, rule: dict) -> str:
    """Format a human-readable error string for a failed constraint."""
    match rule["match"]:
        case "exact":
            return f"{tag}: expected {rule['value']}, got {val}"
        case "in_set":
            return f"{tag}: expected one of {rule['value']}, got {val}"
        case "range":
            return f"{tag}: {val} outside [{rule['min']}, {rule['max']}]"
        case "gt":
            return f"{tag}: {val} must be > {rule['min']}"
        case _:
            return f"{tag}: unknown match type '{rule['match']}'"


def config_check(incar: Incar, constraints: dict) -> list[str]:
    """Check parsed INCAR values against config constraints.

    When a tag is missing from the INCAR, checks whether the VASP default
    (from _VASP_DEFAULTS) satisfies the constraint before flagging an error.

    Args:
        incar: Parsed pymatgen Incar object.
        constraints: Dict of tag -> {match, value/min/max} from properties.json.

    Returns:
        List of error strings (empty if all pass).
    """
    errors = []
    for tag, rule in constraints.items():
        # Try both upper and original case
        val = incar.get(tag.upper(), incar.get(tag))
        if val is None:
            default = _VASP_DEFAULTS.get(tag.upper())
            if default is not None and _check_value(default, rule):
                continue
            errors.append(f"Missing required tag: {tag}")
            continue

        if not _check_value(val, rule):
            errors.append(_format_error(tag, _coerce(val, rule), rule))

    return errors


def llm_judge(
    incar_text: str,
    step_description: str,
    step_type: str,
    task_description: str = "",
    model: str | None = None,
) -> dict:
    """Use LLM to check INCAR for physics-critical errors.

    Args:
        incar_text: Raw INCAR file content.
        step_description: What this calculation step does.
        step_type: "relaxation", "neb", etc.
        task_description: Full task context (question.txt) for the judge.
        model: LiteLLM model ID. Defaults to config judge model.

    Returns:
        {"pass": bool, "issues": [str]}
    """
    if model is None:
        model = _load_judge_model()

    prompt = f"""You are a VASP expert reviewer. Check this INCAR for fundamental correctness errors that would produce physically wrong results or cause the calculation to fail.

Overall task:
{task_description}

This specific step: {step_description} (type: {step_type})

INCAR:
{incar_text}

Focus ONLY on:
- Wrong calculation type for the task (e.g., wrong IBRION for the method)
- Settings that produce wrong physics for the system geometry (e.g., ISIF=3 for a surface slab allows cell shape to change, collapsing the vacuum layer)
- Missing tags that are essential for this calculation type
- Tags with values that would cause VASP to crash or give meaningless results

IGNORE efficiency concerns: higher-than-needed ENCUT, extra output tags (LWAVE, LCHARG), or non-default but harmless settings are NOT errors.

Return JSON: {{"pass": true/false, "issues": ["list of physics-critical errors if any"]}}"""

    api_key = _load_judge_api_key()
    kwargs = {"model": model, "messages": [{"role": "user", "content": prompt}]}
    if api_key:
        kwargs["api_key"] = api_key

    # Request JSON output
    kwargs["response_format"] = {"type": "json_object"}

    response = litellm.completion(**kwargs)
    content = response.choices[0].message.content

    try:
        parsed = json.loads(content)
        if not isinstance(parsed, dict):
            return {
                "pass": False,
                "issues": [f"Judge returned non-dict JSON: {content[:200]}"],
            }
        return parsed
    except (json.JSONDecodeError, TypeError):
        return {
            "pass": False,
            "issues": [f"Failed to parse judge response: {content[:200]}"],
        }


def evaluate_incar_task(
    properties: dict,
    task_name: str,
    task_description: str = "",
    judge_model: str | None = None,
    run_llm_judge: bool = False,
) -> str | list:
    """Three-layer evaluation of INCAR generation task.

    Evaluates each INCAR step through syntax check, config constraints,
    and optionally LLM-as-judge. Agent returns file paths; evaluator reads
    the INCAR content from disk.

    Args:
        properties: Dict from agent's final_answer (step names -> file paths).
        task_name: Task name matching question_segments/ directory.
        task_description: Full task context (question.txt) for the LLM judge.
        judge_model: LiteLLM model ID for LLM judge. None uses config default.
        run_llm_judge: Whether to run Layer 3 LLM judge (default False).

    Returns:
        "ok" if all steps pass, or [error_msgs..., n_errors, n_total].
    """
    task_props = _load_properties(task_name)
    expected_steps = task_props["properties"]
    errors = []
    n_total = len(expected_steps)

    for prop_name, step_spec in expected_steps.items():
        file_path = properties.get(prop_name)
        if file_path is None:
            errors.append(f"{prop_name}: not found in agent output")
            continue

        if not isinstance(file_path, str) or not file_path.strip():
            errors.append(f"{prop_name}: empty or non-string value")
            continue

        # Read INCAR content from file path
        incar_text = _read_incar_from_path(file_path)
        if incar_text is None:
            errors.append(f"{prop_name}: file not found at {file_path}")
            continue

        if not incar_text.strip():
            errors.append(f"{prop_name}: file is empty at {file_path}")
            continue

        # Layer 1: syntax check
        incar, syntax_warnings = syntax_check(incar_text)
        if incar is None:
            errors.append(
                f"{prop_name}: INCAR parse failed - {'; '.join(syntax_warnings)}"
            )
            continue

        # Layer 2: config constraint check
        config_errs = config_check(incar, step_spec["config_constraints"])

        # Layer 3: LLM judge (optional)
        step_errors = []
        if config_errs:
            step_errors.extend(config_errs)

        if run_llm_judge:
            judge_result = llm_judge(
                incar_text,
                step_spec["description"],
                step_spec["step_type"],
                task_description=task_description,
                model=judge_model,
            )
            if not judge_result.get("pass", True):
                issues = judge_result.get("issues", [])
                step_errors.append(
                    "LLM judge FAIL: " + "; ".join(issues) if issues
                    else "LLM judge FAIL (no details)"
                )

        if step_errors:
            errors.append(f"{prop_name}: " + " | ".join(step_errors))

    if errors:
        errors.append(len(errors))
        errors.append(n_total)
        return errors
    return "ok"
