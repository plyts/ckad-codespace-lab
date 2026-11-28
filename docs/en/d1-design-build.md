---
title: Application Design and Build
color: bleu
---
# 1 · Application Design and Build <small>(20%)</small>

Curriculum skills: define, build and modify container images; choose and use the right workload
resource (Deployment, DaemonSet, Job, CronJob…); understand multi-container Pod design patterns
(sidecar, init); use persistent and ephemeral volumes. Full details in the [course](cours-d1.html).

## Picking the right resource

| Need | Resource | Starting command |
|---|---|---|
| A throwaway test process | Pod | `k run x --image=… $do` |
| A long-running service, updated without downtime | Deployment | `k create deployment x --image=… --replicas=N $do` |
| One Pod on **every** node (agent, collector) | DaemonSet | generated Deployment, `kind: DaemonSet`, no `replicas` |
| A task that must **finish** | Job | `k create job x --image=… $do -- cmd` |
| A scheduled task | CronJob | `k create cronjob x --image=… --schedule='*/5 * * * *' $do -- cmd` |

{{capture:create-deploy-dry}}

## Job and CronJob

Fields to know, all under the Job's `spec` (not under `template`): `completions`, `parallelism`,
`backoffLimit`, `activeDeadlineSeconds`, and `restartPolicy: Never|OnFailure` in the template. For a
CronJob: `schedule`, `concurrencyPolicy` (`Allow`, `Forbid`, `Replace`), `successfulJobsHistoryLimit`,
`failedJobsHistoryLimit`, `suspend`.

```bash
k create job test --from=cronjob/backup     # run a CronJob right now
```

:::piege restartPolicy
A Job rejects `restartPolicy: Always` (the Pod default). `kubectl create job` sets `Never` for you;
if you write the YAML by hand, do not forget it.
:::

## Multi-container Pods

```text
   Pod ───────────────────────────────────────────────────────────┐
   │ initContainers (in order, each to completion)                 │
   │   prepare ──▶ done                                             │
   │ initContainers with restartPolicy: Always = native SIDECAR    │
   │   shipper ──────────────── lives with the Pod ────────────▶    │
   │ containers                                                     │
   │   app ───────────────────────────────────────────────────▶    │
   │            shared emptyDir volume: /var/log/app               │
   └────────────────────────────────────────────────────────────────┘
```

- **Init container**: prepares something (file, waiting for a service) then stops. The Pod stays
  `Init:0/1` until it finishes.
- **Native sidecar** (stable since 1.33): an `initContainer` with `restartPolicy: Always`. It starts
  before the main container and stops after it.
- Sharing almost always goes through an `emptyDir` volume mounted in both containers.

:::examen
`kubectl logs <pod> -c <container>`: with several containers, `-c` is required, otherwise kubectl
asks you to choose. Same for `kubectl exec <pod> -c <container> -- …`.
:::

## Volumes

| Type | Lifetime | Use |
|---|---|---|
| `emptyDir` | the Pod's | sharing between containers, cache; `medium: Memory` = tmpfs, `sizeLimit` |
| `configMap`, `secret` | the object's | configuration files (see domain 4) |
| `persistentVolumeClaim` | independent of the Pod | data to keep |

The PVC requests storage, the StorageClass provides it (here `standard`, kind's local-path
provisioner, in `WaitForFirstConsumer` mode: the PVC stays `Pending` until the first Pod uses it.
That is normal).

:::piege Missing StorageClass
A PVC pointing to a missing class stays `Pending` forever, and `storageClassName` is immutable: it
must be recreated. See scenario `s5-pannes`.
:::

## Building an image

```bash
docker build -t ckad/hello:v1 .           # or podman build
docker save -o hello.tar ckad/hello:v1    # export (podman save -o …)
docker image inspect ckad/hello:v1 --format '{{json .Config.Labels}}'
```

Dockerfile instructions you must be able to change: `FROM`, `COPY`, `RUN`, `ENV`, `LABEL`, `EXPOSE`,
`USER`, `WORKDIR`, `CMD` and `ENTRYPOINT`.

## Exercises of this domain

{{exercices:1}}
