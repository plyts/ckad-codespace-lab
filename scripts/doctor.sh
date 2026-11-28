#!/usr/bin/env bash
# doctor.sh — vérifie que le labo est sain et qu'il ne contient AUCUNE IA.
# PASS = conforme · WARN = à regarder · FAIL = à corriger. Code retour 1 si un FAIL.
set -uo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
# shellcheck source=/dev/null
source versions.env
# Langue : CKAD_LANG, sinon .progress/lang (ex lang en|fr), sinon français.
if [[ -z "${CKAD_LANG:-}" && -f "$ROOT/.progress/lang" ]]; then CKAD_LANG="$(tr -d '[:space:]' < "$ROOT/.progress/lang")"; fi
L() { if [[ "${CKAD_LANG:-fr}" == en ]]; then printf '%s' "$2"; else printf '%s' "$1"; fi; }
g=$'\e[32m'; r=$'\e[31m'; y=$'\e[33m'; o=$'\e[0m'; [[ -t 1 ]] || { g=; r=; y=; o=; }
nfail=0
pass() { echo "${g}PASS${o} $*"; }
warn() { echo "${y}WARN${o} $*"; }
fail() { echo "${r}FAIL${o} $*"; nfail=$((nfail + 1)); }

echo "== $(L "Aucune IA dans le dépôt" "No AI in the repository")"
agent_files=(CLAUDE.md .claude AGENTS.md .codex GEMINI.md .gemini .cursor .cursorrules .windsurfrules
             .aider.conf.yml .aiderignore .continue .github/copilot-instructions.md .github/instructions
             .github/prompts .clinerules .roo)
found=()
for f in "${agent_files[@]}"; do [[ -e "$f" ]] && found+=("$f"); done
if ((${#found[@]})); then fail "$(L "fichiers d'agent présents :" "agent files present:") ${found[*]} $(L "(à supprimer après la construction)" "(delete them after the build)")"
else pass "$(L "aucun fichier d'agent" "no agent file") (CLAUDE.md, AGENTS.md, .codex, .cursor, copilot-instructions…)"; fi

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
[[ -z "$bad_ext" ]] && pass "$(L "aucune extension d'IA dans les devcontainers ni dans les recommandations" "no AI extension in the devcontainers or recommendations")" \
                    || fail "$(L "extensions d'IA :" "AI extensions:") $bad_ext"

if grep -q '"chat.disableAIFeatures": true' .vscode/settings.json \
   && grep -q '"chat.disableAIFeatures": true' .devcontainer/lab/devcontainer.json; then
  pass "chat.disableAIFeatures $(L "activé (espace de travail et devcontainer)" "enabled (workspace and devcontainer)")"
else fail "chat.disableAIFeatures $(L "absent de .vscode/settings.json ou du devcontainer" "missing from .vscode/settings.json or the devcontainer")"; fi

echo "== $(L "Aucune IA dans l'environnement" "No AI in the environment")"
clis=()
for c in claude codex gemini aider cursor-agent copilot; do command -v "$c" >/dev/null 2>&1 && clis+=("$c ($(command -v "$c"))"); done
if command -v gh >/dev/null 2>&1 && gh extension list 2>/dev/null | grep -qi copilot; then clis+=("gh copilot"); fi
((${#clis[@]})) && fail "$(L "agents d'IA installés :" "AI agents installed:") ${clis[*]}" || pass "$(L "aucun agent d'IA dans le PATH" "no AI agent in the PATH")"
keys=()
for v in ANTHROPIC_API_KEY OPENAI_API_KEY GEMINI_API_KEY CLAUDE_CODE_OAUTH_TOKEN; do [[ -n "${!v:-}" ]] && keys+=("$v"); done
((${#keys[@]})) && fail "$(L "clés d'API d'IA dans l'environnement :" "AI API keys in the environment:") ${keys[*]} $(L "(supprime-les des secrets Codespaces)" "(remove them from Codespaces secrets)")" \
               || pass "$(L "aucune clé d'API d'IA dans l'environnement" "no AI API key in the environment")"
ls ~/.vscode-remote/extensions 2>/dev/null | grep -qiE "$ai_ext" \
  && fail "$(L "extension d'IA installée dans VS Code :" "AI extension installed in VS Code:") $(ls ~/.vscode-remote/extensions | grep -iE "$ai_ext" | tr '\n' ' ')" \
  || pass "$(L "aucune extension d'IA installée dans VS Code distant" "no AI extension installed in remote VS Code")"

echo "== $(L "Outils aux versions figées" "Tools at pinned versions") (versions.env)"
chk() { local have; have="$($2 2>/dev/null)"; [[ "$have" == *"$3"* ]] && pass "$1 $3" || fail "$1 : $(L attendu expected) $3, $(L trouvé found) ${have:-$(L absent missing)}"; }
chk kind "kind version" "$KIND_VERSION"
chk kubectl "kubectl version --client" "$KUBECTL_VERSION"
chk helm "helm version --short" "$HELM_VERSION"
chk yq "yq --version" "$YQ_VERSION"
command -v python3 >/dev/null && pass "python3 $(python3 -V 2>&1 | cut -d' ' -f2)" || fail "python3 $(L absent missing)"
python3 -c 'import markdown' 2>/dev/null && pass "$(L "module markdown (guide HTML)" "markdown module (HTML guide)")" || warn "$(L "module markdown absent" "markdown module missing"): pip install -r docs/requirements.txt (site build)"

echo "== Clusters"
if docker info >/dev/null 2>&1; then pass "Docker $(L joignable reachable)"; else fail "Docker $(L injoignable unreachable)"; fi
for c in ckad-a ckad-b; do
  if kind get clusters 2>/dev/null | grep -qx "$c"; then
    v=$(kubectl --context "$c" version -o json 2>/dev/null | python3 -c 'import sys,json;print(json.load(sys.stdin)["serverVersion"]["gitVersion"])' 2>/dev/null)
    [[ "$v" == "$K8S_VERSION" ]] && pass "$c $(L en on) $v ($(L "version de l'examen" "exam version"))" || fail "$c : $(L serveur server) ${v:-$(L injoignable unreachable)}, $(L attendu expected) $K8S_VERSION"
  else
    [[ $c == ckad-a ]] && fail "$c $(L absent missing) : lab up a" || warn "$c $(L absent missing) (lab up b : $(L "pour s'entraîner au changement de contexte" "to practise switching contexts"))"
  fi
done
for c in $(kind get clusters 2>/dev/null); do
  grep -qx "netpol@$c=1" .progress/caps 2>/dev/null && pass "[$c] $(L "NetworkPolicy réellement appliquées" "NetworkPolicies really enforced") (lab netpol-test $c)" \
    || warn "[$c] $(L "NetworkPolicy non prouvées : contrôles de trafic en SKIP" "NetworkPolicies not proven: traffic checks SKIP") (lab netpol-test $c)"
  grep -qx "metrics@$c=1" .progress/caps 2>/dev/null && pass "[$c] metrics-server $(L installé installed) (kubectl top)" || warn "[$c] metrics-server $(L absent missing) (kubectl top)"
done

echo "== $(L "Réponses cachées" "Hidden answers")"
n_ex=$(find exercises scenarios mock-exams -name task.md 2>/dev/null | wc -l)
n_ans=$(find .answers -name solution.sh 2>/dev/null | wc -l)
[[ "$n_ex" == "$n_ans" ]] && pass "$n_ans $(L "réponses pour" "answers for") $n_ex $(L "unités (.answers/, masqué dans VS Code)" "units (.answers/, hidden in VS Code)")" \
                         || fail "$n_ex $(L "unités mais" "units but") $n_ans $(L réponses answers)"

echo
((nfail)) && { echo "${r}$nfail $(L "point(s) à corriger." "item(s) to fix.")${o}"; exit 1; } || echo "${g}$(L "Labo conforme." "Lab compliant.")${o}"
