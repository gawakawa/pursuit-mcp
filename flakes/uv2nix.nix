{
  inputs,
  flake-parts-lib,
  ...
}:
let
  inherit (flake-parts-lib) mkPerSystemOption;
in
{
  options.perSystem = mkPerSystemOption (
    { lib, ... }:
    {
      options = {
        python = lib.mkOption {
          type = lib.types.package;
          description = "Python interpreter to use";
        };
        devVirtualenv = lib.mkOption {
          type = lib.types.package;
          description = "Development virtualenv with editable install";
        };
        prodVirtualenv = lib.mkOption {
          type = lib.types.package;
          description = "Production virtualenv";
        };
      };
    }
  );

  config.perSystem =
    { pkgs, lib, ... }:
    let
      workspace = inputs.uv2nix.lib.workspace.loadWorkspace { workspaceRoot = ../.; };

      overlay = workspace.mkPyprojectOverlay {
        sourcePreference = "wheel";
      };

      editableOverlay = workspace.mkEditablePyprojectOverlay {
        root = "$REPO_ROOT";
      };

      python = pkgs.python312;

      pythonSet =
        (pkgs.callPackage inputs.pyproject-nix.build.packages { inherit python; }).overrideScope
          (
            lib.composeManyExtensions [
              inputs.pyproject-build-systems.overlays.default
              overlay
            ]
          );

      editablePythonSet = pythonSet.overrideScope editableOverlay;
    in
    {
      inherit python;

      devVirtualenv = editablePythonSet.mkVirtualEnv "pursuit-mcp-dev" workspace.deps.all;

      prodVirtualenv = pythonSet.mkVirtualEnv "pursuit-mcp" workspace.deps.default;
    };
}
