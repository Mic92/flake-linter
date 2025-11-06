# flake-linter

A tool to detect and report duplicate dependencies in Nix flakes.

## The Problem

Nix flakes use a lock file (`flake.lock`) to pin dependencies to specific versions, ensuring reproducible builds.
However, when multiple flakes in your dependency tree depend on the same upstream flake (like `nixpkgs` or `flake-utils`),
they might reference different versions of it.
This creates several issues:

### Why Duplicate Dependencies Are Problematic

1. **Increased Closure Size**: Each version of a dependency must be downloaded and stored separately, significantly increasing disk usage and download times.

2. **Evaluation Performance**: Nix has to evaluate multiple versions of the same flake, slowing down your build times and `nix flake` commands.

3. **Inconsistent Behavior**: Different parts of your project might use different versions of the same packages, leading to subtle bugs and version conflicts.

### When This Happens

This commonly occurs when:
- Your project uses multiple third-party flakes
- Those flakes haven't synchronized their `flake.lock` updates
- Transitive dependencies pin different versions of common utilities (like `flake-utils`, `nixpkgs`, etc.)

## Solution

`flake-linter` scans your `flake.lock` file and identifies all cases where the same dependency appears multiple times with different versions,
helping you spot these issues before they impact your project.

## Usage

```bash
$ cd your-flake-project
$ nix run github:Mic92/flake-linter
github:numtide/flake-utils has multiple versions:
  flake-utils is used by: crane, pre-commit-hooks-nix, root, rust-overlay
  flake-utils_2 is used by: lanzaboote
```

### Options

```bash
# Run on a specific flake.lock file
$ flake-linter /path/to/flake.lock

# Show all dependencies (including single versions)
$ flake-linter --verbose

# Exit with error code if duplicates are found (useful for CI)
$ flake-linter --fail-if-multiple-versions
```

## Installation

Run directly with Nix:
```bash
nix run github:Mic92/flake-linter
```

Or add to your flake inputs for regular use:
```nix
{
  inputs.flake-linter.url = "github:Mic92/flake-linter";
}
```

## What to Do When Duplicates Are Found

1. **Update Inputs**: Run `nix flake update` to try getting your dependencies on the same versions
2. **Override Inputs**: Use flake input follows to force dependencies to use your version:
   ```nix
   inputs.some-flake.inputs.nixpkgs.follows = "nixpkgs";
   ```

## License

MIT
