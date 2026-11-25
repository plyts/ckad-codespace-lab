#!/usr/bin/env bash
# Solution de référence : d1-02 — Job à complétions multiples
kubectl config use-context ckad-a
kubectl -n d1-02 create job counter --image=busybox:1.37 --dry-run=client -o yaml \
  -- sh -c 'echo traitement terminé' > job.yaml
# Ajouter sous spec: (au même niveau que template:) completions, parallelism, backoffLimit
cat > job.yaml <<'EOF'
apiVersion: batch/v1
kind: Job
metadata:
  name: counter
  namespace: d1-02
spec:
  completions: 3        # 3 Pods doivent réussir
  parallelism: 2        # 2 au plus en même temps
  backoffLimit: 2       # au plus 2 relances en cas d'échec
  template:
    spec:
      restartPolicy: Never   # Never ou OnFailure : obligatoire pour un Job
      containers:
      - name: counter
        image: busybox:1.37
        command: ["sh", "-c", "echo traitement terminé"]
EOF
kubectl apply -f job.yaml
kubectl -n d1-02 wait --for=condition=Complete job/counter --timeout=120s
