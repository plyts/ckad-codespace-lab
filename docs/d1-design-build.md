---
title: Application Design and Build
color: bleu
---
# 1 · Application Design and Build <small>(20 %)</small>

Compétences du curriculum : définir, construire et modifier des images de conteneur ; choisir la
bonne ressource de charge (Deployment, DaemonSet, Job, CronJob…) ; comprendre les Pods
multi-conteneurs (sidecar, init) ; utiliser des volumes persistants et éphémères.

## Choisir la bonne ressource

| Besoin | Ressource | Commande de départ |
|---|---|---|
| Un processus de test, jetable | Pod | `k run x --image=… $do` |
| Un service qui tourne en continu, mis à jour sans coupure | Deployment | `k create deployment x --image=… --replicas=N $do` |
| Un Pod sur **chaque** nœud (agent, collecteur) | DaemonSet | Deployment généré, `kind: DaemonSet`, sans `replicas` |
| Un traitement qui doit **finir** | Job | `k create job x --image=… $do -- cmd` |
| Un traitement planifié | CronJob | `k create cronjob x --image=… --schedule='*/5 * * * *' $do -- cmd` |

{{capture:create-deploy-dry}}

## Job et CronJob

Champs à connaître, tous sous `spec` du Job (pas sous `template`) : `completions`,
`parallelism`, `backoffLimit`, `activeDeadlineSeconds`, et `restartPolicy: Never|OnFailure` dans
le template. Pour un CronJob : `schedule`, `concurrencyPolicy` (`Allow`, `Forbid`, `Replace`),
`successfulJobsHistoryLimit`, `failedJobsHistoryLimit`, `suspend`.

```bash
k create job test --from=cronjob/backup     # lancer un CronJob tout de suite
```

:::piege restartPolicy
Un Job refuse `restartPolicy: Always` (celle des Pods par défaut). `kubectl create job` met
`Never` pour toi ; si tu écris le YAML à la main, ne l'oublie pas.
:::

## Pods multi-conteneurs

```text
   Pod ───────────────────────────────────────────────────────────┐
   │ initContainers (dans l'ordre, chacun jusqu'au bout)           │
   │   prepare ──▶ fini                                             │
   │ initContainers avec restartPolicy: Always = SIDECAR natif     │
   │   shipper ──────────────── vit avec le Pod ───────────────▶    │
   │ containers                                                     │
   │   app ───────────────────────────────────────────────────▶    │
   │            volume emptyDir partagé : /var/log/app             │
   └────────────────────────────────────────────────────────────────┘
```

- **Init container** : prépare quelque chose (fichier, attente d'un service) puis s'arrête. Le
  Pod reste en `Init:0/1` tant qu'il n'a pas fini.
- **Sidecar natif** (stable depuis 1.33) : un `initContainer` avec `restartPolicy: Always`. Il
  démarre avant le conteneur principal et s'arrête après lui.
- Le partage passe presque toujours par un volume `emptyDir` monté dans les deux conteneurs.

:::examen
`kubectl logs <pod> -c <conteneur>` : avec plusieurs conteneurs, `-c` est obligatoire, sinon
kubectl te demande de choisir. `kubectl exec <pod> -c <conteneur> -- …` de même.
:::

## Volumes

| Type | Durée de vie | Usage |
|---|---|---|
| `emptyDir` | celle du Pod | partage entre conteneurs, cache ; `medium: Memory` = tmpfs, `sizeLimit` |
| `configMap`, `secret` | celle de l'objet | fichiers de configuration (voir domaine 4) |
| `persistentVolumeClaim` | indépendante du Pod | données à garder |

Le PVC demande du stockage, la StorageClass le fournit (ici `standard`, provisionneur
local-path de kind, en mode `WaitForFirstConsumer` : le PVC reste `Pending` jusqu'au premier Pod
qui l'utilise. C'est normal).

:::piege StorageClass inexistante
Un PVC qui vise une classe absente reste `Pending` pour toujours, et `storageClassName` est
immuable : il faut le recréer. Voir le scénario `s5-pannes`.
:::

## Construire une image

```bash
docker build -t ckad/hello:v1 .           # ou podman build
docker save -o hello.tar ckad/hello:v1    # exporter (podman save -o …)
docker image inspect ckad/hello:v1 --format '{{json .Config.Labels}}'
```

Instructions du Dockerfile à savoir modifier : `FROM`, `COPY`, `RUN`, `ENV`, `LABEL`, `EXPOSE`,
`USER`, `WORKDIR`, `CMD` et `ENTRYPOINT`.

## Exercices du domaine

{{exercices:1}}
