#!/usr/bin/env bash
# Solution de référence : d1-03 — CronJob de sauvegarde
kubectl config use-context ckad-a
kubectl -n d1-03 create cronjob backup --image=busybox:1.37 --schedule='*/5 * * * *' \
  --dry-run=client -o yaml -- sh -c 'echo sauvegarde' > cj.yaml
# On ajoute les trois champs sous spec du CronJob :
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
# Tester sans attendre 5 minutes : kubectl -n d1-03 create job test --from=cronjob/backup
