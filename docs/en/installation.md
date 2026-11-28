---
title: The lab
color: gris
---
# 0 · The lab

## What runs in your Codespace

```text
Codespace (Debian container, Docker-in-Docker)
├── kind: cluster ckad-a  ─ 1 control-plane + 2 workers ─ Kubernetes v1.37
│          └── Traefik (Ingress), metrics-server, kindnet (CNI + NetworkPolicy)
├── kind: cluster ckad-b  ─ 1 node (lab up b): practise switching contexts
├── bin/: lab, ex, mock, site
└── ~/ckad/<id>/: your answer files
```

Why kind: one configuration file per cluster, one command to recreate a clean one (`lab reset`),
several clusters and contexts like in the exam, and a Kubernetes version chosen by the node image.

{{capture:lab-status}}

## The two configurations

| Configuration | What for |
|---|---|
| `CKAD lab` | Working: VS Code, terminal, guide on port 8000 |
| `CKAD exam` | Timed practice: remote Linux desktop (port 6080), a terminal and Firefox, no extensions |

:::examen
In the exam, every task starts with an `ssh <host>` to a machine where `kubectl`, the `k` alias,
bash completion, `yq`, `curl` and `wget` are ready. In the lab, `lab ssh ckad-a` opens a shell that
only knows that cluster. Type `exit` to come back, like in the exam.
:::

## Contexts: the first reflex

{{capture:contexts}}

```bash
kubectl config use-context ckad-a
```

:::piege The wrong context
The most expensive mistake in the exam: doing a task right… on the wrong cluster. The check finds
nothing and the task scores 0. `ex check` warns you when your current context is not the exercise's.
:::

## The shell, set up like in the exam

`postCreate` adds to `~/.bashrc`:

```bash
alias k=kubectl
source <(kubectl completion bash)
complete -o default -F __start_kubectl k
export do="--dry-run=client -o yaml"     # k run web --image=nginx $do > web.yaml
export now="--force --grace-period 0"    # k delete pod web $now
```

and to `~/.vimrc`: `set expandtab tabstop=2 shiftwidth=2 autoindent`. In vim, the Insert key is
forbidden in the exam: use `i`.

## Are NetworkPolicies really enforced?

A CNI that ignores NetworkPolicies lets everything through, and a networking exercise looks solved
while proving nothing. So `lab up` runs this real test: a Pod reaches nginx, then a `deny-all` rule
must cut the traffic.

{{capture:netpol-test}}

If the test fails on your cluster, blocked-traffic checks show as **SKIP** (grey), never as a false
PASS.

## Lab commands

| Command | Effect |
|---|---|
| `lab up [a\|b\|all]` | Creates the cluster(s), preloads images, installs Traefik and metrics-server, tests NetworkPolicies |
| `lab reset a` | Destroys and recreates `ckad-a` (about 3 minutes) |
| `lab wake` | After a sleep: restarts nodes, DNS (CoreDNS) and Ingress |
| `lab status` | Versions, clusters, nodes |
| `bash scripts/doctor.sh` | Checks there is no AI, the versions and the clusters |

## Your first Pod, right now

```bash
ex start d1-01
```

Type your answer, then run `ex check d1-01`. If something is missing, the script says what and why
(the lab's messages follow the language chosen with `ex lang en`):

{{capture:check-fail}}

Once the Pod is created:

{{capture:check-pass}}
