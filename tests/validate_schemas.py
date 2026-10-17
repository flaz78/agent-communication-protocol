#!/usr/bin/env python3
"""ACP v1.1 - deterministic test runner.

Usage:
    python tests/validate_schemas.py                 # run all deterministic checks
    python tests/validate_schemas.py --handoff F     # validate one handoff JSON file
    python tests/validate_schemas.py --task F        # validate one task contract JSON file

No third-party dependencies. If the `jsonschema` package is installed it is used
as a second, independent validator (cross-check); otherwise a built-in validator
covering the JSON Schema subset used by ACP schemas is used.
Exit code 0 = all checks passed.
"""
from __future__ import annotations

import argparse
import copy
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCHEMAS = ROOT / "schemas"
SKILL_TEST_PATHS = ("tests/validate_schemas.py", "tests/test-cases.md", "tests/evals.json", "tests/fixtures/")

# --------------------------------------------------------------------------
# Minimal JSON Schema (draft 2020-12 subset) validator
# --------------------------------------------------------------------------
SUPPORTED = {
    "$schema", "$id", "$defs", "$ref", "title", "description", "type", "required",
    "properties", "additionalProperties", "items", "enum", "const", "pattern",
    "minLength", "maxLength", "minItems", "uniqueItems", "allOf", "if", "then",
    "format",
}
_TYPES = {
    "object": dict, "array": list, "string": str, "boolean": bool,
    "integer": int, "number": (int, float), "null": type(None),
}


def _type_ok(value, t):
    if t in ("integer", "number") and isinstance(value, bool):
        return False
    return isinstance(value, _TYPES[t])


def _resolve(root, ref):
    if not ref.startswith("#/"):
        raise ValueError(f"Unsupported $ref: {ref}")
    node = root
    for part in ref[2:].split("/"):
        node = node[part]
    return node


def mini_validate(instance, schema, root=None, path="$"):
    """Return a list of error strings (empty = valid)."""
    root = schema if root is None else root
    errors = []
    unknown = set(schema) - SUPPORTED
    if unknown:
        raise ValueError(f"Schema keyword(s) not supported by mini validator: {unknown}")
    if "$ref" in schema:
        errors += mini_validate(instance, _resolve(root, schema["$ref"]), root, path)
    if "type" in schema and not _type_ok(instance, schema["type"]):
        return errors + [f"{path}: expected {schema['type']}"]
    if "enum" in schema and instance not in schema["enum"]:
        errors.append(f"{path}: {instance!r} not in {schema['enum']}")
    if "const" in schema and instance != schema["const"]:
        errors.append(f"{path}: expected const {schema['const']!r}")
    if isinstance(instance, str):
        if "minLength" in schema and len(instance) < schema["minLength"]:
            errors.append(f"{path}: shorter than {schema['minLength']}")
        if "maxLength" in schema and len(instance) > schema["maxLength"]:
            errors.append(f"{path}: longer than {schema['maxLength']}")
        if "pattern" in schema and not re.search(schema["pattern"], instance):
            errors.append(f"{path}: does not match {schema['pattern']}")
    if isinstance(instance, list):
        if "minItems" in schema and len(instance) < schema["minItems"]:
            errors.append(f"{path}: fewer than {schema['minItems']} items")
        if schema.get("uniqueItems"):
            dumped = [json.dumps(i, sort_keys=True) for i in instance]
            if len(dumped) != len(set(dumped)):
                errors.append(f"{path}: items not unique")
        if "items" in schema:
            for i, item in enumerate(instance):
                errors += mini_validate(item, schema["items"], root, f"{path}[{i}]")
    if isinstance(instance, dict):
        for key in schema.get("required", []):
            if key not in instance:
                errors.append(f"{path}: missing required '{key}'")
        props = schema.get("properties", {})
        for key, val in instance.items():
            if key in props:
                errors += mini_validate(val, props[key], root, f"{path}.{key}")
            elif schema.get("additionalProperties") is False:
                errors.append(f"{path}: unexpected property '{key}'")
    for sub in schema.get("allOf", []):
        errors += mini_validate(instance, sub, root, path)
    if "if" in schema:
        if not mini_validate(instance, schema["if"], root, path):
            if "then" in schema:
                errors += mini_validate(instance, schema["then"], root, path)
    return errors


def jsonschema_validate(instance, schema):
    """Cross-check with the `jsonschema` package if available. Returns errors or None."""
    try:
        import jsonschema  # type: ignore
    except ImportError:
        return None
    validator = jsonschema.Draft202012Validator(schema)
    return [f"$.{'.'.join(map(str, e.absolute_path))}: {e.message}" for e in validator.iter_errors(instance)]


# --------------------------------------------------------------------------
# Semantic (non-schema) checks for handoffs
# --------------------------------------------------------------------------
SECRET_PATTERNS = [
    re.compile(r"sk-[A-Za-z0-9_\-]{20,}"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"ghp_[A-Za-z0-9]{30,}"),
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    re.compile(r"xox[baprs]-[A-Za-z0-9\-]{10,}"),
]


def semantic_handoff_errors(h):
    errors = []
    status = h.get("status")
    blockers = [i for i in h.get("open_issues", []) if i.get("severity") == "blocker"]
    if status == "completed":
        unmet = [a["id"] for a in h.get("acceptance_criteria", []) if a.get("status") != "met"]
        if unmet:
            errors.append(f"status 'completed' but criteria not met: {unmet}")
        if blockers:
            errors.append("status 'completed' with blocker open_issues")
        if any(t.get("status") in ("failed", "error") for t in h.get("test_results", [])):
            errors.append("status 'completed' with failed tests")
    if status == "blocked" and not blockers:
        errors.append("status 'blocked' requires at least one blocker in open_issues")
    if status == "failed" and not h.get("open_issues"):
        errors.append("status 'failed' requires the reason in open_issues")
    dump = json.dumps(h)
    for pat in SECRET_PATTERNS:
        if pat.search(dump):
            errors.append(f"possible secret matching /{pat.pattern}/")
    return errors


def validate_handoff(h, schema):
    errs = mini_validate(h, schema)
    js = jsonschema_validate(h, schema)
    if js is not None and bool(js) != bool(errs):
        errs.append(f"VALIDATOR DISAGREEMENT mini={len(errs)} jsonschema={len(js)}: {js}")
    return errs + semantic_handoff_errors(h)


def validate_task(t, schema):
    errs = mini_validate(t, schema)
    js = jsonschema_validate(t, schema)
    if js is not None and bool(js) != bool(errs):
        errs.append(f"VALIDATOR DISAGREEMENT mini={len(errs)} jsonschema={len(js)}: {js}")
    return errs


# --------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------
def load(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def apply_patch(doc, case):
    doc = copy.deepcopy(doc)
    for key in case.get("delete", []):
        doc.pop(key)
    for ptr, value in case.get("set", {}).items():
        parts = ptr.split("/")
        node = doc
        for part in parts[:-1]:
            node = node[int(part)] if isinstance(node, list) else node[part]
        last = parts[-1]
        if isinstance(node, list):
            node[int(last)] = value
        else:
            node[last] = value
    return doc


def parse_frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not m:
        return None
    raw = m.group(1)
    try:
        import yaml  # type: ignore
        return yaml.safe_load(raw)
    except ImportError:
        data = {}
        for line in raw.splitlines():
            mm = re.match(r'^([A-Za-z_-]+):\s*(.*)$', line)
            if mm and not line.startswith(" "):
                val = mm.group(2).strip()
                if len(val) >= 2 and val[0] == val[-1] == '"':
                    val = val[1:-1]
                data[mm.group(1)] = val if val else {}
        return data


# --------------------------------------------------------------------------
# Checks
# --------------------------------------------------------------------------
results = []


def check(cid, name, test_ids, fn):
    try:
        problems = fn() or []
    except Exception as exc:  # report, don't crash
        problems = [f"exception: {exc!r}"]
    results.append((cid, name, test_ids, problems))


def c_frontmatter():
    text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    fm = parse_frontmatter(text)
    if fm is None:
        return ["SKILL.md: missing or malformed YAML frontmatter"]
    p = []
    allowed = {"name", "description", "license", "allowed-tools", "metadata", "compatibility"}
    extra = set(fm) - allowed
    if extra:
        p.append(f"unexpected frontmatter keys: {extra}")
    name = fm.get("name", "")
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", str(name)) or len(name) > 64:
        p.append(f"invalid name: {name!r}")
    if name != ROOT.name:
        p.append(f"name {name!r} differs from folder {ROOT.name!r}")
    desc = str(fm.get("description", ""))
    if not desc:
        p.append("missing description")
    if len(desc) > 1024:
        p.append(f"description too long: {len(desc)}")
    if "<" in desc or ">" in desc:
        p.append("description contains angle brackets")
    for needed in ["ACP CODING", "handoff", "review", "Not needed"]:
        if needed.lower() not in desc.lower():
            p.append(f"description lacks discovery cue: {needed!r}")
    comp = fm.get("compatibility", "")
    if comp and len(str(comp)) > 500:
        p.append("compatibility too long")
    body_lines = text.count("\n")
    if body_lines > 500:
        p.append(f"SKILL.md too long for progressive disclosure: {body_lines} lines")
    n_skill = [q for q in ROOT.rglob("SKILL.md")]
    if len(n_skill) != 1:
        p.append(f"expected exactly one SKILL.md, found {len(n_skill)}")
    return p


def c_references():
    p = []
    ref_re = re.compile(r"`((?:\.\./)?(?:references|schemas|examples|tests|agents|benchmark)/[A-Za-z0-9_./\-]+)`|\]\(((?:\.\./)?[A-Za-z0-9_./\-]+\.(?:md|json|yaml|py))\)")
    for md in list(ROOT.rglob("*.md")):
        text = md.read_text(encoding="utf-8")
        for m in ref_re.finditer(text):
            target = (m.group(1) or m.group(2)).split("::")[0]
            target = target.rstrip(".")
            # Paths under tests/ in examples may describe the user's own repo
            # (e.g. tests/auth/...); only check files that belong to this skill.
            norm = target.lstrip("./")
            if norm.startswith("tests/") and not norm.startswith(SKILL_TEST_PATHS):
                continue
            # A reference may be relative to the file itself or to the skill root.
            candidates = [(md.parent / target).resolve(), (ROOT / target).resolve()]
            if not any(c.exists() for c in candidates):
                p.append(f"{md.relative_to(ROOT)}: broken reference {target}")
    return p


def c_schemas_wellformed():
    p = []
    for s in SCHEMAS.glob("*.json"):
        schema = load(s)
        if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
            p.append(f"{s.name}: not draft 2020-12")
        try:
            mini_validate({}, schema)  # also raises on unsupported keywords
        except ValueError as exc:
            p.append(f"{s.name}: {exc}")
        try:
            import jsonschema  # type: ignore
            jsonschema.Draft202012Validator.check_schema(schema)
        except ImportError:
            pass
        except Exception as exc:
            p.append(f"{s.name}: meta-schema error {exc}")
    required = {"protocol_version", "task_id", "source_agent", "target_agent", "objective", "status",
                "completed_work", "verified_findings", "unverified_hypotheses", "decisions",
                "modified_artifacts", "constraints", "test_results", "open_issues", "next_actions",
                "acceptance_criteria"}
    hs = load(SCHEMAS / "handoff.schema.json")
    missing = required - set(hs["required"])
    if missing:
        p.append(f"handoff schema missing required fields: {missing}")
    states = set(hs["properties"]["status"]["enum"])
    if states != {"pending", "in_progress", "blocked", "ready_for_review", "completed", "failed"}:
        p.append(f"handoff states differ from spec: {states}")
    return p


def c_examples_valid():
    p = []
    hs, ts = load(SCHEMAS / "handoff.schema.json"), load(SCHEMAS / "task.schema.json")
    for e in validate_handoff(load(ROOT / "examples/handoff.json"), hs):
        p.append(f"examples/handoff.json: {e}")
    for e in validate_task(load(ROOT / "examples/task-contract.json"), ts):
        p.append(f"examples/task-contract.json: {e}")
    return p


def c_negative_fixtures():
    p = []
    hs = load(SCHEMAS / "handoff.schema.json")
    base = load(ROOT / "examples/handoff.json")
    for case in load(ROOT / "tests/fixtures/invalid-handoffs.json")["cases"]:
        errs = validate_handoff(apply_patch(base, case), hs)
        if not errs:
            p.append(f"{case['id']} accepted but should be rejected: {case['reason']}")
    # task contract: L3 without rollback must be rejected
    ts = load(SCHEMAS / "task.schema.json")
    t = load(ROOT / "examples/task-contract.json")
    t["level"] = "L3"
    if not validate_task(t, ts):
        p.append("task contract L3 without impact_analysis/rollback accepted")
    t = load(ROOT / "examples/task-contract.json")
    t["modes"] = ["CODING", "DEPLOY"]
    if not validate_task(t, ts):
        p.append("task contract with unknown mode accepted")
    return p


def c_test_catalog():
    p = []
    text = (ROOT / "tests/test-cases.md").read_text(encoding="utf-8")
    for i in range(1, 16):
        tid = f"T{i:02d}"
        m = re.search(rf"^## {tid} .*?(?=^## T\d\d |\Z)", text, re.DOTALL | re.MULTILINE)
        if not m:
            p.append(f"{tid} missing")
            continue
        block = m.group(0)
        for field in ["**Input:**", "**Comportamento atteso:**", "**Criteri di successo:**", "**Verifica:**"]:
            if field not in block:
                p.append(f"{tid} lacks {field}")
    evals = load(ROOT / "tests/evals.json")
    ids = {e["id"] for e in evals["evals"]}
    llm_tests = {"T01", "T02", "T03", "T04", "T05", "T06", "T07", "T08", "T09", "T10", "T12", "T13", "T14", "T15"}
    covered = {t for e in evals["evals"] for t in e["covers"]}
    if not llm_tests <= covered:
        p.append(f"evals.json does not cover: {sorted(llm_tests - covered)}")
    if len(ids) != len(evals["evals"]):
        p.append("duplicate eval ids")
    for e in evals["evals"]:
        for k in ("id", "covers", "prompt", "expected_modes", "assertions"):
            if k not in e:
                p.append(f"eval {e.get('id')} lacks {k}")
        if not e.get("assertions"):
            p.append(f"eval {e.get('id')} has no assertions")
    return p


def c_mode_coverage():
    p = []
    skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    for mode in ["PROMPT", "CODING", "HANDOFF", "REVIEW", "COMPRESS"]:
        if not re.search(rf"^### {mode}\b", skill, re.MULTILINE):
            p.append(f"SKILL.md lacks section for mode {mode}")
    for lvl in ["L0", "L1", "L2", "L3"]:
        if lvl not in skill:
            p.append(f"SKILL.md lacks level {lvl}")
    if "ACP Core" not in skill or "ACP Engineering" not in skill:
        p.append("ACP Core / ACP Engineering not distinguished")
    return p


def run_all():
    check("D1", "Frontmatter SKILL.md valido", ["T15"], c_frontmatter)
    check("D2", "Riferimenti interni esistenti", [], c_references)
    check("D3", "Schemi ben formati e conformi alla specifica", ["T11"], c_schemas_wellformed)
    check("D4", "Esempi conformi agli schemi", ["T05", "T10", "T11"], c_examples_valid)
    check("D5", "Fixture non valide rifiutate", ["T08", "T11"], c_negative_fixtures)
    check("D6", "Catalogo test T01-T15 e evals completi", [], c_test_catalog)
    check("D7", "Cinque modalita' e quattro livelli presenti", ["T01"], c_mode_coverage)
    failed = 0
    for cid, name, tids, problems in results:
        tag = "PASS" if not problems else "FAIL"
        failed += bool(problems)
        cov = f" [{', '.join(tids)}]" if tids else ""
        print(f"{tag}  {cid}  {name}{cov}")
        for pr in problems:
            print(f"      - {pr}")
    try:
        import jsonschema  # noqa: F401
        backend = "mini validator + jsonschema cross-check"
    except ImportError:
        backend = "mini validator only (jsonschema not installed)"
    print(f"\n{len(results) - failed}/{len(results)} checks passed ({backend})")
    return 1 if failed else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--handoff", help="validate a handoff JSON file")
    ap.add_argument("--task", help="validate a task contract JSON file")
    a = ap.parse_args()
    if a.handoff or a.task:
        code = 0
        if a.handoff:
            errs = validate_handoff(load(a.handoff), load(SCHEMAS / "handoff.schema.json"))
            print("VALID" if not errs else "INVALID", a.handoff)
            for e in errs:
                print("  -", e)
            code |= bool(errs)
        if a.task:
            errs = validate_task(load(a.task), load(SCHEMAS / "task.schema.json"))
            print("VALID" if not errs else "INVALID", a.task)
            for e in errs:
                print("  -", e)
            code |= bool(errs)
        return int(code)
    return run_all()


if __name__ == "__main__":
    sys.exit(main())
