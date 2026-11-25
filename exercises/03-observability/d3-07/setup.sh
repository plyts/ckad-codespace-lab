# Préparation de d3-07 (CTX, NS, OUT fournis par le lanceur)
mkdir -p "$OUT"
cat > "$OUT/old.yaml" <<'EOF'
apiVersion: batch/v1beta1
kind: CronJob
metadata:
  name: cleanup
  namespace: d3-07
spec:
  schedule: "0 3 * * *"
  jobTemplate:
    spec:
      template:
        spec:
          restartPolicy: OnFailure
          containers:
          - name: cleanup
            image: busybox:1.37
            command: ["sh", "-c", "echo nettoyage"]
---
apiVersion: policy/v1beta1
kind: PodDisruptionBudget
metadata:
  name: web-pdb
  namespace: d3-07
spec:
  minAvailable: 1
  selector:
    matchLabels:
      app: web
EOF
