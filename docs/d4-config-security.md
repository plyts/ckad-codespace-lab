---
title: Application Environment, Configuration and Security
color: orange
---
# 4 · Environment, Configuration and Security <small>(25 %)</small>

Le domaine le plus lourd. Compétences du curriculum : découvrir et utiliser les ressources qui
étendent Kubernetes (CRD, opérateurs) ; authentification, autorisation et contrôle d'admission ;
requests, limits et quotas ; ConfigMaps ; Secrets ; ServiceAccounts ; SecurityContexts.

## ConfigMap et Secret : quatre façons de les consommer

| Forme | YAML dans le conteneur |
|---|---|
| Toutes les clés en variables | `envFrom: [{configMapRef: {name: cfg}}]` (ou `secretRef`) |
| Une clé dans une variable | `env: [{name: MODE, valueFrom: {configMapKeyRef: {name: cfg, key: MODE}}}]` (ou `secretKeyRef`) |
| Un fichier par clé | `volumes: [{name: c, configMap: {name: cfg}}]` + `volumeMounts` (ou `secret: {secretName: …}`) |
| Une seule clé en fichier | `configMap: {name: cfg, items: [{key: index.html, path: index.html}]}` |

```bash
k create configmap cfg --from-literal=MODE=prod --from-file=nginx.conf
k create secret generic db --from-literal=password='S3cr3t!'
k get secret db -o jsonpath='{.data.password}' | base64 -d
k set env deploy/api --from=secret/db --prefix=DB_
```

:::piege Clé absente
Une variable qui référence une clé inexistante bloque le démarrage :
`CreateContainerConfigError` (entrée du [journal](journal.html)). Un Secret n'est **pas**
chiffré : `data` est simplement encodé en base64.
:::

:::pourquoi
Les variables d'environnement sont lues au démarrage : modifier la ConfigMap ne change rien sans
redémarrage (`k rollout restart deploy/x`). Les fichiers montés, eux, sont mis à jour après un
délai, sauf avec `subPath`.
:::

## Requests, limits, QoS, quotas

```bash
k set resources deploy api --requests=cpu=50m,memory=32Mi --limits=cpu=100m,memory=64Mi
```

- **requests** : ce que le scheduler réserve (un Pod trop gourmand reste `Pending`,
  `FailedScheduling`).
- **limits** : CPU bridé au-delà ; mémoire dépassée = conteneur tué (`OOMKilled`).
- QoS : `Guaranteed` (requests = limits partout), `Burstable`, `BestEffort` (rien).
- **ResourceQuota** : plafonds du namespace (`pods`, `requests.cpu`…). Avec un quota sur les
  requests, tout Pod **doit** déclarer ses requests… sauf si une **LimitRange** injecte des
  valeurs par défaut.

## ServiceAccounts et RBAC

```text
ServiceAccount monitor ──(RoleBinding)──▶ Role pod-reader : get, list, watch sur pods, pods/log
          (identité)                           (droits, dans UN namespace)
ClusterRole + ClusterRoleBinding = la même chose pour tout le cluster
```

```bash
k create serviceaccount monitor
k create role pod-reader --verb=get,list,watch --resource=pods,pods/log
k create rolebinding monitor-pod-reader --role=pod-reader --serviceaccount=<ns>:monitor
k auth can-i list pods -n <ns> --as=system:serviceaccount:<ns>:monitor
k set serviceaccount deploy/api monitor
```

{{capture:auth-can-i}}

Le contrôle d'admission vient ensuite : même autorisée, une requête peut être refusée ou
modifiée (par exemple ResourceQuota, LimitRange, Pod Security Admission).

## SecurityContext

| Niveau Pod (`spec.securityContext`) | Niveau conteneur (`containers[].securityContext`) |
|---|---|
| `runAsUser`, `runAsGroup`, `runAsNonRoot`, `fsGroup` | les mêmes `runAs*`, plus `allowPrivilegeEscalation`, `readOnlyRootFilesystem`, `capabilities {drop, add}`, `privileged` |

Le niveau conteneur l'emporte. `capabilities` et `readOnlyRootFilesystem` n'existent **qu'au
niveau conteneur**.

## Étendre Kubernetes : CRD

```bash
k get crd
k api-resources --api-group=lab.ckad.io
k explain backup.spec
```

Une CRD ajoute un `kind` (ici `Backup`, `apiVersion: lab.ckad.io/v1`) ; un opérateur est un
contrôleur qui agit sur ces objets. À l'examen, on te demande surtout de **trouver** la ressource
et de créer un objet valide.

## Exercices du domaine

{{exercices:4}}
