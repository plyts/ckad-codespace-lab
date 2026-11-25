#!/usr/bin/env bash
# À chaque démarrage du Codespace : relance les nœuds kind arrêtés par la mise en veille.
set -uo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
for i in $(seq 1 30); do docker info >/dev/null 2>&1 && break; sleep 1; done
for c in $(kind get clusters 2>/dev/null); do
  for n in $(kind get nodes --name "$c" 2>/dev/null); do
    docker start "$n" >/dev/null 2>&1 || true
  done
done
"$ROOT/bin/lab" status 2>/dev/null | head -3 || true
