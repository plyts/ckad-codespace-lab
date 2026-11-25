# Boutique : l'application fil conducteur

Trois composants, déployés et modifiés au fil de quatre journées (`ex scenario`) :

```text
 navigateur ──▶ Ingress (Traefik) ──▶ front (nginx, port 80)
                                         │
                                         ▼
                                      api (http-echo, port 5678, Service port 80)
                                         │
                                         ▼
                                      redis (port 6379)
```

- `jour1.yaml` : état de référence à la fin de la journée 1 (v1 déployée)
- `jour2.yaml` : état de référence à la fin de la journée 2 (configuration, secrets, ressources, 3 réplicas)

Les scénarios des journées suivantes partent de ces états : chaque journée est indépendante et
réinitialisable (`ex start s3-jour3` rejoue d'abord l'état de la journée 2).
Les manifestes n'ont pas de namespace : ils sont appliqués avec `-n <namespace du scénario>`.
