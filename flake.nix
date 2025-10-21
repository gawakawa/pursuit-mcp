{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-parts.url = "github:hercules-ci/flake-parts";
    treefmt-nix.url = "github:numtide/treefmt-nix";
    mcp-servers-nix.url = "github:natsukium/mcp-servers-nix";
  };

  outputs =
    inputs:
    inputs.flake-parts.lib.mkFlake { inherit inputs; } {
      systems = [
        "x86_64-linux"
        "aarch64-darwin"
      ];

      imports = [ inputs.treefmt-nix.flakeModule ];

      perSystem =
        {
          self',
          pkgs,
          system,
          ...
        }:
        let
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

          mcpConfig = inputs.mcp-servers-nix.lib.mkConfig pkgs {
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

            default = self'.packages.pursuit-mcp;
          };

          devShells.default = pkgs.mkShell {
            buildInputs = devPackages;

            shellHook = ''
              cat ${mcpConfig} > .mcp.json
              echo "Generated .mcp.json"
            '';
          };

          treefmt = {
            programs = {
              nixfmt.enable = true;
              ruff-format.enable = true;
              ruff-check.enable = true;
            };
          };
        };
    };
}
