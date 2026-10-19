{ pkgs, ... }:

{
  packages = with pkgs; [
    git
    shellcheck
    actionlint
    python3
  ];

  tasks."harness:check".exec = "bash scripts/check";
}
