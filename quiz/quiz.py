"""QCU CKAD (questions à choix unique), bilingue. Une seule bonne réponse par question.

Q(id, domaine, question{fr,en}, choix, bonne_réponse (index), explication{fr,en}, cmd, verify)
  choix   : liste ; une chaîne = commande ou texte identique dans les deux langues, un dict = {fr, en}
  cmd     : la commande claire qui illustre la réponse (affichée après la réponse)
  verify  : script exécuté par scripts/verify-quiz.py dans le namespace « quiz » (contexte ckad-a) ;
            None si la question est purement conceptuelle (la commande reste affichée)
Domaines : 0 bases, 1 à 5 domaines officiels, 6 scénarios et technique d'examen.
"""

QUESTIONS = []


def Q(qid, domain, q, choices, answer, why, cmd, verify=None):
    QUESTIONS.append({"id": qid, "domain": domain, "q": q, "choices": choices, "answer": answer,
                      "why": why, "cmd": cmd, "verify": verify})


def T(fr, en):
    return {"fr": fr, "en": en}


DOMAINS = {
    "0": T("Bases", "Foundations"),
    "1": T("Application Design and Build", "Application Design and Build"),
    "2": T("Application Deployment", "Application Deployment"),
    "3": T("Observability and Maintenance", "Observability and Maintenance"),
    "4": T("Environment, Configuration and Security", "Environment, Configuration and Security"),
    "5": T("Services and Networking", "Services and Networking"),
    "6": T("Scénarios et technique d'examen", "Scenarios and exam technique"),
}


def intro(lang):
    if lang == "fr":
        return (f"{len(QUESTIONS)} questions à choix unique couvrent toutes les notions de l'examen, les scénarios du "
                "fil conducteur et la technique d'examen. Chaque réponse est expliquée par une commande précise ; les "
                "commandes marquées ✔ ont été **exécutées** par `scripts/verify-quiz.py`. Choisis un domaine, réponds, "
                "lis l'explication. Ton score reste dans ton navigateur. Dans le terminal du labo : `ex quiz`.")
    return (f"{len(QUESTIONS)} single-choice questions cover every exam topic, the running scenarios and exam technique. "
            "Each answer is explained with a precise command; commands marked ✔ were **executed** by "
            "`scripts/verify-quiz.py`. Pick a domain, answer, read the explanation. Your score stays in your browser. "
            "In the lab terminal: `ex quiz`.")


def export():
    return {"domains": DOMAINS, "questions": QUESTIONS}


# ===================================================================================== 0 · Bases
Q("b-context", "0", T("Quelle commande fait de `ckad-b` le contexte courant ?", "Which command makes `ckad-b` the current context?"),
  ["kubectl config set-context ckad-b", "kubectl config use-context ckad-b", "kubectl context ckad-b", "kubectl config current-context ckad-b"],
  1, T("`use-context` change le contexte courant ; `set-context` modifie un contexte, `current-context` l'affiche.",
       "`use-context` switches the current context; `set-context` edits a context, `current-context` prints it."),
  "kubectl config use-context ckad-b && kubectl config current-context",
  "kubectl config use-context ckad-b && kubectl config current-context && kubectl config use-context ckad-a")

Q("b-defaultns", "0", T("Comment définir `prod` comme namespace par défaut du contexte courant ?",
                        "How do you make `prod` the default namespace of the current context?"),
  ["kubectl namespace prod", "kubectl config set-context --current --namespace=prod", "export NAMESPACE=prod",
   "kubectl config use-context --namespace=prod"],
  1, T("Le namespace par défaut est un attribut du contexte, modifié par `set-context --current`.",
       "The default namespace is a context attribute, changed with `set-context --current`."),
  "kubectl config set-context --current --namespace=prod",
  "kubectl config set-context --current --namespace=prod && kubectl config view --minify | grep 'namespace: prod' && kubectl config set-context --current --namespace=default")

Q("b-explain", "0", T("Quelle commande affiche tous les sous-champs de `spec.strategy` d'un Deployment ?",
                      "Which command shows every sub-field of a Deployment's `spec.strategy`?"),
  ["kubectl describe deployment strategy", "kubectl explain deployment.spec.strategy --recursive",
   "kubectl get deployment -o strategy", "kubectl api-resources deployment.spec.strategy"],
  1, T("`explain` lit le schéma OpenAPI ; `--recursive` déroule l'arborescence.",
       "`explain` reads the OpenAPI schema; `--recursive` expands the tree."),
  "kubectl explain deployment.spec.strategy --recursive", "kubectl explain deployment.spec.strategy --recursive")

Q("b-dryrun", "0", T("Générer le YAML d'un Pod `web` (nginx) sans le créer :", "Generate a `web` Pod's YAML (nginx) without creating it:"),
  ["kubectl run web --image=nginx --dry-run=client -o yaml", "kubectl create pod web --image=nginx -o yaml",
   "kubectl get pod web -o yaml --export", "kubectl run web --image=nginx --output=file"],
  0, T("`--dry-run=client -o yaml` imprime l'objet sans l'envoyer ; `create pod` n'existe pas, `--export` a été supprimé.",
       "`--dry-run=client -o yaml` prints the object without sending it; `create pod` does not exist, `--export` was removed."),
  "kubectl run web --image=nginx --dry-run=client -o yaml > web.yaml",
  "kubectl -n quiz run web --image=nginx --dry-run=client -o yaml | grep 'kind: Pod'")

Q("b-shortname", "0", T("Comment lister les types de ressources du groupe `apps` avec leurs noms courts ?",
                        "How do you list the `apps` group resource types with their short names?"),
  ["kubectl get apps", "kubectl api-versions apps", "kubectl api-resources --api-group=apps", "kubectl explain apps"],
  2, T("`api-resources` donne nom, nom court, version, namespace oui/non et kind.",
       "`api-resources` gives name, short name, version, namespaced yes/no and kind."),
  "kubectl api-resources --api-group=apps", "kubectl api-resources --api-group=apps | grep deployments")

Q("b-labelsel", "0", T("Lister les Pods `app=shop` qui ne sont **pas** `tier=db` :", "List `app=shop` Pods that are **not** `tier=db`:"),
  ["kubectl get pods -l app=shop -l tier=db --invert", "kubectl get pods -l 'app=shop,tier!=db'",
   "kubectl get pods --selector app=shop --not tier=db", "kubectl get pods -l app=shop | grep -v db"],
  1, T("Les sélecteurs se combinent par virgule (ET) ; `!=` exclut une valeur.", "Selectors combine with commas (AND); `!=` excludes a value."),
  "kubectl get pods -l 'app=shop,tier!=db' --show-labels", "kubectl -n quiz get pods -l 'app=shop,tier!=db'")

Q("b-removelabel", "0", T("Retirer le label `env` du Pod `api` :", "Remove the `env` label from Pod `api`:"),
  ["kubectl label pod api env=", "kubectl label pod api env-", "kubectl unlabel pod api env", "kubectl label pod api --remove env"],
  1, T("Le suffixe `-` après la clé supprime le label.", "A trailing `-` after the key removes the label."),
  "kubectl label pod api env-", "kubectl -n quiz label pod tool env=x --overwrite && kubectl -n quiz label pod tool env-")

Q("b-jsonpath", "0", T("Écrire l'IP du Pod `web` dans `/tmp/ip.txt` :", "Write Pod `web`'s IP into `/tmp/ip.txt`:"),
  ["kubectl get pod web -o wide > /tmp/ip.txt", "kubectl get pod web -o jsonpath='{.status.podIP}' > /tmp/ip.txt",
   "kubectl describe pod web | grep IP > /tmp/ip.txt", "kubectl get pod web --ip > /tmp/ip.txt"],
  1, T("jsonpath extrait exactement la valeur, sans en-tête ni autre texte.", "jsonpath extracts exactly the value, without headers or extra text."),
  "kubectl get pod web -o jsonpath='{.status.podIP}' > /tmp/ip.txt",
  "kubectl -n quiz get pod tool -o jsonpath='{.status.podIP}' > /tmp/ip.txt && grep -E '^[0-9.]+$' /tmp/ip.txt")

Q("b-replace", "0", T("Le champ que tu modifies sur un Pod existant est immuable. Que faire ?",
                      "The field you change on an existing Pod is immutable. What do you do?"),
  ["kubectl apply -f pod.yaml --force-update", "kubectl replace --force -f pod.yaml", "kubectl patch pod --immutable=false",
   "kubectl edit pod --recreate"],
  1, T("`replace --force` supprime puis recrée l'objet depuis le fichier.", "`replace --force` deletes then recreates the object from the file."),
  "kubectl get pod web -o yaml > pod.yaml && vim pod.yaml && kubectl replace --force -f pod.yaml",
  "kubectl -n quiz get pod tool -o yaml > /tmp/tool.yaml && kubectl replace --force -f /tmp/tool.yaml && kubectl -n quiz wait --for=condition=Ready pod/tool --timeout=60s")

Q("b-sortby", "0", T("Lister les Pods de tous les namespaces, triés par date de création :", "List Pods in all namespaces, sorted by creation time:"),
  ["kubectl get pods -A --sort-by=.metadata.creationTimestamp", "kubectl get pods --all --order=age",
   "kubectl get pods -A | sort -k5", "kubectl get pods -A --sort-by=age"],
  0, T("`--sort-by` prend un chemin JSON, pas un nom de colonne.", "`--sort-by` takes a JSON path, not a column name."),
  "kubectl get pods -A --sort-by=.metadata.creationTimestamp", "kubectl get pods -A --sort-by=.metadata.creationTimestamp | head -3")

# ===================================================================================== 1 · Design and Build
Q("d1-cmdargs", "1", T("Dans un Pod, quel champ remplace l'`ENTRYPOINT` de l'image ?", "In a Pod, which field overrides the image `ENTRYPOINT`?"),
  ["args", "command", "entrypoint", "exec"],
  1, T("`command` remplace ENTRYPOINT, `args` remplace CMD.", "`command` overrides ENTRYPOINT, `args` overrides CMD."),
  "kubectl run t --image=busybox:1.37 --command -- sleep 3600 && kubectl get pod t -o jsonpath='{.spec.containers[0].command}'",
  "kubectl -n quiz run t --image=busybox:1.37 --command --dry-run=server -o jsonpath='{.spec.containers[0].command}' -- sleep 3600 | grep sleep")

Q("d1-run-args", "1", T("`kubectl run x --image=busybox -- sleep 60` place `sleep 60` dans :", "`kubectl run x --image=busybox -- sleep 60` puts `sleep 60` into:"),
  ["command", "args", "env", "lifecycle.postStart"],
  1, T("Sans `--command`, ce qui suit `--` devient `args`.", "Without `--command`, what follows `--` becomes `args`."),
  "kubectl run x --image=busybox:1.37 --dry-run=client -o jsonpath='{.spec.containers[0].args}' -- sleep 60",
  "kubectl -n quiz run x --image=busybox:1.37 --dry-run=client -o jsonpath='{.spec.containers[0].args}' -- sleep 60 | grep sleep")

Q("d1-job-fields", "1", T("Un Job doit réussir 5 fois, 2 Pods à la fois. Quels champs, et où ?",
                          "A Job must succeed 5 times, 2 Pods at a time. Which fields, and where?"),
  [T("`spec.completions: 5`, `spec.parallelism: 2`", "`spec.completions: 5`, `spec.parallelism: 2`"),
   T("`spec.template.spec.completions: 5`, `parallelism: 2`", "`spec.template.spec.completions: 5`, `parallelism: 2`"),
   T("`spec.replicas: 5`, `spec.maxSurge: 2`", "`spec.replicas: 5`, `spec.maxSurge: 2`"),
   T("`spec.backoffLimit: 5`, `spec.parallelism: 2`", "`spec.backoffLimit: 5`, `spec.parallelism: 2`")],
  0, T("`completions` et `parallelism` sont sous `spec` du Job, pas dans le template ; `backoffLimit` compte les relances.",
       "`completions` and `parallelism` live under the Job's `spec`, not the template; `backoffLimit` counts retries."),
  "kubectl create job j --image=busybox:1.37 --dry-run=client -o yaml -- echo ok | yq '.spec.completions=5 | .spec.parallelism=2' | kubectl apply -f -",
  "kubectl -n quiz create job j --image=busybox:1.37 --dry-run=client -o yaml -- echo ok | yq '.spec.completions=5 | .spec.parallelism=2' | kubectl -n quiz apply --dry-run=server -f -")

Q("d1-job-restart", "1", T("Quelle `restartPolicy` est **refusée** dans un Job ?", "Which `restartPolicy` is **rejected** in a Job?"),
  ["Never", "OnFailure", "Always", T("Aucune", "None")],
  2, T("Un Job doit pouvoir se terminer : `Always` est interdit.", "A Job must be able to finish: `Always` is forbidden."),
  "kubectl explain job.spec.template.spec.restartPolicy",
  "kubectl -n quiz create job bad --image=busybox:1.37 --dry-run=client -o yaml -- echo | yq '.spec.template.spec.restartPolicy=\"Always\"' | kubectl -n quiz apply --dry-run=server -f - 2>&1 | grep -i 'valid values'")

Q("d1-cron-schedule", "1", T("Quelle planification lance un CronJob toutes les 15 minutes ?", "Which schedule runs a CronJob every 15 minutes?"),
  ["15 * * * *", "*/15 * * * *", "* */15 * * *", "@every 15m"],
  1, T("`*/15` dans le champ minute = toutes les 15 minutes ; `15 * * * *` = à la 15e minute de chaque heure.",
       "`*/15` in the minute field = every 15 minutes; `15 * * * *` = at minute 15 of every hour."),
  "kubectl create cronjob c --image=busybox:1.37 --schedule='*/15 * * * *' -- date",
  "kubectl -n quiz create cronjob c --image=busybox:1.37 --schedule='*/15 * * * *' --dry-run=server -- date")

Q("d1-cron-now", "1", T("Exécuter tout de suite le CronJob `backup` :", "Run the `backup` CronJob right now:"),
  ["kubectl run backup --from=cronjob", "kubectl create job backup-now --from=cronjob/backup",
   "kubectl trigger cronjob backup", "kubectl rollout restart cronjob/backup"],
  1, T("`create job --from=cronjob/<nom>` instancie le modèle du CronJob.", "`create job --from=cronjob/<name>` instantiates the CronJob template."),
  "kubectl create job backup-now --from=cronjob/backup",
  "kubectl -n quiz create job c-now --from=cronjob/c --dry-run=server 2>/dev/null || (kubectl -n quiz create cronjob c --image=busybox:1.37 --schedule='0 1 * * *' -- date && kubectl -n quiz create job c-now --from=cronjob/c --dry-run=server)")

Q("d1-cron-forbid", "1", T("Une exécution ne doit jamais démarrer tant que la précédente tourne :", "A run must never start while the previous one is still running:"),
  ["concurrencyPolicy: Allow", "concurrencyPolicy: Forbid", "concurrencyPolicy: Replace", "suspend: true"],
  1, T("`Forbid` saute l'exécution ; `Replace` tue la précédente ; `suspend` arrête toute planification.",
       "`Forbid` skips the run; `Replace` kills the previous one; `suspend` stops all scheduling."),
  "kubectl patch cronjob c -p '{\"spec\":{\"concurrencyPolicy\":\"Forbid\"}}'",
  "kubectl -n quiz get cronjob c >/dev/null 2>&1 || kubectl -n quiz create cronjob c --image=busybox:1.37 --schedule='0 1 * * *' -- date; kubectl -n quiz patch cronjob c -p '{\"spec\":{\"concurrencyPolicy\":\"Forbid\"}}'")

Q("d1-sidecar", "1", T("Comment déclare-t-on un **sidecar natif** ?", "How do you declare a **native sidecar**?"),
  [T("Un second conteneur sous `containers`", "A second container under `containers`"),
   T("Un `initContainer` avec `restartPolicy: Always`", "An `initContainer` with `restartPolicy: Always`"),
   T("Un conteneur avec `sidecar: true`", "A container with `sidecar: true`"),
   T("Un `ephemeralContainer`", "An `ephemeralContainer`")],
  1, T("Depuis 1.29 (stable en 1.33), un init container `restartPolicy: Always` démarre avant l'app et vit avec elle.",
       "Since 1.29 (stable in 1.33), an init container with `restartPolicy: Always` starts before the app and lives with it."),
  "kubectl explain pod.spec.initContainers.restartPolicy",
  "printf 'apiVersion: v1\\nkind: Pod\\nmetadata: {name: sc}\\nspec:\\n  initContainers: [{name: s, image: busybox:1.37, restartPolicy: Always, command: [sleep, \"3600\"]}]\\n  containers: [{name: a, image: busybox:1.37, command: [sleep, \"3600\"]}]\\n' | kubectl -n quiz apply --dry-run=server -f -")

Q("d1-init-order", "1", T("Deux init containers sont déclarés. Comment s'exécutent-ils ?", "Two init containers are declared. How do they run?"),
  [T("En parallèle, avant l'application", "In parallel, before the app"),
   T("Dans l'ordre, chacun jusqu'au bout, avant l'application", "In order, each to completion, before the app"),
   T("En même temps que l'application", "Alongside the app"),
   T("Seulement si l'application échoue", "Only if the app fails")],
  1, T("Les init containers sont séquentiels ; le Pod reste `Init:N/M` tant qu'ils n'ont pas fini.",
       "Init containers are sequential; the Pod stays `Init:N/M` until they finish."),
  "kubectl get pod web -o jsonpath='{.status.initContainerStatuses[*].state}'")

Q("d1-multilogs", "1", T("Lire les logs du conteneur `shipper` du Pod `web` :", "Read the logs of container `shipper` in Pod `web`:"),
  ["kubectl logs web/shipper", "kubectl logs web -c shipper", "kubectl logs shipper -p web", "kubectl logs web --container-name shipper"],
  1, T("`-c` (ou `--container`) choisit le conteneur.", "`-c` (or `--container`) selects the container."),
  "kubectl logs web -c shipper --tail=20", "kubectl -n quiz logs multi -c side --tail=1")

Q("d1-emptydir-mem", "1", T("Un volume temporaire en RAM, limité à 64Mi :", "A temporary RAM-backed volume capped at 64Mi:"),
  ["emptyDir: {medium: Memory, sizeLimit: 64Mi}", "hostPath: {path: /dev/shm, size: 64Mi}",
   "tmpfs: {size: 64Mi}", "emptyDir: {type: ram, limit: 64Mi}"],
  0, T("`emptyDir.medium: Memory` monte un tmpfs ; `sizeLimit` le borne.", "`emptyDir.medium: Memory` mounts a tmpfs; `sizeLimit` caps it."),
  "kubectl explain pod.spec.volumes.emptyDir",
  "printf 'apiVersion: v1\\nkind: Pod\\nmetadata: {name: m}\\nspec:\\n  volumes: [{name: v, emptyDir: {medium: Memory, sizeLimit: 64Mi}}]\\n  containers: [{name: a, image: busybox:1.37, command: [sleep, \"60\"], volumeMounts: [{name: v, mountPath: /v}]}]\\n' | kubectl -n quiz apply --dry-run=server -f -")

Q("d1-pvc-pending", "1", T("Un PVC reste `Pending` avec la StorageClass `standard` de kind et aucun Pod ne l'utilise. Pourquoi ?",
                            "A PVC stays `Pending` with kind's `standard` StorageClass and no Pod uses it. Why?"),
  [T("La StorageClass est en panne", "The StorageClass is broken"),
   T("`volumeBindingMode: WaitForFirstConsumer` : il attend un Pod", "`volumeBindingMode: WaitForFirstConsumer`: it waits for a Pod"),
   T("Il manque un PV créé à la main", "A manually created PV is missing"),
   T("Le namespace a un quota", "The namespace has a quota")],
  1, T("Le provisionnement attend le premier Pod consommateur, pour choisir le bon nœud.",
       "Provisioning waits for the first consuming Pod, to pick the right node."),
  "kubectl get storageclass standard -o jsonpath='{.volumeBindingMode}'",
  "kubectl get storageclass standard -o jsonpath='{.volumeBindingMode}' | grep WaitForFirstConsumer")

Q("d1-pvc-mode", "1", T("Quel mode d'accès permet à **un seul nœud** de monter le volume en lecture-écriture ?",
                        "Which access mode lets **a single node** mount the volume read-write?"),
  ["ReadWriteMany", "ReadOnlyMany", "ReadWriteOnce", "ReadWriteOncePod"],
  2, T("`ReadWriteOnce` = un nœud ; `ReadWriteOncePod` = un seul Pod ; `ReadWriteMany` = plusieurs nœuds.",
       "`ReadWriteOnce` = one node; `ReadWriteOncePod` = a single Pod; `ReadWriteMany` = many nodes."),
  "kubectl explain pvc.spec.accessModes")

Q("d1-pv-scope", "1", T("Lequel de ces objets n'appartient à **aucun** namespace ?", "Which of these objects belongs to **no** namespace?"),
  ["PersistentVolumeClaim", "PersistentVolume", "ConfigMap", "ServiceAccount"],
  1, T("Les PV (comme les nœuds, les StorageClass, les ClusterRoles) sont à l'échelle du cluster.",
       "PVs (like nodes, StorageClasses, ClusterRoles) are cluster-scoped."),
  "kubectl api-resources --namespaced=false | grep -E 'persistentvolumes|storageclasses'",
  "kubectl api-resources --namespaced=false | grep -q '^persistentvolumes '")

Q("d1-daemonset-cp", "1", T("Un DaemonSet ignore le nœud control-plane. La correction :", "A DaemonSet skips the control-plane node. The fix:"),
  [T("Ajouter `replicas: 3`", "Add `replicas: 3`"),
   T("Tolérer `node-role.kubernetes.io/control-plane:NoSchedule`", "Tolerate `node-role.kubernetes.io/control-plane:NoSchedule`"),
   T("Ajouter `nodeName: control-plane`", "Add `nodeName: control-plane`"),
   T("Retirer le taint avec `kubectl uncordon`", "Remove the taint with `kubectl uncordon`")],
  1, T("Le control-plane porte un taint NoSchedule ; une toleration autorise le Pod à y aller.",
       "The control plane carries a NoSchedule taint; a toleration allows the Pod there."),
  "kubectl describe node ckad-a-control-plane | grep Taints",
  "kubectl describe node ckad-a-control-plane | grep -q 'node-role.kubernetes.io/control-plane:NoSchedule'")

Q("d1-nodeselector", "1", T("Forcer un Pod sur les nœuds étiquetés `disk=ssd` :", "Force a Pod onto nodes labelled `disk=ssd`:"),
  ["spec.nodeName: disk=ssd", "spec.nodeSelector: {disk: ssd}", "spec.tolerations: [{key: disk, value: ssd}]", "metadata.labels: {disk: ssd}"],
  1, T("`nodeSelector` filtre les nœuds par labels ; une toleration ne fait qu'autoriser un nœud tainté.",
       "`nodeSelector` filters nodes by labels; a toleration only allows a tainted node."),
  "kubectl run fast --image=nginx --dry-run=client -o yaml | yq '.spec.nodeSelector={\"disk\":\"ssd\"}' | kubectl apply -f -",
  "kubectl -n quiz run fast --image=nginx --dry-run=client -o yaml | yq '.spec.nodeSelector={\"disk\":\"ssd\"}' | kubectl -n quiz apply --dry-run=server -f -")

Q("d1-docker-save", "1", T("Exporter l'image `app:v1` dans `app.tar` :", "Export image `app:v1` into `app.tar`:"),
  ["docker export app:v1 > app.tar", "docker save -o app.tar app:v1", "docker push app:v1 app.tar", "docker build -o app.tar app:v1"],
  1, T("`save` exporte une **image** (couches et tags) ; `export` exporte le système de fichiers d'un **conteneur**.",
       "`save` exports an **image** (layers and tags); `export` exports a **container**'s filesystem."),
  "docker save -o app.tar app:v1   # podman save -o app.tar app:v1",
  "docker save -o /tmp/quiz-bb.tar busybox:1.37 && tar -tf /tmp/quiz-bb.tar | grep -q manifest.json")

Q("d1-expose-inst", "1", T("Que fait l'instruction `EXPOSE 8080` d'un Dockerfile ?", "What does a Dockerfile `EXPOSE 8080` instruction do?"),
  [T("Elle publie le port sur l'hôte", "It publishes the port on the host"),
   T("Elle documente le port ; rien n'est publié", "It documents the port; nothing is published"),
   T("Elle crée un Service Kubernetes", "It creates a Kubernetes Service"),
   T("Elle ouvre le pare-feu du nœud", "It opens the node firewall")],
  1, T("C'est une métadonnée ; il faut un Service (ou `-p` avec docker) pour exposer.",
       "It is metadata; you need a Service (or `-p` with docker) to expose."),
  "docker image inspect app:v1 --format '{{json .Config.ExposedPorts}}'")

Q("d1-statefulset", "1", T("Quel nom DNS stable reçoit le Pod `db-0` d'un StatefulSet `db` (Service headless `db`, namespace `data`) ?",
                           "Which stable DNS name does Pod `db-0` of StatefulSet `db` get (headless Service `db`, namespace `data`)?"),
  ["db.data.svc.cluster.local", "db-0.db.data.svc.cluster.local", "db-0.data.pod.cluster.local", "db-0.statefulset.data"],
  1, T("Avec un Service headless (`clusterIP: None`), chaque Pod a `<pod>.<service>.<ns>.svc.cluster.local`.",
       "With a headless Service (`clusterIP: None`), each Pod gets `<pod>.<service>.<ns>.svc.cluster.local`."),
  "kubectl run t --rm -it --image=busybox:1.37 --restart=Never -- nslookup db-0.db.data.svc.cluster.local")

# ===================================================================================== 2 · Deployment
Q("d2-setimage", "2", T("Passer le conteneur `nginx` du Deployment `web` en `nginx:1.28-alpine` :",
                        "Update container `nginx` of Deployment `web` to `nginx:1.28-alpine`:"),
  ["kubectl set image deploy/web nginx=nginx:1.28-alpine", "kubectl update deploy web --image=nginx:1.28-alpine",
   "kubectl rollout image deploy/web nginx:1.28-alpine", "kubectl patch deploy web --image nginx:1.28-alpine"],
  0, T("`set image <ressource> <conteneur>=<image>` déclenche un rolling update.", "`set image <resource> <container>=<image>` triggers a rolling update."),
  "kubectl set image deploy/web nginx=nginx:1.28-alpine && kubectl rollout status deploy/web",
  "kubectl -n quiz set image deploy/web nginx=nginx:1.28-alpine && kubectl -n quiz rollout status deploy/web --timeout=120s")

Q("d2-history", "2", T("Afficher les révisions du Deployment `web` :", "Show the revisions of Deployment `web`:"),
  ["kubectl get rs web --history", "kubectl rollout history deploy/web", "kubectl describe deploy web --revisions", "kubectl rollout log deploy/web"],
  1, T("`rollout history` liste les révisions ; `--revision=N` détaille l'une d'elles.", "`rollout history` lists revisions; `--revision=N` details one."),
  "kubectl rollout history deploy/web --revision=2", "kubectl -n quiz rollout history deploy/web")

Q("d2-undo", "2", T("Revenir à la révision **1** du Deployment `web` :", "Roll Deployment `web` back to revision **1**:"),
  ["kubectl rollout undo deploy/web", "kubectl rollout undo deploy/web --to-revision=1", "kubectl rollback deploy/web 1", "kubectl set revision deploy/web 1"],
  1, T("Sans `--to-revision`, `undo` revient à la révision **précédente**, pas forcément à la 1.",
       "Without `--to-revision`, `undo` goes back to the **previous** revision, not necessarily 1."),
  "kubectl rollout undo deploy/web --to-revision=1",
  "kubectl -n quiz rollout undo deploy/web --to-revision=1 && kubectl -n quiz rollout status deploy/web --timeout=120s")

Q("d2-cause", "2", T("Faire apparaître un motif dans `rollout history` (`--record` n'existe plus) :", "Show a cause in `rollout history` (`--record` is gone):"),
  ["kubectl annotate deploy web kubernetes.io/change-cause='v2'", "kubectl label deploy web change-cause=v2",
   "kubectl rollout history deploy/web --set-cause=v2", "kubectl set cause deploy/web v2"],
  0, T("La colonne CHANGE-CAUSE lit l'annotation `kubernetes.io/change-cause`.", "The CHANGE-CAUSE column reads the `kubernetes.io/change-cause` annotation."),
  "kubectl annotate deploy web kubernetes.io/change-cause='v2' --overwrite",
  "kubectl -n quiz annotate deploy web kubernetes.io/change-cause='quiz' --overwrite")

Q("d2-maxunavail", "2", T("La mise à jour ne doit jamais réduire la capacité. Quel réglage ?", "The update must never reduce capacity. Which setting?"),
  ["maxSurge: 0", "maxUnavailable: 0", "minReadySeconds: 0", "strategy.type: Recreate"],
  1, T("`maxUnavailable: 0` interdit de retirer un Pod avant qu'un nouveau soit prêt (avec `maxSurge` ≥ 1).",
       "`maxUnavailable: 0` forbids removing a Pod before a new one is ready (with `maxSurge` ≥ 1)."),
  "kubectl patch deploy web -p '{\"spec\":{\"strategy\":{\"rollingUpdate\":{\"maxSurge\":1,\"maxUnavailable\":0}}}}'",
  "kubectl -n quiz patch deploy web -p '{\"spec\":{\"strategy\":{\"rollingUpdate\":{\"maxSurge\":1,\"maxUnavailable\":0}}}}'")

Q("d2-recreate", "2", T("Passer en `Recreate` échoue : `may not be specified when strategy type is 'Recreate'`. Pourquoi ?",
                        "Switching to `Recreate` fails: `may not be specified when strategy type is 'Recreate'`. Why?"),
  [T("Recreate exige `replicas: 1`", "Recreate requires `replicas: 1`"),
   T("Le bloc `rollingUpdate` doit être supprimé", "The `rollingUpdate` block must be removed"),
   T("Il faut d'abord `rollout pause`", "You must `rollout pause` first"),
   T("Recreate n'existe plus", "Recreate no longer exists")],
  1, T("Remplace toute la stratégie : un patch JSON `replace /spec/strategy`.", "Replace the whole strategy: a JSON `replace /spec/strategy` patch."),
  "kubectl patch deploy web --type=json -p '[{\"op\":\"replace\",\"path\":\"/spec/strategy\",\"value\":{\"type\":\"Recreate\"}}]'",
  "kubectl -n quiz patch deploy web --type=json -p '[{\"op\":\"replace\",\"path\":\"/spec/strategy\",\"value\":{\"type\":\"Recreate\"}}]' --dry-run=server")

Q("d2-scale", "2", T("Passer le Deployment `web` à 5 réplicas :", "Scale Deployment `web` to 5 replicas:"),
  ["kubectl scale deploy web --replicas=5", "kubectl set replicas deploy/web 5", "kubectl autoscale deploy web --replicas=5", "kubectl rollout scale deploy/web 5"],
  0, T("`scale` modifie `spec.replicas` ; `autoscale` crée un HPA.", "`scale` changes `spec.replicas`; `autoscale` creates an HPA."),
  "kubectl scale deploy web --replicas=5", "kubectl -n quiz scale deploy web --replicas=3")

Q("d2-hpa", "2", T("Créer un HPA de 2 à 6 réplicas à 70 % de CPU :", "Create an HPA from 2 to 6 replicas at 70% CPU:"),
  ["kubectl autoscale deploy web --min=2 --max=6 --cpu-percent=70", "kubectl scale deploy web --min=2 --max=6",
   "kubectl create hpa web --cpu=70", "kubectl set autoscale deploy/web 2-6 70%"],
  0, T("Le pourcentage s'applique aux **requests** CPU des conteneurs : sans requests, l'HPA ne calcule rien.",
       "The percentage applies to container CPU **requests**: without requests, the HPA computes nothing."),
  "kubectl autoscale deploy web --min=2 --max=6 --cpu-percent=70 && kubectl get hpa web",
  "kubectl -n quiz autoscale deploy web --min=2 --max=6 --cpu-percent=70 --dry-run=server")

Q("d2-bluegreen", "2", T("Blue/green : comment basculer le trafic de `version=blue` vers `version=green` ?",
                         "Blue/green: how do you switch traffic from `version=blue` to `version=green`?"),
  [T("Supprimer le Deployment blue", "Delete the blue Deployment"),
   T("Changer le sélecteur du Service vers `version=green`", "Change the Service selector to `version=green`"),
   T("Faire un rollout undo", "Run a rollout undo"),
   T("Changer l'image du Deployment blue", "Change the blue Deployment's image")],
  1, T("Le Service choisit ses Pods par sélecteur : la bascule est instantanée et réversible.",
       "The Service picks Pods by selector: the switch is instant and reversible."),
  "kubectl patch svc web -p '{\"spec\":{\"selector\":{\"app\":\"web\",\"version\":\"green\"}}}'",
  "kubectl -n quiz patch svc web -p '{\"spec\":{\"selector\":{\"app\":\"web\"}}}'")

Q("d2-canary", "2", T("Canary à environ 20 % sans changer le Service (sélecteur `app=api`) :", "A ~20% canary without changing the Service (selector `app=api`):"),
  [T("4 Pods stables + 1 Pod canary, tous `app=api`", "4 stable Pods + 1 canary Pod, all `app=api`"),
   T("Une annotation `canary-weight: 20`", "A `canary-weight: 20` annotation"),
   T("`maxSurge: 20%`", "`maxSurge: 20%`"),
   T("Un second Service à 20 %", "A second Service at 20%")],
  0, T("Sans maillage de services, la proportion vient du nombre de Pods derrière le même sélecteur.",
       "Without a service mesh, the share comes from the Pod count behind the same selector."),
  "kubectl scale deploy api-stable --replicas=4 && kubectl scale deploy api-canary --replicas=1")

Q("d2-helm-install", "2", T("Installer le chart local `./webapp` comme release `shop` dans `prod`, avec 3 réplicas :",
                            "Install local chart `./webapp` as release `shop` in `prod`, with 3 replicas:"),
  ["helm install ./webapp shop -n prod --replicas 3", "helm -n prod install shop ./webapp --set replicaCount=3",
   "helm create shop ./webapp -n prod", "kubectl apply -k ./webapp -n prod"],
  1, T("Ordre : `helm install <release> <chart>` ; les valeurs par `--set` ou `-f`.", "Order: `helm install <release> <chart>`; values via `--set` or `-f`."),
  "helm -n prod install shop ./webapp --set replicaCount=3",
  "helm -n quiz install shop $ROOT/app/charts/webapp --set replicaCount=1 --dry-run=server >/dev/null")

Q("d2-helm-values", "2", T("Voir les valeurs **par défaut** d'un chart :", "Show a chart's **default** values:"),
  ["helm get values ./webapp", "helm show values ./webapp", "helm values ./webapp", "helm inspect release webapp"],
  1, T("`show values` lit le chart ; `get values <release>` lit ce qui a été appliqué à une release.",
       "`show values` reads the chart; `get values <release>` reads what was applied to a release."),
  "helm show values ./webapp > values.yaml", "helm show values $ROOT/app/charts/webapp | grep replicaCount")

Q("d2-helm-rollback", "2", T("Revenir à la révision 1 de la release `shop` :", "Roll release `shop` back to revision 1:"),
  ["helm undo shop 1", "helm rollback shop 1", "helm upgrade shop --revision 1", "kubectl rollout undo release/shop"],
  1, T("`helm history shop` liste les révisions ; `helm rollback shop N` y revient (nouvelle révision).",
       "`helm history shop` lists revisions; `helm rollback shop N` returns to one (as a new revision)."),
  "helm -n prod history shop && helm -n prod rollback shop 1")

Q("d2-helm-list", "2", T("Lister les releases Helm de **tous** les namespaces :", "List Helm releases in **all** namespaces:"),
  ["helm list --all", "helm list -A", "helm ls --namespaces", "kubectl get releases -A"],
  1, T("`-A` (`--all-namespaces`) ; `--all` affiche aussi les releases en échec ou désinstallées.",
       "`-A` (`--all-namespaces`); `--all` also shows failed or uninstalled releases."),
  "helm list -A", "helm list -A >/dev/null")

Q("d2-kustomize-apply", "2", T("Appliquer l'overlay Kustomize du dossier `overlays/prod` :", "Apply the Kustomize overlay in `overlays/prod`:"),
  ["kubectl apply -f overlays/prod", "kubectl apply -k overlays/prod", "kustomize apply overlays/prod", "kubectl kustomize --apply overlays/prod"],
  1, T("`-k` passe par Kustomize ; `kubectl kustomize <dir>` affiche seulement le résultat.", "`-k` goes through Kustomize; `kubectl kustomize <dir>` only prints the result."),
  "kubectl kustomize overlays/prod && kubectl apply -k overlays/prod",
  "mkdir -p /tmp/qk && kubectl create configmap k --from-literal=a=b --dry-run=client -o yaml > /tmp/qk/cm.yaml && printf 'resources: [cm.yaml]\\nnamespace: quiz\\nnamePrefix: p-\\n' > /tmp/qk/kustomization.yaml && kubectl apply -k /tmp/qk --dry-run=server")

Q("d2-kustomize-image", "2", T("Dans un `kustomization.yaml`, changer le tag de l'image `nginx` en `1.28-alpine` :",
                               "In a `kustomization.yaml`, change image `nginx`'s tag to `1.28-alpine`:"),
  ["images: [{name: nginx, newTag: 1.28-alpine}]", "patches: [{image: nginx:1.28-alpine}]", "imageTag: 1.28-alpine", "replacements: [{nginx: 1.28-alpine}]"],
  0, T("Le champ `images` remplace nom, tag ou digest sans toucher aux manifestes.", "The `images` field rewrites name, tag or digest without touching manifests."),
  "kubectl kustomize overlays/prod | grep image:")

# ===================================================================================== 3 · Observability
Q("d3-readiness", "3", T("Quelle sonde retire un Pod des Endpoints du Service **sans** le redémarrer ?",
                         "Which probe removes a Pod from the Service Endpoints **without** restarting it?"),
  ["livenessProbe", "readinessProbe", "startupProbe", "healthProbe"],
  1, T("readiness = prêt à recevoir du trafic ; liveness = vivant (sinon redémarrage).", "readiness = ready for traffic; liveness = alive (else restart)."),
  "kubectl explain pod.spec.containers.readinessProbe")

Q("d3-startup", "3", T("Une application démarre en 90 s. Comment éviter que la liveness la tue au démarrage ?",
                       "An app takes 90 s to start. How do you keep liveness from killing it at startup?"),
  [T("Une `startupProbe` (failureThreshold × periodSeconds ≥ 90 s)", "A `startupProbe` (failureThreshold × periodSeconds ≥ 90 s)"),
   T("Supprimer la liveness", "Remove the liveness probe"),
   T("`restartPolicy: Never`", "`restartPolicy: Never`"),
   T("Une readiness plus longue", "A longer readiness probe")],
  0, T("Tant que la startupProbe n'a pas réussi, liveness et readiness sont suspendues.", "Until the startupProbe succeeds, liveness and readiness are paused."),
  "startupProbe: {httpGet: {path: /, port: 8080}, failureThreshold: 30, periodSeconds: 3}")

Q("d3-probe-exec", "3", T("Une sonde qui réussit si le fichier `/tmp/healthy` existe :", "A probe that succeeds if `/tmp/healthy` exists:"),
  ["exec: {command: [cat, /tmp/healthy]}", "file: {path: /tmp/healthy}", "httpGet: {path: /tmp/healthy}", "tcpSocket: {path: /tmp/healthy}"],
  0, T("`exec` réussit si la commande sort avec le code 0.", "`exec` succeeds when the command exits with code 0."),
  "livenessProbe: {exec: {command: [cat, /tmp/healthy]}, periodSeconds: 5}",
  "printf 'apiVersion: v1\\nkind: Pod\\nmetadata: {name: pr}\\nspec:\\n  containers: [{name: a, image: busybox:1.37, command: [sleep, \"60\"], livenessProbe: {exec: {command: [cat, /tmp/healthy]}}}]\\n' | kubectl -n quiz apply --dry-run=server -f -")

Q("d3-previous", "3", T("Un conteneur redémarre en boucle. Voir les logs de l'instance **précédente** :", "A container keeps restarting. Show the **previous** instance's logs:"),
  ["kubectl logs web --last", "kubectl logs web --previous", "kubectl logs web --since=crash", "kubectl describe web --logs"],
  1, T("`--previous` (`-p`) lit le conteneur mort avant le redémarrage.", "`--previous` (`-p`) reads the container that died before the restart."),
  "kubectl logs web --previous --tail=20")

Q("d3-crashloop", "3", T("STATUS `CrashLoopBackOff` signifie :", "STATUS `CrashLoopBackOff` means:"),
  [T("L'image est introuvable", "The image cannot be found"),
   T("Le conteneur démarre puis s'arrête, et le kubelet espace les relances", "The container starts then exits, and the kubelet backs off restarts"),
   T("Le Pod n'a pas de nœud", "The Pod has no node"),
   T("Une ConfigMap manque", "A ConfigMap is missing")],
  1, T("Diagnostic : `describe` (Last State, Exit Code) et `logs --previous`.", "Diagnosis: `describe` (Last State, Exit Code) and `logs --previous`."),
  "kubectl describe pod web | grep -A4 'Last State' && kubectl logs web --previous")

Q("d3-exit127", "3", T("Le code de sortie d'un conteneur est 127. Cause la plus probable ?", "A container's exit code is 127. Most likely cause?"),
  [T("Mémoire dépassée", "Out of memory"), T("Commande introuvable", "Command not found"),
   T("Sonde en échec", "Probe failure"), T("Arrêt normal", "Normal stop")],
  1, T("127 = commande introuvable (faute de frappe) ; 137 = tué (SIGKILL, souvent OOM) ; 0 = succès.",
       "127 = command not found (typo); 137 = killed (SIGKILL, often OOM); 0 = success."),
  "kubectl get pod web -o jsonpath='{.status.containerStatuses[0].lastState.terminated.exitCode}'")

Q("d3-oom", "3", T("`OOMKilled`, code 137. La bonne correction :", "`OOMKilled`, exit code 137. The right fix:"),
  [T("Augmenter `limits.memory` (ou réduire la consommation)", "Raise `limits.memory` (or reduce consumption)"),
   T("Augmenter `requests.cpu`", "Raise `requests.cpu`"),
   T("Ajouter une liveness", "Add a liveness probe"),
   T("Passer en `restartPolicy: Never`", "Switch to `restartPolicy: Never`")],
  0, T("Le conteneur a dépassé sa limite mémoire ; le CPU, lui, est seulement bridé.", "The container exceeded its memory limit; CPU is only throttled."),
  "kubectl set resources deploy web --limits=memory=256Mi")

Q("d3-pending", "3", T("Un Pod reste `Pending`. Où trouver la cause en premier ?", "A Pod stays `Pending`. Where do you find the cause first?"),
  ["kubectl logs pod", T("Les événements : `kubectl describe pod`", "The events: `kubectl describe pod`"), "kubectl top pod", "kubectl exec pod -- dmesg"],
  1, T("Le conteneur n'a pas démarré : pas de logs. Le scheduler explique dans `FailedScheduling`.",
       "The container never started: no logs. The scheduler explains in `FailedScheduling`."),
  "kubectl describe pod web | tail -8",
  "kubectl -n quiz describe pod tool | grep -q Events")

Q("d3-events", "3", T("Lister les événements du namespace, les plus récents à la fin :", "List the namespace events, newest last:"),
  ["kubectl get events --sort-by=.lastTimestamp", "kubectl events --reverse", "kubectl describe events --latest", "kubectl logs events"],
  0, T("`--sort-by=.lastTimestamp` ; `--field-selector involvedObject.name=<x>` filtre un objet.",
       "`--sort-by=.lastTimestamp`; `--field-selector involvedObject.name=<x>` filters one object."),
  "kubectl get events --sort-by=.lastTimestamp | tail", "kubectl -n quiz get events --sort-by=.lastTimestamp >/dev/null")

Q("d3-imagepull", "3", T("`ErrImagePull` puis `ImagePullBackOff`. Correction la plus fréquente :", "`ErrImagePull` then `ImagePullBackOff`. Most common fix:"),
  [T("Corriger le nom ou le tag de l'image", "Fix the image name or tag"), T("Augmenter la mémoire", "Raise memory"),
   T("Ajouter une readiness", "Add a readiness probe"), T("Recréer le namespace", "Recreate the namespace")],
  0, T("Image ou tag inexistant, registre privé sans `imagePullSecrets` : lis l'événement `Failed to pull image`.",
       "Missing image or tag, private registry without `imagePullSecrets`: read the `Failed to pull image` event."),
  "kubectl set image deploy/web web=nginx:1.27-alpine")

Q("d3-configerr", "3", T("`CreateContainerConfigError` indique le plus souvent :", "`CreateContainerConfigError` most often means:"),
  [T("Une ConfigMap, un Secret ou une clé référencés n'existent pas", "A referenced ConfigMap, Secret or key does not exist"),
   T("Le nœud est plein", "The node is full"), T("L'image est trop grosse", "The image is too large"),
   T("Le Service n'a pas d'Endpoints", "The Service has no Endpoints")],
  0, T("Le kubelet ne peut pas construire l'environnement du conteneur : vois `describe`.", "The kubelet cannot build the container's environment: see `describe`."),
  "kubectl describe pod web | grep -i 'couldn\\|not found'")

Q("d3-top", "3", T("Trouver le Pod qui consomme le plus de CPU dans `prod` :", "Find the Pod using the most CPU in `prod`:"),
  ["kubectl top pods -n prod --sort-by=cpu", "kubectl get pods -n prod --sort-by=cpu", "kubectl describe nodes --top", "kubectl metrics pods -n prod"],
  0, T("`top` lit metrics-server ; `get --sort-by` ne connaît pas la consommation.", "`top` reads metrics-server; `get --sort-by` knows nothing about usage."),
  "kubectl top pods -n prod --sort-by=cpu | head -2")

Q("d3-debug", "3", T("Le Pod `api` utilise une image sans shell. Comment l'inspecter de l'intérieur ?",
                     "Pod `api` uses an image without a shell. How do you inspect it from inside?"),
  ["kubectl exec -it api -- sh", "kubectl debug -it api --image=busybox:1.37 --target=api", "kubectl attach api --shell", "kubectl cp busybox api:/bin/sh"],
  1, T("`debug` ajoute un conteneur éphémère ; `--target` partage les processus du conteneur visé.",
       "`debug` adds an ephemeral container; `--target` shares the target container's processes."),
  "kubectl debug -it api --image=busybox:1.37 --target=api -- sh")

Q("d3-portforward", "3", T("Tester le Service `web` (port 80) depuis ton poste, sans l'exposer :", "Test Service `web` (port 80) from your machine without exposing it:"),
  ["kubectl expose svc web --local", "kubectl port-forward svc/web 8080:80", "kubectl proxy svc/web 8080", "kubectl tunnel web 80"],
  1, T("`port-forward` ouvre `localhost:8080` vers le port 80 du Service.", "`port-forward` opens `localhost:8080` to the Service's port 80."),
  "kubectl port-forward svc/web 8080:80 & curl -s localhost:8080")

Q("d3-deprecated", "3", T("`no matches for kind \"CronJob\" in version \"batch/v1beta1\"`. La correction :", "`no matches for kind \"CronJob\" in version \"batch/v1beta1\"`. The fix:"),
  ["apiVersion: batch/v1", "apiVersion: batch/v2", "apiVersion: apps/v1", "kubectl convert -f cron.yaml"],
  0, T("CronJob est en `batch/v1` depuis 1.21 (v1beta1 retiré en 1.25) ; `kubectl convert` n'est pas installé à l'examen.",
       "CronJob is `batch/v1` since 1.21 (v1beta1 removed in 1.25); `kubectl convert` is not installed in the exam."),
  "kubectl api-resources | grep cronjobs", "kubectl api-resources | grep -q 'batch/v1 .*CronJob'")

Q("d3-ingress-v1", "3", T("En convertissant un Ingress `v1beta1` vers `networking.k8s.io/v1`, quel champ devient obligatoire ?",
                          "Converting a `v1beta1` Ingress to `networking.k8s.io/v1`, which field becomes mandatory?"),
  ["pathType", "ingressClass", "servicePort", "hostNetwork"],
  0, T("En v1, chaque chemin a un `pathType`, et le backend devient `service: {name, port: {number}}`.",
       "In v1, every path has a `pathType`, and the backend becomes `service: {name, port: {number}}`."),
  "kubectl explain ingress.spec.rules.http.paths.pathType")

# ===================================================================================== 4 · Config & Security
Q("d4-cm-literal", "4", T("Créer la ConfigMap `app` avec `MODE=prod` :", "Create ConfigMap `app` with `MODE=prod`:"),
  ["kubectl create configmap app --from-literal=MODE=prod", "kubectl create cm app MODE=prod",
   "kubectl create configmap app --data MODE=prod", "kubectl create configmap app --from-env=MODE=prod"],
  0, T("Sources possibles : `--from-literal`, `--from-file`, `--from-env-file`.", "Possible sources: `--from-literal`, `--from-file`, `--from-env-file`."),
  "kubectl create configmap app --from-literal=MODE=prod", "kubectl -n quiz create configmap app --from-literal=MODE=prod --dry-run=server")

Q("d4-cm-file", "4", T("`--from-file=nginx.conf` crée quelle clé ?", "`--from-file=nginx.conf` creates which key?"),
  [T("`nginx.conf`, avec le contenu du fichier", "`nginx.conf`, with the file content"), T("`file`", "`file`"),
   T("Une clé par ligne", "One key per line"), T("`data`", "`data`")],
  0, T("La clé est le nom du fichier ; `--from-file=autre=nginx.conf` la renomme.", "The key is the file name; `--from-file=other=nginx.conf` renames it."),
  "kubectl create configmap ng --from-file=nginx.conf",
  "printf 'x\\n' > /tmp/nginx.conf && kubectl -n quiz create configmap ng --from-file=/tmp/nginx.conf --dry-run=client -o yaml | grep -q 'nginx.conf:'")

Q("d4-envfrom", "4", T("Injecter **toutes** les clés de la ConfigMap `app` comme variables :", "Inject **all** keys of ConfigMap `app` as env vars:"),
  ["envFrom: [{configMapRef: {name: app}}]", "env: [{name: app, valueFrom: configMap}]", "volumes: [{configMap: {name: app}}]", "configMap: {name: app, all: true}"],
  0, T("`envFrom` importe tout ; `env[].valueFrom.configMapKeyRef` une seule clé.", "`envFrom` imports everything; `env[].valueFrom.configMapKeyRef` a single key."),
  "kubectl set env deploy/web --from=configmap/app",
  "kubectl -n quiz get configmap app >/dev/null 2>&1 || kubectl -n quiz create configmap app --from-literal=MODE=prod; kubectl -n quiz set env deploy/web --from=configmap/app --dry-run=server")

Q("d4-secret-decode", "4", T("Lire en clair la clé `password` du Secret `db` :", "Read the `password` key of Secret `db` in plain text:"),
  ["kubectl get secret db -o jsonpath='{.data.password}' | base64 -d", "kubectl decrypt secret db password",
   "kubectl get secret db --show-values", "kubectl describe secret db"],
  0, T("`data` est encodé en base64 (pas chiffré) ; `describe` n'affiche que les tailles.", "`data` is base64-encoded (not encrypted); `describe` only shows sizes."),
  "kubectl get secret db -o jsonpath='{.data.password}' | base64 -d",
  "kubectl -n quiz get secret db -o jsonpath='{.data.password}' | base64 -d | grep -q S3cr3t")

Q("d4-secret-env", "4", T("Une variable `DB_PASSWORD` qui lit la clé `password` du Secret `db` :", "An env var `DB_PASSWORD` reading key `password` of Secret `db`:"),
  ["valueFrom: {secretKeyRef: {name: db, key: password}}", "valueFrom: {configMapKeyRef: {name: db, key: password}}",
   "value: secret://db/password", "envFrom: [{secretRef: {name: db, key: password}}]"],
  0, T("`secretKeyRef` pour une clé ; `envFrom.secretRef` pour tout le Secret.", "`secretKeyRef` for one key; `envFrom.secretRef` for the whole Secret."),
  "env: [{name: DB_PASSWORD, valueFrom: {secretKeyRef: {name: db, key: password}}}]")

Q("d4-secret-tls", "4", T("Créer un Secret TLS pour un Ingress :", "Create a TLS Secret for an Ingress:"),
  ["kubectl create secret tls shop-tls --cert=tls.crt --key=tls.key", "kubectl create secret generic shop-tls --tls",
   "kubectl create certificate shop-tls", "kubectl create secret ssl shop-tls --cert=tls.crt"],
  0, T("Type `kubernetes.io/tls`, clés `tls.crt` et `tls.key` ; l'Ingress le référence dans `spec.tls[].secretName`.",
       "Type `kubernetes.io/tls`, keys `tls.crt` and `tls.key`; the Ingress references it in `spec.tls[].secretName`."),
  "kubectl create secret tls shop-tls --cert=tls.crt --key=tls.key")

Q("d4-registry", "4", T("Une image vient d'un registre privé. Que faut-il au Pod ?", "An image comes from a private registry. What does the Pod need?"),
  [T("Un Secret `docker-registry` référencé dans `imagePullSecrets`", "A `docker-registry` Secret referenced in `imagePullSecrets`"),
   T("Un ServiceAccount admin", "An admin ServiceAccount"), T("`imagePullPolicy: Never`", "`imagePullPolicy: Never`"),
   T("Une NetworkPolicy egress", "An egress NetworkPolicy")],
  0, T("Le kubelet s'authentifie au registre avec ce Secret.", "The kubelet authenticates to the registry with that Secret."),
  "kubectl create secret docker-registry regcred --docker-server=reg.example.com --docker-username=u --docker-password=p",
  "kubectl -n quiz create secret docker-registry regcred --docker-server=reg.example.com --docker-username=u --docker-password=p --dry-run=server")

Q("d4-sa", "4", T("Faire tourner le Deployment `web` sous le ServiceAccount `deployer` :", "Run Deployment `web` under ServiceAccount `deployer`:"),
  ["kubectl set serviceaccount deploy/web deployer", "kubectl patch sa deployer --deployment web", "kubectl create rolebinding web --sa=deployer", "kubectl annotate deploy web sa=deployer"],
  0, T("Modifie `spec.template.spec.serviceAccountName` et relance les Pods.", "Changes `spec.template.spec.serviceAccountName` and rolls the Pods."),
  "kubectl create sa deployer && kubectl set serviceaccount deploy/web deployer",
  "kubectl -n quiz get sa deployer >/dev/null 2>&1 || kubectl -n quiz create sa deployer; kubectl -n quiz set serviceaccount deploy/web deployer --dry-run=server")

Q("d4-automount", "4", T("Empêcher le montage du jeton de ServiceAccount dans un Pod :", "Prevent the ServiceAccount token from being mounted in a Pod:"),
  ["automountServiceAccountToken: false", "serviceAccountName: none", "tokenMount: disabled", "securityContext.noToken: true"],
  0, T("Se règle sur le Pod (prioritaire) ou sur le ServiceAccount.", "Set on the Pod (takes precedence) or on the ServiceAccount."),
  "kubectl patch sa deployer -p '{\"automountServiceAccountToken\": false}'")

Q("d4-token", "4", T("Obtenir un jeton temporaire pour le ServiceAccount `deployer` :", "Get a short-lived token for ServiceAccount `deployer`:"),
  ["kubectl create token deployer", "kubectl get secret deployer-token", "kubectl sa token deployer", "kubectl auth token deployer"],
  0, T("Depuis 1.24, les jetons ne sont plus des Secrets automatiques : `create token` en émet un.",
       "Since 1.24, tokens are no longer automatic Secrets: `create token` issues one."),
  "kubectl create token deployer --duration=1h",
  "kubectl -n quiz get sa deployer >/dev/null 2>&1 || kubectl -n quiz create sa deployer; kubectl -n quiz create token deployer --duration=10m >/dev/null")

Q("d4-role", "4", T("Une Role qui permet de lire les Pods et leurs logs :", "A Role allowing to read Pods and their logs:"),
  ["kubectl create role r --verb=get,list,watch --resource=pods,pods/log", "kubectl create role r --verb=read --resource=pods",
   "kubectl create clusterrolebinding r --resource=pods", "kubectl create role r --verb=* --resource=pods"],
  0, T("Les logs sont la sous-ressource `pods/log` ; moindre privilège : pas de `*`.", "Logs are the `pods/log` subresource; least privilege: no `*`."),
  "kubectl create role r --verb=get,list,watch --resource=pods,pods/log",
  "kubectl -n quiz create role r --verb=get,list,watch --resource=pods,pods/log --dry-run=server")

Q("d4-rolebinding", "4", T("Lier la Role `r` au ServiceAccount `bot` du namespace `quiz` :", "Bind Role `r` to ServiceAccount `bot` in namespace `quiz`:"),
  ["kubectl create rolebinding rb --role=r --serviceaccount=quiz:bot", "kubectl create rolebinding rb --role=r --user=bot",
   "kubectl create rolebinding rb --role=r --serviceaccount=bot", "kubectl bind role r bot"],
  0, T("Format `<namespace>:<nom>` pour `--serviceaccount`.", "Format `<namespace>:<name>` for `--serviceaccount`."),
  "kubectl -n quiz create rolebinding rb --role=r --serviceaccount=quiz:bot",
  "kubectl -n quiz create rolebinding rb --role=r --serviceaccount=quiz:bot --dry-run=server")

Q("d4-cani", "4", T("Vérifier si le ServiceAccount `bot` (namespace `quiz`) peut supprimer des Pods :", "Check whether ServiceAccount `bot` (namespace `quiz`) can delete Pods:"),
  ["kubectl auth can-i delete pods -n quiz --as=system:serviceaccount:quiz:bot", "kubectl auth can-i delete pods --sa bot",
   "kubectl get rolebinding bot --can delete", "kubectl auth check bot delete pods"],
  0, T("`--as` prend l'identité complète `system:serviceaccount:<ns>:<nom>` ; réponse `yes`/`no`.",
       "`--as` takes the full identity `system:serviceaccount:<ns>:<name>`; answer `yes`/`no`."),
  "kubectl auth can-i --list -n quiz --as=system:serviceaccount:quiz:bot",
  "kubectl auth can-i delete pods -n quiz --as=system:serviceaccount:quiz:bot | grep -q no")

Q("d4-clusterrole-ns", "4", T("Donner les droits de la ClusterRole `view` dans **un seul** namespace :", "Grant ClusterRole `view` in **a single** namespace:"),
  [T("Un RoleBinding qui référence la ClusterRole", "A RoleBinding referencing the ClusterRole"),
   T("Un ClusterRoleBinding", "A ClusterRoleBinding"), T("Copier la ClusterRole en Role", "Copy the ClusterRole into a Role"),
   T("Impossible", "Impossible")],
  0, T("Un RoleBinding limite au namespace les droits d'une ClusterRole.", "A RoleBinding scopes a ClusterRole's rights to its namespace."),
  "kubectl -n quiz create rolebinding view --clusterrole=view --serviceaccount=quiz:bot",
  "kubectl -n quiz create rolebinding view --clusterrole=view --serviceaccount=quiz:bot --dry-run=server")

Q("d4-qos", "4", T("requests = limits pour CPU et mémoire dans tous les conteneurs. Classe QoS ?", "requests = limits for CPU and memory in every container. QoS class?"),
  ["Guaranteed", "Burstable", "BestEffort", "Critical"],
  0, T("Burstable si requests < limits ou partielles ; BestEffort si rien.", "Burstable if requests < limits or partial; BestEffort if none."),
  "kubectl get pod web -o jsonpath='{.status.qosClass}'")

Q("d4-resources", "4", T("Fixer requests et limits sur le Deployment `web` :", "Set requests and limits on Deployment `web`:"),
  ["kubectl set resources deploy web --requests=cpu=100m,memory=64Mi --limits=cpu=200m,memory=128Mi",
   "kubectl scale deploy web --cpu=100m --memory=64Mi", "kubectl limit deploy web cpu=200m", "kubectl set limits deploy/web 200m"],
  0, T("`set resources` modifie le template, ce qui relance les Pods.", "`set resources` edits the template, which rolls the Pods."),
  "kubectl set resources deploy web --requests=cpu=100m,memory=64Mi --limits=cpu=200m,memory=128Mi",
  "kubectl -n quiz set resources deploy web --requests=cpu=20m,memory=16Mi --limits=cpu=100m,memory=64Mi --dry-run=server")

Q("d4-quota", "4", T("Une ResourceQuota sur `requests.cpu` existe. Un Pod sans requests est :", "A ResourceQuota on `requests.cpu` exists. A Pod without requests is:"),
  [T("Refusé, sauf si une LimitRange injecte des valeurs par défaut", "Rejected, unless a LimitRange injects defaults"),
   T("Accepté en BestEffort", "Accepted as BestEffort"), T("Mis en Pending", "Set to Pending"), T("Accepté avec 0", "Accepted with 0")],
  0, T("L'admission exige alors des requests ; une LimitRange (`defaultRequest`) les fournit.", "Admission then requires requests; a LimitRange (`defaultRequest`) provides them."),
  "kubectl create quota q --hard=requests.cpu=1,pods=5")

Q("d4-limitrange", "4", T("Quel objet donne des requests et limits **par défaut** aux conteneurs d'un namespace ?", "Which object gives **default** requests and limits to a namespace's containers?"),
  ["LimitRange", "ResourceQuota", "PriorityClass", "PodDisruptionBudget"],
  0, T("LimitRange : `defaultRequest`, `default`, `min`, `max` par conteneur ; ResourceQuota : totaux du namespace.",
       "LimitRange: per-container `defaultRequest`, `default`, `min`, `max`; ResourceQuota: namespace totals."),
  "kubectl describe limitrange -n quiz")

Q("d4-runasuser", "4", T("Exécuter **tous** les conteneurs d'un Pod en utilisateur 1000 :", "Run **all** containers of a Pod as user 1000:"),
  ["spec.securityContext.runAsUser: 1000", "spec.containers[].user: 1000", "metadata.uid: 1000", "spec.serviceAccountName: 1000"],
  0, T("Le securityContext du Pod s'applique à tous les conteneurs (le niveau conteneur l'emporte).",
       "The Pod securityContext applies to all containers (container level wins)."),
  "kubectl exec web -- id -u")

Q("d4-capabilities", "4", T("Où déclare-t-on `capabilities: {drop: [ALL]}` ?", "Where do you declare `capabilities: {drop: [ALL]}`?"),
  [T("Au niveau conteneur uniquement", "At container level only"), T("Au niveau Pod uniquement", "At Pod level only"),
   T("Aux deux niveaux", "At both levels"), T("Dans le ServiceAccount", "In the ServiceAccount")],
  0, T("`capabilities`, `readOnlyRootFilesystem`, `allowPrivilegeEscalation` et `privileged` n'existent que par conteneur.",
       "`capabilities`, `readOnlyRootFilesystem`, `allowPrivilegeEscalation` and `privileged` exist only per container."),
  "kubectl explain pod.spec.containers.securityContext.capabilities")

Q("d4-readonly", "4", T("Rendre le système de fichiers racine d'un conteneur non modifiable :", "Make a container's root filesystem read-only:"),
  ["securityContext: {readOnlyRootFilesystem: true}", "volumeMounts: [{mountPath: /, readOnly: true}]", "securityContext: {fsGroup: 0}", "spec.readOnly: true"],
  0, T("Écris dans des volumes (`emptyDir`) si l'application a besoin de fichiers temporaires.", "Write to volumes (`emptyDir`) if the app needs temporary files."),
  "kubectl exec web -- touch /test   # Read-only file system")

Q("d4-psa", "4", T("Imposer le profil `restricted` des Pod Security Standards au namespace `prod` :", "Enforce the `restricted` Pod Security Standard on namespace `prod`:"),
  ["kubectl label ns prod pod-security.kubernetes.io/enforce=restricted", "kubectl annotate ns prod podsecurity=restricted",
   "kubectl create podsecuritypolicy restricted -n prod", "kubectl patch ns prod --security=restricted"],
  0, T("Pod Security Admission se pilote par labels de namespace (`enforce`, `warn`, `audit`) ; les PSP n'existent plus.",
       "Pod Security Admission is driven by namespace labels (`enforce`, `warn`, `audit`); PSPs no longer exist."),
  "kubectl label ns prod pod-security.kubernetes.io/enforce=restricted",
  "kubectl label ns quiz pod-security.kubernetes.io/warn=baseline --overwrite && kubectl label ns quiz pod-security.kubernetes.io/warn-")

Q("d4-crd", "4", T("Trouver le `kind` et la version d'une ressource personnalisée du groupe `ops.example.com` :", "Find the `kind` and version of a custom resource in group `ops.example.com`:"),
  ["kubectl api-resources --api-group=ops.example.com", "kubectl get crd ops.example.com -o kind", "kubectl describe operator ops", "kubectl explain ops.example.com"],
  0, T("`api-resources` donne APIVERSION et KIND ; `explain <kind>.spec` donne les champs.", "`api-resources` gives APIVERSION and KIND; `explain <kind>.spec` gives the fields."),
  "kubectl get crd && kubectl api-resources --api-group=ops.example.com", "kubectl get crd >/dev/null")

Q("d4-admission", "4", T("Une requête autorisée par RBAC est quand même refusée par un quota. Quelle étape l'a refusée ?",
                         "A request allowed by RBAC is still rejected by a quota. Which stage rejected it?"),
  [T("L'authentification", "Authentication"), T("L'autorisation", "Authorization"), T("Le contrôle d'admission", "Admission control"), T("Le scheduler", "The scheduler")],
  2, T("Ordre : authentification → autorisation (RBAC) → admission (quotas, LimitRange, Pod Security…).",
       "Order: authentication → authorization (RBAC) → admission (quotas, LimitRange, Pod Security…)."),
  "kubectl describe quota -n quiz")

# ===================================================================================== 5 · Services & Networking
Q("d5-expose", "5", T("Exposer le Deployment `api` (conteneur sur 5678) sur le port 80 du Service :", "Expose Deployment `api` (container on 5678) on Service port 80:"),
  ["kubectl expose deploy api --port=80 --target-port=5678", "kubectl expose deploy api --port=5678 --target-port=80",
   "kubectl create service api --port=80:5678", "kubectl expose deploy api --node-port=80"],
  0, T("`port` = port du Service, `targetPort` = port du conteneur.", "`port` = Service port, `targetPort` = container port."),
  "kubectl expose deploy api --port=80 --target-port=5678",
  "kubectl -n quiz expose deploy web --name=web2 --port=80 --target-port=80 --dry-run=server")

Q("d5-noendpoints", "5", T("Un Service n'a aucun Endpoint alors que les Pods tournent. Cause la plus probable ?", "A Service has no Endpoints while Pods run. Most likely cause?"),
  [T("Le sélecteur ne correspond pas aux labels des Pods", "The selector does not match the Pod labels"),
   T("Le targetPort est faux", "The targetPort is wrong"), T("Le DNS est en panne", "DNS is broken"), T("Le type est ClusterIP", "The type is ClusterIP")],
  0, T("Un mauvais targetPort donne des Endpoints mais `Connection refused` ; aucun Endpoint = sélecteur ou readiness.",
       "A wrong targetPort gives Endpoints but `Connection refused`; no Endpoints = selector or readiness."),
  "kubectl get endpointslices -l kubernetes.io/service-name=web && kubectl get pods --show-labels",
  "kubectl -n quiz get endpointslices -l kubernetes.io/service-name=web | grep -q web")

Q("d5-refused", "5", T("Les Endpoints existent mais l'appel répond `Connection refused`. Que vérifier ?", "Endpoints exist but calls get `Connection refused`. What do you check?"),
  [T("Le `targetPort` contre le port réel du conteneur", "The `targetPort` against the container's real port"),
   T("Le sélecteur", "The selector"), T("Le namespace du client", "The client's namespace"), T("Le quota", "The quota")],
  0, T("Rien n'écoute sur le port ciblé : aligne `targetPort` sur `containerPort`.", "Nothing listens on the target port: align `targetPort` with `containerPort`."),
  "kubectl get svc web -o jsonpath='{.spec.ports[0].targetPort}'; kubectl get pod -l app=web -o jsonpath='{..containerPort}'")

Q("d5-nodeport", "5", T("Plage par défaut des ports `NodePort` :", "Default `NodePort` range:"),
  ["1-1024", "30000-32767", "8000-9000", "Any free port"],
  1, T("Le nodePort est ouvert sur **tous** les nœuds ; on peut le choisir dans la plage.", "The nodePort opens on **every** node; you may pick one in the range."),
  "kubectl expose deploy web --type=NodePort --port=80 --dry-run=client -o yaml | yq '.spec.ports[0].nodePort=30080'")

Q("d5-dns", "5", T("Nom DNS complet du Service `db` dans le namespace `data` :", "Fully qualified DNS name of Service `db` in namespace `data`:"),
  ["db.data.svc.cluster.local", "data.db.svc.cluster.local", "db.svc.data.cluster.local", "db.data.cluster.local"],
  0, T("Forme `<service>.<namespace>.svc.<domaine>` ; dans le même namespace, `db` suffit.", "Form `<service>.<namespace>.svc.<domain>`; within the namespace, `db` is enough."),
  "kubectl run t --rm -it --image=busybox:1.37 --restart=Never -- nslookup db.data.svc.cluster.local",
  "kubectl -n quiz run dnsq --image=busybox:1.37 --restart=Never -- nslookup web.quiz.svc.cluster.local && kubectl -n quiz wait --for=jsonpath='{.status.phase}'=Succeeded pod/dnsq --timeout=60s")

Q("d5-headless", "5", T("Un Service **headless** se déclare avec :", "A **headless** Service is declared with:"),
  ["clusterIP: None", "type: Headless", "selector: {}", "ports: []"],
  0, T("Pas d'IP virtuelle : le DNS renvoie directement les IP des Pods (StatefulSet).", "No virtual IP: DNS returns the Pod IPs directly (StatefulSet)."),
  "kubectl create service clusterip db --clusterip=None --tcp=5432:5432",
  "kubectl -n quiz create service clusterip dbh --clusterip=None --tcp=5432:5432 --dry-run=server")

Q("d5-externalname", "5", T("Un Service qui n'est qu'un alias DNS vers `api.example.com` :", "A Service that is only a DNS alias to `api.example.com`:"),
  ["kubectl create service externalname ext --external-name=api.example.com", "kubectl expose ext --dns=api.example.com",
   "kubectl create service clusterip ext --host=api.example.com", "kubectl create ingress ext --rule=api.example.com"],
  0, T("Type `ExternalName` : un enregistrement CNAME, sans sélecteur ni proxy.", "Type `ExternalName`: a CNAME record, no selector, no proxy."),
  "kubectl create service externalname ext --external-name=api.example.com",
  "kubectl -n quiz create service externalname ext --external-name=api.example.com --dry-run=server")

Q("d5-ingress-create", "5", T("Créer un Ingress `shop` (classe `traefik`) : `shop.local/` vers `front:80` :", "Create Ingress `shop` (class `traefik`): `shop.local/` to `front:80`:"),
  ["kubectl create ingress shop --class=traefik --rule='shop.local/*=front:80'", "kubectl expose ingress shop --host=shop.local --service=front",
   "kubectl create ingress shop --rule='front:80=shop.local'", "kubectl create route shop shop.local front:80"],
  0, T("`--rule='hôte/chemin=service:port'` ; l'étoile = `pathType: Prefix`.", "`--rule='host/path=service:port'`; the star = `pathType: Prefix`."),
  "kubectl create ingress shop --class=traefik --rule='shop.local/*=front:80'",
  "kubectl -n quiz create ingress shop --class=traefik --rule='shop.local/*=web:80' --dry-run=server")

Q("d5-ingress-port", "5", T("Le backend d'un Ingress vise quel port ?", "An Ingress backend targets which port?"),
  [T("Le port du **Service**", "The **Service** port"), T("Le port du conteneur", "The container port"),
   T("Le nodePort", "The nodePort"), T("Le port 80 toujours", "Always port 80")],
  0, T("`backend.service.port.number` (ou `.name`) est le port du Service.", "`backend.service.port.number` (or `.name`) is the Service port."),
  "kubectl describe ingress shop")

Q("d5-ingressclass", "5", T("Un Ingress n'a pas d'ADDRESS et rien ne répond. Premier contrôle :", "An Ingress has no ADDRESS and nothing answers. First check:"),
  ["kubectl get ingressclass", "kubectl get nodes", "kubectl top pods", "kubectl get pv"],
  0, T("Sans `ingressClassName` existant (ou classe par défaut), aucun contrôleur ne prend l'Ingress.",
       "Without an existing `ingressClassName` (or default class), no controller picks the Ingress up."),
  "kubectl get ingressclass && kubectl get ingress shop -o jsonpath='{.spec.ingressClassName}'", "kubectl get ingressclass | grep -q traefik")

Q("d5-np-default-deny", "5", T("Bloquer tout trafic **entrant** vers tous les Pods d'un namespace :", "Block all **incoming** traffic to every Pod of a namespace:"),
  ["podSelector: {} + policyTypes: [Ingress], sans règle ingress", "podSelector: {} + ingress: [{}]",
   "policyTypes: [Egress] seulement", "namespaceSelector: {} + ingress: [{}]"],
  0, T("`podSelector: {}` sélectionne tout ; `Ingress` sans règle n'autorise rien. `ingress: [{}]` autoriserait tout.",
       "`podSelector: {}` selects everything; `Ingress` with no rule allows nothing. `ingress: [{}]` would allow everything."),
  "printf 'apiVersion: networking.k8s.io/v1\\nkind: NetworkPolicy\\nmetadata: {name: deny}\\nspec: {podSelector: {}, policyTypes: [Ingress]}\\n' | kubectl apply -f -",
  "printf 'apiVersion: networking.k8s.io/v1\\nkind: NetworkPolicy\\nmetadata: {name: deny}\\nspec: {podSelector: {}, policyTypes: [Ingress]}\\n' | kubectl -n quiz apply --dry-run=server -f -")

Q("d5-np-and-or", "5", T("Dans `from`, `namespaceSelector` et `podSelector` dans le **même** élément signifient :", "In `from`, `namespaceSelector` and `podSelector` in the **same** item mean:"),
  [T("ET : ces Pods-là dans ce namespace-là", "AND: those Pods in that namespace"), T("OU", "OR"),
   T("Erreur de validation", "A validation error"), T("Seul le podSelector compte", "Only the podSelector counts")],
  0, T("Deux éléments de liste distincts = OU ; un seul élément avec les deux sélecteurs = ET.", "Two separate list items = OR; one item with both selectors = AND."),
  "kubectl describe netpol -n quiz")

Q("d5-np-ns", "5", T("Autoriser l'entrée depuis tout le namespace `traefik` :", "Allow ingress from the whole `traefik` namespace:"),
  ["from: [{namespaceSelector: {matchLabels: {kubernetes.io/metadata.name: traefik}}}]", "from: [{namespace: traefik}]",
   "from: [{podSelector: {matchLabels: {namespace: traefik}}}]", "from: [{ipBlock: {namespace: traefik}}]"],
  0, T("Chaque namespace porte automatiquement le label `kubernetes.io/metadata.name`.", "Every namespace automatically carries the `kubernetes.io/metadata.name` label."),
  "kubectl get ns traefik --show-labels", "kubectl get ns traefik --show-labels | grep -q 'kubernetes.io/metadata.name=traefik'")

Q("d5-np-dns", "5", T("Après une politique `Egress`, les noms ne se résolvent plus (`bad address`). Que manque-t-il ?", "After an `Egress` policy, names no longer resolve (`bad address`). What is missing?"),
  [T("Une règle vers le port 53 (UDP et TCP)", "A rule to port 53 (UDP and TCP)"), T("Une règle Ingress", "An Ingress rule"),
   T("Un Service headless", "A headless Service"), T("Une IngressClass", "An IngressClass")],
  0, T("Autorise le DNS : `egress: [{ports: [{protocol: UDP, port: 53}, {protocol: TCP, port: 53}]}]`.", "Allow DNS: `egress: [{ports: [{protocol: UDP, port: 53}, {protocol: TCP, port: 53}]}]`."),
  "egress: [{ports: [{protocol: UDP, port: 53}, {protocol: TCP, port: 53}]}]")

Q("d5-np-port", "5", T("Dans une NetworkPolicy, `ports[].port` désigne :", "In a NetworkPolicy, `ports[].port` refers to:"),
  [T("Le port du conteneur (Pod)", "The container (Pod) port"), T("Le port du Service", "The Service port"),
   T("Le nodePort", "The nodePort"), T("Le port de l'Ingress", "The Ingress port")],
  0, T("La politique filtre au niveau du Pod, après la traduction du Service.", "The policy filters at Pod level, after Service translation."),
  "kubectl get pod -l app=api -o jsonpath='{..containerPort}'")

# ===================================================================================== 6 · Scénarios et examen
Q("s-jour3", "6", T("Journée 3 : la v2 de l'API est en `CrashLoopBackOff`, la v1 tourne encore. Le plus sûr et rapide :",
                    "Day 3: API v2 is in `CrashLoopBackOff`, v1 still runs. The safest and fastest move:"),
  ["kubectl rollout undo deploy/api", "kubectl delete deploy api", "kubectl scale deploy api --replicas=0", "kubectl edit pod api-xxx"],
  0, T("Le rollback restaure le template v1 ; `maxUnavailable` a gardé des Pods v1, donc pas de coupure.",
       "The rollback restores the v1 template; `maxUnavailable` kept v1 Pods, so no outage."),
  "kubectl rollout history deploy/api && kubectl rollout undo deploy/api && kubectl rollout status deploy/api")

Q("s-jour4", "6", T("Journée 4 : le front ne doit pas joindre Redis, l'API oui. Où poser la NetworkPolicy ?",
                    "Day 4: the front must not reach Redis, the API must. Where does the NetworkPolicy go?"),
  [T("Sur les Pods Redis (destination), `from` = Pods API", "On the Redis Pods (destination), `from` = API Pods"),
   T("Sur les Pods front, en Ingress", "On the front Pods, as Ingress"), T("Sur le Service redis", "On the redis Service"),
   T("Sur le namespace kube-system", "On the kube-system namespace")],
  0, T("Une politique Ingress protège les Pods qu'elle sélectionne et liste les sources autorisées.",
       "An Ingress policy protects the Pods it selects and lists the allowed sources."),
  "kubectl describe netpol api-to-redis")

Q("s-pannes", "6", T("Un PVC vise la StorageClass `fast`, qui n'existe pas. Comment corriger ?", "A PVC targets StorageClass `fast`, which does not exist. How do you fix it?"),
  [T("Recréer le PVC avec une classe existante (`storageClassName` est immuable)", "Recreate the PVC with an existing class (`storageClassName` is immutable)"),
   T("`kubectl edit pvc` et changer la classe", "`kubectl edit pvc` and change the class"), T("Redémarrer le nœud", "Restart the node"),
   T("Ajouter un quota", "Add a quota")],
  0, T("Supprime le Pod et le PVC, corrige `storageClassName`, recrée-les.", "Delete the Pod and the PVC, fix `storageClassName`, recreate them."),
  "kubectl get pvc data -o yaml > pvc.yaml && kubectl delete pvc data && sed -i 's/fast/standard/' pvc.yaml && kubectl apply -f pvc.yaml")

Q("s-forbidden", "6", T("`User \"system:serviceaccount:rapports:reporter\" cannot list resource \"pods\"`. Correction minimale :",
                        "`User \"system:serviceaccount:rapports:reporter\" cannot list resource \"pods\"`. Minimal fix:"),
  [T("Role `get,list` sur pods + RoleBinding au ServiceAccount", "Role `get,list` on pods + RoleBinding to the ServiceAccount"),
   T("ClusterRoleBinding vers cluster-admin", "ClusterRoleBinding to cluster-admin"), T("Supprimer le ServiceAccount", "Delete the ServiceAccount"),
   T("Ajouter un Secret", "Add a Secret")],
  0, T("Moindre privilège : juste les verbes et ressources refusés, dans ce namespace.", "Least privilege: only the denied verbs and resources, in that namespace."),
  "kubectl -n rapports create role reporter --verb=get,list --resource=pods && kubectl -n rapports create rolebinding reporter --role=reporter --serviceaccount=rapports:reporter")

Q("e-first", "6", T("Au début de chaque tâche d'examen, que fais-tu en premier ?", "At the start of each exam task, what do you do first?"),
  [T("`ssh` vers l'hôte indiqué, puis vérifier le contexte", "`ssh` to the given host, then check the context"),
   T("Ouvrir la documentation", "Open the documentation"), T("Écrire le YAML", "Write the YAML"), T("Supprimer le namespace", "Delete the namespace")],
  0, T("Chaque tâche se fait sur un hôte désigné ; un travail sur le mauvais cluster vaut 0.", "Each task runs on a designated host; work on the wrong cluster scores 0."),
  "ssh <hôte> && kubectl config current-context")

Q("e-tools", "6", T("Lequel de ces outils **n'est pas** annoncé sur les hôtes d'examen ?", "Which of these tools is **not** announced on exam hosts?"),
  ["yq", "jq", "curl", "kubectl (alias k)"],
  1, T("Annoncés : `kubectl` + alias `k` + complétion, `yq`, `curl`, `wget`, `man`. Pour extraire du JSON : jsonpath.",
       "Announced: `kubectl` + `k` alias + completion, `yq`, `curl`, `wget`, `man`. To extract JSON: jsonpath."),
  "kubectl get pod web -o jsonpath='{.status.podIP}'")

Q("e-paste", "6", T("Coller dans le terminal d'examen :", "Paste into the exam terminal:"),
  ["Ctrl+V", "Ctrl+Shift+V", "Shift+Insert", "Alt+V"],
  1, T("Ctrl+Maj+C / Ctrl+Maj+V dans le terminal ; la touche Inser est interdite.", "Ctrl+Shift+C / Ctrl+Shift+V in the terminal; the Insert key is forbidden."),
  "vim: :set paste  →  i  →  Ctrl+Shift+V  →  Esc  →  :set nopaste")

Q("e-docs", "6", T("Quelle documentation est autorisée pendant le CKAD ?", "Which documentation is allowed during the CKAD?"),
  [T("kubernetes.io/docs, kubernetes.io/blog et helm.sh/docs", "kubernetes.io/docs, kubernetes.io/blog and helm.sh/docs"),
   T("Tout Internet", "The whole Internet"), T("Aucune", "None"), T("La doc Gateway API seulement", "Gateway API docs only")],
  0, T("La doc Gateway API est réservée au CKA ; la recherche de kubernetes.io est permise, sans ouvrir de résultat externe.",
       "Gateway API docs are CKA-only; kubernetes.io search is allowed, without opening external results."),
  "https://kubernetes.io/docs/reference/kubectl/quick-reference/")

Q("e-time", "6", T("Une tâche à 4 % bloque depuis 8 minutes. La bonne décision :", "A 4% task has been stuck for 8 minutes. The right call:"),
  [T("La noter et passer à la suivante", "Flag it and move on"), T("Insister jusqu'au bout", "Persist to the end"),
   T("Recommencer l'examen", "Restart the exam"), T("Supprimer ses ressources", "Delete its resources")],
  0, T("Environ une minute par point : reviens-y en seconde passe ; le crédit partiel compte.", "About one minute per point: come back in a second pass; partial credit counts."),
  "mock time 4")
