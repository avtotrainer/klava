{
  description = "KLAVA typing trainer development shell";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-25.11";

  outputs = { self, nixpkgs }:
    let
      system = "x86_64-linux";
      pkgs = import nixpkgs { inherit system; };
      python = pkgs.python3.withPackages (ps: [
        ps.tkinter
      ]);
    in
    {
      devShells.${system}.default = pkgs.mkShell {
        packages = [
          python
        ];
      };
    };
}
