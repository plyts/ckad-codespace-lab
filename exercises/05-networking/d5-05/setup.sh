# Préparation de d5-05 (CTX, NS, OUT fournis par le lanceur)
k(){ kubectl --context "$CTX" -n "$NS" "$@"; }
k apply -f - <<'EOF'
apiVersion: apps/v1
kind: Deployment
metadata: {name: front}
spec:
  replicas: 1
  selector: {matchLabels: {app: front}}
  template:
    metadata: {labels: {app: front}}
    spec:
      containers:
      - {name: front, image: "hashicorp/http-echo:1.0.0", args: ["-text=front"], ports: [{containerPort: 5678}]}
---
apiVersion: v1
kind: Service
metadata: {name: front}
spec:
  selector: {app: front}
  ports: [{port: 80, targetPort: 5678}]
---
apiVersion: apps/v1
kind: Deployment
metadata: {name: api}
spec:
  replicas: 1
  selector: {matchLabels: {app: api}}
  template:
    metadata: {labels: {app: api}}
    spec:
      containers:
      - {name: api, image: "hashicorp/http-echo:1.0.0", args: ["-text=api"], ports: [{containerPort: 5678}]}
---
apiVersion: v1
kind: Service
metadata: {name: api}
spec:
  selector: {app: api}
  ports: [{port: 8080, targetPort: 5678}]
EOF
