---
id: d2-01
title: Premier Deployment
domain: 2
level: debutant
context: ckad-a
namespace: d2-01
time: 3
doc: https://kubernetes.io/docs/concepts/workloads/controllers/deployment/
skill: deployments
---
Dans le namespace `d2-01`, crée un Deployment `front` : image `nginx:1.27-alpine`,
**3 réplicas**, Pods étiquetés `app=front`. Les 3 réplicas doivent être prêts.
