{ pkgs, ... }:

{
  packages = with pkgs; [
    git
    shellcheck
    sqlite
  ];

  tasks."harness:check".exec = "bash scripts/check";
}
