---
title: Error log
color: gris
---
# Error log

Each entry was **triggered on purpose** in the `journal` namespace by
`scripts/capture-docs.sh journal`, and its output is real. Entries marked *encountered* are errors
that happened by accident while building the lab.

{{capture:err-overview}}

## E1 · CrashLoopBackOff *(triggered)*

Exercises: `d3-04`, `s3-jour3`.

{{capture:err-crashloop}}

- **In plain words**: the container starts then exits; the kubelet restarts it, spacing the attempts
  (back-off).
- **Cause**: the command exits with a non-zero code (here `exit 1`; 127 = command not found).
- **Diagnosis**: `k describe pod` (Last State, Exit Code), `k logs <pod> --previous`.
- **Fix**: correct the command, the configuration or whatever is missing, then check that `RESTARTS`
  is stable and `READY 1/1`.
- **Avoid it**: try the command with `k run t --rm -it --image=… -- sh`.

## E2 · ImagePullBackOff / ErrImagePull *(triggered)*

Exercises: `d2-04`, `d3-05`.

{{capture:err-imagepull}}

- **Cause**: missing image or tag, private registry without `imagePullSecrets`, typo.
- **Fix**: `k set image deploy/<d> <container>=<image:tag>`.

## E3 · CreateContainerConfigError *(triggered)*

Exercise: `s5-pannes`.

{{capture:err-configerror}}

- **Cause**: a variable references a missing ConfigMap or key (or a missing Secret).
- **Fix**: create the key (or make the reference `optional: true` if intended).

## E4 · Pod Pending: FailedScheduling *(triggered)*

Exercises: `d3-06`, `m4-07`.

{{capture:err-pending}}

- **Cause**: impossible requests (64 CPUs), nodeSelector or affinity without a matching node,
  untolerated taint, unbound PVC.
- **Fix**: correct the Pod spec (`k replace --force -f`).

## E5 · OOMKilled *(triggered)*

{{capture:err-oomkilled}}

- **Cause**: the container exceeds its memory limit (32Mi here); exit code 137.
- **Fix**: raise `limits.memory` or reduce consumption.

## E6 · FailedMount *(triggered)*

{{capture:err-failedmount}}

- **Cause**: the Secret or ConfigMap mounted as a volume does not exist; the Pod stays
  `ContainerCreating`.
- **Fix**: create the object; the Pod then starts on its own.

## E7 · Forbidden (RBAC) *(triggered)*

Exercises: `d4-07`, `s6-panne-rbac`.

{{capture:err-forbidden}}

- **Diagnosis**: the message gives the identity, the verb, the resource and the namespace.
- **Fix**: a minimal Role and RoleBinding; check with `k auth can-i … --as=…`.

## E8 · Invalid *(triggered)*

{{capture:err-invalid}}

And badly indented YAML, rejected before even reaching the API:

{{capture:err-yaml}}

- **Avoid it**: generate the YAML (`$do`), indent with 2 spaces, `k apply --dry-run=server -f`.

## E9 · Service without Endpoints *(triggered)*

Exercises: `d5-04`, `s5-pannes`, `m1-06`.

{{capture:err-noendpoints}}

- **Cause**: the Service selector matches no ready Pod.
- **Fix**: align selector and labels (`k get pods --show-labels`).

## E10 · Connection refused *(triggered)*

{{capture:err-refused}}

- **Cause**: Endpoints exist but the `targetPort` is wrong (nothing listens on 8080); or the app does
  not listen on the expected interface.
- **Fix**: `targetPort` = the real `containerPort`.

## E11 · NetworkPolicy that blocks too much *(triggered)*

Exercises: `d5-07`, `s4-jour4`.

{{capture:err-netpol}}

- **Cause**: an `Egress` policy with no rule cuts everything, DNS included (port 53): the name `web`
  no longer resolves.
- **Fix**: allow DNS (UDP and TCP 53) in addition to the intended destinations.

## Errors encountered while building the lab *(encountered)*

| No. | Error | Cause | Fix |
|---|---|---|---|
| R1 | `kubelet is configured to not run on a host using cgroup v1` | Kubernetes ≥ 1.35 rejects cgroup v1 by default | `failCgroupV1: false`, applied by `lab` only on cgroup v1 hosts |
| R2 | `runc create failed: … failed to update /proc/self/oom_score_adj: Permission denied` | host without `CAP_SYS_RESOURCE` | `restrict_oom_score_adj = true` in containerd, only when detected |
| R3 | `ctr: content digest sha256:… not found` on `kind load docker-image` | Docker ≥ 29 with its containerd image store exports a single platform | import only the local platform into each node (`lab`) |
| R4 | namespace stuck `Terminating`: `stale GroupVersion discovery: metrics.k8s.io/v1beta1` | metrics-server installed without its image | install metrics-server only when the image is available |
| R5 | `serviceaccount "default" not found` right after creating a namespace | race with the ServiceAccount controller | wait for the `default` ServiceAccount before creating Pods |
| R6 | `429 Too Many Requests` from Docker Hub | anonymous rate limit | fall back to the `mirror.gcr.io` mirror |
| R7 | after Docker restarts, DNS `bad address` and Traefik unable to reach the API (x509) | stale node network rules right after the restart | `lab wake`: restart CoreDNS, then Traefik |
| R8 | Traefik `Pending` during a rolling restart | `hostPort` 80 exists once per node | `strategy: Recreate` for Traefik |
| R9 | Ingress `Exact` path answered by `/` | Traefik ranks routes by rule length | use `Prefix` paths in the course; noted as a pitfall |
