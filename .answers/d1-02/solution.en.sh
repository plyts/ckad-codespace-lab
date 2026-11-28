#!/usr/bin/env bash
# Reference solution: d1-02 — Job with several completions
kubectl config use-context ckad-a
kubectl -n d1-02 create job counter --image=busybox:1.37 --dry-run=client -o yaml \
  -- sh -c 'echo traitement terminé' > job.yaml
# Add under spec: (same level as template:) completions, parallelism, backoffLimit
cat > job.yaml <<'EOF'
apiVersion: batch/v1
kind: Job
metadata:
  name: counter
  namespace: d1-02
spec:
  completions: 3        # 3 Pods must succeed
  parallelism: 2        # at most 2 at the same time
  backoffLimit: 2       # at most 2 retries on failure
  template:
    spec:
      restartPolicy: Never   # Never or OnFailure: mandatory for a Job
      containers:
      - name: counter
        image: busybox:1.37
        command: ["sh", "-c", "echo traitement terminé"]
EOF
kubectl apply -f job.yaml
kubectl -n d1-02 wait --for=condition=Complete job/counter --timeout=120s
