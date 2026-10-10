"""Check documented user-supplied inputs without reading their contents."""

from pathlib import Path
import json
import os


def main():
    project = Path(__file__).resolve().parent
    root = Path(os.environ.get("PROJECT_DATA_DIR", project)).expanduser()
    inputs = json.loads((project / "inputs.json").read_text(encoding="utf-8"))
    missing = []
    for pattern in inputs["required"]:
        matches = list(root.glob(pattern.rstrip("/")))
        present = any(
            path.is_dir() if pattern.endswith("/") else path.is_file() for path in matches
        )
        print(f"{'OK' if present else 'MISSING'}: {pattern}")
        if not present:
            missing.append(pattern)
    if not inputs["required"]:
        print(
            "No fixed external inputs required; see README for bundled data or CLI-supplied paths."
        )
    if missing:
        print("Add the listed inputs yourself; see README.md. No downloads are performed.")
    return int(bool(missing))


if __name__ == "__main__":
    raise SystemExit(main())
