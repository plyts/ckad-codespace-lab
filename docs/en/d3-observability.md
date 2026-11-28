---
title: Application Observability and Maintenance
color: vert
---
# 3 · Observability and Maintenance <small>(15%)</small>

Curriculum skills: understand API deprecations; implement probes and health checks; use built-in CLI
tools to monitor applications; use container logs; debug in Kubernetes. Full details in the
[course](cours-d3.html).

## Probes

| Probe | Question asked | On failure |
|---|---|---|
| `startupProbe` | Has the app finished starting? | The other two wait; after `failureThreshold` failures, restart |
| `readinessProbe` | Can it receive traffic? | Pod removed from Endpoints, **not** restarted |
| `livenessProbe` | Is it still alive? | Container **restarted** |

Three mechanisms: `httpGet {path, port}`, `tcpSocket {port}`, `exec {command}` (and `grpc`).
Settings: `initialDelaySeconds`, `periodSeconds`, `timeoutSeconds`, `failureThreshold`,
`successThreshold`.

```yaml
readinessProbe:
  httpGet: {path: /, port: 80}
  periodSeconds: 5
livenessProbe:
  tcpSocket: {port: 80}
  initialDelaySeconds: 10
  periodSeconds: 15
```

:::piege Liveness on the wrong port
A liveness probe aimed at a closed port restarts the container forever while the app is fine. The
events say `Liveness probe failed: … connection refused`. Exercise `d3-09`.
:::

## The diagnostic method

```text
k get pods                  → STATUS points the way: Pending, ImagePullBackOff, CrashLoopBackOff, CreateContainerConfigError…
k describe pod <p>          → Events at the bottom, State / Last State / Exit Code / Restart Count
k logs <p> [--previous]     → what the app wrote (before the last crash with --previous)
k get events --sort-by=.lastTimestamp
k exec -it <p> -- sh        → look from inside (if the image has a shell)
k debug <p> -it --image=busybox:1.37 --target=<container>   → ephemeral container, for images without a shell
```

{{capture:events}}

{{capture:logs}}

{{capture:exec}}

Real cases, with their outputs, are in the [Error log](journal.html): CrashLoopBackOff,
ImagePullBackOff, CreateContainerConfigError, Pending, OOMKilled, FailedMount.

## Monitoring: kubectl top

```bash
k top nodes
k top pods -n <ns> --sort-by=cpu
k top pods -n <ns> --containers
```

Requires metrics-server (installed by `lab up`). Metrics show up about a minute after Pods start.

## API deprecations

A removed API no longer applies: `no matches for kind "CronJob" in version "batch/v1beta1"`.

```bash
k api-resources | grep -i cronjob      # current group/version
k explain cronjob | head -3            # VERSION
```

| Old | Current | Removed in |
|---|---|---|
| `batch/v1beta1` CronJob | `batch/v1` | 1.25 |
| `policy/v1beta1` PodDisruptionBudget | `policy/v1` | 1.25 |
| `networking.k8s.io/v1beta1` Ingress | `networking.k8s.io/v1` (with `pathType` and `backend.service`) | 1.22 |
| `autoscaling/v2beta2` HPA | `autoscaling/v2` | 1.26 |

Reference: [Deprecated API Migration Guide](https://kubernetes.io/docs/reference/using-api/deprecation-guide/).

## Exercises of this domain

{{exercices:3}}
