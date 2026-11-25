---
title: Application Observability and Maintenance
color: vert
---
# 3 · Observability and Maintenance <small>(15 %)</small>

Compétences du curriculum : comprendre les dépréciations d'API ; mettre en œuvre les sondes et
contrôles de santé ; surveiller les applications avec les outils CLI ; utiliser les logs des
conteneurs ; déboguer dans Kubernetes.

## Les sondes

| Sonde | Question posée | Si elle échoue |
|---|---|---|
| `startupProbe` | L'application a-t-elle fini de démarrer ? | Les deux autres attendent ; après `failureThreshold` échecs, redémarrage |
| `readinessProbe` | Peut-elle recevoir du trafic ? | Pod retiré des Endpoints, **pas** redémarré |
| `livenessProbe` | Est-elle encore vivante ? | Conteneur **redémarré** |

Trois mécanismes : `httpGet {path, port}`, `tcpSocket {port}`, `exec {command}` (et `grpc`).
Réglages : `initialDelaySeconds`, `periodSeconds`, `timeoutSeconds`, `failureThreshold`,
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

:::piege Liveness sur le mauvais port
Une liveness qui vise un port fermé fait redémarrer le conteneur sans fin, alors que
l'application va bien. Les événements disent `Liveness probe failed: … connection refused`.
Exercice `d3-09`.
:::

## La méthode de diagnostic

```text
k get pods                  → le STATUS oriente : Pending, ImagePullBackOff, CrashLoopBackOff, CreateContainerConfigError…
k describe pod <p>          → Events en bas, State / Last State / Exit Code / Restart Count
k logs <p> [--previous]     → ce que l'application a écrit (avant le dernier crash avec --previous)
k get events --sort-by=.lastTimestamp
k exec -it <p> -- sh        → regarder de l'intérieur (si l'image a un shell)
k debug <p> -it --image=busybox:1.37 --target=<conteneur>   → conteneur éphémère, pour les images sans shell
```

{{capture:events}}

{{capture:logs}}

{{capture:exec}}

Les cas réels, avec leurs sorties, sont dans le [Journal des erreurs](journal.html) :
CrashLoopBackOff, ImagePullBackOff, CreateContainerConfigError, Pending, OOMKilled, FailedMount.

## Surveiller : kubectl top

```bash
k top nodes
k top pods -n <ns> --sort-by=cpu
k top pods -n <ns> --containers
```

Il faut metrics-server (installé par `lab up`). Les mesures arrivent environ une minute après le
démarrage des Pods.

## Dépréciations d'API

Une API retirée ne s'applique plus : `no matches for kind "CronJob" in version "batch/v1beta1"`.

```bash
k api-resources | grep -i cronjob      # groupe/version actuels
k explain cronjob | head -3            # VERSION
```

| Ancienne | Actuelle | Retirée en |
|---|---|---|
| `batch/v1beta1` CronJob | `batch/v1` | 1.25 |
| `policy/v1beta1` PodDisruptionBudget | `policy/v1` | 1.25 |
| `networking.k8s.io/v1beta1` Ingress | `networking.k8s.io/v1` (avec `pathType` et `backend.service`) | 1.22 |
| `autoscaling/v2beta2` HPA | `autoscaling/v2` | 1.26 |

Référence : [Deprecated API Migration Guide](https://kubernetes.io/docs/reference/using-api/deprecation-guide/).

## Exercices du domaine

{{exercices:3}}
