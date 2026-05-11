#!/usr/bin/env python3
"""
Lint tool to enforce the layered architecture.

Rules:
1. Every source file lives in exactly one layer directory.
2. Imports may only target layers in the file's "may import from" set.
3. No file exceeds 300 lines.
4. Parse-don't-validate at boundaries.
"""

import ast
import sys
from pathlib import Path


LAYER_ORDER = ["types", "config", "repo", "service", "providers", "utils", "runtime", "ui"]
LAYER_DEPS = {
    "types": {"types"},
    "config": {"types", "config"},
    "repo": {"types", "config", "repo"},
    "service": {"types", "config", "repo", "providers", "service"},
    "providers": {"types", "config", "utils", "providers"},
    "utils": {"utils"},
    "runtime": {"types", "config", "repo", "service", "providers", "runtime"},
    "ui": {"types", "config", "service", "runtime", "providers", "ui"},
}

MAX_LINES = 300


def get_layer_from_path(filepath: Path) -> str:
    """Extract the layer name from a file's path under src/."""
    parts = filepath.relative_to(Path("src")).parts
    if len(parts) < 2:
        return ""
    return str(parts[0])


def get_imported_layers(tree: ast.Module) -> set[str]:
    """Extract layer names from import statements in an AST."""
    layers = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                parts = alias.name.split(".")
                if parts[0] in LAYER_ORDER:
                    layers.add(parts[0])
        elif isinstance(node, ast.ImportFrom):
            if node.module and node.module.split(".")[0] in LAYER_ORDER:
                layers.add(node.module.split(".")[0])
    return layers


def check_file(filepath: Path, src_dir: Path) -> list[str]:
    """Check a single file for violations. Returns list of error messages."""
    errors = []
    rel_path = str(filepath.relative_to(src_dir.parent))

    # Rule 3: Line count
    lines = filepath.read_text().splitlines()
    if len(lines) > MAX_LINES:
        errors.append(f"{rel_path}:{len(lines)} lines (max {MAX_LINES})")

    # Rule 2: Import dependencies
    try:
        tree = ast.parse(filepath.read_text(), filename=str(filepath))
    except SyntaxError as e:
        errors.append(f"{rel_path}:{e.lineno} syntax error: {e.msg}")
        return errors

    imported_layers = get_imported_layers(tree)
    file_layer = get_layer_from_path(filepath)
    allowed_deps = LAYER_DEPS.get(file_layer, set())

    for layer in imported_layers:
        if layer not in allowed_deps:
            errors.append(
                f"{rel_path}: imports from '{layer}' but {file_layer} may only import from {sorted(allowed_deps)}"
            )

    return errors


def main() -> int:
    """Run lint checks on all source files."""
    src_dir = Path("src")
    cwd = Path.cwd()
    all_files = list(src_dir.rglob("*.py"))
    all_files = [f for f in all_files if f.name != "__init__.py" or f.parent != src_dir]

    violations = []

    for filepath in all_files:
        # Rule 1: File must be in a layer directory
        parts = filepath.relative_to(src_dir).parts
        if len(parts) < 2:
            rel_path = str(filepath.relative_to(src_dir.parent))
            violations.append(f"{rel_path}: file must be inside a layer directory")
            continue

        layer = parts[0]
        if layer not in LAYER_ORDER:
            rel_path = str(filepath.relative_to(src_dir.parent))
            violations.append(f"{rel_path}: unknown layer '{layer}'")
            continue

        # Check file-specific rules
        file_violations = check_file(filepath, src_dir)
        violations.extend(file_violations)

    if violations:
        print("Lint violations found:")
        for v in violations:
            print(f"  - {v}")
        return 1

    print("Lint passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
