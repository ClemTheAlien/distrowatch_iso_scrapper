let

  nixpkgs = fetchTarball "https://github.com/NixOS/nixpkgs/tarball/nixos-25.05";

  pkgs = import nixpkgs { config = {}; overlays = []; };

in


pkgs.mkShellNoCC {

  packages = with pkgs; [
    python3
  ];
  shellHook = ''
  source ./.venv/bin/activate
  pip install -r requirments.txt
  '';

}