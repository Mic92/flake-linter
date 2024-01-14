# flake-linter

Find duplicate dependencies in flakes

```
$ cd blended
$ nix run https://github.com/Mic92/flake-linter --
github:numtide/flake-utils has multiple versions:
  flake-utils is used by: crane, pre-commit-hooks-nix, root, rust-overlay
  flake-utils_2 is used by: lanzaboote
```
