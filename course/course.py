"""Cours complet CKAD — données bilingues (fr/en) du cours publié dans le guide HTML.

Chaque notion :
  id, title{fr,en}, text{fr,en}   explication
  cmd      commandes (communes aux deux langues), affichées telles quelles
  run      script exécuté par scripts/verify-course.py (True = cmd lui-même ; chaîne = script dédié ;
           None = illustratif, non exécuté — signalé comme tel dans le guide)
  yaml     manifeste validé par le serveur d'API (kubectl apply --dry-run=server -n cours)
  requires capacité nécessaire (« metrics », « netpol ») : sinon la vérification est SKIP
  trap{fr,en}  piège ; exam{fr,en}  conseil d'examen
Tout s'exécute dans le namespace « cours » (et « cours-b ») du contexte ckad-a.
"""

CHAPTERS = []


def chapter(cid, color, title, intro):
    CHAPTERS.append({"id": cid, "color": color, "title": title, "intro": intro, "concepts": []})


def concept(cid, title, text, cmd=None, run=True, yaml=None, trap=None, exam=None, requires=None):
    CHAPTERS[-1]["concepts"].append({"id": cid, "title": title, "text": text, "cmd": cmd, "run": run,
                                     "yaml": yaml, "trap": trap, "exam": exam, "requires": requires})


def T(fr, en):
    return {"fr": fr, "en": en}


# =====================================================================================================
chapter("bases", "gris", T("0 · Les bases", "0 · Foundations"), T(
    "Ce que tout le reste suppose : le cluster, kubectl, les contextes, la documentation intégrée, "
    "et les deux façons de créer des objets.",
    "What everything else assumes: the cluster, kubectl, contexts, the built-in documentation, "
    "and the two ways to create objects."))

concept("architecture", T("Architecture d'un cluster", "Cluster architecture"), T(
    "Le **control-plane** porte l'API server (seul point d'entrée), etcd (la base d'état), le scheduler "
    "(qui choisit un nœud pour chaque Pod) et le controller-manager (les boucles de réconciliation). Chaque "
    "**nœud** exécute le kubelet (qui démarre les conteneurs via le runtime, ici containerd) et kube-proxy "
    "(les règles des Services). Tu décris un état voulu ; les contrôleurs font converger l'état réel.",
    "The **control plane** runs the API server (the only entry point), etcd (the state store), the scheduler "
    "(which picks a node for each Pod) and the controller manager (reconciliation loops). Every **node** runs "
    "the kubelet (which starts containers through the runtime, containerd here) and kube-proxy (Service rules). "
    "You declare a desired state; controllers converge the real state towards it."),
    cmd=r"""
kubectl cluster-info
kubectl get nodes -o wide
kubectl get pods -n kube-system -o wide
""",
    exam=T("Tu n'administres pas le cluster au CKAD (c'est le CKA) : tu dois seulement savoir où regarder.",
           "You do not administer the cluster in the CKAD (that is the CKA): you only need to know where to look."))

concept("contexts", T("Contextes et namespaces", "Contexts and namespaces"), T(
    "Un **contexte** associe un cluster, un utilisateur et un namespace par défaut, dans le kubeconfig "
    "(`~/.kube/config`). Un **namespace** isole les noms et porte quotas, RBAC et NetworkPolicy. Chaque "
    "tâche d'examen impose son contexte et son namespace.",
    "A **context** binds a cluster, a user and a default namespace in the kubeconfig (`~/.kube/config`). "
    "A **namespace** scopes names and carries quotas, RBAC and NetworkPolicies. Every exam task imposes "
    "its context and namespace."),
    cmd=r"""
kubectl config get-contexts
kubectl config current-context
kubectl config use-context ckad-a
kubectl create namespace cours --dry-run=client -o yaml | kubectl apply -f -
kubectl config set-context --current --namespace=cours   # namespace par défaut / default namespace
kubectl config view --minify | grep namespace
kubectl config set-context --current --namespace=default
kubectl get pods -A | head -5                            # tous les namespaces / all namespaces
""",
    trap=T("Une tâche parfaite sur le mauvais cluster vaut 0. Lis l'en-tête, change de contexte, vérifie.",
           "A perfect answer on the wrong cluster scores 0. Read the header, switch context, check."),
    exam=T("Préfère `-n <ns>` explicite à chaque commande : moins de surprises qu'un namespace par défaut oublié.",
           "Prefer an explicit `-n <ns>` on every command: fewer surprises than a forgotten default namespace."))

concept("explain", T("Documentation intégrée : explain, api-resources", "Built-in docs: explain, api-resources"), T(
    "`kubectl explain` donne le schéma de n'importe quel champ, avec sa version d'API. `api-resources` liste "
    "les types, leurs noms courts, leur groupe et s'ils sont dans un namespace. C'est plus rapide que de "
    "chercher dans le navigateur.",
    "`kubectl explain` prints the schema of any field, with its API version. `api-resources` lists types, "
    "short names, groups and whether they are namespaced. Faster than searching in the browser."),
    cmd=r"""
kubectl explain pod.spec.containers.livenessProbe
kubectl explain deployment.spec.strategy --recursive
kubectl api-resources --namespaced=true | head
kubectl api-resources --api-group=apps
kubectl api-versions | grep -E '^(apps|batch|networking)'
""")

concept("imperative", T("Impératif, déclaratif et --dry-run", "Imperative, declarative and --dry-run"), T(
    "Les commandes **impératives** (`run`, `create`, `expose`, `set`, `scale`) sont les plus rapides. "
    "Le **déclaratif** (`apply -f`) est reproductible. Le geste d'examen combine les deux : générer le YAML "
    "avec `--dry-run=client -o yaml`, le retoucher dans vim, puis `apply`. `--dry-run=server` fait valider "
    "par l'API sans rien créer. `replace --force` supprime et recrée (champs immuables).",
    "**Imperative** commands (`run`, `create`, `expose`, `set`, `scale`) are the fastest. **Declarative** "
    "(`apply -f`) is reproducible. The exam move combines both: generate YAML with `--dry-run=client -o yaml`, "
    "edit it in vim, then `apply`. `--dry-run=server` validates against the API without creating anything. "
    "`replace --force` deletes and recreates (immutable fields)."),
    cmd=r"""
export do="--dry-run=client -o yaml"
kubectl -n cours run web --image=nginx:1.27-alpine --port=80 $do > /tmp/web.yaml
kubectl apply -f /tmp/web.yaml --dry-run=server
kubectl apply -f /tmp/web.yaml
kubectl -n cours wait --for=condition=Ready pod/web --timeout=90s
sed -i 's/nginx:1.27-alpine/nginx:1.28-alpine/' /tmp/web.yaml
kubectl diff -f /tmp/web.yaml || true          # code 1 = des différences / differences found
kubectl replace --force -f /tmp/web.yaml       # l'image d'un Pod se change aussi par set image
kubectl -n cours delete pod web --now
""",
    trap=T("`kubectl create -f` échoue si l'objet existe ; `apply -f` le met à jour.",
           "`kubectl create -f` fails if the object exists; `apply -f` updates it."))

concept("labels", T("Labels, sélecteurs, annotations", "Labels, selectors, annotations"), T(
    "Les **labels** (`clé=valeur`) servent aux sélecteurs : Deployment → Pods, Service → Endpoints, "
    "NetworkPolicy → Pods. Les sélecteurs sont d'égalité (`app=web`, `tier!=db`) ou d'ensemble "
    "(`app in (a,b)`, `!canary`). Les **annotations** portent des métadonnées non sélectionnables "
    "(motif d'un rollout, configuration d'un contrôleur).",
    "**Labels** (`key=value`) drive selectors: Deployment → Pods, Service → Endpoints, NetworkPolicy → Pods. "
    "Selectors are equality-based (`app=web`, `tier!=db`) or set-based (`app in (a,b)`, `!canary`). "
    "**Annotations** carry non-selectable metadata (rollout cause, controller settings)."),
    cmd=r"""
kubectl -n cours run a --image=busybox:1.37 --labels=app=shop,tier=front -- sleep 3600
kubectl -n cours run b --image=busybox:1.37 --labels=app=shop,tier=db -- sleep 3600
kubectl -n cours get pods --show-labels
kubectl -n cours get pods -l app=shop,tier!=db
kubectl -n cours get pods -l 'tier in (front,db)' -L tier
kubectl -n cours label pod a env=prod
kubectl -n cours label pod a env=dev --overwrite
kubectl -n cours label pod a env-                 # retirer un label / remove a label
kubectl -n cours annotate pod a owner='equipe-web'
kubectl -n cours delete pod a b --now
""")

concept("output", T("Formats de sortie : jsonpath, custom-columns, tri", "Output formats: jsonpath, custom-columns, sorting"), T(
    "`-o wide|yaml|json|name`, puis **jsonpath** pour extraire une valeur (souvent à écrire dans un fichier "
    "demandé par la tâche), **custom-columns** pour un tableau, `--sort-by` et `--field-selector` pour trier "
    "et filtrer côté serveur.",
    "`-o wide|yaml|json|name`, then **jsonpath** to extract a value (often to write into a file the task asks "
    "for), **custom-columns** for a table, `--sort-by` and `--field-selector` to sort and filter server-side."),
    cmd=r"""
kubectl get nodes -o jsonpath='{.items[*].metadata.name}'; echo
kubectl get nodes -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.status.nodeInfo.kubeletVersion}{"\n"}{end}'
kubectl get pods -A -o custom-columns=NS:.metadata.namespace,POD:.metadata.name,NODE:.spec.nodeName | head -4
kubectl get pods -A --sort-by=.metadata.creationTimestamp | tail -3
kubectl get pods -A --field-selector=status.phase=Running | head -3
kubectl get nodes -o name > /tmp/nodes.txt && cat /tmp/nodes.txt
""",
    exam=T("`yq` est installé sur les hôtes d'examen, pas `jq` : pour le JSON, reste sur jsonpath.",
           "`yq` is installed on exam hosts, `jq` is not: for JSON, stick to jsonpath."))

# =====================================================================================================
chapter("d1", "bleu", T("1 · Application Design and Build (20 %)", "1 · Application Design and Build (20%)"), T(
    "Images, Pods, ressources de charge, Pods multi-conteneurs, volumes et placement.",
    "Images, Pods, workload resources, multi-container Pods, volumes and scheduling."))

concept("images", T("Images de conteneur : Dockerfile, build, export", "Container images: Dockerfile, build, export"), T(
    "Une image est construite à partir d'un `Dockerfile` : `FROM` (base), `RUN` (étape de construction), `COPY`, "
    "`ENV`, `WORKDIR`, `USER`, `EXPOSE` (documentaire), `LABEL`, `ENTRYPOINT` et `CMD`. On la **tag**, on "
    "l'**exporte** (`save`) ou on la **pousse** (`push`). `podman` accepte les mêmes commandes que `docker`.",
    "An image is built from a `Dockerfile`: `FROM` (base), `RUN` (build step), `COPY`, `ENV`, `WORKDIR`, `USER`, "
    "`EXPOSE` (documentation), `LABEL`, `ENTRYPOINT` and `CMD`. You **tag** it, **export** it (`save`) or "
    "**push** it. `podman` takes the same commands as `docker`."),
    cmd=r"""
mkdir -p /tmp/img && cd /tmp/img
printf 'hello\n' > index.html
cat > Dockerfile <<'EOF'
FROM busybox:1.37
LABEL maintainer=ckad
ENV APP_VERSION=v1
WORKDIR /www
COPY index.html .
EXPOSE 8080
USER 1000
CMD ["httpd", "-f", "-p", "8080", "-h", "/www"]
EOF
docker build -t cours/hello:v1 .
docker tag cours/hello:v1 cours/hello:latest
docker image inspect cours/hello:v1 --format '{{json .Config.Labels}} {{.Config.User}}'
docker save -o /tmp/img/hello.tar cours/hello:v1 && ls -l /tmp/img/hello.tar
# docker push registry.example.com/cours/hello:v1     (registre / registry : non exécuté ici)
""",
    trap=T("`EXPOSE` ne publie rien : seul le Service ou `-p` le fait. `CMD` est remplacé par les `args` du Pod, "
           "`ENTRYPOINT` par son `command`.",
           "`EXPOSE` publishes nothing: only a Service or `-p` does. `CMD` is overridden by the Pod's `args`, "
           "`ENTRYPOINT` by its `command`."))

concept("pods", T("Pods : command, args, env, restartPolicy", "Pods: command, args, env, restartPolicy"), T(
    "Le Pod est l'unité d'ordonnancement : un ou plusieurs conteneurs qui partagent le réseau (même IP) et les "
    "volumes. `command` remplace l'ENTRYPOINT de l'image, `args` son CMD. `restartPolicy` vaut `Always` "
    "(défaut), `OnFailure` ou `Never`. `imagePullPolicy` : `IfNotPresent` (défaut pour un tag fixe), `Always` "
    "(défaut pour `latest`), `Never`.",
    "The Pod is the scheduling unit: one or more containers sharing the network (same IP) and volumes. "
    "`command` overrides the image ENTRYPOINT, `args` its CMD. `restartPolicy` is `Always` (default), "
    "`OnFailure` or `Never`. `imagePullPolicy`: `IfNotPresent` (default for a fixed tag), `Always` (default for "
    "`latest`), `Never`."),
    cmd=r"""
kubectl -n cours run once --image=busybox:1.37 --restart=Never --env=WHO=ckad -- sh -c 'echo hello $WHO'
kubectl -n cours wait --for=jsonpath='{.status.phase}'=Succeeded pod/once --timeout=60s
kubectl -n cours logs once
kubectl -n cours run cmd --image=busybox:1.37 --command -- sleep 3600   # --command : remplace l'ENTRYPOINT
kubectl -n cours get pod cmd -o jsonpath='{.spec.containers[0].command}'; echo
kubectl -n cours delete pod once cmd --now
""",
    yaml=r"""
apiVersion: v1
kind: Pod
metadata:
  name: demo
  labels: {app: demo}
spec:
  restartPolicy: Always
  containers:
  - name: app
    image: busybox:1.37
    imagePullPolicy: IfNotPresent
    command: ["sh", "-c"]               # remplace ENTRYPOINT / overrides ENTRYPOINT
    args: ["echo $(GREETING) && sleep 3600"]
    env:
    - name: GREETING
      value: bonjour
    - name: POD_IP                      # Downward API
      valueFrom: {fieldRef: {fieldPath: status.podIP}}
""",
    trap=T("`kubectl run x --image=y -- a b` met `a b` dans `args` ; avec `--command`, dans `command`.",
           "`kubectl run x --image=y -- a b` puts `a b` in `args`; with `--command`, in `command`."))

concept("deployments", T("Deployments et ReplicaSets", "Deployments and ReplicaSets"), T(
    "Un **Deployment** gère des **ReplicaSets**, qui maintiennent un nombre de Pods identiques. Chaque "
    "modification du template crée un nouveau ReplicaSet (une révision). Le sélecteur (`spec.selector`) est "
    "immuable et doit correspondre aux labels du template.",
    "A **Deployment** manages **ReplicaSets**, which keep a number of identical Pods running. Every template "
    "change creates a new ReplicaSet (a revision). The selector (`spec.selector`) is immutable and must match "
    "the template labels."),
    cmd=r"""
kubectl -n cours create deployment front --image=nginx:1.27-alpine --replicas=2 --port=80
kubectl -n cours rollout status deploy/front --timeout=120s
kubectl -n cours get deploy,rs,pods -l app=front
kubectl -n cours scale deploy front --replicas=3
kubectl -n cours rollout status deploy/front --timeout=120s
""",
    trap=T("Supprimer un Pod d'un Deployment ne sert à rien : le ReplicaSet le recrée.",
           "Deleting a Pod owned by a Deployment is pointless: the ReplicaSet recreates it."))

concept("daemonset", T("DaemonSet", "DaemonSet"), T(
    "Un Pod par nœud (agents de logs, de monitoring). Pas de `replicas`. Pour couvrir le control-plane, il "
    "faut tolérer son taint `node-role.kubernetes.io/control-plane:NoSchedule`.",
    "One Pod per node (log or monitoring agents). No `replicas`. To cover the control plane, tolerate its "
    "`node-role.kubernetes.io/control-plane:NoSchedule` taint."),
    cmd=r"""
kubectl -n cours create deployment agent --image=busybox:1.37 $do -- sleep 3600 > /tmp/ds.yaml
yq -i '.kind = "DaemonSet" | del(.spec.replicas) | del(.spec.strategy) | del(.status)' /tmp/ds.yaml
kubectl apply -f /tmp/ds.yaml
kubectl -n cours rollout status ds/agent --timeout=120s
kubectl -n cours get ds agent
""",
    yaml=r"""
apiVersion: apps/v1
kind: DaemonSet
metadata: {name: node-agent}
spec:
  selector: {matchLabels: {app: node-agent}}
  template:
    metadata: {labels: {app: node-agent}}
    spec:
      tolerations:
      - {key: node-role.kubernetes.io/control-plane, operator: Exists, effect: NoSchedule}
      containers:
      - {name: agent, image: "busybox:1.37", command: ["sleep", "3600"]}
""")

concept("statefulset", T("StatefulSet et Service headless", "StatefulSet and headless Service"), T(
    "Pour les applications à identité stable (bases de données) : Pods nommés `web-0`, `web-1`…, créés dans "
    "l'ordre, avec un nom DNS stable via un **Service headless** (`clusterIP: None`) et, au besoin, un PVC par "
    "Pod (`volumeClaimTemplates`).",
    "For apps that need a stable identity (databases): Pods named `web-0`, `web-1`…, created in order, with a "
    "stable DNS name through a **headless Service** (`clusterIP: None`) and, if needed, one PVC per Pod "
    "(`volumeClaimTemplates`)."),
    cmd=r"""
kubectl apply -n cours -f - <<'EOF'
apiVersion: v1
kind: Service
metadata: {name: db}
spec:
  clusterIP: None
  selector: {app: db}
  ports: [{port: 6379}]
---
apiVersion: apps/v1
kind: StatefulSet
metadata: {name: db}
spec:
  serviceName: db
  replicas: 2
  selector: {matchLabels: {app: db}}
  template:
    metadata: {labels: {app: db}}
    spec:
      containers: [{name: redis, image: "redis:7.4-alpine", ports: [{containerPort: 6379}]}]
EOF
kubectl -n cours rollout status sts/db --timeout=180s
kubectl -n cours get pods -l app=db                       # db-0, db-1
kubectl -n cours run dns --image=busybox:1.37 --restart=Never -- nslookup db-0.db.cours.svc.cluster.local
kubectl -n cours wait --for=jsonpath='{.status.phase}'=Succeeded pod/dns --timeout=60s && kubectl -n cours logs dns
""")

concept("jobs", T("Job", "Job"), T(
    "Un **Job** exécute des Pods jusqu'à réussite. Champs (sous `spec`, pas sous `template`) : `completions` "
    "(réussites voulues), `parallelism`, `backoffLimit` (relances, 6 par défaut), `activeDeadlineSeconds` "
    "(durée maximale), `ttlSecondsAfterFinished` (nettoyage). Le template exige `restartPolicy: Never` ou "
    "`OnFailure`.",
    "A **Job** runs Pods until they succeed. Fields (under `spec`, not under `template`): `completions` "
    "(required successes), `parallelism`, `backoffLimit` (retries, 6 by default), `activeDeadlineSeconds` "
    "(max duration), `ttlSecondsAfterFinished` (cleanup). The template needs `restartPolicy: Never` or "
    "`OnFailure`."),
    cmd=r"""
kubectl -n cours create job calc --image=busybox:1.37 $do -- sh -c 'echo calcul fini' > /tmp/job.yaml
yq -i '.spec.completions = 3 | .spec.parallelism = 2 | .spec.backoffLimit = 2 | .spec.ttlSecondsAfterFinished = 600' /tmp/job.yaml
kubectl apply -f /tmp/job.yaml
kubectl -n cours wait --for=condition=Complete job/calc --timeout=120s
kubectl -n cours get job calc
kubectl -n cours logs job/calc
""",
    trap=T("`restartPolicy: Always` est refusé dans un Job.", "`restartPolicy: Always` is rejected in a Job."))

concept("cronjobs", T("CronJob", "CronJob"), T(
    "Un **CronJob** crée des Jobs selon un horaire cron (`minute heure jour mois jour-semaine`). "
    "`concurrencyPolicy` : `Allow` (défaut), `Forbid` (saute si la précédente tourne), `Replace`. "
    "`successfulJobsHistoryLimit` (3), `failedJobsHistoryLimit` (1), `suspend`, `startingDeadlineSeconds`.",
    "A **CronJob** creates Jobs on a cron schedule (`minute hour day month weekday`). `concurrencyPolicy`: "
    "`Allow` (default), `Forbid` (skip while the previous run is active), `Replace`. "
    "`successfulJobsHistoryLimit` (3), `failedJobsHistoryLimit` (1), `suspend`, `startingDeadlineSeconds`."),
    cmd=r"""
kubectl -n cours create cronjob nightly --image=busybox:1.37 --schedule='0 2 * * *' -- sh -c 'date'
kubectl -n cours patch cronjob nightly -p '{"spec":{"concurrencyPolicy":"Forbid","successfulJobsHistoryLimit":2}}'
kubectl -n cours create job nightly-now --from=cronjob/nightly       # lancer tout de suite / run now
kubectl -n cours wait --for=condition=Complete job/nightly-now --timeout=90s
kubectl -n cours patch cronjob nightly -p '{"spec":{"suspend":true}}'
kubectl -n cours get cronjob nightly
""")

concept("multicontainer", T("Pods multi-conteneurs : init, sidecar, ambassador, adapter", "Multi-container Pods: init, sidecar, ambassador, adapter"), T(
    "Les **init containers** s'exécutent dans l'ordre, chacun jusqu'au bout, avant les conteneurs principaux "
    "(préparer un fichier, attendre un service). Un **sidecar natif** est un init container avec "
    "`restartPolicy: Always` : il démarre avant l'application et vit avec elle (collecte de logs, proxy). "
    "Motifs classiques : **ambassador** (proxy vers l'extérieur), **adapter** (normalise la sortie de l'app). "
    "Les conteneurs partagent `localhost` et les volumes.",
    "**Init containers** run in order, each to completion, before the main containers (prepare a file, wait "
    "for a service). A **native sidecar** is an init container with `restartPolicy: Always`: it starts before "
    "the app and lives alongside it (log shipping, proxy). Classic patterns: **ambassador** (proxy to the "
    "outside), **adapter** (normalises the app's output). Containers share `localhost` and volumes."),
    cmd=r"""
kubectl apply -n cours -f - <<'EOF'
apiVersion: v1
kind: Pod
metadata: {name: multi}
spec:
  volumes: [{name: shared, emptyDir: {}}]
  initContainers:
  - name: prepare
    image: busybox:1.37
    command: ["sh", "-c", "echo prêt > /data/ready"]
    volumeMounts: [{name: shared, mountPath: /data}]
  - name: shipper                        # sidecar natif / native sidecar
    image: busybox:1.37
    restartPolicy: Always
    command: ["sh", "-c", "touch /data/app.log; tail -F /data/app.log"]
    volumeMounts: [{name: shared, mountPath: /data}]
  containers:
  - name: app
    image: busybox:1.37
    command: ["sh", "-c", "cat /data/ready; while true; do date >> /data/app.log; sleep 2; done"]
    volumeMounts: [{name: shared, mountPath: /data}]
EOF
kubectl -n cours wait --for=condition=Ready pod/multi --timeout=90s
kubectl -n cours logs multi -c app --tail=1
kubectl -n cours logs multi -c shipper --tail=2
kubectl -n cours get pod multi -o jsonpath='{.spec.initContainers[*].name}'; echo
""",
    trap=T("Avec plusieurs conteneurs, `logs` et `exec` exigent `-c <conteneur>`.",
           "With several containers, `logs` and `exec` require `-c <container>`."))

concept("volumes", T("Volumes éphémères : emptyDir, hostPath, projected", "Ephemeral volumes: emptyDir, hostPath, projected"), T(
    "`emptyDir` vit et meurt avec le Pod (`medium: Memory` = tmpfs, `sizeLimit`). `hostPath` monte un dossier "
    "du nœud (à éviter hors tests). `projected` réunit dans un même dossier ConfigMap, Secret, Downward API "
    "et jeton de ServiceAccount. `subPath` monte un seul fichier ou sous-dossier.",
    "`emptyDir` lives and dies with the Pod (`medium: Memory` = tmpfs, `sizeLimit`). `hostPath` mounts a node "
    "directory (avoid outside tests). `projected` merges ConfigMap, Secret, Downward API and ServiceAccount "
    "token into one directory. `subPath` mounts a single file or subdirectory."),
    cmd=r"""
kubectl -n cours create configmap app-conf --from-literal=mode=prod
kubectl apply -n cours -f - <<'EOF'
apiVersion: v1
kind: Pod
metadata: {name: vols, labels: {app: vols}}
spec:
  volumes:
  - name: scratch
    emptyDir: {medium: Memory, sizeLimit: 16Mi}
  - name: all-in-one
    projected:
      sources:
      - configMap: {name: app-conf}
      - downwardAPI: {items: [{path: labels, fieldRef: {fieldPath: metadata.labels}}]}
  containers:
  - name: app
    image: busybox:1.37
    command: ["sleep", "3600"]
    volumeMounts:
    - {name: scratch, mountPath: /scratch}
    - {name: all-in-one, mountPath: /etc/app}
    - {name: all-in-one, mountPath: /mode.txt, subPath: mode}
EOF
kubectl -n cours wait --for=condition=Ready pod/vols --timeout=90s
kubectl -n cours exec vols -- sh -c 'ls /etc/app; cat /mode.txt; echo; df -h /scratch | tail -1'
""",
    trap=T("Un fichier monté avec `subPath` n'est pas mis à jour quand la ConfigMap change.",
           "A file mounted through `subPath` is not refreshed when the ConfigMap changes."))

concept("persistent", T("PersistentVolume, PersistentVolumeClaim, StorageClass", "PersistentVolume, PersistentVolumeClaim, StorageClass"), T(
    "Le **PV** est un stockage du cluster (objet sans namespace), le **PVC** une demande dans un namespace, la "
    "**StorageClass** un provisionneur dynamique. Un PVC se lie à un PV compatible (classe, taille, mode "
    "d'accès : `ReadWriteOnce`, `ReadOnlyMany`, `ReadWriteMany`, `ReadWriteOncePod`). `persistentVolumeReclaimPolicy` : "
    "`Retain` ou `Delete`. Avec `volumeBindingMode: WaitForFirstConsumer`, le PVC reste `Pending` jusqu'au "
    "premier Pod.",
    "A **PV** is cluster storage (not namespaced), a **PVC** a request inside a namespace, a **StorageClass** a "
    "dynamic provisioner. A PVC binds to a compatible PV (class, size, access mode: `ReadWriteOnce`, "
    "`ReadOnlyMany`, `ReadWriteMany`, `ReadWriteOncePod`). `persistentVolumeReclaimPolicy`: `Retain` or "
    "`Delete`. With `volumeBindingMode: WaitForFirstConsumer`, the PVC stays `Pending` until the first Pod."),
    cmd=r"""
kubectl get storageclass
kubectl apply -f - <<'EOF'
apiVersion: v1
kind: PersistentVolume
metadata: {name: cours-pv}
spec:
  capacity: {storage: 100Mi}
  accessModes: [ReadWriteOnce]
  persistentVolumeReclaimPolicy: Retain
  storageClassName: manuel
  hostPath: {path: /tmp/cours-pv}
EOF
kubectl apply -n cours -f - <<'EOF'
apiVersion: v1
kind: PersistentVolumeClaim
metadata: {name: data}
spec:
  accessModes: [ReadWriteOnce]
  storageClassName: manuel
  resources: {requests: {storage: 50Mi}}
---
apiVersion: v1
kind: Pod
metadata: {name: writer}
spec:
  volumes: [{name: data, persistentVolumeClaim: {claimName: data}}]
  containers:
  - {name: w, image: "busybox:1.37", command: ["sh", "-c", "echo ok > /data/f && sleep 3600"], volumeMounts: [{name: data, mountPath: /data}]}
EOF
kubectl -n cours wait --for=condition=Ready pod/writer --timeout=120s
kubectl get pv cours-pv; kubectl -n cours get pvc data
""",
    trap=T("Un PVC lié à un PV prend toute la capacité du PV (100Mi ici), pas seulement ce qu'il demande.",
           "A PVC bound to a PV gets the PV's whole capacity (100Mi here), not just what it asked for."))

concept("scheduling", T("Placement : nodeSelector, affinité, taints et tolerations", "Scheduling: nodeSelector, affinity, taints and tolerations"), T(
    "`nodeSelector` impose des labels de nœud. `affinity.nodeAffinity` l'exprime avec des opérateurs "
    "(`In`, `NotIn`, `Exists`), en obligatoire (`required…`) ou préféré (`preferred…`). Un **taint** "
    "(`clé=valeur:NoSchedule|PreferNoSchedule|NoExecute`) repousse les Pods qui n'ont pas la **toleration** "
    "correspondante.",
    "`nodeSelector` requires node labels. `affinity.nodeAffinity` expresses it with operators (`In`, `NotIn`, "
    "`Exists`), required (`required…`) or preferred (`preferred…`). A **taint** (`key=value:NoSchedule|"
    "PreferNoSchedule|NoExecute`) repels Pods that lack the matching **toleration**."),
    cmd=r"""
kubectl label node ckad-a-worker disk=ssd --overwrite
kubectl -n cours run fast --image=busybox:1.37 $do -- sleep 3600 > /tmp/fast.yaml
yq -i '.spec.nodeSelector = {"disk": "ssd"}' /tmp/fast.yaml && kubectl apply -f /tmp/fast.yaml
kubectl -n cours wait --for=condition=Ready pod/fast --timeout=90s
kubectl -n cours get pod fast -o jsonpath='{.spec.nodeName}'; echo
kubectl taint node ckad-a-worker2 dedie=ia:NoSchedule
kubectl describe node ckad-a-worker2 | grep Taints
kubectl taint node ckad-a-worker2 dedie=ia:NoSchedule-     # retirer / remove
kubectl label node ckad-a-worker disk-
""",
    yaml=r"""
apiVersion: v1
kind: Pod
metadata: {name: affine}
spec:
  affinity:
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
        - matchExpressions:
          - {key: kubernetes.io/os, operator: In, values: [linux]}
  tolerations:
  - {key: dedie, operator: Equal, value: ia, effect: NoSchedule}
  containers:
  - {name: app, image: "busybox:1.37", command: ["sleep", "3600"]}
""",
    trap=T("Une toleration **autorise** un nœud tainté, elle n'y **envoie** pas le Pod : pour cela, ajoute un nodeSelector ou une affinité.",
           "A toleration **allows** a tainted node, it does not **send** the Pod there: add a nodeSelector or affinity for that."))

# =====================================================================================================
chapter("d2", "jaune", T("2 · Application Deployment (20 %)", "2 · Application Deployment (20%)"), T(
    "Mises à jour progressives, retour arrière, mise à l'échelle, blue/green, canary, Helm et Kustomize.",
    "Rolling updates, rollbacks, scaling, blue/green, canary, Helm and Kustomize."))

concept("rolling", T("Rolling update, historique, rollback", "Rolling update, history, rollback"), T(
    "`strategy.type: RollingUpdate` (défaut) remplace progressivement les Pods selon `maxSurge` (Pods en plus) "
    "et `maxUnavailable` (Pods en moins), 25 % par défaut. `Recreate` arrête tout puis recrée. Chaque révision "
    "est un ReplicaSet ; `rollout undo` revient en arrière, `--to-revision` cible une révision. Le motif se pose "
    "par l'annotation `kubernetes.io/change-cause` (`--record` n'existe plus).",
    "`strategy.type: RollingUpdate` (default) replaces Pods progressively according to `maxSurge` (extra Pods) "
    "and `maxUnavailable` (missing Pods), 25% by default. `Recreate` stops everything then recreates. Each "
    "revision is a ReplicaSet; `rollout undo` goes back, `--to-revision` targets one. The cause is set through "
    "the `kubernetes.io/change-cause` annotation (`--record` is gone)."),
    cmd=r"""
kubectl -n cours patch deploy front -p '{"spec":{"minReadySeconds":2,"strategy":{"rollingUpdate":{"maxSurge":1,"maxUnavailable":0}}}}'
kubectl -n cours set image deploy/front nginx=nginx:1.28-alpine
kubectl -n cours annotate deploy front kubernetes.io/change-cause='nginx 1.28' --overwrite
kubectl -n cours rollout status deploy/front --timeout=180s
kubectl -n cours rollout history deploy/front
kubectl -n cours rollout history deploy/front --revision=2
kubectl -n cours rollout undo deploy/front
kubectl -n cours rollout status deploy/front --timeout=180s
kubectl -n cours rollout restart deploy/front          # nouveaux Pods, même spec / new Pods, same spec
kubectl -n cours rollout status deploy/front --timeout=180s
""",
    trap=T("Pour passer en `Recreate`, retire aussi le bloc `rollingUpdate`, sinon l'API refuse.",
           "To switch to `Recreate`, also remove the `rollingUpdate` block, otherwise the API rejects it."))

concept("scaling", T("Mise à l'échelle et HorizontalPodAutoscaler", "Scaling and HorizontalPodAutoscaler"), T(
    "`scale` fixe le nombre de réplicas. Un **HPA** (`autoscaling/v2`) l'ajuste entre `minReplicas` et "
    "`maxReplicas` selon une métrique (CPU en pourcentage des **requests**). Il faut metrics-server et des "
    "requests CPU sur les conteneurs.",
    "`scale` sets the replica count. An **HPA** (`autoscaling/v2`) adjusts it between `minReplicas` and "
    "`maxReplicas` from a metric (CPU as a percentage of **requests**). It needs metrics-server and CPU "
    "requests on the containers."),
    cmd=r"""
kubectl -n cours set resources deploy front --requests=cpu=20m,memory=16Mi
kubectl -n cours autoscale deploy front --min=2 --max=5 --cpu-percent=70
kubectl -n cours get hpa front
kubectl -n cours get hpa front -o yaml | yq '.spec'
""",
    yaml=r"""
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata: {name: api}
spec:
  scaleTargetRef: {apiVersion: apps/v1, kind: Deployment, name: api}
  minReplicas: 2
  maxReplicas: 6
  metrics:
  - type: Resource
    resource: {name: cpu, target: {type: Utilization, averageUtilization: 60}}
""")

concept("bluegreen", T("Blue/green et canary avec les primitives", "Blue/green and canary with primitives"), T(
    "Un Service envoie le trafic à **tous** les Pods qui correspondent à son sélecteur. **Blue/green** : deux "
    "Deployments (`version=blue`, `version=green`), on bascule en changeant le sélecteur du Service. "
    "**Canary** : le Service ne sélectionne que `app=…` ; la proportion de trafic suit le nombre de Pods "
    "(4 stables + 1 canary ≈ 20 %).",
    "A Service sends traffic to **all** Pods matching its selector. **Blue/green**: two Deployments "
    "(`version=blue`, `version=green`); switch by changing the Service selector. **Canary**: the Service only "
    "selects `app=…`; the traffic share follows the Pod count (4 stable + 1 canary ≈ 20%)."),
    cmd=r"""
for c in blue green; do
  kubectl -n cours create deployment web-$c --image=hashicorp/http-echo:1.0.0 $do -- /http-echo -text=$c \
    | yq ".spec.selector.matchLabels = {\"app\":\"web\",\"version\":\"$c\"} | .spec.template.metadata.labels = {\"app\":\"web\",\"version\":\"$c\"}" \
    | kubectl apply -f -
done
kubectl -n cours create service clusterip web --tcp=80:5678 $do | yq '.spec.selector = {"app":"web","version":"blue"}' | kubectl apply -f -
kubectl -n cours rollout status deploy/web-green --timeout=120s
kubectl -n cours patch svc web -p '{"spec":{"selector":{"app":"web","version":"green"}}}'    # bascule / switch
kubectl -n cours get endpointslices -l kubernetes.io/service-name=web
""")

concept("helm", T("Helm", "Helm"), T(
    "Helm installe des **charts** (paquets de manifestes paramétrés) sous forme de **releases**. Les valeurs "
    "se passent par `--set clé=valeur` ou `-f valeurs.yaml`. Chaque `upgrade` crée une révision ; `rollback` "
    "revient à une révision. helm.sh/docs fait partie de la documentation autorisée.",
    "Helm installs **charts** (parameterised manifest packages) as **releases**. Values are passed with "
    "`--set key=value` or `-f values.yaml`. Each `upgrade` creates a revision; `rollback` returns to one. "
    "helm.sh/docs is part of the allowed documentation."),
    cmd=r"""
# helm repo add bitnami https://charts.bitnami.com/bitnami && helm repo update && helm search repo nginx  (réseau / network)
CHART=$ROOT/app/charts/webapp
helm show values $CHART
helm template demo $CHART --set replicaCount=2 | grep -E 'kind|replicas'
helm -n cours install shop $CHART --set replicaCount=2 --wait --timeout 3m
helm -n cours list
helm -n cours upgrade shop $CHART --set replicaCount=3 --set image.tag=1.28-alpine --wait --timeout 3m
helm -n cours get values shop
helm -n cours history shop
helm -n cours rollback shop 1 --wait --timeout 3m
helm -n cours uninstall shop
""",
    trap=T("`helm upgrade` sans `--reuse-values` repart des valeurs par défaut du chart : repasse toutes tes valeurs.",
           "`helm upgrade` without `--reuse-values` starts from the chart defaults: pass all your values again."))

concept("kustomize", T("Kustomize", "Kustomize"), T(
    "Kustomize assemble une **base** et des **overlays** sans template : `resources`, `namespace`, "
    "`namePrefix`/`nameSuffix`, `labels`, `images`, `replicas`, `patches` (patch stratégique ou JSON 6902), "
    "`configMapGenerator`/`secretGenerator` (nom suffixé par un hachage). Intégré à kubectl : "
    "`kubectl kustomize` (aperçu) et `kubectl apply -k`.",
    "Kustomize composes a **base** and **overlays** without templates: `resources`, `namespace`, "
    "`namePrefix`/`nameSuffix`, `labels`, `images`, `replicas`, `patches` (strategic merge or JSON 6902), "
    "`configMapGenerator`/`secretGenerator` (hash-suffixed names). Built into kubectl: `kubectl kustomize` "
    "(preview) and `kubectl apply -k`."),
    cmd=r"""
mkdir -p /tmp/kz/base /tmp/kz/prod
kubectl create deployment api --image=nginx:1.27-alpine $do > /tmp/kz/base/deploy.yaml
cat > /tmp/kz/base/kustomization.yaml <<'EOF'
resources: [deploy.yaml]
EOF
cat > /tmp/kz/prod/kustomization.yaml <<'EOF'
resources: [../base]
namespace: cours
namePrefix: prod-
labels:
- pairs: {env: prod}
replicas:
- {name: api, count: 2}
images:
- {name: nginx, newTag: 1.28-alpine}
configMapGenerator:
- name: api-conf
  literals: [MODE=prod]
patches:
- target: {kind: Deployment, name: api}
  patch: |-
    - op: add
      path: /spec/template/spec/containers/0/env
      value: [{name: MODE, value: prod}]
EOF
kubectl kustomize /tmp/kz/prod | grep -E 'name: prod-|image:|replicas'
kubectl apply -k /tmp/kz/prod
kubectl -n cours rollout status deploy/prod-api --timeout=120s
""")

# =====================================================================================================
chapter("d3", "vert", T("3 · Application Observability and Maintenance (15 %)", "3 · Application Observability and Maintenance (15%)"), T(
    "Sondes, logs, événements, débogage, métriques et dépréciations d'API.",
    "Probes, logs, events, debugging, metrics and API deprecations."))

concept("probes", T("Sondes : liveness, readiness, startup", "Probes: liveness, readiness, startup"), T(
    "**startupProbe** : tant qu'elle n'a pas réussi, les deux autres attendent. **readinessProbe** : en échec, "
    "le Pod sort des Endpoints du Service (pas de redémarrage). **livenessProbe** : en échec, le conteneur est "
    "redémarré. Mécanismes : `httpGet`, `tcpSocket`, `exec`, `grpc`. Réglages : `initialDelaySeconds`, "
    "`periodSeconds`, `timeoutSeconds`, `failureThreshold`, `successThreshold`.",
    "**startupProbe**: until it succeeds, the other two wait. **readinessProbe**: on failure, the Pod leaves "
    "the Service Endpoints (no restart). **livenessProbe**: on failure, the container is restarted. "
    "Mechanisms: `httpGet`, `tcpSocket`, `exec`, `grpc`. Settings: `initialDelaySeconds`, `periodSeconds`, "
    "`timeoutSeconds`, `failureThreshold`, `successThreshold`."),
    cmd=r"""
kubectl apply -n cours -f - <<'EOF'
apiVersion: v1
kind: Pod
metadata: {name: probed}
spec:
  containers:
  - name: web
    image: nginx:1.27-alpine
    startupProbe:
      httpGet: {path: /, port: 80}
      failureThreshold: 10
      periodSeconds: 2
    readinessProbe:
      httpGet: {path: /, port: 80}
      periodSeconds: 5
    livenessProbe:
      tcpSocket: {port: 80}
      initialDelaySeconds: 5
      periodSeconds: 10
  - name: worker
    image: busybox:1.37
    command: ["sh", "-c", "touch /tmp/healthy; sleep 3600"]
    livenessProbe:
      exec: {command: ["cat", "/tmp/healthy"]}
      periodSeconds: 10
EOF
kubectl -n cours wait --for=condition=Ready pod/probed --timeout=120s
kubectl -n cours describe pod probed | grep -E 'Liveness|Readiness|Startup'
""",
    trap=T("Une liveness trop agressive (port faux, délai trop court) fait redémarrer une application saine en boucle.",
           "An over-aggressive liveness probe (wrong port, too short a delay) restarts a healthy app in a loop."))

concept("logs", T("Logs des conteneurs", "Container logs"), T(
    "`kubectl logs` lit la sortie standard d'un conteneur. `-c` choisit le conteneur, `--previous` lit "
    "l'instance précédente (après un crash), `-f` suit, `--tail`, `--since`, `-l` sélectionne par label, "
    "`--all-containers`, `--prefix` ; `deploy/x` ou `job/x` choisit un Pod de l'objet.",
    "`kubectl logs` reads a container's standard output. `-c` picks the container, `--previous` reads the "
    "previous instance (after a crash), `-f` follows, `--tail`, `--since`, `-l` selects by label, "
    "`--all-containers`, `--prefix`; `deploy/x` or `job/x` picks a Pod of that object."),
    cmd=r"""
kubectl -n cours logs multi -c app --tail=2
kubectl -n cours logs multi --all-containers --prefix --tail=1
kubectl -n cours logs deploy/front --tail=3 --since=1h
kubectl -n cours logs -l app=front --tail=1 --prefix
kubectl -n cours logs job/calc
# kubectl -n cours logs -f deploy/front        (suit en continu / follows : Ctrl+C)
""")

concept("events", T("describe et événements", "describe and events"), T(
    "`describe` montre l'état détaillé et, en bas, les **événements** (ordonnancement, téléchargement d'image, "
    "sondes, montages). `get events` les liste pour tout le namespace : triés par `--sort-by=.lastTimestamp`, "
    "filtrés par objet avec `--field-selector`.",
    "`describe` shows the detailed state and, at the bottom, the **events** (scheduling, image pulls, probes, "
    "mounts). `get events` lists them for the whole namespace: sorted with `--sort-by=.lastTimestamp`, "
    "filtered by object with `--field-selector`."),
    cmd=r"""
kubectl -n cours describe pod probed | tail -8
kubectl -n cours get events --sort-by=.lastTimestamp | tail -5
kubectl -n cours get events --field-selector involvedObject.name=probed,type=Normal | tail -3
kubectl -n cours get events --field-selector type=Warning
""")

concept("exec", T("exec, cp, port-forward", "exec, cp, port-forward"), T(
    "`exec` lance une commande dans un conteneur (`-it … -- sh` pour un shell). `cp` copie entre le poste et un "
    "Pod (il faut `tar` dans l'image). `port-forward` ouvre un tunnel local vers un Pod ou un Service, pour "
    "tester sans exposer.",
    "`exec` runs a command in a container (`-it … -- sh` for a shell). `cp` copies between your machine and a "
    "Pod (`tar` must exist in the image). `port-forward` opens a local tunnel to a Pod or Service, to test "
    "without exposing."),
    cmd=r"""
kubectl -n cours exec probed -c web -- nginx -v
kubectl -n cours exec probed -c worker -- ls /tmp
echo bonjour > /tmp/salut.txt
kubectl -n cours cp /tmp/salut.txt probed:/tmp/salut.txt -c worker
kubectl -n cours exec probed -c worker -- cat /tmp/salut.txt
kubectl -n cours expose deploy front --port=80 --name=front
kubectl -n cours port-forward svc/front 18080:80 >/dev/null 2>&1 & PF=$!
sleep 3; curl -s http://localhost:18080 | grep -o '<title>.*</title>'; kill $PF
# kubectl -n cours exec -it probed -c worker -- sh     (shell interactif / interactive shell)
""")

concept("debug", T("kubectl debug et conteneurs éphémères", "kubectl debug and ephemeral containers"), T(
    "Pour une image sans shell (distroless), `kubectl debug` ajoute un **conteneur éphémère** (busybox) au Pod "
    "en cours ; `--target` partage l'espace de processus du conteneur visé. `--copy-to` crée une copie du Pod "
    "modifiable (changer la commande, l'image). `kubectl debug node/<nœud>` ouvre un Pod privilégié sur un nœud.",
    "For an image without a shell (distroless), `kubectl debug` adds an **ephemeral container** (busybox) to the "
    "running Pod; `--target` shares the target container's process namespace. `--copy-to` creates an editable "
    "copy of the Pod (change command, image). `kubectl debug node/<node>` opens a privileged Pod on a node."),
    cmd=r"""
kubectl -n cours run echo --image=hashicorp/http-echo:1.0.0 -- -text=ok      # image sans shell / no shell
kubectl -n cours wait --for=condition=Ready pod/echo --timeout=60s
kubectl -n cours debug echo --image=busybox:1.37 --target=echo -c dbg -- sh -c 'ps; sleep 30'
sleep 5; kubectl -n cours logs echo -c dbg
kubectl -n cours debug echo --copy-to=echo-copy --image=busybox:1.37 --set-image=echo=busybox:1.37 -- sleep 3600
kubectl -n cours get pod echo-copy
# kubectl debug node/ckad-a-worker -it --image=busybox:1.37     (shell sur le nœud / node shell)
""")

concept("metrics", T("kubectl top et métriques", "kubectl top and metrics"), T(
    "`kubectl top` affiche CPU et mémoire réellement consommés (fournis par metrics-server, environ une minute "
    "après le démarrage). Trier : `--sort-by=cpu|memory` ; par conteneur : `--containers`.",
    "`kubectl top` shows actual CPU and memory usage (served by metrics-server, about a minute after start). "
    "Sort with `--sort-by=cpu|memory`; per container with `--containers`."),
    cmd=r"""
for i in $(seq 1 30); do kubectl top nodes >/dev/null 2>&1 && break; sleep 5; done
kubectl top nodes
kubectl top pods -n kube-system --sort-by=memory | head -4
kubectl top pods -n cours --containers | head -5
""",
    requires="metrics")

concept("troubleshooting", T("Diagnostiquer un Pod : les états", "Troubleshooting a Pod: the states"), T(
    "Le STATUS oriente le diagnostic : **Pending** (scheduler : ressources, nodeSelector, taint, PVC), "
    "**ContainerCreating** (volume, réseau), **ImagePullBackOff/ErrImagePull** (image, tag, registre), "
    "**CreateContainerConfigError** (ConfigMap/Secret ou clé absente), **CrashLoopBackOff** (le processus "
    "sort : logs `--previous`, code de sortie), **OOMKilled** (limite mémoire, code 137), **Completed** "
    "(normal pour un Job), **Terminating** bloqué (finalizers). Voir le Journal des erreurs du guide.",
    "STATUS drives the diagnosis: **Pending** (scheduler: resources, nodeSelector, taint, PVC), "
    "**ContainerCreating** (volume, network), **ImagePullBackOff/ErrImagePull** (image, tag, registry), "
    "**CreateContainerConfigError** (missing ConfigMap/Secret or key), **CrashLoopBackOff** (the process exits: "
    "`--previous` logs, exit code), **OOMKilled** (memory limit, code 137), **Completed** (normal for a Job), "
    "stuck **Terminating** (finalizers). See the guide's Error log."),
    cmd=r"""
kubectl -n cours run broken --image=busybox:1.37 -- sh -c 'echo boom; exit 3'
for i in $(seq 1 30); do kubectl -n cours get pod broken -o jsonpath='{.status.containerStatuses[0].lastState.terminated.exitCode}' | grep -q 3 && break; sleep 2; done
kubectl -n cours get pod broken
kubectl -n cours get pod broken -o jsonpath='{.status.containerStatuses[0].lastState.terminated.exitCode}'; echo
kubectl -n cours logs broken --previous || kubectl -n cours logs broken
kubectl -n cours describe pod broken | grep -A3 'Last State'
kubectl -n cours delete pod broken --now
""")

concept("deprecations", T("Dépréciations d'API", "API deprecations"), T(
    "Une version d'API retirée ne s'applique plus (`no matches for kind … in version …`). Trouve la version "
    "actuelle avec `api-resources` ou `explain`, puis corrige `apiVersion` et les champs qui ont changé "
    "(Ingress v1 : `pathType` obligatoire, `backend.service.name/port`). Le plugin `kubectl convert` n'est pas "
    "installé à l'examen. Référence : *Deprecated API Migration Guide*.",
    "A removed API version no longer applies (`no matches for kind … in version …`). Find the current version "
    "with `api-resources` or `explain`, then fix `apiVersion` and the fields that changed (Ingress v1: "
    "mandatory `pathType`, `backend.service.name/port`). The `kubectl convert` plugin is not installed in the "
    "exam. Reference: *Deprecated API Migration Guide*."),
    cmd=r"""
kubectl api-resources | grep -E '^(cronjobs|poddisruptionbudgets|horizontalpodautoscalers|ingresses) '
kubectl explain cronjob | head -3
kubectl explain ingress.spec.rules.http.paths.backend --api-version=networking.k8s.io/v1 | head -12
printf 'apiVersion: batch/v1beta1\nkind: CronJob\nmetadata: {name: old}\nspec: {schedule: "@daily", jobTemplate: {spec: {template: {spec: {restartPolicy: Never, containers: [{name: c, image: busybox}]}}}}}\n' \
  | kubectl -n cours apply --dry-run=server -f - || echo "→ batch/v1beta1 retiré : utiliser batch/v1"
""")

# =====================================================================================================
chapter("d4", "orange", T("4 · Application Environment, Configuration and Security (25 %)", "4 · Application Environment, Configuration and Security (25%)"), T(
    "ConfigMaps, Secrets, ServiceAccounts, RBAC, admission, ressources, SecurityContext et CRD.",
    "ConfigMaps, Secrets, ServiceAccounts, RBAC, admission, resources, SecurityContext and CRDs."))

concept("configmaps", T("ConfigMap", "ConfigMap"), T(
    "Configuration non sensible, en clés/valeurs. Création : `--from-literal`, `--from-file` (clé = nom du "
    "fichier), `--from-env-file`. Consommation : toutes les clés en variables (`envFrom`), une clé "
    "(`valueFrom.configMapKeyRef`), en fichiers (volume `configMap`, `items` pour choisir les clés). Les "
    "variables ne changent qu'au redémarrage ; les fichiers montés se mettent à jour (sauf `subPath`). "
    "`immutable: true` fige l'objet.",
    "Non-sensitive key/value configuration. Created with `--from-literal`, `--from-file` (key = file name), "
    "`--from-env-file`. Consumed as all keys in env vars (`envFrom`), one key (`valueFrom.configMapKeyRef`), "
    "or files (`configMap` volume, `items` to pick keys). Env vars only change on restart; mounted files are "
    "refreshed (except with `subPath`). `immutable: true` freezes the object."),
    cmd=r"""
printf 'LEVEL=debug\nCOLOR=blue\n' > /tmp/app.env
printf 'server { listen 8080; }\n' > /tmp/site.conf
kubectl -n cours create configmap web-conf --from-env-file=/tmp/app.env   # --from-env-file ne se combine pas
kubectl -n cours patch configmap web-conf -p '{"data":{"MODE":"prod"}}'    # avec --from-literal (refus kubectl)
kubectl -n cours create configmap nginx-conf --from-file=default.conf=/tmp/site.conf
kubectl -n cours get configmap web-conf -o yaml | yq '.data'
kubectl -n cours run cfg --image=busybox:1.37 $do -- sh -c 'env | sort; sleep 3600' > /tmp/cfg.yaml
yq -i '.spec.containers[0].envFrom = [{"configMapRef": {"name": "web-conf"}}]
       | .spec.containers[0].env = [{"name": "ONLY_MODE", "valueFrom": {"configMapKeyRef": {"name": "web-conf", "key": "MODE"}}}]
       | .spec.volumes = [{"name": "conf", "configMap": {"name": "nginx-conf"}}]
       | .spec.containers[0].volumeMounts = [{"name": "conf", "mountPath": "/etc/nginx/conf.d"}]' /tmp/cfg.yaml
kubectl apply -f /tmp/cfg.yaml && kubectl -n cours wait --for=condition=Ready pod/cfg --timeout=60s
kubectl -n cours exec cfg -- sh -c 'echo $LEVEL $ONLY_MODE; cat /etc/nginx/conf.d/default.conf'
""",
    trap=T("Une clé absente référencée par `configMapKeyRef` bloque le démarrage (`CreateContainerConfigError`), sauf `optional: true`.",
           "A missing key referenced by `configMapKeyRef` blocks startup (`CreateContainerConfigError`), unless `optional: true`."))

concept("secrets", T("Secret", "Secret"), T(
    "Comme une ConfigMap, pour les données sensibles : `generic`, `docker-registry` (authentification au "
    "registre, référencée par `imagePullSecrets`), `tls` (certificat + clé). `data` est encodé en **base64** — "
    "pas chiffré ; `stringData` accepte du texte clair à la création. Consommation : `envFrom.secretRef`, "
    "`valueFrom.secretKeyRef`, volume `secret` (`defaultMode`).",
    "Like a ConfigMap, for sensitive data: `generic`, `docker-registry` (registry auth, referenced through "
    "`imagePullSecrets`), `tls` (certificate + key). `data` is **base64**-encoded — not encrypted; `stringData` "
    "accepts plain text on creation. Consumed via `envFrom.secretRef`, `valueFrom.secretKeyRef`, `secret` volume "
    "(`defaultMode`)."),
    cmd=r"""
kubectl -n cours create secret generic db --from-literal=user=app --from-literal='password=S3cr3t!'
kubectl -n cours get secret db -o jsonpath='{.data.password}' | base64 -d; echo
kubectl -n cours create secret docker-registry regcred --docker-server=registry.example.com \
  --docker-username=ckad --docker-password=pass --docker-email=ckad@example.com
openssl req -x509 -nodes -newkey rsa:2048 -days 1 -subj /CN=shop.lab.local -keyout /tmp/tls.key -out /tmp/tls.crt 2>/dev/null
kubectl -n cours create secret tls shop-tls --cert=/tmp/tls.crt --key=/tmp/tls.key
kubectl -n cours get secrets
""",
    yaml=r"""
apiVersion: v1
kind: Pod
metadata: {name: uses-secret}
spec:
  imagePullSecrets: [{name: regcred}]
  volumes:
  - name: creds
    secret: {secretName: db, defaultMode: 0400}
  containers:
  - name: app
    image: busybox:1.37
    command: ["sleep", "3600"]
    env:
    - name: DB_PASSWORD
      valueFrom: {secretKeyRef: {name: db, key: password}}
    envFrom:
    - secretRef: {name: db}
      prefix: DB_
    volumeMounts: [{name: creds, mountPath: /etc/creds, readOnly: true}]
""")

concept("serviceaccounts", T("ServiceAccount et jetons", "ServiceAccount and tokens"), T(
    "Un **ServiceAccount** est l'identité d'un Pod auprès de l'API. Chaque namespace a `default`. Le Pod le "
    "choisit par `serviceAccountName` ; le jeton est monté dans `/var/run/secrets/kubernetes.io/serviceaccount` "
    "sauf `automountServiceAccountToken: false`. `kubectl create token` émet un jeton temporaire.",
    "A **ServiceAccount** is a Pod's identity towards the API. Every namespace has `default`. The Pod picks it "
    "with `serviceAccountName`; the token is mounted in `/var/run/secrets/kubernetes.io/serviceaccount` unless "
    "`automountServiceAccountToken: false`. `kubectl create token` issues a short-lived token."),
    cmd=r"""
kubectl -n cours create serviceaccount reader
kubectl -n cours set serviceaccount deploy/front reader
kubectl -n cours rollout status deploy/front --timeout=120s
kubectl -n cours get pods -l app=front -o custom-columns=POD:.metadata.name,SA:.spec.serviceAccountName
kubectl -n cours create token reader --duration=10m | cut -c1-20; echo …
kubectl -n cours patch serviceaccount reader -p '{"automountServiceAccountToken": false}'
""")

concept("rbac", T("RBAC : Role, ClusterRole, bindings", "RBAC: Role, ClusterRole, bindings"), T(
    "Une **Role** liste des droits (verbes × ressources) dans un namespace ; une **ClusterRole**, à l'échelle "
    "du cluster ou réutilisable. Un **RoleBinding** / **ClusterRoleBinding** les accorde à des sujets "
    "(utilisateur, groupe, ServiceAccount). Sous-ressources : `pods/log`, `pods/exec`, `deployments/scale`. "
    "`auth can-i` vérifie, `--as` usurpe une identité, `--list` liste tout.",
    "A **Role** lists permissions (verbs × resources) in a namespace; a **ClusterRole** does so cluster-wide or "
    "as a reusable template. A **RoleBinding** / **ClusterRoleBinding** grants them to subjects (user, group, "
    "ServiceAccount). Subresources: `pods/log`, `pods/exec`, `deployments/scale`. `auth can-i` checks, `--as` "
    "impersonates, `--list` lists everything."),
    cmd=r"""
kubectl -n cours create role pod-reader --verb=get,list,watch --resource=pods,pods/log
kubectl -n cours create rolebinding reader-pods --role=pod-reader --serviceaccount=cours:reader
kubectl auth can-i list pods -n cours --as=system:serviceaccount:cours:reader
kubectl auth can-i delete pods -n cours --as=system:serviceaccount:cours:reader || true
kubectl auth can-i --list -n cours --as=system:serviceaccount:cours:reader | head -6
kubectl create clusterrole cours-node-viewer --verb=get,list --resource=nodes
kubectl create clusterrolebinding cours-node-viewer --clusterrole=cours-node-viewer --serviceaccount=cours:reader
kubectl auth can-i list nodes --as=system:serviceaccount:cours:reader
kubectl -n cours create rolebinding view-all --clusterrole=view --serviceaccount=cours:reader   # ClusterRole dans un namespace
""",
    trap=T("Le sujet d'un ServiceAccount s'écrit `<namespace>:<nom>` dans `--serviceaccount`, et `system:serviceaccount:<ns>:<nom>` dans `--as`.",
           "A ServiceAccount subject is `<namespace>:<name>` in `--serviceaccount`, and `system:serviceaccount:<ns>:<name>` in `--as`."))

concept("authn", T("Authentification, autorisation, admission", "Authentication, authorization, admission"), T(
    "Chaque requête passe trois étapes : **authentification** (qui ? certificat client, jeton de "
    "ServiceAccount, OIDC — défini dans le kubeconfig), **autorisation** (a-t-il le droit ? RBAC), "
    "**contrôle d'admission** (la requête est-elle acceptable ? ResourceQuota, LimitRange, Pod Security "
    "Admission, webhooks). Un refus d'autorisation donne `Forbidden` ; un refus d'admission, un message du "
    "contrôleur concerné.",
    "Every request goes through three steps: **authentication** (who? client certificate, ServiceAccount "
    "token, OIDC — defined in the kubeconfig), **authorization** (allowed? RBAC), **admission control** (is the "
    "request acceptable? ResourceQuota, LimitRange, Pod Security Admission, webhooks). An authorization "
    "refusal gives `Forbidden`; an admission refusal, a message from the controller involved."),
    cmd=r"""
kubectl config view --minify -o jsonpath='{.users[0].name}'; echo
kubectl config view --minify | grep -E 'client-certificate|token' | sed 's/:.*/: …/'
kubectl auth whoami
kubectl -n cours get secrets --as=system:serviceaccount:cours:reader || true     # Forbidden
""")

concept("resources", T("Requests, limits et QoS", "Requests, limits and QoS"), T(
    "**requests** : ce que le scheduler réserve (un Pod trop gourmand reste `Pending`). **limits** : CPU bridé "
    "au-delà, mémoire dépassée = `OOMKilled`. Unités : CPU en cœurs (`500m` = 0,5), mémoire en `Mi`/`Gi`. "
    "Classe **QoS** : `Guaranteed` (requests = limits partout), `Burstable`, `BestEffort` (rien).",
    "**requests**: what the scheduler reserves (an oversized Pod stays `Pending`). **limits**: CPU is throttled "
    "above it, memory over it = `OOMKilled`. Units: CPU in cores (`500m` = 0.5), memory in `Mi`/`Gi`. **QoS** "
    "class: `Guaranteed` (requests = limits everywhere), `Burstable`, `BestEffort` (nothing)."),
    cmd=r"""
kubectl -n cours set resources deploy front --requests=cpu=50m,memory=32Mi --limits=cpu=50m,memory=32Mi
kubectl -n cours rollout status deploy/front --timeout=120s
kubectl -n cours get pods -l app=front -o jsonpath='{.items[0].status.qosClass}'; echo
kubectl describe node ckad-a-worker | grep -A6 'Allocated resources'
""")

concept("quotas", T("ResourceQuota et LimitRange", "ResourceQuota and LimitRange"), T(
    "Une **ResourceQuota** plafonne un namespace (`pods`, `requests.cpu`, `limits.memory`, nombre d'objets…). "
    "Avec un quota sur les requests/limits, un Pod qui n'en déclare pas est **refusé**, sauf si une "
    "**LimitRange** injecte des valeurs par défaut (`defaultRequest`, `default`) et borne `min`/`max`.",
    "A **ResourceQuota** caps a namespace (`pods`, `requests.cpu`, `limits.memory`, object counts…). With a "
    "quota on requests/limits, a Pod that declares none is **rejected**, unless a **LimitRange** injects "
    "defaults (`defaultRequest`, `default`) and enforces `min`/`max`."),
    cmd=r"""
kubectl create namespace cours-b --dry-run=client -o yaml | kubectl apply -f -
kubectl -n cours-b create quota small --hard=pods=3,requests.cpu=500m,requests.memory=256Mi,limits.cpu=1,limits.memory=512Mi
kubectl -n cours-b run nolimits --image=busybox:1.37 -- sleep 3600 || echo "→ refusé : must specify requests/limits"
kubectl apply -n cours-b -f - <<'EOF'
apiVersion: v1
kind: LimitRange
metadata: {name: defaults}
spec:
  limits:
  - type: Container
    defaultRequest: {cpu: 50m, memory: 32Mi}
    default: {cpu: 100m, memory: 64Mi}
    max: {cpu: 500m, memory: 256Mi}
EOF
kubectl -n cours-b run withdefaults --image=busybox:1.37 -- sleep 3600
kubectl -n cours-b describe quota small
""")

concept("securitycontext", T("SecurityContext", "SecurityContext"), T(
    "Au niveau **Pod** : `runAsUser`, `runAsGroup`, `runAsNonRoot`, `fsGroup` (groupe des volumes), "
    "`seccompProfile`. Au niveau **conteneur** (prioritaire) : les mêmes `runAs*`, plus "
    "`allowPrivilegeEscalation`, `readOnlyRootFilesystem`, `privileged`, `capabilities: {add, drop}` — ces "
    "derniers n'existent qu'au niveau conteneur.",
    "At **Pod** level: `runAsUser`, `runAsGroup`, `runAsNonRoot`, `fsGroup` (volume group), `seccompProfile`. "
    "At **container** level (takes precedence): the same `runAs*`, plus `allowPrivilegeEscalation`, "
    "`readOnlyRootFilesystem`, `privileged`, `capabilities: {add, drop}` — the latter exist only at container "
    "level."),
    cmd=r"""
kubectl apply -n cours -f - <<'EOF'
apiVersion: v1
kind: Pod
metadata: {name: hardened}
spec:
  securityContext:
    runAsUser: 1000
    runAsGroup: 3000
    fsGroup: 2000
    runAsNonRoot: true
    seccompProfile: {type: RuntimeDefault}
  volumes: [{name: data, emptyDir: {}}]
  containers:
  - name: app
    image: busybox:1.37
    command: ["sh", "-c", "id; touch /data/ok && ls -ln /data; sleep 3600"]
    volumeMounts: [{name: data, mountPath: /data}]
    securityContext:
      allowPrivilegeEscalation: false
      readOnlyRootFilesystem: true
      capabilities: {drop: ["ALL"]}
EOF
kubectl -n cours wait --for=condition=Ready pod/hardened --timeout=60s
kubectl -n cours logs hardened
kubectl -n cours exec hardened -- touch /root-fs-test || echo "→ racine en lecture seule / read-only root"
""")

concept("podsecurity", T("Pod Security Admission", "Pod Security Admission"), T(
    "Les **Pod Security Standards** (`privileged`, `baseline`, `restricted`) s'appliquent par namespace via des "
    "labels : `pod-security.kubernetes.io/enforce` (refuse), `warn` (avertit), `audit` (journalise). Un Pod "
    "non conforme est refusé à la création.",
    "**Pod Security Standards** (`privileged`, `baseline`, `restricted`) are applied per namespace through "
    "labels: `pod-security.kubernetes.io/enforce` (reject), `warn` (warn), `audit` (log). A non-compliant Pod "
    "is rejected on creation."),
    cmd=r"""
kubectl label namespace cours-b pod-security.kubernetes.io/enforce=restricted --overwrite
kubectl -n cours-b run root-pod --image=busybox:1.37 --dry-run=server -- sleep 3600 || echo "→ refusé par restricted"
kubectl label namespace cours-b pod-security.kubernetes.io/enforce-
""")

concept("crd", T("CRD et opérateurs", "CRDs and operators"), T(
    "Une **CustomResourceDefinition** ajoute un type à l'API (groupe, version, `kind`, schéma OpenAPI). Un "
    "**opérateur** est un contrôleur qui agit sur ces objets. À l'examen : trouver la ressource "
    "(`get crd`, `api-resources --api-group`), lire son schéma (`explain`) et créer un objet valide.",
    "A **CustomResourceDefinition** adds a type to the API (group, version, `kind`, OpenAPI schema). An "
    "**operator** is a controller acting on those objects. In the exam: find the resource (`get crd`, "
    "`api-resources --api-group`), read its schema (`explain`) and create a valid object."),
    cmd=r"""
kubectl apply -f - <<'EOF'
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata: {name: certificats.cours.lab}
spec:
  group: cours.lab
  scope: Namespaced
  names: {plural: certificats, singular: certificat, kind: Certificat, shortNames: [cert]}
  versions:
  - name: v1
    served: true
    storage: true
    schema:
      openAPIV3Schema:
        type: object
        properties:
          spec:
            type: object
            required: [domaine]
            properties:
              domaine: {type: string}
              jours: {type: integer, minimum: 1}
EOF
kubectl wait --for=condition=Established crd/certificats.cours.lab --timeout=30s
for i in $(seq 1 30); do kubectl explain certificat.spec >/dev/null 2>&1 && break; sleep 1; done
kubectl api-resources --api-group=cours.lab
kubectl explain certificat.spec
printf 'apiVersion: cours.lab/v1\nkind: Certificat\nmetadata: {name: shop}\nspec: {domaine: shop.lab.local, jours: 90}\n' | kubectl -n cours apply -f -
kubectl -n cours get cert
""")

# =====================================================================================================
chapter("d5", "violet", T("5 · Services and Networking (20 %)", "5 · Services and Networking (20%)"), T(
    "Services, EndpointSlices, DNS, Ingress et NetworkPolicy.",
    "Services, EndpointSlices, DNS, Ingress and NetworkPolicy."))

concept("services", T("Services : ClusterIP, NodePort, LoadBalancer, ExternalName", "Services: ClusterIP, NodePort, LoadBalancer, ExternalName"), T(
    "Un **Service** donne une IP et un nom stables à un ensemble de Pods (sélecteur). `port` = port du Service, "
    "`targetPort` = port du conteneur (numéro ou nom). Types : `ClusterIP` (interne, défaut), `NodePort` "
    "(30000-32767 sur chaque nœud), `LoadBalancer` (IP externe fournie par le cloud), `ExternalName` (alias DNS).",
    "A **Service** gives a stable IP and name to a set of Pods (selector). `port` = Service port, `targetPort` = "
    "container port (number or name). Types: `ClusterIP` (internal, default), `NodePort` (30000-32767 on every "
    "node), `LoadBalancer` (external IP from the cloud), `ExternalName` (DNS alias)."),
    cmd=r"""
kubectl -n cours expose deploy front --name=front-np --type=NodePort --port=80 $do | yq '.spec.ports[0].nodePort = 30090' | kubectl apply -f -
kubectl -n cours create service externalname docs --external-name=kubernetes.io
kubectl -n cours get svc -o wide
kubectl -n cours run np --image=busybox:1.37 --restart=Never -- wget -qO- -T 5 http://$(kubectl get node ckad-a-worker -o jsonpath='{.status.addresses[0].address}'):30090
kubectl -n cours wait --for=jsonpath='{.status.phase}'=Succeeded pod/np --timeout=60s && kubectl -n cours logs np | grep -o '<title>.*</title>'
""",
    yaml=r"""
apiVersion: v1
kind: Service
metadata: {name: api}
spec:
  type: ClusterIP
  selector: {app: api}
  ports:
  - name: http
    port: 80             # port du Service / Service port
    targetPort: http     # nom du containerPort / containerPort name
    protocol: TCP
""")

concept("endpoints", T("EndpointSlices et dépannage d'un Service", "EndpointSlices and Service troubleshooting"), T(
    "Les **EndpointSlices** listent les Pods prêts derrière un Service. Vide : le sélecteur ne correspond à "
    "aucun Pod prêt (labels, readiness). Rempli mais `Connection refused` : `targetPort` faux. Toujours "
    "commencer par là.",
    "**EndpointSlices** list the ready Pods behind a Service. Empty: the selector matches no ready Pod (labels, "
    "readiness). Populated but `Connection refused`: wrong `targetPort`. Always start there."),
    cmd=r"""
kubectl -n cours get endpointslices -l kubernetes.io/service-name=front
kubectl -n cours describe svc front | grep -E 'Selector|TargetPort|Endpoints'
kubectl -n cours get pods -l app=front -o wide
kubectl -n cours create service clusterip ghost --tcp=80:80
kubectl -n cours get endpointslices -l kubernetes.io/service-name=ghost    # aucun endpoint / no endpoint
""")

concept("dns", T("DNS des Services et des Pods", "Service and Pod DNS"), T(
    "Nom d'un Service : `<svc>` (même namespace), `<svc>.<ns>`, `<svc>.<ns>.svc.cluster.local`. Un Pod "
    "d'un StatefulSet derrière un Service headless : `<pod>.<svc>.<ns>.svc.cluster.local`. Le résolveur est "
    "CoreDNS (`kube-dns` dans `kube-system`).",
    "A Service name: `<svc>` (same namespace), `<svc>.<ns>`, `<svc>.<ns>.svc.cluster.local`. A StatefulSet Pod "
    "behind a headless Service: `<pod>.<svc>.<ns>.svc.cluster.local`. The resolver is CoreDNS (`kube-dns` in "
    "`kube-system`)."),
    cmd=r"""
kubectl -n kube-system get svc kube-dns
kubectl -n cours run lookup --image=busybox:1.37 --restart=Never -- sh -c 'nslookup front; nslookup front.cours.svc.cluster.local; cat /etc/resolv.conf'
kubectl -n cours wait --for=jsonpath='{.status.phase}'=Succeeded pod/lookup --timeout=60s && kubectl -n cours logs lookup
""")

concept("ingress", T("Ingress, IngressClass et TLS", "Ingress, IngressClass and TLS"), T(
    "Un **Ingress** route le HTTP(S) entrant vers des Services selon l'hôte et le chemin (`pathType`: "
    "`Prefix`, `Exact`, `ImplementationSpecific`). Il faut un **contrôleur** (ici Traefik) et une "
    "`ingressClassName` existante. `tls` référence un Secret de type `kubernetes.io/tls`. `defaultBackend` "
    "reçoit ce qui ne correspond à aucune règle. Le backend vise le **port du Service**.",
    "An **Ingress** routes incoming HTTP(S) to Services by host and path (`pathType`: `Prefix`, `Exact`, "
    "`ImplementationSpecific`). It needs a **controller** (Traefik here) and an existing `ingressClassName`. "
    "`tls` references a `kubernetes.io/tls` Secret. `defaultBackend` receives anything matching no rule. The "
    "backend targets the **Service port**."),
    cmd=r"""
kubectl get ingressclass
kubectl -n cours create ingress shop --class=traefik \
  --rule='shop.lab.local/*=front:80' \
  --rule='shop.lab.local/blue*=web:80'                 # * = pathType Prefix ; sans * = Exact
kubectl -n cours create ingress shop-secure --class=traefik --rule='secure.lab.local/*=front:80,tls=shop-tls'
kubectl -n cours describe ingress shop | sed -n '/Rules:/,$p' | head -8
sleep 3
kubectl -n cours run curl --image=busybox:1.37 --restart=Never -- wget -qO- -T 5 --header=Host:shop.lab.local http://traefik.traefik.svc/blue
kubectl -n cours wait --for=jsonpath='{.status.phase}'=Succeeded pod/curl --timeout=60s && kubectl -n cours logs curl
# Codespace : curl -H 'Host: shop.lab.local' http://localhost:8080/
""",
    trap=T("Garde HTTP et TLS dans deux Ingress : avec certains contrôleurs (dont Traefik), une section `tls` rend "
           "toutes les règles de l'Ingress HTTPS seulement. Vérifie aussi l'ordre des chemins : Traefik classe les "
           "routes par longueur de règle, si bien qu'un `Exact` court peut perdre contre `/` en `Prefix` (constaté "
           "dans ce labo).",
           "Keep HTTP and TLS in two Ingresses: with some controllers (Traefik included), a `tls` section makes every "
           "rule of that Ingress HTTPS-only. Also check path ordering: Traefik ranks routes by rule length, so a short "
           "`Exact` path can lose to a `/` `Prefix` (observed in this lab)."),
    yaml=r"""
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata: {name: api}
spec:
  ingressClassName: traefik
  tls:
  - hosts: [api.lab.local]
    secretName: shop-tls
  defaultBackend:
    service: {name: front, port: {number: 80}}
  rules:
  - host: api.lab.local
    http:
      paths:
      - path: /v1
        pathType: Prefix
        backend:
          service: {name: front, port: {number: 80}}
      - path: /health
        pathType: Exact
        backend:
          service: {name: front, port: {number: 80}}
""")

concept("networkpolicy", T("NetworkPolicy", "NetworkPolicy"), T(
    "Dès qu'une politique **sélectionne** un Pod pour un sens (`policyTypes: Ingress|Egress`), tout ce qui "
    "n'est pas autorisé dans ce sens est refusé pour ce Pod ; les politiques s'additionnent. Sources/"
    "destinations : `podSelector` (même namespace), `namespaceSelector` (label "
    "`kubernetes.io/metadata.name`), `ipBlock`. Dans `from`/`to`, deux éléments = **OU** ; `namespaceSelector` "
    "et `podSelector` dans le même élément = **ET**. En Egress, pense au DNS (53/UDP et TCP). Il faut un CNI "
    "qui les applique.",
    "As soon as a policy **selects** a Pod for a direction (`policyTypes: Ingress|Egress`), everything not "
    "allowed in that direction is denied for that Pod; policies add up. Sources/destinations: `podSelector` "
    "(same namespace), `namespaceSelector` (label `kubernetes.io/metadata.name`), `ipBlock`. In `from`/`to`, "
    "two items = **OR**; `namespaceSelector` and `podSelector` in the same item = **AND**. For Egress, remember "
    "DNS (53/UDP and TCP). The CNI must enforce them."),
    cmd=r"""
kubectl apply -n cours -f - <<'EOF'
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata: {name: default-deny-ingress}
spec:
  podSelector: {matchLabels: {app: front}}
  policyTypes: [Ingress]
---
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata: {name: front-from-allowed}
spec:
  podSelector: {matchLabels: {app: front}}
  policyTypes: [Ingress]
  ingress:
  - from:
    - podSelector: {matchLabels: {access: "true"}}
    - namespaceSelector: {matchLabels: {kubernetes.io/metadata.name: traefik}}
    ports: [{protocol: TCP, port: 80}]
EOF
kubectl -n cours run ok --image=busybox:1.37 --labels=access=true --restart=Never -- wget -qO- -T 3 http://front
kubectl -n cours run ko --image=busybox:1.37 --restart=Never -- wget -qO- -T 3 http://front
kubectl -n cours wait --for=jsonpath='{.status.phase}'=Succeeded pod/ok --timeout=60s
kubectl -n cours wait --for=jsonpath='{.status.phase}'=Failed pod/ko --timeout=60s
kubectl -n cours logs ko                                       # download timed out
""",
    requires="netpol",
    yaml=r"""
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata: {name: api-egress}
spec:
  podSelector: {matchLabels: {app: api}}
  policyTypes: [Egress]
  egress:
  - to:
    - namespaceSelector: {matchLabels: {kubernetes.io/metadata.name: data}}
      podSelector: {matchLabels: {app: db}}         # même élément = ET / same item = AND
    ports: [{protocol: TCP, port: 5432}]
  - to:
    - ipBlock: {cidr: 10.0.0.0/8, except: [10.0.5.0/24]}
  - ports:                                           # DNS
    - {protocol: UDP, port: 53}
    - {protocol: TCP, port: 53}
""",
    trap=T("Une politique `Egress` sans le port 53 casse la résolution : `bad address` au lieu d'un refus.",
           "An `Egress` policy without port 53 breaks name resolution: `bad address` instead of a refusal."))

# =====================================================================================================
chapter("exam", "gris", T("6 · Technique d'examen", "6 · Exam technique"), T(
    "Le terminal, vim, la vitesse et le temps : ce qui transforme le savoir en points.",
    "The terminal, vim, speed and time: what turns knowledge into points."))

concept("speed", T("Shell et vim rapides", "Fast shell and vim"), T(
    "Sur les hôtes d'examen : `k` = kubectl et complétion déjà prêts. Ajoute `$do` et `$now`. Dans vim : "
    "`:set paste` avant de coller, `>>`/`<<` pour indenter, `V` puis `>` pour un bloc, `dd`, `yy`, `p`, `u`, "
    "`/mot` pour chercher, `:wq`. La touche Inser est interdite : utilise `i`.",
    "On exam hosts: `k` = kubectl and completion are already set. Add `$do` and `$now`. In vim: `:set paste` "
    "before pasting, `>>`/`<<` to indent, `V` then `>` for a block, `dd`, `yy`, `p`, `u`, `/word` to search, "
    "`:wq`. The Insert key is forbidden: use `i`."),
    cmd=r"""
alias k=kubectl
export do="--dry-run=client -o yaml" now="--force --grace-period 0"
cat >> ~/.vimrc <<'EOF'
set expandtab tabstop=2 shiftwidth=2 autoindent
EOF
k -n cours run tmp --image=busybox:1.37 $do -- sleep 60 > /tmp/tmp.yaml
k apply -f /tmp/tmp.yaml && k -n cours delete pod tmp $now
""",
    run=None,
    exam=T("Copier-coller dans le terminal d'examen : Ctrl+Maj+C / Ctrl+Maj+V.",
           "Copy-paste in the exam terminal: Ctrl+Shift+C / Ctrl+Shift+V."))

concept("timing", T("Gérer les deux heures", "Managing the two hours"), T(
    "15 à 20 tâches, 2 heures, 66 % pour réussir, crédit partiel par vérification. Compte environ une minute "
    "par point. Première passe sur tout ce qui est rapide, puis les tâches notées de côté. Avant chaque tâche : "
    "`ssh` vers l'hôte indiqué, contexte, namespace. Finis par les fichiers demandés (chemin exact). "
    "Documentation : kubernetes.io/docs, kubernetes.io/blog, helm.sh/docs.",
    "15-20 tasks, 2 hours, 66% to pass, partial credit per check. Budget about one minute per point. First "
    "pass on everything quick, then the tasks you flagged. Before each task: `ssh` to the given host, context, "
    "namespace. Finish with the requested files (exact path). Documentation: kubernetes.io/docs, "
    "kubernetes.io/blog, helm.sh/docs."),
    cmd=r"""
# Début de chaque tâche / start of every task
ssh <hôte>                        # indiqué dans l'en-tête / given in the header
kubectl config use-context <ctx>
kubectl config current-context
# … travail … puis vérification à la main / then check by hand
kubectl -n <ns> get <objet> -o yaml | less
exit                               # retour à la base / back to base
""",
    run=None)
