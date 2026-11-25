#!/usr/bin/env bash
# Installe les outils du labo aux versions figées de versions.env (idempotent).
# Utilisé par les deux configurations Codespaces (lab, exam) et par GitHub Actions.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
# shellcheck source=/dev/null
source "$ROOT/versions.env"
ARCH="$(uname -m)"; case "$ARCH" in x86_64) ARCH=amd64 ;; aarch64|arm64) ARCH=arm64 ;; esac
BIN="${BIN_DIR:-/usr/local/bin}"
SUDO=""; [[ -w "$BIN" ]] || SUDO="sudo"

need() { # nom version-attendue commande-version
  local have
  have="$($3 2>/dev/null || true)"
  [[ "$have" == *"$2"* ]]
}

if ! need kind "$KIND_VERSION" "kind version"; then
  echo "==> kind $KIND_VERSION"
  $SUDO curl -fsSLo "$BIN/kind" "https://github.com/kubernetes-sigs/kind/releases/download/$KIND_VERSION/kind-linux-$ARCH"
  $SUDO chmod +x "$BIN/kind"
fi
if ! need kubectl "$KUBECTL_VERSION" "kubectl version --client"; then
  echo "==> kubectl $KUBECTL_VERSION"
  $SUDO curl -fsSLo "$BIN/kubectl" "https://dl.k8s.io/release/$KUBECTL_VERSION/bin/linux/$ARCH/kubectl"
  $SUDO chmod +x "$BIN/kubectl"
fi
if ! need helm "$HELM_VERSION" "helm version --short"; then
  echo "==> helm $HELM_VERSION"
  tmp="$(mktemp -d)"
  curl -fsSL "https://get.helm.sh/helm-$HELM_VERSION-linux-$ARCH.tar.gz" | tar -xz -C "$tmp"
  $SUDO install -m 0755 "$tmp/linux-$ARCH/helm" "$BIN/helm"
  rm -rf "$tmp"
fi
if ! need yq "$YQ_VERSION" "yq --version"; then
  echo "==> yq $YQ_VERSION (présent à l'examen)"
  $SUDO curl -fsSLo "$BIN/yq" "https://github.com/mikefarah/yq/releases/download/$YQ_VERSION/yq_linux_$ARCH"
  $SUDO chmod +x "$BIN/yq"
fi
echo "outils : kind $(kind version | awk '{print $2}') · kubectl $KUBECTL_VERSION · helm $(helm version --short) · yq $YQ_VERSION"
