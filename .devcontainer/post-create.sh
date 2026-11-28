#!/usr/bin/env bash
# Lancé une fois à la création du Codespace : outils, shell, cluster ckad-a.
# MODE=exam ajoute le bureau "comme à l'examen" (terminal + Firefox).
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

bash .devcontainer/install-tools.sh
bash .devcontainer/shell-setup.sh
python3 -m pip install --quiet --disable-pip-version-check -r docs/requirements.txt || \
  echo "WARN : module markdown non installé (le guide HTML ne se construira pas) / markdown module not installed (the HTML guide will not build)"

if [[ "${MODE:-lab}" == "exam" ]]; then
  # Bureau Linux comme à l'examen : un terminal et Firefox (docs autorisées seulement, à toi de t'y tenir).
  sudo apt-get update -qq
  sudo DEBIAN_FRONTEND=noninteractive apt-get install -y -qq xfce4-terminal firefox-esr >/dev/null
fi

# Le cluster principal ; ckad-b se crée à la demande (lab up b) pour économiser le quota.
bin/lab up a || echo "WARN : cluster non créé, relance / cluster not created, rerun: lab up a"
bash scripts/doctor.sh || true
echo
echo "Labo prêt. Commence par : ex list   puis   ex start d1-01"
echo "Lab ready. In English: ex lang en   then   ex list   and   ex start d1-01"
