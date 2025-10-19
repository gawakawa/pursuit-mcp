{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
    mcp-servers-nix.url = "github:natsukium/mcp-servers-nix";
  };

  outputs =
    {
      self,
      nixpkgs,
      flake-utils,
      mcp-servers-nix,
      ...
    }:
    flake-utils.lib.eachDefaultSystem (
      system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        python = pkgs.python312;

        ciPackages = with pkgs; [
          python312
          ruff
          uv
        ];

        devPackages =
          ciPackages
          ++ (with pkgs; [
            # Additional development tools can be added here
          ]);

        mcpConfig = mcp-servers-nix.lib.mkConfig pkgs {
          programs = {
            nixos.enable = true;
            serena.enable = true;
          };
        };
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

          ci = pkgs.buildEnv {
            name = "ci";
            paths = ciPackages;
          };

          mcp-config = mcpConfig;

          default = self.packages.${system}.pursuit-mcp;
        };

        devShells.default = pkgs.mkShell {
          buildInputs = devPackages;

          shellHook = ''
            cat ${mcpConfig} > .mcp.json
            echo "Generated .mcp.json"
          '';
        };
      }
    );
}
