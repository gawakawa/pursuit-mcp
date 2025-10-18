{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs =
    {
      self,
      nixpkgs,
      flake-utils,
      ...
    }:
    flake-utils.lib.eachDefaultSystem (
      system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        python = pkgs.python312;
      in
      {
        packages = {
          pursuit-mcp = python.pkgs.buildPythonApplication {
            pname = "pursuit-mcp";
            version = "0.1.0";
            src = ./.;

            pyproject = true;
            build-system = [ python.pkgs.hatchling ];
            dependencies = with python.pkgs; [
              fastmcp
              httpx
              mcp
            ];
          };

          default = self.packages.${system}.pursuit-mcp;
        };

        devShells.default = pkgs.mkShell {
          buildInputs = with pkgs; [
            python312
            ruff
            uv
          ];

          shellHook = '''';
        };
      }
    );
}
