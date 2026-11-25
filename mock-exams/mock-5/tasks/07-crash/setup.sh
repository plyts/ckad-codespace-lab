# Préparation de m5-07 (CTX, NS, OUT fournis par le lanceur)
k(){ kubectl --context "$CTX" -n "$NS" "$@"; }
k apply -f - <<'EOF'
apiVersion: apps/v1
kind: Deployment
metadata: {name: notifier}
spec:
  replicas: 1
  selector: {matchLabels: {app: notifier}}
  template:
    metadata: {labels: {app: notifier}}
    spec:
      containers:
      - name: notifier
        image: busybox:1.37
        command: ["sh", "-c", "test -f /config/ready || exit 3; sleep 3600"]
EOF
