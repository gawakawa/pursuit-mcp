{ flake-parts-lib, ... }:
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
    { config, pkgs, ... }:
    {
      ciPackages = [ pkgs.uv ];

      packages = {
        ci = pkgs.buildEnv {
          name = "ci";
          paths = config.ciPackages;
        };

        default =
          pkgs.runCommand "pursuit-mcp"
            {
              nativeBuildInputs = [ pkgs.makeWrapper ];
            }
            ''
              mkdir -p $out/bin
              makeWrapper ${config.prodVirtualenv}/bin/pursuit-mcp $out/bin/pursuit-mcp \
                --unset PYTHONPATH
            '';
      };
    };
}
