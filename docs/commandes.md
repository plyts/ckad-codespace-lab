---
title: Commandes kubectl
color: gris
---
# Les commandes kubectl, une par une

Regroupées par usage. Chaque sortie est une capture réelle sur l'application fil conducteur
(namespace `guide`).

```text
 explorer        créer            modifier             observer            sécurité / contexte
 get, describe   run, create,     edit, patch,         logs, exec,         auth can-i,
 explain,        apply, expose    set image/env/       events, top         config use-context
 api-resources                    resources, scale,
                                  label, annotate,
                                  rollout, delete
```

## Explorer

| Commande | À quoi elle sert | Options utiles |
|---|---|---|
| `get` | Lister | `-o wide`, `-o yaml`, `-o jsonpath=…`, `-o custom-columns=…`, `-l`, `-L`, `--show-labels`, `-A`, `-w` |
| `describe` | Détail et **événements** | pour tout ce qui ne démarre pas |
| `explain` | Documentation des champs | `--recursive` |
| `api-resources` | Noms courts, groupes, namespaced ou non | `--api-group=…`, `--namespaced=false` |

{{capture:get-labels}}

## Créer

| Commande | Crée |
|---|---|
| `run` | un Pod (`--image`, `--labels`, `--port`, `--env`, `--command -- …`, `--rm -it` pour un Pod jetable) |
| `create deployment\|job\|cronjob\|configmap\|secret\|service\|ingress\|role\|rolebinding\|quota\|serviceaccount` | l'objet nommé |
| `expose` | un Service devant un Deployment, un Pod ou un ReplicaSet |
| `apply -f` / `apply -k` | depuis un fichier / un dossier Kustomize |

Toujours avec `$do` (`--dry-run=client -o yaml`) quand il faut retoucher le YAML :

{{capture:create-deploy-dry}}

## Modifier

| Commande | Exemple |
|---|---|
| `edit` | `k edit deploy api` (ouvre vim) |
| `patch` | `k patch svc web -p '{"spec":{"selector":{"app":"web"}}}'` ; `--type=json` pour remplacer un élément de liste |
| `set image` | `k set image deploy/front front=nginx:1.28-alpine` |
| `set env` | `k set env deploy/api --from=secret/db --prefix=DB_` |
| `set resources` | `k set resources deploy/api --requests=cpu=50m --limits=memory=64Mi` |
| `set serviceaccount` | `k set serviceaccount deploy/api monitor` |
| `scale` | `k scale deploy api --replicas=3` |
| `label` / `annotate` | `k label pod web tier=front` ; `k annotate deploy x kubernetes.io/change-cause='…'` |
| `rollout` | `status`, `history`, `undo [--to-revision=N]`, `restart`, `pause`, `resume` |
| `replace --force -f` | supprimer et recréer (champs immuables d'un Pod) |
| `delete` | `k delete pod web $now` pour aller vite (seulement quand c'est sûr) |

{{capture:scale}}

## Observer

{{capture:logs}}

{{capture:exec}}

{{capture:events}}

## Sécurité et contextes

{{capture:auth-can-i}}

{{capture:contexts}}

## Réflexes de vitesse

```bash
alias k=kubectl                                  # déjà là à l'examen
export do="--dry-run=client -o yaml"             # k create deploy x --image=y $do > x.yaml
export now="--force --grace-period 0"            # k delete pod x $now
k config set-context --current --namespace=d1-04 # namespace par défaut du contexte courant
k explain pod.spec --recursive | less            # / pour chercher dans less
k get pods -o jsonpath='{.items[*].metadata.name}'
yq '.spec.template.spec.containers[0].image' deploy.yaml   # yq est installé à l'examen (jq ne l'est pas)
```

Dans vim : `:set paste` avant de coller un bloc YAML, `>>` / `<<` pour indenter une ligne,
`V` puis `>` pour un bloc, `u` pour annuler.

:::examen
Copier-coller dans le terminal d'examen : **Ctrl+Maj+C / Ctrl+Maj+V**. Dans Firefox :
Ctrl+C / Ctrl+V.
:::
