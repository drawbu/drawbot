{
  description = "Drawbot";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";

    mach-nix.url = "github:davhau/mach-nix";
  };

  outputs = { self, nixpkgs, mach-nix, flake-utils, ... }:
    let
      appName = "drawbot";
      pythonVersion = "python310";
    in
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        mach = mach-nix.lib.${system};

        pythonApp = mach.buildPythonApplication ./.;
        pythonAppEnv = mach.mkPython {
          python = pythonVersion;
          requirements = "";
        };
        pythonAppImage = pkgs.dockerTools.buildLayeredImage {
          name = pythonApp.pname;
          contents = [ pythonApp ];
          config.Cmd = [ "${pythonApp}/bin/${appName}" ];
        };
      in
      rec
      {
        packages = {
          image = pythonAppImage;

          pythonPkg = pythonApp;
          default = packages.pythonPkg;
        };

        apps.default = {
          type = "app";
          program = "${packages.pythonPkg}/bin/${appName}";
        };

        devShells.default = pkgs.mkShell {
          packages = [ pythonAppEnv ];

          shellHook = ''
            export PYTHONPATH="${pythonAppEnv}/bin/python"
          '';
        };
      }
    );
}
