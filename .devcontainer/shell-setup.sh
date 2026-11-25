#!/usr/bin/env bash
# Réglages du shell et de vim, proches du terminal d'examen (alias k, complétion, vim pour YAML).
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MARK="# >>> labo CKAD >>>"

if ! grep -q "$MARK" ~/.bashrc 2>/dev/null; then
  cat >> ~/.bashrc <<EOF
$MARK
export PATH="$ROOT/bin:\$PATH"
source <(kubectl completion bash)
alias k=kubectl
complete -o default -F __start_kubectl k
# Réflexes de vitesse : k run x --image=y \$do > x.yaml   ·   k delete pod x \$now
export do="--dry-run=client -o yaml"
export now="--force --grace-period 0"
# <<< labo CKAD <<<
EOF
fi

if [[ ! -f ~/.vimrc ]] || ! grep -q "labo CKAD" ~/.vimrc; then
  cat >> ~/.vimrc <<'EOF'
" labo CKAD : YAML avec 2 espaces, jamais de tabulation
set expandtab tabstop=2 shiftwidth=2 softtabstop=2 autoindent
set number ruler
syntax on
EOF
fi
mkdir -p ~/ckad ~/ckad-questions
echo "shell prêt : alias k, complétion, \$do, \$now, vim réglé pour le YAML"
