import argparse
import json
import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any


def flake_url(dep: dict[str, Any]) -> str | None:
    locked = dep.get("locked")
    if locked is None:
        return None
    match locked["type"]:
        case "github" | "gitlab" | "sourcehut":
            url = f"{locked['type']}:{locked['owner']}/{locked['repo']}"
            if host := locked.get("host"):  # gitlab / sourcehut
                url += f"?host={host}"
            return url
        case "git" | "hg":
            return f"{locked['type']}:{locked['url']}"
        case "path":
            return f"{locked['type']}:{locked['path']}"
        case _:
            print(f"Unknown input type {locked['type']}")
    return None


@dataclass
class Flake:
    deps: dict[str, list[str]]
    reverse_deps: dict[str, list[str]]


@dataclass
class Options:
    lock_path: Path
    verbose: bool


def analyze_flake(flake_lock: dict[str, Any]) -> Flake:
    reverse_deps = defaultdict(list)
    deps = defaultdict(list)
    for name, dep in flake_lock["nodes"].items():
        for inputs in dep.get("inputs", {}).values():
            if isinstance(inputs, str):
                reverse_deps[inputs].append(name)
            elif isinstance(inputs, list):
                for i in inputs:
                    reverse_deps[i].append(name)
        url = flake_url(dep)
        if url is None:
            continue
        deps[url].append(name)
    return Flake(deps, reverse_deps)


def parse_args() -> Options:
    parser = argparse.ArgumentParser()
    parser.add_argument("flake_lock", nargs="?", default="flake.lock")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()
    lock_path = Path(args.flake_lock)
    if lock_path.is_dir():
        lock_path = lock_path / "flake.lock"

    if not lock_path.exists():
        print(f"flake.lock not found at {lock_path}", file=sys.stderr)
        sys.exit(1)

    return Options(lock_path=lock_path, verbose=args.verbose)


def main() -> None:
    options = parse_args()
    flake = analyze_flake(json.loads(options.lock_path.read_text()))

    for url, aliases in flake.deps.items():
        if len(aliases) == 1:
            if options.verbose:
                print(f"{url} is only used by {aliases[0]}")
            continue
        print(f"{url} has multiple versions:")
        for alias in aliases:
            dependencies = flake.reverse_deps[alias]
            print(f"  {alias} is used by: {', '.join(dependencies)}")


if __name__ == "__main__":
    main()
