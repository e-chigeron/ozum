{ pkgs, ... }:

{
  packages = with pkgs; [
    git
    shellcheck
  ];

  tasks."harness:check".exec = "bash scripts/check";
}
