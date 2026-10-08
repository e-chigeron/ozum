{ pkgs, ... }:

{
  packages = with pkgs; [
    git
    shellcheck
    actionlint
  ];

  tasks."harness:check".exec = "bash scripts/check";
}
