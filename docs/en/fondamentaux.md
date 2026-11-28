---
title: Fundamentals
color: gris
---
# Fundamentals: cluster, Pods, labels

## The cluster in one picture

```text
                 ┌──────────── control plane ────────────┐
 kubectl ──────▶ │ kube-apiserver ◀──▶ etcd               │
                 │ scheduler · controller-manager         │
                 └───────────────┬────────────────────────┘
                                 │ (kubelet on every node)
         ┌───────────────────────┼───────────────────────┐
     worker 1                worker 2                 control plane
   kubelet + containerd    kubelet + containerd     (system Pods, Traefik)
   [Pod] [Pod]             [Pod] [Pod]
```

You only talk to the **API server**. You submit a desired state (a manifest) and controllers make
the cluster converge to it. The whole CKAD rests on that: describe, then check that the real state
follows.

{{capture:nodes}}

## Anatomy of a manifest

```yaml
apiVersion: v1            # API group/version (v1, apps/v1, batch/v1, networking.k8s.io/v1…)
kind: Pod                 # object type
metadata:                 # identity: name, namespace, labels, annotations
  name: web
  namespace: guide
  labels:
    app: web
spec:                     # desired state (what YOU write)
  containers:
  - name: web
    image: nginx:1.27-alpine
    ports:
    - containerPort: 80
# status:                 # real state (written by the cluster): never write it yourself
```

Never write it from memory: generate it.

{{capture:run-dry}}

:::examen
`--dry-run=client -o yaml` (the `$do` variable) then `vim` is move number 1 in the exam. Useful
generators: `run` (Pod), `create deployment|job|cronjob|configmap|secret|service|ingress|role|rolebinding|quota|serviceaccount`, `expose`.
:::

## Finding a field: `kubectl explain`

{{capture:explain-probe}}

`--recursive` prints the whole tree at once:

{{capture:explain-recursive}}

## Namespaces

A namespace scopes names and carries quotas, RBAC permissions and NetworkPolicies. Each lab exercise
has its own (`d1-01`, `m3-07`…), just as each exam task gives its own. The label
`kubernetes.io/metadata.name=<name>` is set automatically: NetworkPolicies use it.

{{capture:api-resources}}

## Labels and selectors

Labels are `key=value` tags. **Selectors** tie objects together: a Deployment finds its Pods, a
Service its Endpoints, a NetworkPolicy the Pods it protects.

{{capture:get-labels}}

Set-based selector, with an extra label column:

{{capture:selector}}

:::piege The selector that matches nothing
A Service whose selector matches no Pod has no Endpoint, and every call fails. See the "Service
without Endpoints" entry of the [error log](journal.html).
:::

## Extracting a value: jsonpath and custom-columns

{{capture:jsonpath}}

{{capture:custom-columns}}

Both are used to **write an answer into a file** (common in the exam) and to check by hand. The lab
checks do the same (`jp` in `lib/check.sh`).
