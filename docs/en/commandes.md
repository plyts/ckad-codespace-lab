---
title: kubectl commands
color: gris
---
# kubectl commands, one by one

Grouped by purpose. Each output is a real capture on the running-scenario application (namespace
`guide`).

```text
 explore         create           modify               observe             security / context
 get, describe   run, create,     edit, patch,         logs, exec,         auth can-i,
 explain,        apply, expose    set image/env/       events, top         config use-context
 api-resources                    resources, scale,
                                  label, annotate,
                                  rollout, delete
```

## Explore

| Command | What it does | Useful options |
|---|---|---|
| `get` | List | `-o wide`, `-o yaml`, `-o jsonpath=…`, `-o custom-columns=…`, `-l`, `-L`, `--show-labels`, `-A`, `-w` |
| `describe` | Details and **events** | for anything that does not start |
| `explain` | Field documentation | `--recursive` |
| `api-resources` | Short names, groups, namespaced or not | `--api-group=…`, `--namespaced=false` |

{{capture:get-labels}}

## Create

| Command | Creates |
|---|---|
| `run` | a Pod (`--image`, `--labels`, `--port`, `--env`, `--command -- …`, `--rm -it` for a throwaway Pod) |
| `create deployment\|job\|cronjob\|configmap\|secret\|service\|ingress\|role\|rolebinding\|quota\|serviceaccount` | the named object |
| `expose` | a Service in front of a Deployment, Pod or ReplicaSet |
| `apply -f` / `apply -k` | from a file / a Kustomize directory |

Always with `$do` (`--dry-run=client -o yaml`) when the YAML needs editing:

{{capture:create-deploy-dry}}

## Modify

| Command | Example |
|---|---|
| `edit` | `k edit deploy api` (opens vim) |
| `patch` | `k patch svc web -p '{"spec":{"selector":{"app":"web"}}}'`; `--type=json` to replace a list item |
| `set image` | `k set image deploy/front front=nginx:1.28-alpine` |
| `set env` | `k set env deploy/api --from=secret/db --prefix=DB_` |
| `set resources` | `k set resources deploy/api --requests=cpu=50m --limits=memory=64Mi` |
| `set serviceaccount` | `k set serviceaccount deploy/api monitor` |
| `scale` | `k scale deploy api --replicas=3` |
| `label` / `annotate` | `k label pod web tier=front`; `k annotate deploy x kubernetes.io/change-cause='…'` |
| `rollout` | `status`, `history`, `undo [--to-revision=N]`, `restart`, `pause`, `resume` |
| `replace --force -f` | delete and recreate (immutable Pod fields) |
| `delete` | `k delete pod web $now` to go fast (only when it is safe) |

{{capture:scale}}

## Observe

{{capture:logs}}

{{capture:exec}}

{{capture:events}}

## Security and contexts

{{capture:auth-can-i}}

{{capture:contexts}}

## Speed reflexes

```bash
alias k=kubectl                                  # already there in the exam
export do="--dry-run=client -o yaml"             # k create deploy x --image=y $do > x.yaml
export now="--force --grace-period 0"            # k delete pod x $now
k config set-context --current --namespace=d1-04 # default namespace of the current context
k explain pod.spec --recursive | less            # / to search in less
k get pods -o jsonpath='{.items[*].metadata.name}'
yq '.spec.template.spec.containers[0].image' deploy.yaml   # yq is installed in the exam (jq is not)
```

In vim: `:set paste` before pasting a YAML block, `>>` / `<<` to indent a line, `V` then `>` for a
block, `u` to undo.

:::examen
Copy-paste in the exam terminal: **Ctrl+Shift+C / Ctrl+Shift+V**. In Firefox: Ctrl+C / Ctrl+V.
:::
