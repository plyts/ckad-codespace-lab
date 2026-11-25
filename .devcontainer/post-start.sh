#!/usr/bin/env bash
# À chaque démarrage du Codespace : relance les nœuds kind arrêtés par la mise en veille.
set -uo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
for i in $(seq 1 30); do docker info >/dev/null 2>&1 && break; sleep 1; done
"$ROOT/bin/lab" wake || true
"$ROOT/bin/lab" status 2>/dev/null | head -3 || true
