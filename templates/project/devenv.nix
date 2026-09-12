{ pkgs, ... }:

{
  packages = with pkgs; [
    git
    shellcheck
  ];

  tasks."project:verify".exec = "bash scripts/verify-project";
}
