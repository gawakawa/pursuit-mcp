_: {
  perSystem = _: {
    pre-commit.settings.hooks = {
      treefmt.enable = true;
      statix.enable = true;
      deadnix.enable = true;
      actionlint.enable = true;
      ruff.enable = true;
    };
  };
}
