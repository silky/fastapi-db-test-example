{
  inputs = {
    pyproject-nix.url = "github:nix-community/pyproject.nix";
    pyproject-nix.inputs.nixpkgs.follows = "nixpkgs";

    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { nixpkgs, pyproject-nix, flake-utils, ... }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        inherit (nixpkgs) lib;
        project = pyproject-nix.lib.project.loadPoetryPyproject {
          projectRoot = ./.;
        };

        overlay = _: prev: {
          python3 = prev.python3.override {
            packageOverrides = _: p: {
              fastapi-cli = p.buildPythonPackage rec {
                version = "0.0.4";
                pname = "fastapi-cli";
                format = "pyproject";
                nativeBuildInputs = with p.pythonPackages; [
                  pdm-backend
                ];
                propagatedBuildInputs = with p.pythonPackages; [
                  typer
                  rich
                ];
                src = pkgs.fetchFromGitHub {
                  owner = "tiangolo";
                  repo = "fastapi-cli";
                  rev = "63267a3a59e746e29e6076c19758cc8b23d4f9f4";
                  sha256 = "sha256-EpLf2O5tA16oGjkpEkEyEtSnsc+ENK/4eJFSq1MrCPk=";
                };
              };
            };
          };
        };

        pkgs = import nixpkgs { inherit system; overlays = [ overlay ]; };
        python = pkgs.python3;
      in
      {
        devShells.default =
          let
            arg = project.renderers.withPackages { inherit python; };
            pythonEnv = python.withPackages arg;
          in pkgs.mkShell {
            packages = [ pythonEnv ];
            shellHook = ''
              export PYTHONPATH=''$(pwd)
            '';
          };

        packages.default =
          let
            attrs = project.renderers.buildPythonPackage { inherit python; };
          in python.pkgs.buildPythonPackage attrs;
        }
    );
}

