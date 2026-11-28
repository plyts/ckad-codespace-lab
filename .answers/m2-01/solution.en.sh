#!/usr/bin/env bash
# Reference solution: m2-01 — CronJob and manual run
kubectl config use-context ckad-a

kubectl -n m2-01 create cronjob report --image=busybox:1.37 --schedule='30 1 * * *' \
  --dry-run=client -o yaml -- sh -c 'date' > report.yaml
yq -i '.spec.concurrencyPolicy = "Replace" | .spec.successfulJobsHistoryLimit = 5' report.yaml
kubectl apply -f report.yaml
kubectl -n m2-01 create job report-manual --from=cronjob/report
kubectl -n m2-01 wait --for=condition=Complete job/report-manual --timeout=120s
