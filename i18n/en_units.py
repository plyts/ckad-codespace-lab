"""English content of the exercises and scenarios (source for task.en.md, hints.en.md, check.en.txt).

E(id, title, body, hints[3], checks[(title, why)]) — checks in the exact runtime order of check.sh.
Applied by i18n/apply_en.py, which refuses any count mismatch.
"""
UNITS = {}


def E(uid, title, body, hints, checks):
    UNITS[uid] = {"title": title, "body": body, "hints": hints, "checks": checks}


# ------------------------------------------------------------------ domain 1
E("d1-01", "First nginx Pod", """
In namespace `d1-01`, create a Pod named `web`:

- image `nginx:1.27-alpine`
- label `app=web`
- container port `80`

The Pod must be `Running` and ready.
""", ["`kubectl run` creates a Pod. See `kubectl run --help`: options `--image`, `--labels`, `--port`.",
      "Do not forget the namespace: `-n d1-01`.",
      "`kubectl -n d1-01 run web --image=nginx:1.27-alpine --labels=app=web --port=80`"],
  [("The Pod web exists", "The task asks for a Pod named exactly web, in namespace $NS."),
   ("Image nginx:1.27-alpine", "The tag is part of the image: nginx without a tag pulls latest, not 1.27-alpine."),
   ("Label app=web", "Labels drive selectors (Services, Deployments). Use kubectl run --labels=app=web or kubectl label."),
   ("Container port 80 declared", "containerPort is informational but expected here: kubectl run --port=80 sets it."),
   ("The Pod is ready", "A created Pod is not necessarily started: read the events if it stays Pending or in error.")])

E("d1-02", "Job with several completions", """
In namespace `d1-02`, create a Job named `counter`:

- image `busybox:1.37`, command `sh -c 'echo traitement terminé'`
- it must succeed **3 times** (3 completions), **at most 2 Pods in parallel**
- `backoffLimit` of `2`

The Job must complete successfully.
""", ["`kubectl create job` does not know `completions`: generate the YAML then edit it.",
      "`completions`, `parallelism` and `backoffLimit` live under the Job's `spec` (not under `template`).",
      "`kubectl -n d1-02 create job counter --image=busybox:1.37 --dry-run=client -o yaml -- sh -c 'echo traitement terminé' > job.yaml`, then add the 3 fields."],
  [("The Job counter exists", "You need a Job object (batch/v1), not a Pod."),
   ("completions = 3", "completions = number of Pods that must succeed."),
   ("parallelism = 2", "parallelism = maximum number of Pods at the same time."),
   ("backoffLimit = 2", "backoffLimit caps retries on failure (6 by default)."),
   ("3 Pods succeeded", "The Job must finish. If a Pod fails, read its logs.")])

E("d1-03", "Backup CronJob", """
In namespace `d1-03`, create a CronJob named `backup`:

- runs **every 5 minutes**
- image `busybox:1.37`, command `sh -c 'echo sauvegarde'`
- keeps **2** successful Jobs and **1** failed Job in the history
- a new run must **never** start while the previous one is still running
""", ["`kubectl create cronjob --help`: options `--image` and `--schedule`, the command after `--`.",
      "History limits and `concurrencyPolicy` live under the CronJob's `spec`: generate the YAML and add them.",
      "`kubectl -n d1-03 create cronjob backup --image=busybox:1.37 --schedule='*/5 * * * *' --dry-run=client -o yaml -- sh -c 'echo sauvegarde'`"],
  [("The CronJob backup exists", "You need a CronJob (batch/v1)."),
   ("Scheduled every 5 minutes", "Cron format: minute hour day month weekday. Every 5 minutes: */5 * * * *"),
   ("successfulJobsHistoryLimit = 2", "History of successful Jobs (3 by default)."),
   ("failedJobsHistoryLimit = 1", "History of failed Jobs (1 by default, but explicit here)."),
   ("concurrencyPolicy = Forbid", "Forbid skips a run while the previous one is still running (Allow by default, Replace replaces)."),
   ("Container command", "The requested command is sh -c 'echo sauvegarde'.")])

E("d1-04", "Sidecar following a log file", """
In namespace `d1-04`, create a Pod `logger` with two containers sharing an `emptyDir` volume named
`logs`, mounted on `/var/log/app`:

- main container `app`, image `busybox:1.37`, writing a line every 2 seconds:
  `sh -c 'while true; do echo "tick $(date)" >> /var/log/app/app.log; sleep 2; done'`
- sidecar container `shipper`, image `busybox:1.37`, printing that file continuously:
  `sh -c 'tail -F /var/log/app/app.log'`

Use a **native sidecar** (an init container restarted continuously).
`kubectl logs logger -c shipper` must show the `tick` lines.
""", ["You need YAML: generate a Pod with `kubectl run logger --image=busybox:1.37 --dry-run=client -o yaml`, then complete it.",
      "A native sidecar is declared under `initContainers:` with `restartPolicy: Always`. The volume: `volumes: - name: logs  emptyDir: {}`.",
      "Both containers have `volumeMounts: - name: logs  mountPath: /var/log/app`."],
  [("The Pod logger is Running", "The Pod must run with both containers."),
   ("Container app present", "The main container must be named app."),
   ("Container shipper present", "The sidecar must be named shipper."),
   ("shipper is a native sidecar (initContainer, restartPolicy Always)", "Since Kubernetes 1.29, a native sidecar is an initContainer with restartPolicy: Always: it starts before app and lives with the Pod."),
   ("Both containers mount /var/log/app", "Sharing goes through the same volume mounted in both containers."),
   ("kubectl logs logger -c shipper shows tick lines", "The sidecar reads the file written by app: check the volume and the app.log path.")])

E("d1-05", "Init container preparing content", """
In namespace `d1-05`, create a Pod `site` (label `app=site`):

- an init container `prepare`, image `busybox:1.37`, writing `site prêt` into `/work/index.html`
- a container `nginx`, image `nginx:1.27-alpine`, serving that file: the same `emptyDir` volume is
  mounted on `/usr/share/nginx/html`

An HTTP request on port 80 of the Pod must return `site prêt`.
""", ["Two containers, one shared `emptyDir` volume: the init mounts it on `/work`, nginx on `/usr/share/nginx/html`.",
      "Init command: `sh -c 'echo \"site prêt\" > /work/index.html'`.",
      "To test: `kubectl run tmp --rm -it --image=busybox:1.37 --restart=Never -- wget -qO- http://<Pod IP>`."],
  [("Init container prepare present", "An init container runs to completion BEFORE the main containers."),
   ("Container nginx present", "The main container must be named nginx."),
   ("The Pod is ready", "If the init container fails, the Pod stays in Init:Error or Init:CrashLoopBackOff."),
   ("HTTP on the Pod returns « site prêt »", "nginx serves /usr/share/nginx/html: the init must write into the same volume, as index.html.")])

E("d1-06", "PersistentVolumeClaim and persistent data", """
In namespace `d1-06`:

1. Create a PersistentVolumeClaim `data` of `100Mi`, access mode `ReadWriteOnce`, StorageClass
   `standard`.
2. Create a Pod `writer` (image `busybox:1.37`) mounting this PVC on `/data` and running
   `sh -c 'echo persistant > /data/proof.txt && sleep 3600'`.

The PVC must be `Bound` and the file `/data/proof.txt` must exist in the Pod.
""", ["No imperative command for a PVC: copy the example from the docs (\"PersistentVolumeClaims\").",
      "The Pod declares `volumes: - name: data  persistentVolumeClaim: { claimName: data }` then a `volumeMounts` on `/data`.",
      "A Pending PVC with `WaitForFirstConsumer` is normal as long as the Pod does not exist."],
  [("PVC data Bound", "With kind's standard StorageClass (WaitForFirstConsumer), the PVC stays Pending until a Pod uses it."),
   ("Requested size 100Mi", "The requested size is under spec.resources.requests.storage."),
   ("Mode ReadWriteOnce", "accessModes is a list: [ReadWriteOnce]."),
   ("The Pod writer uses the PVC data", "The Pod volume references the PVC through persistentVolumeClaim.claimName."),
   ("File /data/proof.txt written", "The volume must be mounted on /data in the container.")])

E("d1-07", "Build and export an image", """
Directory `~/ckad/d1-07/` contains a `Dockerfile` and an `index.html`.

1. Edit the `Dockerfile` to add the label `maintainer=ckad`, the environment variable
   `APP_VERSION=v1` and declare port `8080`.
2. Build the image `ckad/hello:v1` with `docker` (or `podman`).
3. Export it into the archive `~/ckad/d1-07/hello.tar`.

(Context and namespace do not apply: this task happens outside the cluster.)
""", ["Three lines to add to the Dockerfile: `LABEL`, `ENV`, `EXPOSE`.",
      "Build: `docker build -t ckad/hello:v1 ~/ckad/d1-07`.",
      "Export: `docker save -o ~/ckad/d1-07/hello.tar ckad/hello:v1` (podman: `podman save -o …`)."],
  [("The image ckad/hello:v1 exists", "The image must be built with the exact tag ckad/hello:v1 (option -t)."),
   ("Label maintainer=ckad", "Dockerfile instruction: LABEL maintainer=ckad, then rebuild."),
   ("Variable APP_VERSION=v1", "Dockerfile instruction: ENV APP_VERSION=v1."),
   ("Port 8080 exposed", "Dockerfile instruction: EXPOSE 8080."),
   ("Archive ~/ckad/d1-07/hello.tar containing ckad/hello:v1", "docker save -o file.tar image:tag writes the image and its tag into the archive.")])

E("d1-08", "DaemonSet on every node", """
In namespace `d1-08`, create a DaemonSet `node-agent` (label `app=node-agent`), image
`busybox:1.37`, command `sh -c 'sleep 3600'`.

A Pod must run on **every** node of the cluster, **control plane included**.
""", ["No `kubectl create daemonset`: generate a Deployment with `--dry-run=client -o yaml`, change `kind` and remove `replicas` and `strategy`.",
      "Control-plane taint: `node-role.kubernetes.io/control-plane:NoSchedule`.",
      "`tolerations: - key: node-role.kubernetes.io/control-plane  operator: Exists  effect: NoSchedule`"],
  [("The DaemonSet node-agent exists", "You need a DaemonSet (apps/v1)."),
   ("One Pod scheduled on every node", "The control plane carries the node-role.kubernetes.io/control-plane:NoSchedule taint: without a toleration, the DaemonSet avoids it."),
   ("All Pods are ready", "Every DaemonSet Pod must be Ready.")])

E("d1-09", "Exam-style: report Pod", """
*Exam-style task — 8 minutes.* Context `ckad-a`, namespace `d1-09`.

Create a Pod `report`:

- an `emptyDir` volume named `work`, **in memory** (`medium: Memory`), limited to `16Mi`
- an init container `stamp` (`busybox:1.37`) writing `rapport du jour` into `/work/report.txt`
- a container `reader` (`busybox:1.37`) running `sh -c 'cat /work/report.txt && sleep 3600'`
- both containers mount `work` on `/work`

Save the manifest you used into `~/ckad/d1-09/report.yaml`.
""", ["Start with the file: `kubectl run report --image=busybox:1.37 --dry-run=client -o yaml > ~/ckad/d1-09/report.yaml`.",
      "`emptyDir: { medium: Memory, sizeLimit: 16Mi }`.",
      "Apply the saved file: `kubectl apply -f ~/ckad/d1-09/report.yaml`."],
  [("Pod report ready", "The Pod must run."),
   ("Volume work in memory", "emptyDir.medium: Memory mounts a tmpfs (RAM)."),
   ("Limit 16Mi", "emptyDir.sizeLimit: 16Mi."),
   ("Init container stamp", "Writing happens in an init container named stamp."),
   ("reader prints the report", "The reader container reads the file written by the init: same volume, same path."),
   ("Manifest saved in ~/ckad/d1-09/report.yaml", "In the exam, a task often asks to save a file at a precise path: it is graded.")])

# ------------------------------------------------------------------ domain 2
E("d2-01", "First Deployment", """
In namespace `d2-01`, create a Deployment `front`: image `nginx:1.27-alpine`, **3 replicas**, Pods
labelled `app=front`. The 3 replicas must be ready.
""", ["`kubectl create deployment --help`: options `--image` and `--replicas`.",
      "`kubectl -n d2-01 create deployment front --image=nginx:1.27-alpine --replicas=3`",
      "Follow the rollout: `kubectl -n d2-01 rollout status deploy/front`."],
  [("Deployment front", "You need a Deployment (apps/v1), not standalone Pods."),
   ("Image nginx:1.27-alpine", "The image is in the Pod template."),
   ("Selector app=front", "kubectl create deployment front automatically sets app=front on the selector and the Pods."),
   ("3 replicas ready", "Replicas must be Running and Ready.")])

E("d2-02", "Scaling", """
Deployment `front` in namespace `d2-02` runs with 1 replica.
Scale it to **5 ready replicas**, without recreating it.
""", ["A single command is enough: `kubectl scale`.",
      "`kubectl -n d2-02 scale deploy front --replicas=5`",
      "Alternative: `kubectl -n d2-02 edit deploy front` and change `spec.replicas`."],
  [("replicas = 5", "kubectl scale changes the Deployment's spec.replicas."),
   ("5 replicas ready", "The new Pods must start."),
   ("Deployment not recreated (same as at the start)", "Scaling creates no new revision: only the Pod count changes.")])

E("d2-03", "Rolling update with a cause", """
In namespace `d2-03`, update Deployment `front` to image `nginx:1.28-alpine` (container `nginx`),
through a rolling update.

Add to the revision the annotation `kubernetes.io/change-cause` with the value `passage en 1.28`, so
that it shows in `kubectl rollout history`.
""", ["`kubectl set image deploy/front <container>=<image>`: the container is named `nginx`.",
      "`kubectl annotate deploy front kubernetes.io/change-cause='passage en 1.28'`",
      "`kubectl -n d2-03 rollout history deploy/front` must show the cause on revision 2."],
  [("Image nginx:1.28-alpine", "kubectl set image deploy/front nginx=nginx:1.28-alpine (container name = nginx)."),
   ("Revision 2", "Every template change creates a revision (a new ReplicaSet)."),
   ("Cause in the history", "--record is gone: annotate the Deployment after the update."),
   ("All replicas updated and ready", "The rolling update must be finished.")])

E("d2-04", "Rollback after a failed update", """
In namespace `d2-04`, an update of Deployment `front` just failed.
Diagnose the failure, then **go back to the previous revision**, which worked.
All replicas must be ready.
""", ["Look at the Pods: `kubectl -n d2-04 get pods`, then `describe` a failing Pod.",
      "`kubectl -n d2-04 rollout history deploy/front` shows the revisions.",
      "`kubectl -n d2-04 rollout undo deploy/front`"],
  [("Image back to nginx:1.27-alpine", "nginx:1.99-nexistepas does not exist: ErrImagePull then ImagePullBackOff. kubectl rollout undo goes back to the previous revision."),
   ("3 replicas updated and ready", "After the rollback, the ImagePullBackOff Pods are replaced."),
   ("No Pod failing to pull", "No Pod of the broken revision may remain.")])

E("d2-05", "Tuning the deployment strategy", """
In namespace `d2-05`, change Deployment `api`:

- a rolling update that **never** removes a Pod before a new one is ready (`maxUnavailable: 0`)
  and creates **at most 1** extra Pod (`maxSurge: 1`)
- a Pod only counts as available after being ready for **5 seconds**
- keep **4** old ReplicaSets at most
""", ["`kubectl -n d2-05 edit deploy api` or `kubectl patch`.",
      "All these fields are under the Deployment's `spec`: `strategy.rollingUpdate`, `minReadySeconds`, `revisionHistoryLimit`.",
      "`kubectl explain deploy.spec --recursive | less` to find the exact names."],
  [("Strategy RollingUpdate", "Two strategies: RollingUpdate (default) and Recreate."),
   ("maxUnavailable = 0", "maxUnavailable: 0 keeps full capacity during the update."),
   ("maxSurge = 1", "maxSurge: 1 allows one Pod more than replicas during the update."),
   ("minReadySeconds = 5", "minReadySeconds is under the Deployment's spec, not in the template."),
   ("revisionHistoryLimit = 4", "revisionHistoryLimit (10 by default): number of old ReplicaSets kept.")])

E("d2-06", "Install a Helm chart", """
A Helm chart is available in `~/ckad/d2-06/webapp`.

1. Install it in namespace `d2-06` as release `shop`, with `replicaCount=2` and
   `image.tag=1.28-alpine`.
2. Write the chart's **default** values (output of `helm show values`) into
   `~/ckad/d2-06/values.txt`.
""", ["`helm install --help`: `-n`, `--set`, and the chart path as second argument.",
      "`helm -n d2-06 install shop ~/ckad/d2-06/webapp --set replicaCount=2 --set image.tag=1.28-alpine`",
      "`helm show values ~/ckad/d2-06/webapp > ~/ckad/d2-06/values.txt`"],
  [("Release shop deployed", "helm install <release> <chart> -n <namespace>."),
   ("replicaCount = 2", "Values are passed with --set replicaCount=2 (or -f values.yaml)."),
   ("Image nginx:1.28-alpine", "--set image.tag=1.28-alpine: a nested key is written with a dot."),
   ("2 replicas ready", "The release Pods must run."),
   ("values.txt contains the default values", "helm show values <chart> > file.")])

E("d2-07", "Blue/green switch", """
In namespace `d2-07`, the **blue** version of the app runs (Deployment `web-blue`) and Service `web`
sends it the traffic.

1. Deploy the **green** version: Deployment `web-green`, 2 replicas, image
   `hashicorp/http-echo:1.0.0` with the argument `-text=green`, port 5678, labels `app=web` and
   `version=green`.
2. Once green is ready, **switch all the traffic** of Service `web` to green.
3. Keep `web-blue` in place (rollback possible).
""", ["Copy the blue Deployment: `kubectl -n d2-07 get deploy web-blue -o yaml > green.yaml`, then replace blue with green (name, labels, selector, argument).",
      "Clean the copied YAML (status, uid, resourceVersion, creationTimestamp) or start from `kubectl create deployment --dry-run=client -o yaml`.",
      "Switch: `kubectl -n d2-07 patch svc web -p '{\"spec\":{\"selector\":{\"app\":\"web\",\"version\":\"green\"}}}'`."],
  [("web-green: 2 replicas ready", "The new version must be ready BEFORE the switch."),
   ("The Service selects version=green", "A blue/green switch is a change of the Service selector."),
   ("web-blue kept", "Keeping blue allows an instant rollback."),
   ("Service web answers green", "The Service must point to the green Pods (port 80 to 5678).")])

E("d2-08", "20% canary", """
In namespace `d2-08`, Service `api` sends traffic to the 5 Pods of `api-v1` (labels `app=api`,
`track=stable`).

Set up a **canary**: about **20%** of the requests must reach a new version, without changing the
Service:

- Deployment `api-v2`, image `hashicorp/http-echo:1.0.0`, argument `-text=api v2`, port 5678,
  labels `app=api` and `track=canary`
- **5 Pods** in total behind the Service: 4 stable and 1 canary
""", ["The Service only selects `app=api`: any Pod with that label receives traffic.",
      "Create `api-v2` (1 replica) then `kubectl -n d2-08 scale deploy api-v1 --replicas=4`.",
      "Check: `kubectl -n d2-08 get endpointslices -l kubernetes.io/service-name=api`."],
  [("api-v2: 1 replica ready", "One canary Pod out of 5 gives about 20% of the traffic."),
   ("api-v1 scaled down to 4 replicas", "4 stable + 1 canary = 5 Pods: the share comes from the Pod count."),
   ("The canary carries app=api and track=canary", "The Service selects app=api: the canary needs that label to receive traffic."),
   ("5 ready Pods behind the Service", "The Service does not change: it sees every app=api Pod."),
   ("The Service selector did not change", "The task forbids changing the Service.")])

E("d2-09", "Exam-style: Kustomize overlay", """
*Exam-style task — 8 minutes.* Context `ckad-a`.

A Kustomize base is provided in `~/ckad/d2-09/base`. Create the overlay
`~/ckad/d2-09/overlays/prod/kustomization.yaml` that:

- uses the base
- deploys into namespace `d2-09`
- prefixes names with `prod-`
- sets the Deployment to **3 replicas**
- adds the label `env=prod` to every resource

Apply the overlay with `kubectl`.
""", ["The overlay references the base by relative path: `resources: [../../base]`.",
      "Useful fields: `namespace`, `namePrefix`, `labels` (or `commonLabels`), `replicas`.",
      "Preview before applying: `kubectl kustomize ~/ckad/d2-09/overlays/prod`, then `kubectl apply -k …`."],
  [("Deployment prod-web created in d2-09", "namePrefix: prod- and namespace: d2-09 in kustomization.yaml, then kubectl apply -k."),
   ("3 replicas ready", "Field replicas: - name: web  count: 3 (the name BEFORE the prefix)."),
   ("Label env=prod on the Deployment", "labels: - pairs: {env: prod} (or commonLabels, deprecated but still accepted)."),
   ("Service prod-web labelled env=prod", "The label must apply to every resource of the base."),
   ("Overlay saved at the right path", "The graded file is ~/ckad/d2-09/overlays/prod/kustomization.yaml and it must be valid.")])

# ------------------------------------------------------------------ domain 3
E("d3-01", "Find a line in the logs", """
Pod `talker` in namespace `d3-01` wrote a line `SECRET_CODE=…` into its logs.
Write **only the code value** (without `SECRET_CODE=`) into `~/ckad/d3-01/code.txt`.
""", ["`kubectl -n d3-01 logs talker` prints the container output.",
      "`grep SECRET_CODE` then `cut -d= -f2`.",
      "`kubectl -n d3-01 logs talker | grep SECRET_CODE | cut -d= -f2 > ~/ckad/d3-01/code.txt`"],
  [("code.txt contains the right code", "kubectl logs talker | grep SECRET_CODE, then keep only the value (cut -d= -f2).")])

E("d3-02", "HTTP liveness probe", """
In namespace `d3-02`, create a Pod `web` (image `nginx:1.27-alpine`) with an HTTP **liveness probe**
`GET /` on port `80`, starting after **5 seconds** and running every **10 seconds**.
""", ["Generate the Pod: `kubectl -n d3-02 run web --image=nginx:1.27-alpine --dry-run=client -o yaml > web.yaml`.",
      "Under the container: `livenessProbe: {httpGet: {path: /, port: 80}, initialDelaySeconds: 5, periodSeconds: 10}`.",
      "Search \"liveness\" in kubernetes.io/docs: the page \"Configure Liveness, Readiness and Startup Probes\" has ready-made examples."],
  [("Liveness httpGet on /", "livenessProbe.httpGet.path: / ."),
   ("Port 80", "livenessProbe.httpGet.port: 80."),
   ("initialDelaySeconds = 5", "Delay before the first attempt."),
   ("periodSeconds = 10", "Interval between two attempts."),
   ("Pod ready, no restart", "A failing liveness probe restarts the container.")])

E("d3-03", "TCP readiness probe on a Deployment", """
In namespace `d3-03`, add to container `api` of Deployment `api` a **TCP readiness probe** on port
`5678`, every `5` seconds, after `2` seconds. Both replicas must become ready again.
""", ["`kubectl -n d3-03 edit deploy api`: the probe goes into `spec.template.spec.containers[0]`.",
      "`readinessProbe: {tcpSocket: {port: 5678}, initialDelaySeconds: 2, periodSeconds: 5}`",
      "Changing the template triggers a rolling update: `kubectl -n d3-03 rollout status deploy/api`."],
  [("Readiness tcpSocket 5678", "readinessProbe.tcpSocket.port: the probe opens a TCP connection."),
   ("periodSeconds 5 / initialDelaySeconds 2", "Both delays are in the probe."),
   ("2 replicas ready", "Readiness: a non-ready Pod leaves the Service Endpoints, without a restart.")])

E("d3-04", "CrashLoopBackOff", """
In namespace `d3-04`, Deployment `worker` keeps restarting.

1. Write the container's **exit code** into `~/ckad/d3-04/exit-code.txt`.
2. Fix the Deployment so that the container sleeps 3600 seconds as intended.
""", ["`kubectl -n d3-04 get pods`, then `kubectl -n d3-04 describe pod <pod>`: look at \"Last State\".",
      "`kubectl -n d3-04 logs <pod> --previous` shows the output of the dead container.",
      "`kubectl -n d3-04 edit deploy worker` and fix `slep` into `sleep`."],
  [("Exit code 127 recorded", "describe pod shows Last State: Terminated, Exit Code. 127 = command not found (slep)."),
   ("1 replica available", "The command must be sleep 3600 (typo: slep)."),
   ("No Pod left in CrashLoopBackOff", "Old Pods disappear once the rolling update is over.")])

E("d3-05", "ImagePullBackOff", """
In namespace `d3-05`, Deployment `cache` does not start.
Find the cause and fix it: it must use the official Redis image `7.4-alpine`.
""", ["`kubectl -n d3-05 get pods` then `describe`: the Events section gives the exact message.",
      "The container is named `redis` (name derived from the image by `kubectl create deployment`).",
      "`kubectl -n d3-05 set image deploy/cache redis=redis:7.4-alpine`"],
  [("Image redis:7.4-alpine", "Tag 7.4-alpinee does not exist: ErrImagePull then ImagePullBackOff (the kubelet spaces its attempts)."),
   ("1 replica ready", "The new Pod must start.")])

E("d3-06", "Pending Pod: read the events", """
In namespace `d3-06`, Pod `big` stays `Pending`.

1. Write into `~/ckad/d3-06/reason.txt` the **reason** (`Reason` field) of the event that explains
   it.
2. Get Pod `big` running (same name, same image) with a request of `50m` CPU.
""", ["`kubectl -n d3-06 describe pod big`: Events section at the bottom.",
      "To recreate: `kubectl -n d3-06 get pod big -o yaml > big.yaml`, fix it, then `kubectl replace --force -f big.yaml`.",
      "`50` CPU versus `50m`: the m suffix means millicores."],
  [("Reason recorded", "kubectl get events (or describe pod): REASON column. 50 whole CPUs fit on no node."),
   ("CPU request 50m", "50 = 50 cores; 50m = 50 millicores. A Pod's resources are changed by recreating it (or through resize)."),
   ("Pod big Running", "The Pod must be scheduled and then start.")])

E("d3-07", "Deprecated APIs: migrate a manifest", """
File `~/ckad/d3-07/old.yaml` comes from an old cluster: `kubectl apply` rejects it.

Fix **the file itself** so that it uses the current API versions, then apply it. CronJob `cleanup`
and PodDisruptionBudget `web-pdb` must exist in namespace `d3-07`.
""", ["`kubectl apply -f ~/ckad/d3-07/old.yaml`: read the error message carefully.",
      "`kubectl api-resources | grep -E 'cronjob|poddisruption'` gives the current group/version.",
      "`kubectl explain cronjob` prints the VERSION at the top."],
  [("CronJob cleanup created", "batch/v1beta1 CronJob was removed in 1.25: use batch/v1."),
   ("PDB web-pdb created", "policy/v1beta1 PodDisruptionBudget was removed in 1.25: use policy/v1."),
   ("No v1beta1 API left in the file", "The task asks to fix the file (it will be reused).")])

E("d3-08", "kubectl top: the greediest Pod", """
In namespace `d3-08`, three Pods `worker-*` run. One of them uses a lot of CPU.
Write its **name** into `~/ckad/d3-08/top.txt`.

(You need metrics-server: wait a minute after startup to get metrics.)
""", ["`kubectl top pods -n d3-08`",
      "Option `--sort-by=cpu`.",
      "`kubectl -n d3-08 top pods --sort-by=cpu --no-headers | head -1 | awk '{print $1}' > ~/ckad/d3-08/top.txt`"],
  [("Name of the greediest Pod", "kubectl top pods --sort-by=cpu ranks Pods by usage.")])

E("d3-09", "Exam-style: misconfigured probes", """
*Exam-style task — 8 minutes.* Context `ckad-a`, namespace `d3-09`.

The Pods of Deployment `orders` keep restarting.

1. Write into `~/ckad/d3-09/cause.txt` the event message explaining the restarts (one line is
   enough).
2. Fix the **liveness probe** so that it targets the application's right port.
3. Add a **startup probe** HTTP `GET /` on that same port, `failureThreshold: 10`,
   `periodSeconds: 2`.
""", ["`kubectl -n d3-09 get events --sort-by=.lastTimestamp | grep -i unhealthy`",
      "Compare the probe port and the container's `containerPort`.",
      "`kubectl -n d3-09 edit deploy orders`: fix the port and add `startupProbe` at the same level as `livenessProbe`."],
  [("cause.txt mentions the liveness probe", "Unhealthy events say \"Liveness probe failed … connection refused\": port 8080 does not listen."),
   ("Liveness on port 5678", "http-echo listens on 5678 (see containerPort)."),
   ("Startup probe GET / 5678", "startupProbe: until it succeeds, liveness and readiness are paused."),
   ("Startup: failureThreshold 10, periodSeconds 2", "10 attempts × 2 s = 20 s to start."),
   ("2 replicas ready and updated", "After the fix, the rolling update replaces the Pods.")])

# ------------------------------------------------------------------ domain 4
E("d4-01", "ConfigMap as environment variables", """
In namespace `d4-01`:

1. Create ConfigMap `app-config` with `APP_MODE=prod` and `APP_COLOR=blue`.
2. Create Pod `app` (image `busybox:1.37`, command `sh -c 'sleep 3600'`) receiving **all** keys of
   that ConfigMap as environment variables.
""", ["`kubectl create configmap --help`: `--from-literal=KEY=value` (repeatable).",
      "For the Pod, generate the YAML with `kubectl run … --dry-run=client -o yaml` and add `envFrom`.",
      "`envFrom: - configMapRef: {name: app-config}`"],
  [("ConfigMap app-config", "kubectl create configmap app-config --from-literal=APP_MODE=prod --from-literal=APP_COLOR=blue"),
   ("The Pod uses envFrom", "envFrom.configMapRef imports every key at once (env.valueFrom: one key at a time)."),
   ("Variables visible in the container", "Variables are only read when the container starts.")])

E("d4-02", "Secret in a variable", """
In namespace `d4-02`:

1. Create the generic Secret `db-cred` with `username=admin` and `password=S3cr3t!`.
2. Create Pod `db-client` (image `busybox:1.37`, `sh -c 'sleep 3600'`) with variable `DB_PASSWORD`
   set from the Secret's `password` key.
""", ["A generic Secret is created like a ConfigMap: `kubectl create secret generic --help` (`--from-literal`). Mind the `!` in bash: single quotes.",
      "The Pod: `kubectl run … --dry-run=client -o yaml`, then add `env` with `valueFrom.secretKeyRef`.",
      "Check: `kubectl -n d4-02 exec db-client -- printenv DB_PASSWORD`."],
  [("Secret db-cred (password)", "In a Secret, data is base64-encoded (not encrypted!). Mind the quotes around S3cr3t! in bash."),
   ("Secret db-cred (username)", "--from-literal=username=admin."),
   ("DB_PASSWORD references the Secret", "env: - name: DB_PASSWORD  valueFrom: secretKeyRef: {name: db-cred, key: password}"),
   ("Value inside the container", "The container sees the decoded value.")])

E("d4-03", "Dedicated ServiceAccount", """
In namespace `d4-03`, create ServiceAccount `deployer`, then Pod `tool` (image `busybox:1.37`,
`sh -c 'sleep 3600'`) using it. The ServiceAccount token must **not** be mounted automatically in
that Pod.
""", ["The ServiceAccount is one imperative command (`kubectl create serviceaccount --help`); the Pod needs YAML.",
      "In the Pod: `serviceAccountName: deployer` and `automountServiceAccountToken: false` under `spec`.",
      "That Pod field is immutable: delete and recreate the Pod if you got it wrong."],
  [("ServiceAccount deployer", "kubectl create serviceaccount deployer."),
   ("The Pod uses deployer", "spec.serviceAccountName (the serviceAccount field alone is deprecated)."),
   ("Token not mounted", "automountServiceAccountToken: false in the Pod (or on the ServiceAccount)."),
   ("Pod ready", "The Pod must run.")])

E("d4-04", "Requests and limits", """
In namespace `d4-04`, create Pod `bounded` (image `nginx:1.27-alpine`) with:

- requests: `100m` CPU and `64Mi` memory
- limits: `200m` CPU and `128Mi` memory

Write its **QoS class** into `~/ckad/d4-04/qos.txt`.
""", ["`kubectl run bounded --image=nginx:1.27-alpine --dry-run=client -o yaml` then add `resources`.",
      "`resources: {requests: {cpu: 100m, memory: 64Mi}, limits: {cpu: 200m, memory: 128Mi}}`",
      "`kubectl get pod bounded -o jsonpath='{.status.qosClass}'`"],
  [("Requests 100m / 64Mi", "resources.requests: what the scheduler reserves."),
   ("Limits 200m / 128Mi", "resources.limits: CPU throttled above, memory killed (OOMKilled)."),
   ("QoS class recorded", "requests < limits: Burstable. requests = limits everywhere: Guaranteed. Nothing: BestEffort."),
   ("Pod ready", "The Pod must run.")])

E("d4-05", "ResourceQuota and LimitRange", """
In namespace `d4-05`:

1. Create ResourceQuota `ns-quota`: at most `5` Pods, `requests.cpu=1`, `requests.memory=1Gi`,
   `limits.cpu=2`, `limits.memory=2Gi`.
2. Create LimitRange `defaults` giving containers without resources: requests `50m` / `32Mi` and
   limits `100m` / `64Mi`.
3. Check it: create Pod `plain` (`nginx:1.27-alpine`) **without** a `resources` section.
""", ["ResourceQuota has an imperative command (`kubectl create quota --help`, option `--hard`); LimitRange does not: copy the docs example \"Configure Default Memory Requests and Limits\".",
      "If the Pod is rejected (`must specify limits`), the LimitRange was missing when it was created: order matters.",
      "`kubectl -n d4-05 create quota ns-quota --hard=pods=5,requests.cpu=1,requests.memory=1Gi,limits.cpu=2,limits.memory=2Gi`"],
  [("Quota: pods=5", "kubectl create quota ns-quota --hard=pods=5,requests.cpu=1,..."),
   ("Quota: requests and limits", "Quota keys contain a dot: requests.cpu."),
   ("LimitRange: default requests", "defaultRequest = requests injected when missing."),
   ("LimitRange: default limits", "default = limits injected when missing (type: Container)."),
   ("The Pod plain got the defaults", "With a quota on requests/limits, a Pod without resources is REJECTED… unless a LimitRange injects them. Create the LimitRange before the Pod.")])

E("d4-06", "Hardened SecurityContext", """
In namespace `d4-06`, create Pod `secure` (image `busybox:1.37`, `sh -c 'sleep 3600'`):

- at **Pod** level: user `1000`, group `3000`, `fsGroup` `2000`
- at **container** level: no privilege escalation, **read-only** root filesystem, **all**
  capabilities dropped
""", ["Two `securityContext` blocks: one under `spec` (Pod), one under the container.",
      "Pod: `runAsUser`, `runAsGroup`, `fsGroup`. Container: `allowPrivilegeEscalation`, `readOnlyRootFilesystem`, `capabilities`.",
      "Check: `kubectl -n d4-06 exec secure -- id`."],
  [("runAsUser / runAsGroup / fsGroup", "These fields are in spec.securityContext (Pod level)."),
   ("allowPrivilegeEscalation false", "Container field: containers[].securityContext."),
   ("readOnlyRootFilesystem true", "Container field only (it does not exist at Pod level)."),
   ("capabilities drop ALL", "capabilities: {drop: [ALL]} (container level)."),
   ("The process runs as uid 1000", "The Pod must run to check it."),
   ("Write refused on /", "Read-only root: touch /test must fail.")])

E("d4-07", "RBAC: Role and RoleBinding", """
In namespace `d4-07`, ServiceAccount `monitor` must be able to **read** Pods (`get`, `list`, `watch`)
and their logs (`pods/log`), and nothing else.

Create Role `pod-reader` and RoleBinding `monitor-pod-reader`.
""", ["Two objects: a Role (the permissions) and a RoleBinding (who receives them). Logs are the `pods/log` subresource.",
      "`kubectl create role --help` (`--verb`, `--resource`) and `kubectl create rolebinding --help` (`--serviceaccount=<ns>:<name>`).",
      "Test: `kubectl auth can-i list pods -n d4-07 --as=system:serviceaccount:d4-07:monitor`."],
  [("monitor can list Pods", "A Role with verbs get,list,watch on pods, bound to the ServiceAccount by a RoleBinding."),
   ("monitor can read logs", "Logs are a subresource: pods/log."),
   ("monitor cannot delete a Pod", "Least privilege: read only."),
   ("monitor cannot see Secrets", "The Role must only cover pods and pods/log."),
   ("Permissions limited to the namespace", "A Role + RoleBinding only applies in its namespace (ClusterRole + ClusterRoleBinding for the whole cluster).")])

E("d4-08", "Use a custom resource (CRD)", """
A backup operator installed a custom resource in the cluster.

1. Find its name, group and version (`kubectl api-resources`, `kubectl explain`).
2. In namespace `d4-08`, create an object of that type named `nightly`, with
   `schedule: "0 2 * * *"` and `retention: 7`.
""", ["`kubectl get crd`, then `kubectl api-resources | grep -i backup`.",
      "`kubectl explain backup.spec` gives the expected fields.",
      "`apiVersion: lab.ckad.io/v1` · `kind: Backup`."],
  [("Backup nightly exists", "The CRD defines kind Backup of group lab.ckad.io, version v1 (apiVersion: lab.ckad.io/v1)."),
   ("schedule and retention", "retention is an integer (no quotes), schedule a string.")])

E("d4-09", "Exam-style: configured application", """
*Exam-style task — 9 minutes.* Context `ckad-a`, namespace `d4-09`.

1. ConfigMap `portal-html`, key `index.html` = `Portal OK`.
2. Secret `portal-key`, key `API_KEY` = `k-7731`.
3. ServiceAccount `portal-sa`.
4. Deployment `portal`, 2 replicas, image `nginx:1.27-alpine`, ServiceAccount `portal-sa`:
   - the ConfigMap mounted as a volume on `/usr/share/nginx/html`
   - variable `API_KEY` read from the Secret
   - requests `50m` CPU and `32Mi` memory
""", ["Three imperative commands: `create configmap --from-literal`, `create secret generic --from-literal`, `create serviceaccount`.",
      "Generate the Deployment: `kubectl -n d4-09 create deployment portal --image=nginx:1.27-alpine --replicas=2 --dry-run=client -o yaml > portal.yaml`.",
      "Add `serviceAccountName`, `volumes` (configMap), `volumeMounts`, `env.valueFrom.secretKeyRef` and `resources`."],
  [("2 replicas ready", "The Deployment must run."),
   ("ServiceAccount portal-sa", "spec.template.spec.serviceAccountName."),
   ("Requests 50m / 32Mi", "The container's resources.requests."),
   ("API_KEY read from the Secret", "env.valueFrom.secretKeyRef {name: portal-key, key: API_KEY}."),
   ("nginx serves « Portal OK »", "A configMap volume creates one file per key: index.html in /usr/share/nginx/html.")])

# ------------------------------------------------------------------ domain 5
E("d5-01", "Expose a Deployment (ClusterIP)", """
In namespace `d5-01`, expose Deployment `web` through a **ClusterIP** Service named `web`, port `80`
to port `80` of the containers.
""", ["`kubectl expose --help`",
      "`kubectl -n d5-01 expose deploy web --port=80 --target-port=80`",
      "Check the Endpoints: `kubectl -n d5-01 get endpointslices`."],
  [("Service web of type ClusterIP", "kubectl expose creates a ClusterIP by default."),
   ("Port 80 → 80", "port = Service port; targetPort = container port."),
   ("2 ready Endpoints", "The Service selector must match the Pod labels (app=web)."),
   ("http://web.$NS answers", "Short DNS name of the Service in the same namespace: web; full: web.$NS.svc.cluster.local.")])

E("d5-02", "NodePort Service", """
In namespace `d5-02`, create a **NodePort** Service `web-np` exposing Deployment `web`: port `80`,
target port `80`, **nodePort `30080`**.
""", ["`kubectl expose` can create a NodePort (`--type`) but not choose its number: generate the YAML with `--dry-run=client -o yaml`.",
      "Add `nodePort: 30080` in `spec.ports[0]`, then apply.",
      "`kubectl -n d5-02 expose deploy web --name=web-np --type=NodePort --port=80 --dry-run=client -o yaml > np.yaml`"],
  [("Type NodePort", "kubectl expose … --type=NodePort."),
   ("nodePort 30080", "kubectl expose cannot choose the nodePort: edit the Service or write the YAML (range 30000-32767)."),
   ("Reachable through a node IP on 30080", "A NodePort opens the same port on every node.")])

E("d5-03", "Service DNS", """
In namespace `d5-03`, a Service `db` exists.

1. Write its **fully qualified DNS name** (FQDN) into `~/ckad/d5-03/fqdn.txt`.
2. Write its **ClusterIP** address into `~/ckad/d5-03/ip.txt`.
3. Check the resolution from a throwaway Pod (`busybox:1.37`, `nslookup`).
""", ["The format is `<service>.<namespace>.svc.cluster.local`.",
      "`kubectl -n d5-03 get svc db -o jsonpath='{.spec.clusterIP}' > ~/ckad/d5-03/ip.txt`",
      "`kubectl -n d5-03 run t --rm -it --image=busybox:1.37 --restart=Never -- nslookup db`"],
  [("FQDN", "Form: <service>.<namespace>.svc.cluster.local (cluster.local is the default domain)."),
   ("ClusterIP", "kubectl get svc db -o jsonpath='{.spec.clusterIP}'.")])

E("d5-04", "Service without Endpoints", """
In namespace `d5-04`, Service `shop` does not answer, although the Pods of Deployment `shop` run.
Fix **the Service** (not the Deployment): `http://shop.d5-04` must answer `shop ok`.
""", ["`kubectl -n d5-04 get endpointslices`: empty = the selector finds no Pod.",
      "Compare `kubectl -n d5-04 get svc shop -o yaml` and `kubectl -n d5-04 get pods --show-labels`.",
      "Two mistakes: the selector AND the targetPort."],
  [("Selector app=shop", "The selector (app=shopp) matches no Pod: a Service without Endpoints."),
   ("targetPort 5678", "http-echo listens on 5678: a wrong targetPort gives Connection refused."),
   ("Deployment unchanged (2 replicas app=shop)", "The task requires fixing the Service."),
   ("http://shop.$NS answers « shop ok »", "Selector AND target port must both be right.")])

E("d5-05", "Ingress with two paths", """
In namespace `d5-05`, Services `front` (port 80) and `api` (port 8080) exist.

Create Ingress `shop` (class `traefik`) for host `shop.lab.local`:

- path `/` (Prefix) to `front:80`
- path `/api` (Prefix) to `api:8080`

Test: `curl -H 'Host: shop.lab.local' http://localhost:8080/api` in the Codespace.
""", ["`kubectl create ingress --help`: option `--rule=host/path*=service:port` (the star = Prefix).",
      "`--class=traefik`",
      "`kubectl -n d5-05 create ingress shop --class=traefik --rule='shop.lab.local/*=front:80' --rule='shop.lab.local/api*=api:8080'`"],
  [("ingressClassName traefik", "The lab controller is Traefik (class traefik). In the exam, the class is given in the task."),
   ("Host shop.lab.local", "rules[].host."),
   ("/ → front", "The / rule (Prefix) must target Service front, port 80."),
   ("/api → api", "The /api rule (Prefix) must target Service api, port 8080 (the Service port, not the container's).")])

E("d5-06", "NetworkPolicy: deny then allow", """
In namespace `d5-06`, Service `api` (Pods `app=api`, port 80) is open to everyone.

1. NetworkPolicy `default-deny`: **blocks all incoming traffic** to every Pod of the namespace.
2. NetworkPolicy `allow-frontend`: allows incoming traffic to Pods `app=api` on port `80`, **only**
   from Pods of the namespace labelled `role=frontend`.
""", ["Copy the examples from the \"Network Policies\" page: there is a \"default deny all ingress traffic\".",
      "`allow-frontend`: `podSelector: {matchLabels: {app: api}}`, `ingress: - from: - podSelector: {matchLabels: {role: frontend}}  ports: - port: 80`.",
      "NetworkPolicies add up: a single rule allowing the traffic is enough."],
  [("default-deny: every Pod, Ingress", "podSelector: {} selects every Pod; policyTypes [Ingress] without an ingress rule = block everything."),
   ("allow-frontend targets app=api", "The policy applies to the Pods selected by podSelector."),
   ("allow-frontend: from role=frontend, port 80", "ingress[].from[].podSelector and ingress[].ports[].port."),
   ("A role=frontend Pod reaches api", "Allowed traffic must go through."),
   ("Another Pod is blocked", "Without the role=frontend label, default-deny applies.")])

E("d5-07", "Egress NetworkPolicy", """
In namespace `d5-07`, create NetworkPolicy `client-egress` applying to Pods `app=client` and letting
them out **only** to:

- Pods `app=db` of namespace `d5-07-db`, TCP port `80`
- the cluster DNS (port `53`, UDP and TCP)

Any other outgoing traffic from those Pods (for example to `web.d5-07`) must be blocked.
""", ["Every namespace carries the automatic label `kubernetes.io/metadata.name=<name>`.",
      "In `to:`, one item with `namespaceSelector` AND `podSelector` = both conditions at once.",
      "Add a second egress rule: `ports: [{protocol: UDP, port: 53}, {protocol: TCP, port: 53}]` without `to` (anywhere)."],
  [("client-egress targets app=client, type Egress", "policyTypes: [Egress] and podSelector app=client."),
   ("Destination: namespace d5-07-db AND Pods app=db", "namespaceSelector (kubernetes.io/metadata.name: d5-07-db) and podSelector in the SAME to item (AND), not two items (OR)."),
   ("DNS allowed (port 53)", "Without DNS, the name db.d5-07-db no longer resolves: egress to 53/UDP and 53/TCP must be allowed."),
   ("app=client reaches db.d5-07-db", "DNS + the db destination must be allowed."),
   ("app=client cannot reach web.d5-07", "Once Egress is in policyTypes, anything not listed is blocked.")])

E("d5-08", "Broken Ingress", """
In namespace `d5-08`, Ingress `blog` serves nothing: a request for host `blog.lab.local` through the
cluster's Ingress controller must return `blog ok`.
Find and fix the mistakes **of the Ingress**.
""", ["`kubectl get ingressclass`: which classes exist?",
      "`kubectl -n d5-08 describe ingress blog`: look at the backend and its port, then `kubectl -n d5-08 get svc blog`.",
      "`kubectl -n d5-08 edit ingress blog`"],
  [("Existing class (traefik)", "There is no nginx IngressClass in this cluster: no controller picks the Ingress up (no ADDRESS)."),
   ("Service port: 80", "The backend targets the SERVICE port (80), not 8080."),
   ("blog.lab.local returns « blog ok »", "Right class + right port: Traefik routes the request.")])

E("d5-09", "Exam-style: publish a protected API", """
*Exam-style task — 9 minutes.* Context `ckad-a`, namespace `d5-09`.

Deployment `catalog` (container port 5678) is not exposed.

1. ClusterIP Service `catalog`, port `8080` to `5678`.
2. Ingress `catalog` (class `traefik`), host `catalog.lab.local`, path `/catalog` (Prefix) to that
   Service.
3. NetworkPolicy `catalog-from-ingress`: Pods `app=catalog` accept incoming traffic **only** from
   namespace `traefik`, port 5678.
""", ["Three objects, three commands: `expose`, `create ingress`, then a NetworkPolicy YAML.",
      "The NetworkPolicy filters at Pod level: the port is the container's (5678), not the Service's.",
      "Namespace `traefik` carries the label `kubernetes.io/metadata.name=traefik`."],
  [("Service catalog 8080 → 5678", "kubectl expose deploy catalog --port=8080 --target-port=5678."),
   ("Ingress: host and path", "--rule='catalog.lab.local/catalog*=catalog:8080'."),
   ("Through the Ingress: catalog ok", "Traffic from Traefik must go through (namespaceSelector traefik)."),
   ("NetworkPolicy: from namespace traefik", "namespaceSelector: {matchLabels: {kubernetes.io/metadata.name: traefik}}."),
   ("Direct access to the Service blocked", "Only Traefik may reach the catalog Pods.")])

# ------------------------------------------------------------------ scenarios
E("s1-jour1", "Shop, day 1: deploy v1", """
**Running scenario, day 1.** Context `ckad-a`, namespace `boutique-j1`.
Deploy v1 of the shop (diagram in `app/boutique/README.md`):

| Component | Deployment | Image and arguments | Replicas | Service |
|---|---|---|---|---|
| data | `redis` | `redis:7.4-alpine` | 1 | `redis`, port 6379 |
| API | `api` | `hashicorp/http-echo:1.0.0`, argument `-text=api v1` (listens on 5678) | 2 | `api`, port **80** to 5678 |
| web | `front` | `nginx:1.27-alpine` | 2 | `front`, port 80 |

Every Deployment carries the label `app=<name>`. Check from a Pod that `http://api` answers `api v1`.
""", ["`kubectl create deployment … --replicas=N` then `kubectl expose deploy … --port=… --target-port=…`: 6 commands in total.",
      "For the http-echo argument: `kubectl create deployment api --image=hashicorp/http-echo:1.0.0 --replicas=2 -- /http-echo -text='api v1'`.",
      "Test: `kubectl -n boutique-j1 run t --rm -i --image=busybox:1.37 --restart=Never -- wget -qO- http://api`."],
  [("Deployment redis: 1 replica(s) ready", "Create Deployment redis with 1 replica(s) and wait until it is ready."),
   ("Deployment api: 2 replica(s) ready", "Create Deployment api with 2 replica(s) and wait until it is ready."),
   ("Deployment front: 2 replica(s) ready", "Create Deployment front with 2 replica(s) and wait until it is ready."),
   ("Service redis 6379", "kubectl expose deploy redis --port=6379."),
   ("Service api: 80 → 5678", "The Service publishes port 80, the container listens on 5678."),
   ("http://api answers « api v1 »", "Selector and ports of Service api."),
   ("http://front answers (nginx)", "Service front, port 80.")])

E("s2-jour2", "Shop, day 2: configuration and scaling", """
**Running scenario, day 2.** Context `ckad-a`, namespace `boutique-j2` (v1 runs there).

1. ConfigMap `front-html`, key `index.html` = `Boutique jour 2`, mounted in `front` on
   `/usr/share/nginx/html`.
2. Secret `redis-auth`, key `password` = `r3d1s-pass`; the API receives variable `REDIS_PASSWORD`
   from that Secret.
3. Container `api`: requests `50m` / `32Mi`, limits `100m` / `64Mi`.
4. Scale the API to **3 replicas**.
""", ["Useful imperative commands: `create configmap`, `create secret generic`, `set env --from=secret/…`, `set resources`, `scale`.",
      "`kubectl -n boutique-j2 set env deploy/api --from=secret/redis-auth --prefix=REDIS_` creates REDIS_PASSWORD.",
      "The volume is mounted with `kubectl edit deploy front` (there is no `kubectl set volume`: go through the YAML)."],
  [("front serves « Boutique jour 2 »", "configMap volume front-html mounted on /usr/share/nginx/html of container front."),
   ("REDIS_PASSWORD from redis-auth", "env.valueFrom.secretKeyRef in container api."),
   ("Secret: password", "kubectl create secret generic redis-auth --from-literal=password=r3d1s-pass."),
   ("Resources of api", "kubectl set resources deploy api --requests=cpu=50m,memory=32Mi --limits=cpu=100m,memory=64Mi."),
   ("api: 3 replicas ready and updated", "kubectl scale deploy api --replicas=3.")])

E("s3-jour3", "Shop, day 3: incident and rollback", """
**Running scenario, day 3.** Context `ckad-a`, namespace `boutique-j3`.

The team just deployed **v2** of the API. The new Pods do not start.

1. Write into `~/ckad/s3-jour3/incident.txt` the **status** shown by the new Pods (STATUS column of
   `kubectl get pods`) and, on a second line, the cause found in their logs.
2. Go back to the **v1 stable** revision.
3. The API must answer `api v1` with 3 ready replicas.
""", ["`kubectl -n boutique-j3 get pods -l app=api` then `kubectl -n boutique-j3 logs <failing-pod>`.",
      "`kubectl -n boutique-j3 rollout history deploy/api`: each revision's cause is shown.",
      "`kubectl -n boutique-j3 rollout undo deploy/api`"],
  [("incident.txt: status recorded", "kubectl get pods shows Error then CrashLoopBackOff (the kubelet spaces restarts)."),
   ("incident.txt: cause recorded", "kubectl logs <pod> (or --previous) prints: flag provided but not defined: -timeout (unknown option of v2)."),
   ("Revision v1 restored", "kubectl rollout undo deploy/api (or --to-revision=N, see rollout history)."),
   ("3 replicas ready and updated", "After the rollback, no v2 Pod is left."),
   ("The API answers api v1", "Service api routes to the v1 Pods.")])

E("s4-jour4", "Shop, day 4: network isolation and Ingress", """
**Running scenario, day 4.** Context `ckad-a`, namespace `boutique-j4`.

1. NetworkPolicy `default-deny`: all **incoming** traffic denied in the namespace.
2. NetworkPolicy `front-to-api`: Pods `app=front` may reach `app=api` (port 5678).
3. NetworkPolicy `api-to-redis`: Pods `app=api` may reach `app=redis` (port 6379).
4. NetworkPolicy `ingress-to-front`: namespace `traefik` may reach `app=front` (port 80).
5. Ingress `boutique` (class `traefik`), host `boutique.lab.local`, `/` to `front:80`.

The front must **not** be able to reach Redis directly; the API must.
""", ["Copy the example NetworkPolicy from the docs and adapt it four times (one per rule).",
      "A NetworkPolicy sits on the **destination** Pods (`podSelector`) and lists the allowed sources (`from`).",
      "`kubectl -n boutique-j4 create ingress boutique --class=traefik --rule='boutique.lab.local/*=front:80'`"],
  [("default-deny", "podSelector: {} + policyTypes: [Ingress], without a rule."),
   ("front-to-api", "The policy sits on the DESTINATION (api) and allows the source (front)."),
   ("api-to-redis", "Destination redis, source api, port 6379."),
   ("Through the Ingress: the shop answers", "Ingress boutique AND NetworkPolicy ingress-to-front (namespaceSelector traefik)."),
   ("front reaches the API", "front-to-api must allow the container port (5678), not the Service's."),
   ("api reaches Redis (PING → PONG)", "api-to-redis must allow app=api Pods to app=redis, port 6379 (Redis is not an HTTP service: tested over TCP)."),
   ("front does not reach Redis", "Only api-to-redis opens Redis, and only to app=api Pods.")])

E("s5-pannes", "Three failures to repair", """
**Failure scenario.** Context `ckad-a`, namespace `pannes`. Three components are broken.
Diagnose each with `get`, `describe`, `events` and `logs`, then repair:

1. Deployment `orders` does not start: it must read `DB_HOST` from ConfigMap `orders-config` (fix
   **the ConfigMap**, not the Deployment);
2. Service `payments` does not answer: `http://payments.pannes` must answer `payments ok`;
3. Pod `uploader` stays `Pending`: its PVC `uploads` (50Mi) must use the StorageClass that exists in
   the cluster.
""", ["`kubectl -n pannes get pods`: each status (CreateContainerConfigError, Pending) points the diagnosis.",
      "`kubectl -n pannes describe pod -l app=orders` and `kubectl -n pannes describe pvc uploads`: read the Events.",
      "For the PVC: `kubectl -n pannes get pvc uploads -o yaml > pvc.yaml`, change the class to `standard`, then delete and recreate PVC and Pod."],
  [("orders ready", "CreateContainerConfigError: key DB_HOST is missing from orders-config (it is named DBHOST)."),
   ("orders-config contains DB_HOST", "The task asks to fix the ConfigMap."),
   ("payments answers", "The Service selector (app=payment) does not match the Pods (app=payments): no Endpoint."),
   ("PVC uploads Bound", "StorageClass fast does not exist (kubectl get storageclass). storageClassName is immutable: recreate the PVC."),
   ("uploader Running", "The Pod waits for its PVC; recreate it if it stays stuck.")])

E("s6-panne-rbac", "Forbidden: repair a ServiceAccount's permissions", """
**Failure scenario.** Context `ckad-a`, namespace `rapports`.

ServiceAccount `reporter` builds a report on the namespace's Pods and ConfigMaps, but it fails: the
errors are in `~/ckad/s6-panne-rbac/forbidden.log`.

Give it **the minimum** permissions: read (`get`, `list`) the Pods and ConfigMaps of namespace
`rapports`. Role `reporter`, RoleBinding `reporter`.
""", ["Read `forbidden.log`: it gives the denied verb, resource and namespace.",
      "`kubectl -n rapports create role reporter --verb=get,list --resource=pods,configmaps`",
      "`kubectl -n rapports create rolebinding reporter --role=reporter --serviceaccount=rapports:reporter`"],
  [("list pods", "forbidden.log: cannot list resource \"pods\" …: a Role and its RoleBinding are missing."),
   ("list configmaps", "The Role must cover pods AND configmaps."),
   ("No reading of Secrets", "Least privilege."),
   ("No deletion", "Read only: get, list."),
   ("Role and RoleBinding named reporter", "RoleBinding reporter references Role reporter.")])
