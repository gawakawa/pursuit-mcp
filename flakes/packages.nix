{ inputs, flake-parts-lib, ... }:
{
  options.perSystem = flake-parts-lib.mkPerSystemOption (
    { lib, ... }:
    {
      options.ciPackages = lib.mkOption {
        type = lib.types.listOf lib.types.package;
        default = [ ];
        description = "Packages for CI environment";
      };
    }
  );

  config.perSystem =
    {
      config,
      pkgs,
      system,
      ...
    }:
    let
      python = pkgs.python312;

      mcpConfig =
        inputs.mcp-servers-nix.lib.mkConfig
          (import inputs.mcp-servers-nix.inputs.nixpkgs {
            inherit system;
          })
          {
            programs = {
              nixos.enable = true;
              serena.enable = true;
            };
          };
    in
    {
      ciPackages = with pkgs; [
        python312
        uv
        ruff
      ];

      packages = {
        pursuit-mcp = python.pkgs.buildPythonApplication {
          pname = "pursuit-mcp";
          version = "0.1.0";
          src = ../.;

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
          paths = config.ciPackages;
        };

        mcp-config = mcpConfig;

        default = config.packages.pursuit-mcp;
      };
    };
}
