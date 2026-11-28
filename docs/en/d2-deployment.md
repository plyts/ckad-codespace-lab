---
title: Application Deployment
color: jaune
---
# 2 · Application Deployment <small>(20%)</small>

Curriculum skills: use Kubernetes primitives for common deployment strategies (blue/green, canary);
understand Deployments and rolling updates; use Helm to deploy existing packages; Kustomize. Full
details in the [course](cours-d2.html).

## Deployment → ReplicaSet → Pods

```text
Deployment front (replicas: 2, template: nginx:1.27)
   └── ReplicaSet front-<hash>   ← one per template revision
          ├── Pod front-<hash>-xxxxx
          └── Pod front-<hash>-yyyyy
```

{{capture:get-all}}

Changing the **template** (image, env, resources, probes) creates a revision and a new ReplicaSet.
Changing `replicas` does not.

## Rolling update, history, rollback

```bash
k set image deploy/front front=nginx:1.28-alpine
k annotate deploy front kubernetes.io/change-cause='move to 1.28'   # --record no longer exists
k rollout status deploy/front
```

{{capture:rollout-history}}

{{capture:rollout-undo}}

After the rollback, the old ReplicaSet takes the replicas back: nothing was deleted.

{{capture:rs-after-undo}}

| Field | Effect |
|---|---|
| `strategy.type: RollingUpdate` (default) | Progressive replacement |
| `rollingUpdate.maxSurge` / `maxUnavailable` | Extra / missing Pods tolerated during the update (25% by default) |
| `strategy.type: Recreate` | Stop everything then recreate (remove the `rollingUpdate` block) |
| `minReadySeconds` | Delay before a Pod counts as available |
| `revisionHistoryLimit` | Old ReplicaSets kept (10 by default) |

:::piege A rollback that "does not work"
`rollout undo` goes back to the **previous** revision. After two failed updates, read
`rollout history` and use `--to-revision=N`.
:::

## Blue/green and canary, without tooling

Both rely on one fact: **a Service sends traffic to every Pod matching its selector**.

- **Blue/green**: two Deployments (`version=blue`, `version=green`); the switch is a change of the
  Service selector (`k patch svc web -p '{"spec":{"selector":{"app":"web","version":"green"}}}'`).
- **Canary**: the Service only selects `app=api`; 4 stable Pods + 1 canary Pod, all `app=api`, give
  the canary about 20% of the traffic. The share comes from the Pod count.

## Helm

```bash
helm -n shop install shop ./chart --set replicaCount=2 --set image.tag=1.28-alpine
helm -n shop list
helm show values ./chart          # default values
helm -n shop get values shop      # applied values
helm -n shop upgrade shop ./chart --set replicaCount=3
helm -n shop history shop
helm -n shop rollback shop 1
helm -n shop uninstall shop
```

:::examen
helm.sh/docs is part of the allowed documentation. Public chart repositories are not guaranteed in
the exam: charts are usually provided locally, like `app/charts/webapp` here.
:::

## Kustomize

```yaml
# overlays/prod/kustomization.yaml
resources: [../../base]
namespace: prod
namePrefix: prod-
labels:
- pairs: {env: prod}
replicas:
- {name: web, count: 3}          # name BEFORE the prefix
images:
- {name: nginx, newTag: 1.28-alpine}
```

```bash
kubectl kustomize overlays/prod    # preview
kubectl apply -k overlays/prod
```

## Exercises of this domain

{{exercices:2}}
