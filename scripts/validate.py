import json, sys, pathlib, yaml
from jsonschema import validate, ValidationError

ROOT = pathlib.Path(__file__).resolve().parents[1]
SCHEMA = json.loads((ROOT / "schema" / "node.schema.json").read_text(encoding="utf-8"))

def main() -> int:
    nodes_dir = ROOT / "data" / "nodes"
    errors = 0
    for yml in nodes_dir.rglob("*.yaml"):
        data = yaml.safe_load(yml.read_text(encoding="utf-8"))
        try:
            validate(instance=data, schema=SCHEMA)
            print(f"[OK] {yml}")
        except ValidationError as e:
            errors += 1
            print(f"[NG] {yml}\\n  -> {e.message}")
    return 1 if errors else 0

if __name__ == "__main__":
    sys.exit(main())