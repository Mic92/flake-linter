{
  description = "Development environment for this project";

  inputs = {
    nixpkgs.url = "git+https://github.com/NixOS/nixpkgs?shallow=1&ref=nixpkgs-unstable";
  };

  outputs =
    { self, nixpkgs }:
    let
      systems = [
        "x86_64-linux"
        "aarch64-linux"
        "x86_64-darwin"
        "aarch64-darwin"
      ];
      eachSystem = f: nixpkgs.lib.genAttrs systems (system: f nixpkgs.legacyPackages.${system});
    in
    {
      packages = eachSystem (pkgs: {
        default = pkgs.python3.pkgs.callPackage ./default.nix { };
      });

      checks = eachSystem (pkgs: {
        package-default = self.packages.${pkgs.stdenv.hostPlatform.system}.default;
      });
    };
}
