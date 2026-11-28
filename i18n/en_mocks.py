"""English content of the mock exams: task templates (same parameters as the French generator) and plan.

Each template returns {body, hints[3], checks[(title, why)]} with checks in check.sh runtime order.
"""
import re


def T(s, **kw):
    return re.sub(r"@([a-z_0-9]+)@", lambda m: str(kw[m.group(1)]), s)


def sidecar(ns, ctx, pod, path, word):
    return dict(body=T("""
In namespace `@ns@`, create Pod `@pod@` with a shared `emptyDir` volume mounted on `@path@`:

- container `writer` (`busybox:1.37`):
  `sh -c 'while true; do echo "@word@ $(date)" >> @path@/out.log; sleep 2; done'`
- **native sidecar** `reader` (`busybox:1.37`): `sh -c 'tail -F @path@/out.log'`
""", ns=ns, pod=pod, path=path, word=word),
        hints=["The sidecar goes under `initContainers` with `restartPolicy: Always`.",
               T("Volume: `volumes: [{name: shared, emptyDir: {}}]`, mounted on `@path@` in both containers.", path=path),
               T("Check: `kubectl -n @ns@ logs @pod@ -c reader`.", ns=ns, pod=pod)],
        checks=[("reader is a native sidecar", "Native sidecar: initContainers + restartPolicy: Always."),
                ("Pod Running", "The Pod must run."),
                (T("reader logs show « @word@ »", word=word), T("Same volume, same path @path@ in both containers.", path=path))])


def init_pod(ns, ctx, pod, text):
    return dict(body=T("""
In namespace `@ns@`, create Pod `@pod@`: an init container `seed` (`busybox:1.37`) writes `@text@`
into `/seed/index.html`; container `web` (`nginx:1.27-alpine`) serves that file (same `emptyDir`
volume mounted on `/usr/share/nginx/html`).
""", ns=ns, pod=pod, text=text),
        hints=["One `emptyDir` volume, two different mount points.",
               T("Init command: `sh -c \"echo '@text@' > /seed/index.html\"`.", text=text),
               "Test: a busybox Pod + `wget -qO- http://<IP>`."],
        checks=[("Init container seed", "initContainers[0].name = seed."),
                ("Pod ready", "The Pod must run."),
                (T("The Pod serves « @text@ »", text=text), "The init writes into the volume nginx serves.")])


def job(ns, ctx, name, completions, parallelism, word):
    return dict(body=T("""
In namespace `@ns@`, create Job `@name@` (`busybox:1.37`, `sh -c 'echo @word@'`) which must succeed
**@completions@ times**, with at most **@parallelism@** Pods in parallel and `backoffLimit: 1`. It
must complete.
""", ns=ns, name=name, completions=completions, parallelism=parallelism, word=word),
        hints=["`kubectl create job … --dry-run=client -o yaml -- sh -c '…'` then edit.",
               "`completions`, `parallelism` and `backoffLimit` are under `spec` (not under `template`).",
               "`kubectl wait --for=condition=Complete job/<name>`"],
        checks=[("completions / parallelism / backoffLimit", "Three fields under the Job's spec."),
                (T("@completions@ successes", completions=completions), "The Job must finish."),
                (T("Logs say « @word@ »", word=word), T("Requested command: echo @word@.", word=word))])


def cronjob(ns, ctx, name, schedule, policy, keep):
    return dict(body=T("""
In namespace `@ns@`, create CronJob `@name@`: schedule `@schedule@`, image `busybox:1.37`, command
`sh -c 'date'`, `concurrencyPolicy: @policy@`, **@keep@** successful Jobs kept. Then trigger a manual
run **right now** as a Job named `@name@-manual`.
""", ns=ns, name=name, schedule=schedule, policy=policy, keep=keep),
        hints=["`kubectl create cronjob --schedule=… --image=… -- sh -c 'date'`",
               "Fields to add: `concurrencyPolicy`, `successfulJobsHistoryLimit`.",
               "`kubectl create job <name> --from=cronjob/<cronjob>`"],
        checks=[("Schedule", "spec.schedule."),
                ("Policy and history", "concurrencyPolicy and successfulJobsHistoryLimit under the CronJob's spec."),
                (T("Job @name@-manual created from the CronJob", name=name), T("kubectl create job @name@-manual --from=cronjob/@name@.", name=name))])


def pvc_pod(ns, ctx, pvc, size, pod, mount, word):
    return dict(body=T("""
In namespace `@ns@`: PVC `@pvc@` of `@size@` (`ReadWriteOnce`, StorageClass `standard`), then Pod
`@pod@` (`busybox:1.37`) mounting it on `@mount@` and running
`sh -c 'echo @word@ > @mount@/data.txt && sleep 3600'`.
""", ns=ns, pvc=pvc, size=size, pod=pod, mount=mount, word=word),
        hints=["Copy the PVC example from the \"Persistent Volumes\" docs.",
               "In the Pod: `volumes: [{name: data, persistentVolumeClaim: {claimName: …}}]`.",
               "A `Pending` PVC without a Pod is normal with `WaitForFirstConsumer`."],
        checks=[(T("PVC @pvc@ Bound, @size@", pvc=pvc, size=size), "WaitForFirstConsumer: Bound as soon as a Pod uses it."),
                ("The Pod mounts the PVC", "volumes[].persistentVolumeClaim.claimName."),
                ("File written", T("Mounted on @mount@.", mount=mount))])


def image_build(uid, tag, label_val, port):
    return dict(body=T("""
Directory `~/ckad/@uid@/app` contains a `Dockerfile`.
Add the label `team=@label_val@` and `EXPOSE @port@` to it, build image `@tag@`, then export it as
`~/ckad/@uid@/image.tar`.
""", uid=uid, tag=tag, label_val=label_val, port=port),
        hints=["Two lines: `LABEL` and `EXPOSE`.", T("`docker build -t @tag@ ~/ckad/@uid@/app`", tag=tag, uid=uid),
               T("`docker save -o ~/ckad/@uid@/image.tar @tag@`", tag=tag, uid=uid)],
        checks=[(T("Label team=@label_val@", label_val=label_val), T("LABEL team=@label_val@ in the Dockerfile, then docker build -t @tag@.", label_val=label_val, tag=tag)),
                (T("Port @port@ exposed", port=port), T("EXPOSE @port@.", port=port)),
                (T("Archive image.tar with tag @tag@", tag=tag), T("docker save -o ~/ckad/@uid@/image.tar @tag@.", uid=uid, tag=tag))])


def daemonset(ns, ctx, name):
    return dict(body=T("""
In namespace `@ns@`, create DaemonSet `@name@` (`busybox:1.37`, `sh -c 'sleep 3600'`) placing a Pod
on **every** node of the cluster, control plane included.
""", ns=ns, name=name),
        hints=["Generate a Deployment, change to `kind: DaemonSet`, remove `replicas` and `strategy`.",
               "Toleration: `key: node-role.kubernetes.io/control-plane, operator: Exists, effect: NoSchedule`.",
               "`kubectl rollout status ds/<name>`"],
        checks=[("One ready Pod per node", "Toleration node-role.kubernetes.io/control-plane:NoSchedule for the control plane.")])


def pod_cmd(ns, ctx, pod, image, labels, port, file_out):
    lab = ",".join(f"{k}={v}" for k, v in labels.items())
    k1, v1 = list(labels.items())[0]
    return dict(body=T("""
In namespace `@ns@`, create Pod `@pod@` (image `@image@`, labels `@lab@`, port `@port@`) and save its
YAML manifest into `@file_out@`.
""", ns=ns, pod=pod, image=image, lab=lab, port=port, file_out=file_out),
        hints=["`kubectl run --dry-run=client -o yaml` generates the manifest.", "Save it, then `kubectl apply -f`.", "Labels: `--labels=a=b,c=d`."],
        checks=[(T("Pod @pod@ ready, image @image@", pod=pod, image=image), T("kubectl run @pod@ --image=@image@ --labels=@lab@ --port=@port@.", pod=pod, image=image, lab=lab, port=port)),
                (T("Label @k1@=@v1@", k1=k1, v1=v1), T("--labels=@lab@.", lab=lab)),
                ("Manifest saved", "kubectl run … --dry-run=client -o yaml > file, or kubectl get pod -o yaml > file.")])


def rolling(ns, ctx, dep, cause):
    return dict(body=T("""
In namespace `@ns@`, update Deployment `@dep@` to `nginx:1.28-alpine` (container `nginx`) with the
cause `@cause@` visible in `kubectl rollout history`. Then scale it to **4 replicas**.
""", ns=ns, dep=dep, cause=cause),
        hints=["`kubectl set image deploy/<d> nginx=nginx:1.28-alpine`", "`kubectl annotate … kubernetes.io/change-cause=…`", "`kubectl scale deploy … --replicas=4`"],
        checks=[("Image 1.28 and 4 replicas ready", "kubectl set image then kubectl scale."),
                ("Revision cause", T("kubectl annotate deploy @dep@ kubernetes.io/change-cause='@cause@'.", dep=dep, cause=cause))])


def rollback(ns, ctx, dep, bad):
    return dict(body=T("""
In namespace `@ns@`, the last update of Deployment `@dep@` failed.
Go back to the revision that worked and write the **number of that revision** (before the rollback)
into `~/ckad/@ns@/revision.txt`.
""", ns=ns, dep=dep),
        hints=["`kubectl rollout history deploy/<d>`", "`kubectl rollout undo deploy/<d> --to-revision=N`", "The expected number is the one BEFORE the rollback."],
        checks=[("Image back to redis:7.4-alpine, 2 replicas ready", T("kubectl rollout undo deploy/@dep@.", dep=dep)),
                ("Revision recorded", "rollout history: the revision that worked is number 1.")])


def helm_upgrade(uid, ns, ctx, release, replicas, msg):
    return dict(body=T("""
Helm release `@release@` (chart `~/ckad/@uid@/webapp`) runs in namespace `@ns@`.
Upgrade it: `replicaCount=@replicas@` and `message=@msg@`. Then write the output of
`helm history @release@` into `~/ckad/@uid@/history.txt`.
""", release=release, uid=uid, ns=ns, replicas=replicas, msg=msg),
        hints=["`helm -n <ns> list`", "`helm upgrade <release> <chart> --set a=b --set c=d`", "`helm history <release>`"],
        checks=[("Revision 2 deployed", T("helm upgrade @release@ <chart> --set …", release=release)),
                (T("@replicas@ replicas ready", replicas=replicas), T("--set replicaCount=@replicas@.", replicas=replicas)),
                ("MESSAGE", T("--set message=@msg@.", msg=msg)),
                ("history.txt", T("helm history @release@ > ~/ckad/@uid@/history.txt.", release=release, uid=uid))])


def canary(ns, ctx, app, stable, canary_n):
    total = stable + canary_n
    return dict(body=T("""
In namespace `@ns@`, Service `@app@` serves @total@ Pods `@app@-stable`. Deploy a canary
`@app@-canary` (`hashicorp/http-echo:1.0.0`, `-text=@app@ v2`, port 5678, labels `app=@app@`,
`track=canary`) so that **@canary_n@ Pod(s) out of @total@** behind the Service run v2. The total
number of Pods stays @total@.
""", ns=ns, app=app, total=total, canary_n=canary_n),
        hints=["The Service only selects `app`: the canary must carry that label.", "Create the canary, then scale the stable one down.", "Check the EndpointSlices."],
        checks=[(T("Canary: @canary_n@ ready", canary_n=canary_n), T("The canary carries app=@app@.", app=app)),
                (T("Stable scaled down to @stable@", stable=stable), T("@stable@ + @canary_n@ = @total@.", stable=stable, canary_n=canary_n, total=total)),
                (T("@total@ ready Endpoints", total=total), T("The Service sees every app=@app@ Pod.", app=app))])


def bluegreen(ns, ctx, app):
    return dict(body=T("""
In namespace `@ns@`, the blue and green versions of `@app@` run; Service `@app@` sends everything to
blue. **Switch** the Service to green, then scale `@app@-blue` to 0 replicas (without deleting it).
""", ns=ns, app=app),
        hints=["`kubectl patch svc … -p '{\"spec\":{\"selector\":{…}}}'`", "The patched selector must keep `app` and change `color`.", "`kubectl scale deploy … --replicas=0`"],
        checks=[("Selector color=green", "Change the Service selector."),
                (T("@app@-blue at 0, kept", app=app), "kubectl scale --replicas=0 keeps the Deployment."),
                ("The Service answers green", "The Service must target the green Pods.")])


def kustomize(uid, ns, ctx, prefix, replicas, label):
    return dict(body=T("""
Kustomize base: `~/ckad/@uid@/base`. Create the overlay `~/ckad/@uid@/overlay` that deploys into
`@ns@`, prefixes names with `@prefix@`, sets **@replicas@ replicas**, adds the label `tier=@label@`,
and replaces the image with `nginx:1.28-alpine`. Apply it.
""", uid=uid, ns=ns, prefix=prefix, replicas=replicas, label=label),
        hints=["`resources: [../base]`", "`images: - name: nginx  newTag: 1.28-alpine`", "`kubectl apply -k ~/ckad/…/overlay`"],
        checks=[(T("@prefix@shop: @replicas@ ready, image 1.28", prefix=prefix, replicas=replicas), "namePrefix, replicas and images in the overlay's kustomization.yaml."),
                (T("Label tier=@label@", label=label), T("labels: - pairs: {tier: @label@}.", label=label))])


def strategy(ns, ctx, dep):
    return dict(body=T("""
In namespace `@ns@`, configure Deployment `@dep@` so that every update **stops all old Pods before**
creating the new ones (`Recreate` strategy). Then update it to `nginx:1.28-alpine`.
""", ns=ns, dep=dep),
        hints=["`kubectl edit deploy …`: `strategy: {type: Recreate}`.", "Remove the `rollingUpdate` block at the same time.", "Then `kubectl set image`."],
        checks=[("Strategy Recreate", "Recreate: also remove strategy.rollingUpdate, otherwise the API refuses."),
                ("Image 1.28, 2 ready", "kubectl set image.")])


def logs_file(ns, ctx, pod, key):
    return dict(body=T("""
In namespace `@ns@`, copy **the whole line** containing `ERROR` from the logs of Pod `@pod@` into
`~/ckad/@ns@/error.txt`.
""", ns=ns, pod=pod),
        hints=["`kubectl logs`", "`| grep ERROR`", T("`> ~/ckad/@ns@/error.txt`", ns=ns)],
        checks=[("ERROR line copied", T("kubectl logs @pod@ | grep ERROR > file.", pod=pod))])


def crash_fix(ns, ctx, dep):
    return dict(body=T("""
In namespace `@ns@`, Deployment `@dep@` is in `CrashLoopBackOff`. Read its command: it waits for a
file. Fix the Deployment **without changing its command**: mount a ConfigMap `@dep@-config` (key
`ready`, value `yes`) on `/config`.
""", ns=ns, dep=dep),
        hints=["`kubectl describe pod`: Exit Code 3.", "`kubectl create configmap … --from-literal=ready=yes`", "Add `volumes` and `volumeMounts` to the template."],
        checks=[("1 replica available", T("Exit code 3: /config/ready is missing. configMap volume @dep@-config mounted on /config.", dep=dep)),
                ("Command unchanged", "The task forbids changing the command."),
                ("ConfigMap mounted", "volumes[].configMap.name.")])


def probes(ns, ctx, dep, path):
    return dict(body=T("""
In namespace `@ns@`, add to the container of Deployment `@dep@`:

- an HTTP **readiness** probe `GET @path@` port 80, every 5 s;
- a TCP **liveness** probe port 80, after 10 s, every 15 s.
""", ns=ns, dep=dep, path=path),
        hints=["`kubectl edit deploy …`", "Two blocks at container level: `readinessProbe` and `livenessProbe`.", "Ready-made examples in the docs \"Configure Liveness, Readiness and Startup Probes\"."],
        checks=[(T("Readiness GET @path@:80, 5 s", path=path), "readinessProbe.httpGet + periodSeconds."),
                ("Liveness TCP 80, 10 s / 15 s", "livenessProbe.tcpSocket + initialDelaySeconds + periodSeconds."),
                ("2 replicas ready and updated", T("@path@ must exist in nginx (/ works).", path=path))])


def imagepull(ns, ctx, dep, bad, good):
    return dict(body=T("""
In namespace `@ns@`, the Pods of Deployment `@dep@` do not start. Write their **status** (STATUS
column) into `~/ckad/@ns@/status.txt`, then fix the image to `@good@`.
""", ns=ns, dep=dep, good=good),
        hints=["`kubectl get pods`", "`kubectl describe pod`: Events.", "`kubectl set image deploy/<d> <container>=<image>`"],
        checks=[("Status recorded", "kubectl get pods: ErrImagePull then ImagePullBackOff."),
                (T("Image fixed, 2 ready", good=good), "kubectl set image.")])


def deprecated_ing(uid, ns, ctx, name, host):
    return dict(body=T("""
`~/ckad/@uid@/ingress.yaml` uses a removed API. Convert **the file** to `networking.k8s.io/v1`
(pathType `Prefix`), then apply it: `@host@` must answer `web ok`.
""", uid=uid, host=host),
        hints=["`kubectl explain ingress --api-version=networking.k8s.io/v1`", "v1 backend: `service: {name: web, port: {number: 80}}`.", "Do not forget `pathType: Prefix`."],
        checks=[("File in networking.k8s.io/v1", "v1beta1 removed in 1.22. In v1: pathType mandatory, backend.service.name and backend.service.port.number."),
                (T("@host@ answers « web ok »", host=host), "The converted Ingress must be applied.")])


def pending_fix(ns, ctx, pod):
    return dict(body=T("""
In namespace `@ns@`, Pod `@pod@` stays `Pending`. Find why in its events, then get it running
**without changing the nodes** (same name, same image).
""", ns=ns, pod=pod),
        hints=["`kubectl describe pod`: Events.", "Look at `spec.nodeSelector`.", "`kubectl get pod -o yaml > f.yaml`, remove the nodeSelector, `kubectl replace --force -f f.yaml`."],
        checks=[("Pod Running", "FailedScheduling: no node has the label disk=ssd required by nodeSelector. Recreate the Pod without that nodeSelector."),
                ("Nodes unchanged (no disk label)", "The task forbids labelling the nodes.")])


def cm_secret_env(ns, ctx, pod, cm, cmval, secret, secval):
    return dict(body=T("""
In namespace `@ns@`: ConfigMap `@cm@` (`LEVEL=@cmval@`) and Secret `@secret@` (`TOKEN=@secval@`).
Pod `@pod@` (`busybox:1.37`, `sh -c 'sleep 3600'`) receiving variable `LOG_LEVEL` from `@cm@` (key
`LEVEL`) and `API_TOKEN` from `@secret@` (key `TOKEN`).
""", ns=ns, pod=pod, cm=cm, cmval=cmval, secret=secret, secval=secval),
        hints=["`create configmap --from-literal`, `create secret generic --from-literal`.", "`env: - name: LOG_LEVEL  valueFrom: configMapKeyRef: {name, key}`", "Same with `secretKeyRef`."],
        checks=[("LOG_LEVEL in the container", "env.valueFrom.configMapKeyRef."),
                ("API_TOKEN in the container", "env.valueFrom.secretKeyRef."),
                ("API_TOKEN comes from the Secret", "No plain value in the Pod.")])


def secret_volume(ns, ctx, dep, secret):
    return dict(body=T("""
In namespace `@ns@`, create Secret `@secret@` from two literals `user=app` and `pass=Zx9-k2`, then
mount it **as a volume**, read-only, on `/etc/creds` in the existing Deployment `@dep@`.
""", ns=ns, dep=dep, secret=secret),
        hints=["`kubectl create secret generic … --from-literal=…`", "`volumes: [{name: creds, secret: {secretName: …}}]`", "`volumeMounts: [{name: creds, mountPath: /etc/creds, readOnly: true}]`"],
        checks=[("File /etc/creds/pass", "A secret volume creates one file per key."),
                ("Read-only mount", "volumeMounts[].readOnly: true.")])


def secctx(ns, ctx, pod, uid):
    return dict(body=T("""
In namespace `@ns@`, create Pod `@pod@` (`busybox:1.37`, `sh -c 'sleep 3600'`) running as user
`@uid@`, **refusing to start as root** (`runAsNonRoot`), forbidding privilege escalation and adding
**only** the `NET_BIND_SERVICE` capability after dropping all the others.
""", ns=ns, pod=pod, uid=uid),
        hints=["Two possible `securityContext` levels (Pod and container).", "`capabilities` exists only at container level.", "`runAsNonRoot: true` requires a non-zero uid."],
        checks=[(T("uid @uid@ and runAsNonRoot", uid=uid), "runAsUser and runAsNonRoot (Pod or container level)."),
                ("drop ALL, add NET_BIND_SERVICE", "capabilities: {drop: [ALL], add: [NET_BIND_SERVICE]} (container level only)."),
                ("No escalation", "allowPrivilegeEscalation: false."),
                (T("id -u = @uid@", uid=uid), "The Pod must run.")])


def rbac(ns, ctx, sa, verbs, resources, deny):
    r0 = resources.split(",")[0]
    checks = [(f"{sa} can {v} {r0}", f"Role {sa}-role + RoleBinding {sa}-binding.") for v in verbs.split(",")]
    checks.append((f"{sa} cannot {deny}", "Least privilege."))
    return dict(body=T("""
In namespace `@ns@`, create ServiceAccount `@sa@`, Role `@sa@-role` (verbs `@verbs@` on
`@resources@`) and RoleBinding `@sa@-binding` tying them together.
""", ns=ns, sa=sa, verbs=verbs, resources=resources),
        hints=["`kubectl create serviceaccount`", "`kubectl create role … --verb=… --resource=…`", "`kubectl create rolebinding … --role=… --serviceaccount=<ns>:<sa>`"],
        checks=checks)


def quota(ns, ctx, pods, cpu, mem):
    return dict(body=T("""
In namespace `@ns@`, create ResourceQuota `team-quota`: at most `@pods@` Pods, `requests.cpu=@cpu@`,
`requests.memory=@mem@`. Then create Pod `probe` (`nginx:1.27-alpine`) with requests `100m` / `64Mi`:
it must be accepted.
""", ns=ns, pods=pods, cpu=cpu, mem=mem),
        hints=["`kubectl create quota --hard=…`", "`kubectl run probe … --dry-run=client -o yaml` then add `resources.requests`.", "There is no `kubectl set resources` for a bare Pod: go through the YAML."],
        checks=[("Quota", T("kubectl create quota team-quota --hard=pods=@pods@,requests.cpu=@cpu@,requests.memory=@mem@.", pods=pods, cpu=cpu, mem=mem)),
                ("Pod probe Running, requests 100m", "With a requests.* quota, a Pod without requests is rejected."),
                ("Quota used", "The Pod must count in the quota.")])


def resources_deploy(ns, ctx, dep, rc, rm, lc, lm):
    return dict(body=T("""
In namespace `@ns@`, give Deployment `@dep@` requests `@rc@` / `@rm@` and limits `@lc@` / `@lm@`.
Write the QoS class of its Pods into `~/ckad/@ns@/qos.txt`.
""", ns=ns, dep=dep, rc=rc, rm=rm, lc=lc, lm=lm),
        hints=["`kubectl set resources --help`", "QoS: `kubectl get pod … -o jsonpath='{.status.qosClass}'`.", "Wait for the end of the rolling update before reading the QoS."],
        checks=[("Resources", T("kubectl set resources deploy @dep@ --requests=… --limits=…", dep=dep)),
                ("QoS recorded", "requests = limits: Guaranteed; otherwise Burstable.")])


def sa_pod(ns, ctx, sa, dep):
    return dict(body=T("""
In namespace `@ns@`, create ServiceAccount `@sa@` and make the existing Deployment `@dep@` run under
that ServiceAccount.
""", ns=ns, sa=sa, dep=dep),
        hints=["`kubectl create serviceaccount`", "`kubectl set serviceaccount deploy/<d> <sa>`", "Check with `-o custom-columns`."],
        checks=[(T("Template: serviceAccountName @sa@", sa=sa), T("kubectl set serviceaccount deploy/@dep@ @sa@.", dep=dep, sa=sa)),
                (T("Running Pods under @sa@", sa=sa), "The rolling update replaces the Pods.")])


def crd_obj(ns, ctx, group, kind, plural, name, field, value):
    return dict(body=T("""
A CRD of group `@group@` is installed. In namespace `@ns@`, create an object `@kind@` named `@name@`
with `spec.@field@: @value@`. Write the list of the group's resources
(`kubectl api-resources --api-group=@group@`) into `~/ckad/@ns@/resources.txt`.
""", group=group, ns=ns, kind=kind, name=name, field=field, value=value),
        hints=["`kubectl get crd`", "`kubectl explain <kind>` gives GROUP and VERSION.", "`apiVersion: <group>/<version>`"],
        checks=[(T("@kind@ @name@", kind=kind, name=name), T("apiVersion: @group@/v1alpha1 (version served by the CRD).", group=group)),
                ("resources.txt", T("kubectl api-resources --api-group=@group@ > file.", group=group))])


def expose(ns, ctx, dep, port, target, stype, nodeport=None):
    np_line = f", nodePort `{nodeport}`" if nodeport else ""
    checks = [("Type and ports", T("kubectl expose deploy @dep@ --name=@dep@-svc --type=@stype@ --port=@port@ --target-port=@target@.", dep=dep, stype=stype, port=port, target=target)),
              ("The Service answers", T("Selector app=@dep@, targetPort 5678.", dep=dep))]
    if nodeport:
        checks.append((f"nodePort {nodeport}", "Edit the Service or write the YAML."))
    return dict(body=T("""
In namespace `@ns@`, expose Deployment `@dep@` (container port 5678) through a `@stype@` Service named
`@dep@-svc`: port `@port@`@np_line@.
""", ns=ns, dep=dep, port=port, stype=stype, np_line=np_line),
        hints=["`kubectl expose --help`", "`--target-port=5678`", "nodePort: `--dry-run=client -o yaml`, then add the field." if nodeport else "Check the EndpointSlices."],
        checks=checks)


def ingress(ns, ctx, host, a, b, path_b):
    return dict(body=T("""
In namespace `@ns@`, create Ingress `@a@-ing` (class `traefik`) for host `@host@`: `/` to Service `@a@`
(port 80) and `@path_b@` to Service `@b@` (port 9090), as `pathType: Prefix`.
""", ns=ns, a=a, b=b, host=host, path_b=path_b),
        hints=["`kubectl create ingress --help`", "`--rule='host/path*=service:port'` (the star = Prefix)", "Two `--rule`."],
        checks=[(T("/ → @a@", a=a), T("Rule / to @a@:80.", a=a)),
                (T("@path_b@ → @b@", path_b=path_b, b=b), T("Rule @path_b@ to @b@:9090 (the Service port).", path_b=path_b, b=b)),
                ("Class traefik", "--class=traefik.")])


def netpol(ns, ctx, target, src_label, port):
    return dict(body=T("""
In namespace `@ns@`, create NetworkPolicy `@target@-access`: Pods `app=@target@` accept incoming
traffic **only** from Pods labelled `@src_label@`, on port `@port@`. Everything else is denied for
those Pods.
""", ns=ns, target=target, src_label=src_label, port=port),
        hints=["Copy the example from the \"Network Policies\" docs.", "`podSelector: {matchLabels: {app: …}}` + `policyTypes: [Ingress]`.", "`ingress: - from: - podSelector: …  ports: - port: …`"],
        checks=[(T("podSelector app=@target@, type Ingress", target=target), "The policy sits on the destination."),
                (T("Source @src_label@, port @port@", src_label=src_label, port=port), "ingress[0].from[0].podSelector and ingress[0].ports[0].port."),
                (T("@src_label@ goes through", src_label=src_label), "Allowed traffic must go through."),
                ("Others are blocked", "An Ingress policy selecting a Pod denies everything it does not list.")])


def netpol_ns(ns, ctx, target, other_ns):
    return dict(body=T("""
In namespace `@ns@`, create NetworkPolicy `from-@other_ns@`: Pods `app=@target@` accept incoming
traffic only from Pods **of namespace `@other_ns@`** (any Pod).
""", ns=ns, target=target, other_ns=other_ns),
        hints=["`namespaceSelector` instead of `podSelector` in `from`.", "`kubectl get ns --show-labels`", "`matchLabels: {kubernetes.io/metadata.name: …}`"],
        checks=[(T("namespaceSelector @other_ns@", other_ns=other_ns), T("Automatic label kubernetes.io/metadata.name=@other_ns@.", other_ns=other_ns)),
                (T("From @other_ns@: OK", other_ns=other_ns), T("Namespace @other_ns@ must go through.", other_ns=other_ns)),
                (T("From @ns@: blocked", ns=ns), "Even the local namespace is denied.")])


def svc_fix(ns, ctx, name, text):
    return dict(body=T("""
In namespace `@ns@`, `http://@name@.@ns@` does not answer. Fix **Service** `@name@` so that it
answers `@text@`. Then write the IP addresses of its Endpoints into `~/ckad/@ns@/endpoints.txt`.
""", ns=ns, name=name, text=text),
        hints=["`kubectl get endpointslices`", "Compare the Service selector with the Pod labels; compare targetPort with containerPort.",
               "`kubectl get endpointslices -l kubernetes.io/service-name=… -o jsonpath='{.items[*].endpoints[*].addresses[*]}'`"],
        checks=[("The Service answers", "Two mistakes: tier=backend does not exist on the Pods (tier=api) and targetPort 8080 instead of 5678."),
                ("endpoints.txt contains the Pod IPs", T("kubectl get endpointslices -l kubernetes.io/service-name=@name@ -o wide.", name=name))])


A, B = "ckad-a", "ckad-b"

EXAMS = {
    1: ("Warm-up", "Six tasks, one per domain (two for domain 4), all on `ckad-a`."),
    2: ("Two clusters", "Nine tasks on `ckad-a` and `ckad-b`: check the context before every task."),
    3: ("Exam pace", "Thirteen tasks: you must skip some and come back to them."),
    4: ("Official conditions #1", "Sixteen tasks, two clusters, 2 hours: exam conditions."),
    5: ("Official conditions #2", "Sixteen tasks, two clusters, 2 hours: exam conditions."),
}
RULES = """Rules: terminal only, `vim` or `nano`, and the documentation allowed in the exam
(kubernetes.io/docs, kubernetes.io/blog, helm.sh/docs). Before every task, **switch context**. A task
that resists: move on and come back. The pass mark is 66%. The tasks are original: they are not
official questions."""

PLAN = {
    1: [("Logging sidecar", lambda ns, c: sidecar(ns, c, "audit", "/var/audit", "event")),
        ("Update with a cause", lambda ns, c: rolling(ns, c, "storefront", "nginx 1.28")),
        ("Readiness and liveness probes", lambda ns, c: probes(ns, c, "catalog", "/index.html")),
        ("ConfigMap and Secret as variables", lambda ns, c: cm_secret_env(ns, c, "worker", "worker-cfg", "debug", "worker-sec", "t0k3n-a1")),
        ("Non-root Pod", lambda ns, c: secctx(ns, c, "hardened", 2000)),
        ("Service to repair", lambda ns, c: svc_fix(ns, c, "inventory", "inventory ok"))],
    2: [("CronJob and manual run", lambda ns, c: cronjob(ns, c, "report", "30 1 * * *", "Replace", 5)),
        ("Persistent storage", lambda ns, c: pvc_pod(ns, c, "cache-pvc", "200Mi", "cache", "/cache", "chaud")),
        ("Helm upgrade", lambda ns, c: helm_upgrade("m2-03", ns, c, "blog", 3, "v2")),
        ("25% canary", lambda ns, c: canary(ns, c, "search", 3, 1)),
        ("Extract an error from logs", lambda ns, c: logs_file(ns, c, "ingestor", "BATCH")),
        ("CrashLoopBackOff: missing file", lambda ns, c: crash_fix(ns, c, "billing")),
        ("ServiceAccount permissions", lambda ns, c: rbac(ns, c, "auditor", "get,list,watch", "deployments,pods", "delete deployments")),
        ("ResourceQuota", lambda ns, c: quota(ns, c, 4, "800m", "512Mi")),
        ("Two-path Ingress", lambda ns, c: ingress(ns, c, "m2.lab.local", "home", "docs", "/docs"))],
    3: [("Parallel Job", lambda ns, c: job(ns, c, "resize", 4, 2, "redimensionné")),
        ("Init container", lambda ns, c: init_pod(ns, c, "landing", "bienvenue m3")),
        ("Container image", lambda ns, c: image_build("m3-03", "ckad/m3-app:1.0", "payments", 9000)),
        ("Kustomize overlay", lambda ns, c: kustomize("m3-04", ns, c, "stg-", 2, "staging")),
        ("Blue/green switch", lambda ns, c: bluegreen(ns, c, "checkout")),
        ("Recreate strategy", lambda ns, c: strategy(ns, c, "legacy")),
        ("Image not found", lambda ns, c: imagepull(ns, c, "queue", "redis:7.4-alpine-oups", "redis:7.4-alpine")),
        ("Ingress on a removed API", lambda ns, c: deprecated_ing("m3-08", ns, c, "legacy-web", "legacy.m3.lab.local")),
        ("ServiceAccount of a Deployment", lambda ns, c: sa_pod(ns, c, "metrics-reader", "collector")),
        ("Resources and QoS", lambda ns, c: resources_deploy(ns, c, "api", "100m", "128Mi", "100m", "128Mi")),
        ("Custom resource", lambda ns, c: crd_obj(ns, c, "ops.m3.lab", "Maintenance", "maintenances", "weekly", "window", "dimanche 02h")),
        ("Ingress NetworkPolicy", lambda ns, c: netpol(ns, c, "ledger", "role=accounting", 80)),
        ("NodePort Service", lambda ns, c: expose(ns, c, "gateway", 80, 5678, "NodePort", 30180))],
    4: [("Pod and manifest", lambda ns, c: pod_cmd(ns, c, "edge", "nginx:1.28-alpine", {"tier": "edge", "env": "prod"}, 80, "~/ckad/m4-01/edge.yaml")),
        ("DaemonSet on every node", lambda ns, c: daemonset(ns, c, "log-agent")),
        ("Native sidecar", lambda ns, c: sidecar(ns, c, "trail", "/trail", "trace")),
        ("Rollback", lambda ns, c: rollback(ns, c, "sessions", "redis:9.9-nexistepas")),
        ("Helm upgrade", lambda ns, c: helm_upgrade("m4-05", ns, c, "wiki", 2, "maj")),
        ("20% canary", lambda ns, c: canary(ns, c, "pricing", 4, 1)),
        ("Pending Pod", lambda ns, c: pending_fix(ns, c, "batch")),
        ("Logs", lambda ns, c: logs_file(ns, c, "sync", "SYNC")),
        ("Probes", lambda ns, c: probes(ns, c, "media", "/")),
        ("Secret as a volume", lambda ns, c: secret_volume(ns, c, "mailer", "smtp-creds")),
        ("RBAC", lambda ns, c: rbac(ns, c, "deployer", "get,list,create,update", "deployments", "delete pods")),
        ("SecurityContext", lambda ns, c: secctx(ns, c, "runner", 1500)),
        ("Quota", lambda ns, c: quota(ns, c, 6, "1", "1Gi")),
        ("Ingress", lambda ns, c: ingress(ns, c, "m4.lab.local", "shop", "cart", "/cart")),
        ("NetworkPolicy by namespace", lambda ns, c: netpol_ns(ns, c, "vault", "m4-15-ops")),
        ("Service to repair", lambda ns, c: svc_fix(ns, c, "orders", "orders ok"))],
    5: [("Job with completions", lambda ns, c: job(ns, c, "migrate", 3, 1, "migré")),
        ("PVC", lambda ns, c: pvc_pod(ns, c, "media-pvc", "150Mi", "media", "/media", "photo")),
        ("Init container", lambda ns, c: init_pod(ns, c, "status", "tout va bien")),
        ("Kustomize", lambda ns, c: kustomize("m5-04", ns, c, "prd-", 3, "prod")),
        ("Rolling update", lambda ns, c: rolling(ns, c, "portal", "montée de version")),
        ("Blue/green", lambda ns, c: bluegreen(ns, c, "profile")),
        ("CrashLoopBackOff", lambda ns, c: crash_fix(ns, c, "notifier")),
        ("ImagePullBackOff", lambda ns, c: imagepull(ns, c, "frontend", "nginx:1.27-alpine3", "nginx:1.27-alpine")),
        ("Removed API", lambda ns, c: deprecated_ing("m5-09", ns, c, "old-site", "old.m5.lab.local")),
        ("ConfigMap and Secret", lambda ns, c: cm_secret_env(ns, c, "agent", "agent-cfg", "warn", "agent-sec", "s3cr3t-b2")),
        ("Resources", lambda ns, c: resources_deploy(ns, c, "render", "200m", "256Mi", "500m", "512Mi")),
        ("CRD", lambda ns, c: crd_obj(ns, c, "data.m5.lab", "Pipeline", "pipelines", "nightly-etl", "source", "s3-bucket")),
        ("ServiceAccount", lambda ns, c: sa_pod(ns, c, "uploader", "ingest")),
        ("ClusterIP Service", lambda ns, c: expose(ns, c, "ranking", 8080, 5678, "ClusterIP")),
        ("NetworkPolicy", lambda ns, c: netpol(ns, c, "secrets-api", "access=granted", 80)),
        ("Ingress", lambda ns, c: ingress(ns, c, "m5.lab.local", "front", "api", "/api"))],
}
