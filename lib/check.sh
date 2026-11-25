# lib/check.sh — API de vérification des exercices (sourcée par chaque check.sh).
#
# Un contrôle vérifie l'ÉTAT du cluster, jamais la méthode : toute réponse valide passe.
# Chaque contrôle en échec affiche : attendu, trouvé, pourquoi, commande de diagnostic, doc.
#
# Variables fournies par le lanceur (ex / mock / selftest) :
#   CTX         contexte kubectl de l'exercice (ckad-a, ckad-b)
#   NS          namespace principal de l'exercice
#   DOC         lien de documentation par défaut
#   CHECK_WAIT  secondes pendant lesquelles un contrôle réessaie avant d'échouer (défaut 3)
#   OUT         dossier des fichiers réponse (~/ckad/<id>)
#
# Fonctions :
#   ck_eq    "titre" "attendu" 'commande'  "pourquoi" "diagnostic" [doc]
#   ck_match "titre" 'regex'   'commande'  "pourquoi" "diagnostic" [doc]
#   ck_true  "titre" 'commande (code retour 0 = OK)' "pourquoi" "diagnostic" [doc]
#   ck_http  "titre" "ns" "labels" "url" 'regex attendue' "pourquoi" "diagnostic" [doc]
#            (url peut commencer par des options wget : "--header=Host:x.lab.local http://traefik.traefik.svc/")
#   ck_http_blocked "titre" "ns" "labels" "url" "pourquoi" "diagnostic" [doc]
# Raccourcis : k (kubectl sur $CTX), kn (kubectl sur $CTX -n $NS), jp KIND NOM JSONPATH [ns]

CHECK_WAIT="${CHECK_WAIT:-3}"
CTX="${CTX:-ckad-a}"
NS="${NS:-default}"
OUT="${OUT:-$HOME/ckad/unknown}"
_ck_n=0; _ck_pass=0; _ck_skip=0
# Capacités mesurées par "lab up" / "lab netpol-test" (fichier .progress/caps).
CAPS_FILE="${CAPS_FILE:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)/.progress/caps}"
cap() { grep -qx "$1@$CTX=1" "$CAPS_FILE" 2>/dev/null; }   # capacité mesurée sur CE cluster

if [[ -t 1 && -z "${NO_COLOR:-}" ]]; then
  _g=$'\e[32m'; _r=$'\e[31m'; _y=$'\e[33m'; _d=$'\e[90m'; _b=$'\e[1m'; _o=$'\e[0m'
else
  _g=; _r=; _y=; _d=; _b=; _o=
fi

k()  { kubectl --context "$CTX" "$@"; }
kn() { kubectl --context "$CTX" -n "$NS" "$@"; }
# jp KIND NOM JSONPATH [namespace] : valeur d'un champ, vide si la ressource n'existe pas.
jp() { kubectl --context "$CTX" -n "${4:-$NS}" get "$1" "$2" -o "jsonpath=$3" 2>/dev/null; }

_ck_report() { # ok titre attendu trouvé pourquoi diag doc   (ok : 1, 0 ou skip)
  local ok="$1" title="$2" exp="$3" found="$4" why="$5" diag="$6" doc="${7:-$DOC}"
  _ck_n=$((_ck_n + 1))
  if [[ "$ok" == skip ]]; then
    _ck_skip=$((_ck_skip + 1))
    printf '%sSKIP%s  %d. %s\n      %s%s%s\n' "$_d" "$_o" "$_ck_n" "$title" "$_d" "$exp" "$_o"
  elif [[ "$ok" == 1 ]]; then
    _ck_pass=$((_ck_pass + 1))
    printf '%sPASS%s  %d. %s\n' "$_g" "$_o" "$_ck_n" "$title"
  else
    printf '%sFAIL%s  %d. %s\n' "$_r" "$_o" "$_ck_n" "$title"
    printf '      %sattendu%s    : %s\n' "$_b" "$_o" "$exp"
    printf '      %strouvé%s     : %s\n' "$_b" "$_o" "${found:-<rien>}"
    printf '      %spourquoi%s   : %s\n' "$_b" "$_o" "$why"
    printf '      %sdiagnostic%s : %s\n' "$_b" "$_o" "$diag"
    [[ -n "$doc" ]] && printf '      %sdoc%s        : %s\n' "$_b" "$_o" "$doc"
  fi
}

# Réessaie une évaluation pendant CHECK_WAIT secondes (les contrôleurs ont besoin de temps).
_ck_retry() { # fonction-de-test
  local deadline=$((SECONDS + CHECK_WAIT))
  while :; do
    "$@" && return 0
    (( SECONDS >= deadline )) && return 1
    sleep 2
  done
}

_ck_found=""
_t_eq()    { _ck_found="$(eval "$_ck_cmd" 2>/dev/null)"; [[ "$_ck_found" == "$_ck_exp" ]]; }
_t_match() { _ck_found="$(eval "$_ck_cmd" 2>/dev/null)"; [[ "$_ck_found" =~ $_ck_exp ]]; }
_t_true()  { _ck_found="$(eval "$_ck_cmd" 2>&1 | tail -3 | tr '\n' ' ')"; eval "$_ck_cmd" >/dev/null 2>&1; }

ck_eq() {
  _ck_exp="$2"; _ck_cmd="$3"
  if _ck_retry _t_eq; then _ck_report 1 "$1"; else _ck_report 0 "$1" "$2" "$_ck_found" "$4" "$5" "${6:-}"; fi
}
ck_match() {
  _ck_exp="$2"; _ck_cmd="$3"
  if _ck_retry _t_match; then _ck_report 1 "$1"; else _ck_report 0 "$1" "valeur correspondant à /$2/" "$_ck_found" "$4" "$5" "${6:-}"; fi
}
ck_true() {
  _ck_cmd="$2"
  if _ck_retry _t_true; then _ck_report 1 "$1"; else _ck_report 0 "$1" "la condition est vraie : $2" "${_ck_found:-condition fausse}" "$3" "$4" "${5:-}"; fi
}

# Pod client jetable, avec des labels donnés, dans un namespace donné : simule un vrai appelant.
_probe_pod=""
_probe_start() { # ns labels
  local ns="$1" labels="$2"
  _probe_pod="ck-probe-$RANDOM$RANDOM"
  kubectl --context "$CTX" -n "$ns" run "$_probe_pod" --image=busybox:1.37 --restart=Never \
    ${labels:+--labels="$labels"} --command -- sleep 120 >/dev/null 2>&1 || return 1
  kubectl --context "$CTX" -n "$ns" wait --for=condition=Ready "pod/$_probe_pod" --timeout=60s >/dev/null 2>&1
}
_probe_stop() { kubectl --context "$CTX" -n "$1" delete pod "$_probe_pod" --now --wait=false >/dev/null 2>&1 || true; }
_probe_get() { # ns "url" — l'url peut être précédée d'options wget, ex. "--header=Host:shop.lab.local http://…"
  # shellcheck disable=SC2086
  kubectl --context "$CTX" -n "$1" exec "$_probe_pod" -- wget -qO- -T 3 $2 2>&1
}

ck_http() { # titre ns labels url regex pourquoi diag [doc]
  local title="$1" ns="$2" labels="$3" url="$4" re="$5" body="" ok=0 deadline
  if _probe_start "$ns" "$labels"; then
    deadline=$((SECONDS + CHECK_WAIT))
    while :; do
      body="$(_probe_get "$ns" "$url" | head -c 300 | tr '\n' ' ')"
      [[ "$body" =~ $re ]] && { ok=1; break; }
      (( SECONDS >= deadline )) && break
      sleep 2
    done
  else
    body="impossible de démarrer le pod client dans le namespace $ns"
  fi
  _probe_stop "$ns"
  if [[ $ok == 1 ]]; then _ck_report 1 "$title"
  else _ck_report 0 "$title" "réponse HTTP de $url contenant /$re/" "$body" "$6" "$7" "${8:-}"; fi
}

ck_http_blocked() { # titre ns labels url pourquoi diag [doc]
  local title="$1" ns="$2" labels="$3" url="$4" body="" ok=0 deadline
  if ! cap netpol; then
    _ck_report skip "$title" "non vérifiable : ce cluster n'applique pas les NetworkPolicy (voir lab netpol-test)"
    return 0
  fi
  if _probe_start "$ns" "$labels"; then
    deadline=$((SECONDS + CHECK_WAIT))
    while :; do
      if body="$(_probe_get "$ns" "$url")"; then body="$(echo "$body" | head -c 200 | tr '\n' ' ')"; else ok=1; break; fi
      (( SECONDS >= deadline )) && break
      sleep 2
    done
  else
    body="impossible de démarrer le pod client dans le namespace $ns"
  fi
  _probe_stop "$ns"
  if [[ $ok == 1 ]]; then _ck_report 1 "$title"
  else _ck_report 0 "$title" "connexion vers $url refusée ou expirée" "réponse reçue : $body" "$5" "$6" "${7:-}"; fi
}

# Appelée automatiquement à la fin du check.sh (trap) : ligne lue par le lanceur.
_ck_summary() { echo "RESULT pass=$_ck_pass total=$_ck_n skip=$_ck_skip"; }
trap _ck_summary EXIT
