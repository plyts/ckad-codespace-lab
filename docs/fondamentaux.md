---
title: Fondamentaux
color: gris
---
# Fondamentaux : cluster, Pods, labels

## Le cluster en une image

```text
                 ┌──────────── control-plane ────────────┐
 kubectl ──────▶ │ kube-apiserver ◀──▶ etcd               │
                 │ scheduler · controller-manager         │
                 └───────────────┬────────────────────────┘
                                 │ (kubelet de chaque nœud)
         ┌───────────────────────┼───────────────────────┐
     worker 1                worker 2                 control-plane
   kubelet + containerd    kubelet + containerd     (Pods système, Traefik)
   [Pod] [Pod]             [Pod] [Pod]
```

Tu ne parles qu'à l'**API server**. Tu y déposes un état voulu (un manifeste) et les contrôleurs
font converger le cluster vers cet état. Tout le CKAD repose là-dessus : on décrit, on vérifie
que l'état réel suit.

{{capture:nodes}}

## L'anatomie d'un manifeste

```yaml
apiVersion: v1            # groupe/version de l'API (v1, apps/v1, batch/v1, networking.k8s.io/v1…)
kind: Pod                 # type d'objet
metadata:                 # identité : nom, namespace, labels, annotations
  name: web
  namespace: guide
  labels:
    app: web
spec:                     # état voulu (ce que TU écris)
  containers:
  - name: web
    image: nginx:1.27-alpine
    ports:
    - containerPort: 80
# status:                 # état réel (ce que le cluster écrit) : ne jamais l'écrire soi-même
```

Ne l'écris jamais de mémoire : fais-le générer.

{{capture:run-dry}}

:::examen
`--dry-run=client -o yaml` (la variable `$do`) puis `vim`, c'est le geste n° 1 de l'examen. Les
générateurs utiles : `run` (Pod), `create deployment|job|cronjob|configmap|secret|service|ingress|role|rolebinding|quota|serviceaccount`, `expose`.
:::

## Trouver un champ : `kubectl explain`

{{capture:explain-probe}}

`--recursive` affiche toute l'arborescence d'un coup :

{{capture:explain-recursive}}

## Namespaces

Un namespace isole les noms et porte les quotas, les droits RBAC et les NetworkPolicy. Chaque
exercice du labo a le sien (`d1-01`, `m3-07`…), comme chaque tâche d'examen précise le sien.
Le label `kubernetes.io/metadata.name=<nom>` est posé automatiquement : on s'en sert dans les
NetworkPolicy.

{{capture:api-resources}}

## Labels et sélecteurs

Les labels sont des étiquettes `clé=valeur`. Les **sélecteurs** relient les objets entre eux :
un Deployment retrouve ses Pods, un Service ses Endpoints, une NetworkPolicy les Pods qu'elle
protège.

{{capture:get-labels}}

Sélecteur par ensemble, avec une colonne de label en plus :

{{capture:selector}}

:::piege Le sélecteur qui ne trouve rien
Un Service dont le sélecteur ne correspond à aucun Pod n'a aucun Endpoint, et tout appel échoue.
C'est l'entrée « Service sans Endpoints » du [journal](journal.html).
:::

## Extraire une valeur : jsonpath et custom-columns

{{capture:jsonpath}}

{{capture:custom-columns}}

Les deux servent à **écrire une réponse dans un fichier** (fréquent à l'examen) et à vérifier à
la main. Les contrôles du labo font la même chose (`jp` dans `lib/check.sh`).
