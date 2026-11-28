---
title: Application Environment, Configuration and Security
color: orange
---
# 4 · Environment, Configuration and Security <small>(25%)</small>

The heaviest domain. Curriculum skills: discover and use resources that extend Kubernetes (CRDs,
operators); authentication, authorization and admission control; requests, limits and quotas;
ConfigMaps; Secrets; ServiceAccounts; SecurityContexts. Full details in the [course](cours-d4.html).

## ConfigMap and Secret: four ways to consume them

| Form | YAML in the container |
|---|---|
| All keys as env vars | `envFrom: [{configMapRef: {name: cfg}}]` (or `secretRef`) |
| One key in one variable | `env: [{name: MODE, valueFrom: {configMapKeyRef: {name: cfg, key: MODE}}}]` (or `secretKeyRef`) |
| One file per key | `volumes: [{name: c, configMap: {name: cfg}}]` + `volumeMounts` (or `secret: {secretName: …}`) |
| A single key as a file | `configMap: {name: cfg, items: [{key: index.html, path: index.html}]}` |

```bash
k create configmap cfg --from-literal=MODE=prod --from-file=nginx.conf
k create secret generic db --from-literal=password='S3cr3t!'
k get secret db -o jsonpath='{.data.password}' | base64 -d
k set env deploy/api --from=secret/db --prefix=DB_
```

:::piege Missing key
A variable referencing a missing key blocks startup: `CreateContainerConfigError` (see the
[error log](journal.html)). A Secret is **not** encrypted: `data` is just base64-encoded.
:::

:::pourquoi
Environment variables are read at startup: changing the ConfigMap changes nothing without a restart
(`k rollout restart deploy/x`). Mounted files are refreshed after a delay, except with `subPath`.
:::

## Requests, limits, QoS, quotas

```bash
k set resources deploy api --requests=cpu=50m,memory=32Mi --limits=cpu=100m,memory=64Mi
```

- **requests**: what the scheduler reserves (an oversized Pod stays `Pending`, `FailedScheduling`).
- **limits**: CPU is throttled above it; memory over it = container killed (`OOMKilled`).
- QoS: `Guaranteed` (requests = limits everywhere), `Burstable`, `BestEffort` (nothing).
- **ResourceQuota**: namespace caps (`pods`, `requests.cpu`…). With a quota on requests, every Pod
  **must** declare requests… unless a **LimitRange** injects defaults.

## ServiceAccounts and RBAC

```text
ServiceAccount monitor ──(RoleBinding)──▶ Role pod-reader: get, list, watch on pods, pods/log
          (identity)                           (permissions, in ONE namespace)
ClusterRole + ClusterRoleBinding = the same thing cluster-wide
```

```bash
k create serviceaccount monitor
k create role pod-reader --verb=get,list,watch --resource=pods,pods/log
k create rolebinding monitor-pod-reader --role=pod-reader --serviceaccount=<ns>:monitor
k auth can-i list pods -n <ns> --as=system:serviceaccount:<ns>:monitor
k set serviceaccount deploy/api monitor
```

{{capture:auth-can-i}}

Admission control comes next: even when authorized, a request may be rejected or changed (for
example by ResourceQuota, LimitRange, Pod Security Admission).

## SecurityContext

| Pod level (`spec.securityContext`) | Container level (`containers[].securityContext`) |
|---|---|
| `runAsUser`, `runAsGroup`, `runAsNonRoot`, `fsGroup` | the same `runAs*`, plus `allowPrivilegeEscalation`, `readOnlyRootFilesystem`, `capabilities {drop, add}`, `privileged` |

Container level wins. `capabilities` and `readOnlyRootFilesystem` exist **only at container level**.

## Extending Kubernetes: CRDs

```bash
k get crd
k api-resources --api-group=lab.ckad.io
k explain backup.spec
```

A CRD adds a `kind` (here `Backup`, `apiVersion: lab.ckad.io/v1`); an operator is a controller acting
on those objects. In the exam you are mostly asked to **find** the resource and create a valid object.

## Exercises of this domain

{{exercices:4}}
