---
title: Services and Networking
color: violet
---
# 5 · Services and Networking <small>(20%)</small>

Curriculum skills: demonstrate a basic understanding of NetworkPolicies; provide and troubleshoot
access to applications through Services; use Ingress rules to expose applications. Full details in
the [course](cours-d5.html).

## Service → EndpointSlice → Pods

```text
Service api (ClusterIP 10.96.x.x, port 80) ──selector app=api──▶ EndpointSlice ──▶ Pod :5678
                                                                              └─▶ Pod :5678
DNS name: api (same namespace) · api.<ns> · api.<ns>.svc.cluster.local
```

{{capture:endpoints}}

{{capture:describe-svc}}

{{capture:dns}}

{{capture:http-api}}

| Type | Access |
|---|---|
| `ClusterIP` (default) | from inside the cluster |
| `NodePort` | `<IP of any node>:30000-32767` |
| `LoadBalancer` | external IP (none in kind without an add-on) |
| `ExternalName` | DNS alias to an external name |

```bash
k expose deploy api --port=80 --target-port=5678                  # ClusterIP
k expose deploy web --type=NodePort --port=80 $do > np.yaml        # then add nodePort: 30080
```

:::piege The two Service failures
Wrong selector: **no Endpoint**. Wrong targetPort: Endpoints exist, but **Connection refused**.
Always start with `k get endpointslices`. See both entries of the [error log](journal.html).
:::

## Ingress

```bash
k create ingress shop --class=traefik \
  --rule='shop.lab.local/*=front:80' \
  --rule='shop.lab.local/api*=api:8080'          # the star = pathType Prefix
curl -H 'Host: shop.lab.local' http://localhost:8080/api    # inside the Codespace
```

The backend targets the **Service port**. Without an existing `ingressClassName`
(`k get ingressclass`), no controller picks the Ingress up.

:::pourquoi
The lab controller is Traefik: ingress-nginx has been retired since March 2026. The `Ingress`
resource is standard, so the same YAML works with the exam's controller; only the class changes, and
the task gives it to you.
:::

## NetworkPolicy

```text
As soon as a NetworkPolicy SELECTS a Pod (podSelector) for a direction (policyTypes),
everything not explicitly allowed in that direction is denied for that Pod.
Policies add up (union of permissions).
```

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata: {name: allow-frontend}
spec:
  podSelector: {matchLabels: {app: api}}      # the protected DESTINATION
  policyTypes: [Ingress]
  ingress:
  - from:
    - podSelector: {matchLabels: {role: frontend}}             # same namespace
    - namespaceSelector: {matchLabels: {kubernetes.io/metadata.name: traefik}}   # OR a whole namespace
    ports:
    - {protocol: TCP, port: 5678}             # CONTAINER port, not the Service port
```

:::piege AND versus OR
In `from` (or `to`), two list items = **OR**. A single item containing both `namespaceSelector`
**and** `podSelector` = **AND** (those Pods, in that namespace). Exercise `d5-07`.
:::

:::piege Egress without DNS
An `Egress` policy that forgets port 53 (UDP and TCP) breaks name resolution: calls by name fail,
calls by IP work. See the "NetworkPolicy that blocks too much" entry of the [error log](journal.html).
:::

## Exercises of this domain

{{exercices:5}}
