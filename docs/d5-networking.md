---
title: Services and Networking
color: violet
---
# 5 · Services and Networking <small>(20 %)</small>

Compétences du curriculum : comprendre les NetworkPolicies ; donner et dépanner l'accès aux
applications par des Services ; exposer des applications par des règles Ingress.

## Service → EndpointSlice → Pods

```text
Service api (ClusterIP 10.96.x.x, port 80) ──sélecteur app=api──▶ EndpointSlice ──▶ Pod :5678
                                                                                └─▶ Pod :5678
nom DNS : api (même namespace) · api.<ns> · api.<ns>.svc.cluster.local
```

{{capture:endpoints}}

{{capture:describe-svc}}

{{capture:dns}}

{{capture:http-api}}

| Type | Accès |
|---|---|
| `ClusterIP` (défaut) | depuis le cluster |
| `NodePort` | `<IP de n'importe quel nœud>:30000-32767` |
| `LoadBalancer` | IP externe (aucune dans kind sans addon) |
| `ExternalName` | alias DNS vers un nom externe |

```bash
k expose deploy api --port=80 --target-port=5678                  # ClusterIP
k expose deploy web --type=NodePort --port=80 $do > np.yaml        # puis ajouter nodePort: 30080
```

:::piege Les deux pannes de Service
Sélecteur faux : **aucun Endpoint**. targetPort faux : Endpoints présents, mais
**Connection refused**. Toujours commencer par `k get endpointslices`. Voir les deux entrées du
[journal](journal.html).
:::

## Ingress

```bash
k create ingress shop --class=traefik \
  --rule='shop.lab.local/*=front:80' \
  --rule='shop.lab.local/api*=api:8080'          # l'étoile = pathType Prefix
curl -H 'Host: shop.lab.local' http://localhost:8080/api    # dans le Codespace
```

Le backend vise le **port du Service**. Sans `ingressClassName` existant (`k get ingressclass`),
aucun contrôleur ne prend l'Ingress.

:::pourquoi
Le contrôleur du labo est Traefik : ingress-nginx est en retraite depuis mars 2026. La ressource
`Ingress` est standard, donc les mêmes YAML marchent avec le contrôleur de l'examen ; seule la
classe change, et la consigne te la donne.
:::

## NetworkPolicy

```text
Dès qu'une NetworkPolicy SÉLECTIONNE un Pod (podSelector) pour un sens (policyTypes),
tout ce qui n'est pas explicitement autorisé dans ce sens est refusé pour ce Pod.
Les politiques s'additionnent (union des autorisations).
```

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata: {name: allow-frontend}
spec:
  podSelector: {matchLabels: {app: api}}      # la DESTINATION protégée
  policyTypes: [Ingress]
  ingress:
  - from:
    - podSelector: {matchLabels: {role: frontend}}             # même namespace
    - namespaceSelector: {matchLabels: {kubernetes.io/metadata.name: traefik}}   # OU tout un namespace
    ports:
    - {protocol: TCP, port: 5678}             # port du CONTENEUR, pas du Service
```

:::piege ET contre OU
Dans `from` (ou `to`), deux éléments de liste = **OU**. Un seul élément qui contient
`namespaceSelector` **et** `podSelector` = **ET** (ces Pods-là, dans ce namespace-là).
Exercice `d5-07`.
:::

:::piege Egress sans DNS
Une politique `Egress` qui oublie le port 53 (UDP et TCP) casse la résolution des noms : les
appels par nom échouent, ceux par IP passent. Voir l'entrée « NetworkPolicy qui bloque trop » du
[journal](journal.html).
:::

## Exercices du domaine

{{exercices:5}}
