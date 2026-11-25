---
id: s3-jour3
title: Boutique, journée 3 : incident et rollback
domain: 0
level: avance
context: ckad-a
namespace: boutique-j3
time: 12
doc: https://kubernetes.io/docs/concepts/workloads/controllers/deployment/#rolling-back-a-deployment
skill: fil-conducteur
---
**Fil conducteur, journée 3.** Contexte `ckad-a`, namespace `boutique-j3`.

L'équipe vient de déployer la **v2** de l'API. Les nouveaux Pods ne démarrent pas.

1. Écris dans `~/ckad/s3-jour3/incident.txt` le **statut** affiché par les nouveaux Pods
   (colonne STATUS de `kubectl get pods`) et, sur une seconde ligne, la cause trouvée dans leurs logs.
2. Reviens à la révision **v1 stable**.
3. L'API doit répondre `api v1` avec 3 réplicas prêts.
