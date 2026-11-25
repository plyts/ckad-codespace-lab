---
title: Cheatsheet
color: gris
---
# Cheatsheet CKAD (une page)

Uniquement des commandes disponibles sur les hôtes d'examen (`kubectl`, `k`, `yq`, `curl`,
`wget`, `vim`).

```bash
# — Début de tâche
ssh <hôte>                         # puis : k config current-context
k config use-context <ctx>
k config set-context --current --namespace=<ns>
export do="--dry-run=client -o yaml" now="--force --grace-period 0"

# — Générer
k run web --image=nginx:1.27-alpine --labels=app=web --port=80 $do > pod.yaml
k create deployment api --image=nginx --replicas=3 $do > deploy.yaml
k create job j --image=busybox:1.37 $do -- sh -c 'echo ok'
k create cronjob c --image=busybox:1.37 --schedule='*/5 * * * *' $do -- date
k create configmap cfg --from-literal=K=V --from-file=f.conf
k create secret generic s --from-literal=password='x'
k create serviceaccount sa
k create role r --verb=get,list --resource=pods,pods/log
k create rolebinding rb --role=r --serviceaccount=<ns>:sa
k create quota q --hard=pods=5,requests.cpu=1
k expose deploy api --port=80 --target-port=5678 [--type=NodePort]
k create ingress i --class=<classe> --rule='h.local/*=svc:80' --rule='h.local/api*=api:8080'

# — Modifier
k set image deploy/api api=nginx:1.28-alpine
k set env deploy/api --from=secret/s --prefix=DB_
k set resources deploy/api --requests=cpu=50m,memory=32Mi --limits=cpu=100m,memory=64Mi
k set serviceaccount deploy/api sa
k scale deploy api --replicas=5
k annotate deploy api kubernetes.io/change-cause='…'
k rollout status|history|undo [--to-revision=N]|restart deploy/api
k replace --force -f pod.yaml
k patch svc web -p '{"spec":{"selector":{"app":"web"}}}'

# — Diagnostiquer
k get pods -o wide --show-labels
k describe pod <p> | tail -20
k logs <p> [-c conteneur] [--previous] [--tail=20]
k get events --sort-by=.lastTimestamp
k exec -it <p> -- sh
k run t --rm -it --image=busybox:1.37 --restart=Never -- wget -qO- -T 3 http://svc.ns
k get endpointslices -l kubernetes.io/service-name=<svc>
k auth can-i list pods -n <ns> --as=system:serviceaccount:<ns>:<sa>
k top pods --sort-by=cpu
k explain deploy.spec.strategy --recursive
k api-resources | grep -i <mot>

# — Extraire
k get pod p -o jsonpath='{.status.podIP}'
k get pods -o custom-columns=N:.metadata.name,I:.spec.containers[0].image
yq '.spec.replicas' deploy.yaml ; yq -i '.spec.replicas = 3' deploy.yaml

# — Helm et Kustomize
helm -n ns install|upgrade rel ./chart --set k=v ; helm -n ns list|history|rollback rel 1
helm show values ./chart
k kustomize dir/ ; k apply -k dir/
```

| Je cherche… | Page de kubernetes.io à ouvrir |
|---|---|
| un YAML de sonde | Configure Liveness, Readiness and Startup Probes |
| une NetworkPolicy | Network Policies |
| un PVC et son Pod | Configure a Pod to Use a PersistentVolume for Storage |
| un securityContext | Configure a Security Context for a Pod or Container |
| un sidecar natif | Sidecar Containers |
| une LimitRange | Configure Default Memory Requests and Limits for a Namespace |
| une API retirée | Deprecated API Migration Guide |
