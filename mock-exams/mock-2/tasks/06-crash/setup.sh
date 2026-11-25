# Préparation de m2-06 (CTX, NS, OUT fournis par le lanceur)
k(){ kubectl --context "$CTX" -n "$NS" "$@"; }
k apply -f - <<'EOF'
apiVersion: apps/v1
kind: Deployment
metadata: {name: billing}
spec:
  replicas: 1
  selector: {matchLabels: {app: billing}}
  template:
    metadata: {labels: {app: billing}}
    spec:
      containers:
      - name: billing
        image: busybox:1.37
        command: ["sh", "-c", "test -f /config/ready || exit 3; sleep 3600"]
EOF
