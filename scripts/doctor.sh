#!/usr/bin/env bash
# doctor.sh — vérifie que le labo est sain et qu'il ne contient AUCUNE IA.
# PASS = conforme · WARN = à regarder · FAIL = à corriger. Code retour 1 si un FAIL.
set -uo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
# shellcheck source=/dev/null
source versions.env
g=$'\e[32m'; r=$'\e[31m'; y=$'\e[33m'; o=$'\e[0m'; [[ -t 1 ]] || { g=; r=; y=; o=; }
nfail=0
pass() { echo "${g}PASS${o} $*"; }
warn() { echo "${y}WARN${o} $*"; }
fail() { echo "${r}FAIL${o} $*"; nfail=$((nfail + 1)); }

echo "== Aucune IA dans le dépôt"
agent_files=(CLAUDE.md .claude AGENTS.md .codex GEMINI.md .gemini .cursor .cursorrules .windsurfrules
             .aider.conf.yml .aiderignore .continue .github/copilot-instructions.md .github/instructions
             .github/prompts .clinerules .roo)
found=()
for f in "${agent_files[@]}"; do [[ -e "$f" ]] && found+=("$f"); done
if ((${#found[@]})); then fail "fichiers d'agent présents : ${found[*]} (à supprimer après la construction)"
else pass "aucun fichier d'agent (CLAUDE.md, AGENTS.md, .codex, .cursor, copilot-instructions…)"; fi

ai_ext='copilot|claude|anthropic|codex|openai|chatgpt|continue\.|cody|tabnine|codeium|gemini|windsurf|cline'
if grep -hoE '"[a-z0-9-]+\.[a-z0-9.-]+"' .devcontainer/*/devcontainer.json .vscode/extensions.json 2>/dev/null \
   | sed -n '/recommendations/,$p' >/dev/null; then :; fi
bad_ext=$(python3 - <<'EOF'
import json, re, glob
bad = re.compile(r"copilot|claude|anthropic|codex|openai|chatgpt|continue\.|cody|tabnine|codeium|gemini|windsurf|cline", re.I)
out = []
for f in glob.glob(".devcontainer/*/devcontainer.json") + [".vscode/extensions.json"]:
    txt = re.sub(r"^\s*//.*$", "", open(f).read(), flags=re.M)
    data = json.loads(txt)
    exts = data.get("recommendations", []) + data.get("customizations", {}).get("vscode", {}).get("extensions", [])
    out += [f"{f}:{e}" for e in exts if bad.search(e)]
print(" ".join(out))
EOF
)
[[ -z "$bad_ext" ]] && pass "aucune extension d'IA dans les devcontainers ni dans les recommandations" \
                    || fail "extensions d'IA : $bad_ext"

if grep -q '"chat.disableAIFeatures": true' .vscode/settings.json \
   && grep -q '"chat.disableAIFeatures": true' .devcontainer/lab/devcontainer.json; then
  pass "chat.disableAIFeatures activé (espace de travail et devcontainer)"
else fail "chat.disableAIFeatures absent de .vscode/settings.json ou du devcontainer"; fi

echo "== Aucune IA dans l'environnement"
clis=()
for c in claude codex gemini aider cursor-agent copilot; do command -v "$c" >/dev/null 2>&1 && clis+=("$c ($(command -v "$c"))"); done
if command -v gh >/dev/null 2>&1 && gh extension list 2>/dev/null | grep -qi copilot; then clis+=("gh copilot"); fi
((${#clis[@]})) && fail "agents d'IA installés : ${clis[*]}" || pass "aucun agent d'IA dans le PATH"
keys=()
for v in ANTHROPIC_API_KEY OPENAI_API_KEY GEMINI_API_KEY CLAUDE_CODE_OAUTH_TOKEN; do [[ -n "${!v:-}" ]] && keys+=("$v"); done
((${#keys[@]})) && fail "clés d'API d'IA dans l'environnement : ${keys[*]} (supprime-les des secrets Codespaces)" \
               || pass "aucune clé d'API d'IA dans l'environnement"
ls ~/.vscode-remote/extensions 2>/dev/null | grep -qiE "$ai_ext" \
  && fail "extension d'IA installée dans VS Code : $(ls ~/.vscode-remote/extensions | grep -iE "$ai_ext" | tr '\n' ' ')" \
  || pass "aucune extension d'IA installée dans VS Code distant"

echo "== Outils aux versions figées (versions.env)"
chk() { local have; have="$($2 2>/dev/null)"; [[ "$have" == *"$3"* ]] && pass "$1 $3" || fail "$1 : attendu $3, trouvé ${have:-absent}"; }
chk kind "kind version" "$KIND_VERSION"
chk kubectl "kubectl version --client" "$KUBECTL_VERSION"
chk helm "helm version --short" "$HELM_VERSION"
chk yq "yq --version" "$YQ_VERSION"
command -v python3 >/dev/null && pass "python3 $(python3 -V 2>&1 | cut -d' ' -f2)" || fail "python3 absent"

echo "== Clusters"
if docker info >/dev/null 2>&1; then pass "Docker joignable"; else fail "Docker injoignable"; fi
for c in ckad-a ckad-b; do
  if kind get clusters 2>/dev/null | grep -qx "$c"; then
    v=$(kubectl --context "$c" version -o json 2>/dev/null | python3 -c 'import sys,json;print(json.load(sys.stdin)["serverVersion"]["gitVersion"])' 2>/dev/null)
    [[ "$v" == "$K8S_VERSION" ]] && pass "$c en $v (version de l'examen)" || fail "$c : serveur ${v:-injoignable}, attendu $K8S_VERSION"
  else
    [[ $c == ckad-a ]] && fail "$c absent : lab up a" || warn "$c absent (lab up b pour s'entraîner au changement de contexte)"
  fi
done
if [[ -f .progress/caps ]]; then
  grep -qx netpol=1 .progress/caps && pass "NetworkPolicy réellement appliquées (lab netpol-test)" \
    || warn "NetworkPolicy non appliquées sur ce cluster : contrôles réseau en SKIP (lab netpol-test)"
  grep -qx metrics=1 .progress/caps && pass "metrics-server installé (kubectl top)" || warn "metrics-server absent (kubectl top)"
else warn "capacités non mesurées : lab netpol-test"; fi

echo "== Réponses cachées"
n_ex=$(find exercises scenarios mock-exams -name task.md 2>/dev/null | wc -l)
n_ans=$(find .answers -name solution.sh 2>/dev/null | wc -l)
[[ "$n_ex" == "$n_ans" ]] && pass "$n_ans réponses pour $n_ex unités (.answers/, masqué dans VS Code)" \
                         || fail "$n_ex unités mais $n_ans réponses"

echo
((nfail)) && { echo "${r}$nfail point(s) à corriger.${o}"; exit 1; } || echo "${g}Labo conforme.${o}"
