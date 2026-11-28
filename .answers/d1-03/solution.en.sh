#!/usr/bin/env bash
# Reference solution: d1-03 — Backup CronJob
kubectl config use-context ckad-a
kubectl -n d1-03 create cronjob backup --image=busybox:1.37 --schedule='*/5 * * * *' \
  --dry-run=client -o yaml -- sh -c 'echo sauvegarde' > cj.yaml
# Add the three fields under the CronJob's spec:
cat > cj.yaml <<'EOF'
apiVersion: batch/v1
kind: CronJob
metadata:
  name: backup
  namespace: d1-03
spec:
  schedule: "*/5 * * * *"
  concurrencyPolicy: Forbid
  successfulJobsHistoryLimit: 2
  failedJobsHistoryLimit: 1
  jobTemplate:
    spec:
      template:
        spec:
          restartPolicy: OnFailure
          containers:
          - name: backup
            image: busybox:1.37
            command: ["sh", "-c", "echo sauvegarde"]
EOF
kubectl apply -f cj.yaml
# Test without waiting 5 minutes: kubectl -n d1-03 create job test --from=cronjob/backup
