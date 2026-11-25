# Préparation de m5-06 (CTX, NS, OUT fournis par le lanceur)
k(){ kubectl --context "$CTX" -n "$NS" "$@"; }
k apply -f - <<'EOF'
apiVersion: apps/v1
kind: Deployment
metadata: {name: profile-blue}
spec:
  replicas: 2
  selector: {matchLabels: {app: profile, color: blue}}
  template:
    metadata: {labels: {app: profile, color: blue}}
    spec:
      containers:
      - {name: profile-blue, image: "hashicorp/http-echo:1.0.0", args: ["-text=blue"], ports: [{containerPort: 5678}]}
---
apiVersion: apps/v1
kind: Deployment
metadata: {name: profile-green}
spec:
  replicas: 2
  selector: {matchLabels: {app: profile, color: green}}
  template:
    metadata: {labels: {app: profile, color: green}}
    spec:
      containers:
      - {name: profile-green, image: "hashicorp/http-echo:1.0.0", args: ["-text=green"], ports: [{containerPort: 5678}]}
---
apiVersion: v1
kind: Service
metadata: {name: profile}
spec:
  selector: {app: profile, color: blue}
  ports: [{port: 80, targetPort: 5678}]
EOF
k rollout status deploy/profile-blue --timeout=180s
k rollout status deploy/profile-green --timeout=180s
