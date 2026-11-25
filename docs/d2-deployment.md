---
title: Application Deployment
color: jaune
---
# 2 · Application Deployment <small>(20 %)</small>

Compétences du curriculum : stratégies de déploiement courantes avec les primitives Kubernetes
(blue/green, canary) ; Deployments et rolling updates ; Helm pour déployer des paquets
existants ; Kustomize.

## Deployment → ReplicaSet → Pods

```text
Deployment front (replicas: 2, template: nginx:1.27)
   └── ReplicaSet front-<hash>   ← un par révision du template
          ├── Pod front-<hash>-xxxxx
          └── Pod front-<hash>-yyyyy
```

{{capture:get-all}}

Changer le **template** (image, env, ressources, sondes) crée une révision et un nouveau
ReplicaSet. Changer `replicas` n'en crée pas.

## Rolling update, historique, rollback

```bash
k set image deploy/front front=nginx:1.28-alpine
k annotate deploy front kubernetes.io/change-cause='passage en 1.28'   # --record n'existe plus
k rollout status deploy/front
```

{{capture:rollout-history}}

{{capture:rollout-undo}}

Après le rollback, l'ancien ReplicaSet reprend les réplicas : rien n'a été supprimé.

{{capture:rs-after-undo}}

| Champ | Effet |
|---|---|
| `strategy.type: RollingUpdate` (défaut) | Remplacement progressif |
| `rollingUpdate.maxSurge` / `maxUnavailable` | Pods en plus / en moins tolérés pendant la mise à jour (25 % par défaut) |
| `strategy.type: Recreate` | Tout arrêter puis tout recréer (retirer le bloc `rollingUpdate`) |
| `minReadySeconds` | Délai avant de considérer un Pod disponible |
| `revisionHistoryLimit` | Anciens ReplicaSets conservés (10 par défaut) |

:::piege Rollback qui « ne marche pas »
`rollout undo` revient à la révision **précédente**. Si tu as fait deux mises à jour ratées,
regarde `rollout history` et utilise `--to-revision=N`.
:::

## Blue/green et canary, sans outil

Les deux reposent sur un fait simple : **un Service envoie le trafic à tous les Pods qui
correspondent à son sélecteur**.

- **Blue/green** : deux Deployments (`version=blue`, `version=green`) ; la bascule consiste à
  changer le sélecteur du Service (`k patch svc web -p '{"spec":{"selector":{"app":"web","version":"green"}}}'`).
- **Canary** : le Service sélectionne seulement `app=api` ; 4 Pods stables + 1 Pod canary, tous
  `app=api`, donnent environ 20 % du trafic au canary. La proportion vient du nombre de Pods.

## Helm

```bash
helm -n shop install shop ./chart --set replicaCount=2 --set image.tag=1.28-alpine
helm -n shop list
helm show values ./chart          # valeurs par défaut
helm -n shop get values shop      # valeurs appliquées
helm -n shop upgrade shop ./chart --set replicaCount=3
helm -n shop history shop
helm -n shop rollback shop 1
helm -n shop uninstall shop
```

:::examen
helm.sh/docs fait partie de la documentation autorisée. Les dépôts de charts publics ne sont
pas garantis à l'examen : les charts sont en général fournis localement, comme
`app/charts/webapp` ici.
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
- {name: web, count: 3}          # nom AVANT le préfixe
images:
- {name: nginx, newTag: 1.28-alpine}
```

```bash
kubectl kustomize overlays/prod    # aperçu
kubectl apply -k overlays/prod
```

## Exercices du domaine

{{exercices:2}}
