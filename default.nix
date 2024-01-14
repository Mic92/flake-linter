{ buildPythonApplication, makeWrapper, setuptools, pytest, ... }:

buildPythonApplication {
  pname = "flake-linter";
  version = "0.0.1";
  src = ./.;
  format = "pyproject";
  buildInputs = [ makeWrapper ];
  nativeBuildInputs = [ setuptools ];
  nativeCheckInputs = [ pytest ];
  checkPhase = ''
    PYTHONPATH= $out/bin/flake-linter --help
  '';
  shellHook = ''
    # workaround because `python setup.py develop` breaks for me
  '';
}
