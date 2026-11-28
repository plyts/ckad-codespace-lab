#!/usr/bin/env bash
# capture-docs.sh — exécute réellement les commandes montrées dans le guide et enregistre
# leurs sorties dans docs/_captures/ (aucune sortie n'est écrite à la main).
# Âges et horodatages sont masqués ; un fichier .meta indique où et quand la capture a eu lieu.
# Usage : scripts/capture-docs.sh [guide|journal|all]   (cluster ckad-a requis)
set -uo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
# shellcheck source=/dev/null
source "$ROOT/versions.env"
OUTD="$ROOT/docs/_captures"
export PATH="$ROOT/bin:$PATH"   # le guide montre « lab status », « ex check » comme dans le Codespace
cd "$ROOT"
mkdir -p "$OUTD"
CTX=ckad-a
k() { kubectl --context "$CTX" "$@"; }
what="${1:-all}"

mask() { # masque âges, horodatages, hachages de Pods et adresses variables
  sed -E \
    -e 's/[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9:.]+Z/<horodatage>/g' \
    -e 's/(Mon|Tue|Wed|Thu|Fri|Sat|Sun), [0-9]{2} [A-Z][a-z]{2} [0-9]{4} [0-9:]+ [+-][0-9]{4}/<horodatage>/g' \
    -e 's/(^|[[:space:]])([0-9]+[smhd]([0-9]+[smh])?)([[:space:]]|$)/\1<âge>\4/g' \
    -e 's/(^|[[:space:]])([0-9]+[smhd]([0-9]+[smh])?)([[:space:]]|$)/\1<âge>\4/g' \
    -e 's/\(x[0-9]+ over [0-9a-z]+\)/(xN sur <durée>)/g' \
    -e 's/\(([0-9]+[smhd])+ ago\)/(il y a <durée>)/g'
}

cap() { # nom "commande" [commande…] : exécute, masque, enregistre (commandes rejouables telles quelles)
  local name="$1"; shift
  local cmd first=1
  : > "$OUTD/$name.txt"
  for cmd in "$@"; do
    { ((first)) || echo; echo "\$ $cmd"; bash -c "$cmd" 2>&1 | mask; } >> "$OUTD/$name.txt"
    first=0
  done
  echo "  capture : $name"
}

# Supprime un Pod jetable d'une capture précédente (hors capture).
fresh() { k -n "$1" delete pod "$2" --ignore-not-found --now >/dev/null 2>&1 || true; }

meta() {
  cat > "$OUTD/$1.meta" <<EOF
capturé le $(date +%Y-%m-%d) sur $(hostname -s 2>/dev/null || echo labo) — kind $KIND_VERSION, Kubernetes $(k version -o json 2>/dev/null | python3 -c 'import sys,json;print(json.load(sys.stdin)["serverVersion"]["gitVersion"])'), contexte $CTX
EOF
}

wait_pods() { k -n "$1" wait --for=condition=Ready pod --all --timeout="${2:-120s}" >/dev/null 2>&1 || true; }

guide() {
  echo "== Captures du guide (namespace guide)"
  k delete ns guide --ignore-not-found --wait=true >/dev/null
  k create ns guide >/dev/null
  k -n guide apply -f "$ROOT/app/boutique/jour1.yaml" >/dev/null
  for d in redis api front; do k -n guide rollout status deploy/$d --timeout=180s >/dev/null; done
  cap lab-status "lab status"
  cap nodes "kubectl get nodes -o wide"
  cap contexts "kubectl config get-contexts"
  cap api-resources "kubectl api-resources --namespaced=true | head -15"
  cap explain-probe "kubectl explain pod.spec.containers.readinessProbe | head -20"
  cap explain-recursive "kubectl explain deploy.spec.strategy --recursive"
  cap run-dry "kubectl -n guide run web --image=nginx:1.27-alpine --labels=app=web --port=80 --dry-run=client -o yaml"
  cap create-deploy-dry "kubectl -n guide create deployment shop --image=nginx:1.27-alpine --replicas=3 --dry-run=client -o yaml"
  cap get-all "kubectl -n guide get deploy,rs,pods,svc -o wide"
  cap get-labels "kubectl -n guide get pods --show-labels"
  cap selector "kubectl -n guide get pods -l 'app in (api,front)' -L tier"
  cap jsonpath "kubectl -n guide get pods -o jsonpath='{range .items[*]}{.metadata.labels.app}{\"\\t\"}{.status.podIP}{\"\\n\"}{end}' | sort"
  cap custom-columns "kubectl -n guide get pods -o custom-columns=POD:.metadata.name,IMAGE:.spec.containers[0].image,NODE:.spec.nodeName | sed -E 's/-[a-z0-9]{8,10}-[a-z0-9]{5}/-<hash>/'"
  cap endpoints "kubectl -n guide get endpointslices -o wide"
  cap describe-svc "kubectl -n guide describe svc api"
  fresh guide dns-test
  cap dns "kubectl -n guide run dns-test --image=busybox:1.37 --restart=Never -- nslookup api.guide.svc.cluster.local && kubectl -n guide wait --for=jsonpath='{.status.phase}'=Succeeded pod/dns-test --timeout=60s" "kubectl -n guide logs dns-test"
  fresh guide http-test
  cap http-api "kubectl -n guide run http-test --image=busybox:1.37 --restart=Never -- wget -qO- http://api && kubectl -n guide wait --for=jsonpath='{.status.phase}'=Succeeded pod/http-test --timeout=60s" "kubectl -n guide logs http-test"
  # Rolling update réel, historique, rollback
  k -n guide annotate deploy front kubernetes.io/change-cause="v1 nginx 1.27" --overwrite >/dev/null
  k -n guide set image deploy/front front=nginx:1.28-alpine >/dev/null
  k -n guide annotate deploy front kubernetes.io/change-cause="passage en 1.28" --overwrite >/dev/null
  k -n guide rollout status deploy/front --timeout=120s >/dev/null
  cap rollout-history "kubectl -n guide rollout history deploy/front"
  cap rollout-undo "kubectl -n guide rollout undo deploy/front && kubectl -n guide rollout status deploy/front --timeout=120s"
  cap rs-after-undo "kubectl -n guide get rs -l app=front -o custom-columns=RS:.metadata.name,DESIRED:.spec.replicas,IMAGE:.spec.template.spec.containers[0].image | sed -E 's/-[a-z0-9]{8,10}( |$)/-<hash>\1/'"
  cap scale "kubectl -n guide scale deploy api --replicas=3 && kubectl -n guide rollout status deploy/api --timeout=120s"
  cap logs "kubectl -n guide logs deploy/front --tail=3"
  cap exec "kubectl -n guide exec deploy/front -- nginx -v"
  cap events "kubectl -n guide get events --sort-by=.lastTimestamp | tail -6"
  cap auth-can-i "kubectl auth can-i create deployments -n guide --as=system:serviceaccount:guide:default; kubectl auth can-i --list -n guide --as=system:serviceaccount:guide:default | head -8"
  cap check-fail "ex start d1-01 >/dev/null && ex check d1-01 | sed -n 1,14p"
  cap check-pass "kubectl -n d1-01 run web --image=nginx:1.27-alpine --labels=app=web --port=80 && kubectl -n d1-01 wait --for=condition=Ready pod/web --timeout=90s" "ex check d1-01 | tail -9"
  cap netpol-test "lab netpol-test ckad-a"
  # Mêmes sorties du labo en anglais (ex lang en), pour la version anglaise du guide.
  (
    export CKAD_LANG=en
    cap lab-status.en "lab status"
    k delete ns d1-01 --ignore-not-found --wait=true >/dev/null
    cap check-fail.en "ex start d1-01 >/dev/null && ex check d1-01 | sed -n 1,14p"
    cap check-pass.en "kubectl -n d1-01 run web --image=nginx:1.27-alpine --labels=app=web --port=80 && kubectl -n d1-01 wait --for=condition=Ready pod/web --timeout=90s" "ex check d1-01 | tail -9"
    cap netpol-test.en "lab netpol-test ckad-a"
  )
  meta guide
  k delete ns d1-01 --wait=false >/dev/null 2>&1 || true
}

journal() {
  echo "== Journal des erreurs : pannes provoquées volontairement (namespace journal)"
  local ns=journal
  k delete ns $ns --ignore-not-found --wait=true >/dev/null
  k create ns $ns >/dev/null
  until k -n $ns get sa default >/dev/null 2>&1; do sleep 1; done
  k -n $ns run crash --image=busybox:1.37 -- sh -c 'echo démarrage; exit 1'
  k -n $ns run pull --image=nginx:1.99-nexistepas
  k -n $ns create configmap app-cfg --from-literal=MODE=prod >/dev/null
  k -n $ns run cfgerr --image=busybox:1.37 --overrides='{"spec":{"containers":[{"name":"cfgerr","image":"busybox:1.37","command":["sleep","3600"],"env":[{"name":"DB","valueFrom":{"configMapKeyRef":{"name":"app-cfg","key":"DB_HOST"}}}]}]}}'
  k -n $ns run pending --image=nginx:1.27-alpine --overrides='{"spec":{"containers":[{"name":"pending","image":"nginx:1.27-alpine","resources":{"requests":{"cpu":"64"}}}]}}'
  k -n $ns run oom --image=busybox:1.37 --overrides='{"spec":{"containers":[{"name":"oom","image":"busybox:1.37","command":["sh","-c","head -c 200m /dev/zero | tail"],"resources":{"limits":{"memory":"32Mi"}}}]}}'
  k -n $ns run mount --image=busybox:1.37 --overrides='{"spec":{"volumes":[{"name":"s","secret":{"secretName":"absent"}}],"containers":[{"name":"mount","image":"busybox:1.37","command":["sleep","3600"],"volumeMounts":[{"name":"s","mountPath":"/s"}]}]}}'
  k -n $ns create deployment web --image=nginx:1.27-alpine >/dev/null
  k -n $ns create service clusterip web-mauvais --tcp=80:80 >/dev/null     # sélecteur app=web-mauvais : aucun Pod
  k -n $ns expose deploy web --name=web-port --port=80 --target-port=8080 >/dev/null
  k -n $ns rollout status deploy/web --timeout=120s >/dev/null
  # Laisser le temps aux pannes de se manifester (redémarrages, back-off)
  for i in $(seq 1 60); do
    k -n $ns get pod crash --no-headers 2>/dev/null | grep -q CrashLoopBackOff \
      && k -n $ns get pod oom -o jsonpath='{.status.containerStatuses[0].lastState.terminated.reason}' 2>/dev/null | grep -q OOMKilled \
      && k -n $ns get pod pull --no-headers 2>/dev/null | grep -q ImagePullBackOff && break
    sleep 3
  done
  cap err-overview "kubectl -n $ns get pods"
  cap err-crashloop "kubectl -n $ns get pod crash" "kubectl -n $ns describe pod crash | sed -n '/^Containers:/,/^Conditions:/p' | grep -E 'State|Reason|Exit Code|Restart Count'" "kubectl -n $ns logs crash"
  cap err-imagepull "kubectl -n $ns describe pod pull | sed -n '/^Events:/,\$p' | tail -6"
  cap err-configerror "kubectl -n $ns describe pod cfgerr | grep -E 'Reason|Error|couldn|not found' | head -5"
  cap err-pending "kubectl -n $ns describe pod pending | sed -n '/^Events:/,\$p'"
  cap err-oomkilled "kubectl -n $ns get pod oom -o jsonpath='{.status.containerStatuses[0].lastState.terminated}' | python3 -m json.tool | grep -E 'reason|exitCode'"
  cap err-failedmount "kubectl -n $ns describe pod mount | sed -n '/^Events:/,\$p' | tail -3"
  cap err-forbidden "kubectl -n $ns get secrets --as=system:serviceaccount:$ns:default"
  cap err-invalid "printf 'apiVersion: v1\nkind: Pod\nmetadata:\n  name: bad\nspec:\n  containers:\n  - name: bad\n    image: nginx\n    ports:\n    - containerPort: \"quatre-vingts\"\n' | kubectl -n $ns apply -f -"
  cap err-yaml "printf 'apiVersion: v1\nkind: Pod\nmetadata:\n  name: bad\nspec:\n containers:\n  - name: bad\n   image: nginx\n' | kubectl -n $ns apply -f -"
  cap err-noendpoints "kubectl -n $ns get endpointslices -l kubernetes.io/service-name=web-mauvais; kubectl -n $ns describe svc web-mauvais | grep -E 'Selector|Endpoints'"
  fresh $ns t
  cap err-refused "kubectl -n $ns get endpointslices -l kubernetes.io/service-name=web-port" "kubectl -n $ns run t --image=busybox:1.37 --restart=Never -- wget -qO- -T 3 http://web-port && kubectl -n $ns wait --for=jsonpath='{.status.phase}'=Failed pod/t --timeout=60s" "kubectl -n $ns logs t"
  if grep -qx "netpol@$CTX=1" "$ROOT/.progress/caps" 2>/dev/null; then
    k -n $ns apply -f - >/dev/null <<'EOF'
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata: {name: trop-stricte}
spec:
  podSelector: {}
  policyTypes: [Egress]
EOF
    fresh $ns t2
    cap err-netpol "kubectl -n $ns get netpol trop-stricte -o yaml | yq .spec" "kubectl -n $ns run t2 --image=busybox:1.37 --restart=Never -- wget -qO- -T 3 http://web && kubectl -n $ns wait --for=jsonpath='{.status.phase}'=Failed pod/t2 --timeout=60s" "kubectl -n $ns logs t2"
  else
    echo "\$ (non capturé : ce cluster n'applique pas les NetworkPolicy — voir lab netpol-test)" > "$OUTD/err-netpol.txt"
  fi
  meta journal
  k delete ns $ns --wait=false >/dev/null
}

case "$what" in
  guide) guide ;;
  journal) journal ;;
  all) guide; journal ;;
esac
