---
title: Journal des erreurs
color: gris
---
# Journal des erreurs

Chaque entrée a été **provoquée volontairement** dans le namespace `journal` par
`scripts/capture-docs.sh journal`, et sa sortie est réelle. Les entrées marquées *rencontrée* sont
des erreurs survenues par accident pendant la construction du labo.

{{capture:err-overview}}

## E1 · CrashLoopBackOff *(provoquée)*

Exercices : `d3-04`, `s3-jour3`.

{{capture:err-crashloop}}

- **En clair** : le conteneur démarre puis s'arrête ; le kubelet le relance en espaçant les
  essais (back-off).
- **Cause** : la commande sort avec un code non nul (ici `exit 1` ; 127 = commande introuvable).
- **Diagnostic** : `k describe pod` (Last State, Exit Code), `k logs <pod> --previous`.
- **Correction** : corriger la commande, la configuration ou ce qui manque, puis vérifier
  `RESTARTS` stable et `READY 1/1`.
- **L'éviter** : tester la commande avec `k run t --rm -it --image=… -- sh`.

## E2 · ImagePullBackOff / ErrImagePull *(provoquée)*

Exercices : `d2-04`, `d3-05`.

{{capture:err-imagepull}}

- **Cause** : image ou tag inexistant, registre privé sans `imagePullSecrets`, faute de frappe.
- **Correction** : `k set image deploy/<d> <conteneur>=<image:tag>`.

## E3 · CreateContainerConfigError *(provoquée)*

Exercice : `s5-pannes`.

{{capture:err-configerror}}

- **Cause** : une variable référence une ConfigMap ou une clé absente (ou un Secret absent).
- **Correction** : créer la clé (ou rendre la référence `optional: true` si c'est voulu).

## E4 · Pod Pending : FailedScheduling *(provoquée)*

Exercices : `d3-06`, `m4-07`.

{{capture:err-pending}}

- **Cause** : requests impossibles (64 CPU), nodeSelector ou affinité sans nœud correspondant,
  taint non toléré, PVC non lié.
- **Correction** : corriger la spec du Pod (`k replace --force -f`).

## E5 · OOMKilled *(provoquée)*

{{capture:err-oomkilled}}

- **Cause** : le conteneur dépasse sa limite mémoire (ici 32Mi) ; code de sortie 137.
- **Correction** : augmenter `limits.memory` ou réduire la consommation.

## E6 · FailedMount *(provoquée)*

{{capture:err-failedmount}}

- **Cause** : le Secret ou la ConfigMap montée en volume n'existe pas ; le Pod reste
  `ContainerCreating`.
- **Correction** : créer l'objet, le Pod démarre alors tout seul.

## E7 · Forbidden (RBAC) *(provoquée)*

Exercices : `d4-07`, `s6-panne-rbac`.

{{capture:err-forbidden}}

- **Diagnostic** : le message donne l'identité, le verbe, la ressource et le namespace.
- **Correction** : un Role et un RoleBinding minimaux ; vérifier avec `k auth can-i … --as=…`.

## E8 · Invalid *(provoquée)*

{{capture:err-invalid}}

Et un YAML mal indenté, refusé avant même l'API :

{{capture:err-yaml}}

- **L'éviter** : générer le YAML (`$do`), indenter avec 2 espaces, `k apply --dry-run=server -f`.

## E9 · Service sans Endpoints *(provoquée)*

Exercices : `d5-04`, `s5-pannes`, `m1-06`.

{{capture:err-noendpoints}}

- **Cause** : le sélecteur du Service ne correspond à aucun Pod prêt.
- **Correction** : aligner sélecteur et labels (`k get pods --show-labels`).

## E10 · Connection refused *(provoquée)*

{{capture:err-refused}}

- **Cause** : Endpoints présents mais `targetPort` faux (rien n'écoute sur 8080) ; ou
  l'application n'écoute pas sur l'interface attendue.
- **Correction** : `targetPort` = `containerPort` réel.

## E11 · NetworkPolicy qui bloque trop *(provoquée)*

Exercices : `d5-07`, `s4-jour4`.

{{capture:err-netpol}}

- **Cause** : une politique `Egress` sans règle coupe tout, y compris le DNS (port 53) : le nom
  `web` ne se résout plus.
- **Correction** : autoriser le DNS (UDP et TCP 53) en plus des destinations voulues.

## Erreurs rencontrées pendant la construction du labo *(rencontrées)*

| N° | Erreur | Cause | Correction |
|---|---|---|---|
| R1 | `kubelet is configured to not run on a host using cgroup v1` | Kubernetes ≥ 1.35 refuse cgroup v1 par défaut | `failCgroupV1: false`, appliqué par `lab` seulement si l'hôte est en cgroup v1 |
| R2 | `runc create failed: … failed to update /proc/self/oom_score_adj: Permission denied` | hôte sans `CAP_SYS_RESOURCE` | `restrict_oom_score_adj = true` dans containerd, seulement si détecté |
| R3 | `ctr: content digest sha256:… not found` sur `kind load docker-image` | Docker ≥ 29 et son magasin d'images containerd n'exportent qu'une plateforme | import de la seule plateforme locale dans chaque nœud (`lab`) |
| R4 | namespace bloqué en `Terminating` : `stale GroupVersion discovery: metrics.k8s.io/v1beta1` | metrics-server installé sans son image | installer metrics-server seulement si l'image est disponible |
| R5 | `serviceaccount "default" not found` juste après la création d'un namespace | course avec le contrôleur des ServiceAccounts | attendre le ServiceAccount `default` avant de créer des Pods |
| R6 | `429 Too Many Requests` de Docker Hub | limite de débit anonyme | repli sur le miroir `mirror.gcr.io` |
| R7 | après un redémarrage de Docker, DNS `bad address` et Traefik qui ne joint plus l'API (x509) | règles réseau du nœud périmées juste après le redémarrage | `lab wake` : relancer CoreDNS, puis Traefik |
| R8 | Traefik `Pending` pendant un redémarrage progressif | le `hostPort` 80 n'existe qu'une fois par nœud | `strategy: Recreate` pour Traefik |
| R9 | chemin d'Ingress `Exact` servi par `/` | Traefik classe les routes par longueur de règle | chemins `Prefix` dans le cours ; noté comme piège |
