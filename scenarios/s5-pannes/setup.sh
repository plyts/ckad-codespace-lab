# Préparation de s5-pannes (CTX, NS, OUT fournis par le lanceur)
k(){ kubectl --context "$CTX" -n "$NS" "$@"; }

k create configmap orders-config --from-literal=DBHOST=db
k apply -f - <<'EOF'
apiVersion: apps/v1
kind: Deployment
metadata: {name: orders}
spec:
  replicas: 1
  selector: {matchLabels: {app: orders}}
  template:
    metadata: {labels: {app: orders}}
    spec:
      containers:
      - name: orders
        image: busybox:1.37
        command: ["sh", "-c", "echo DB=$DB_HOST; sleep 3600"]
        env:
        - name: DB_HOST
          valueFrom: {configMapKeyRef: {name: orders-config, key: DB_HOST}}
---
apiVersion: apps/v1
kind: Deployment
metadata: {name: payments}
spec:
  replicas: 1
  selector: {matchLabels: {app: payments}}
  template:
    metadata: {labels: {app: payments}}
    spec:
      containers:
      - {name: payments, image: "hashicorp/http-echo:1.0.0", args: ["-text=payments ok"], ports: [{containerPort: 5678}]}
---
apiVersion: v1
kind: Service
metadata: {name: payments}
spec:
  selector: {app: payment}
  ports: [{port: 80, targetPort: 5678}]
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata: {name: uploads}
spec:
  accessModes: [ReadWriteOnce]
  storageClassName: fast
  resources: {requests: {storage: 50Mi}}
---
apiVersion: v1
kind: Pod
metadata: {name: uploader}
spec:
  volumes: [{name: up, persistentVolumeClaim: {claimName: uploads}}]
  containers:
  - {name: uploader, image: "busybox:1.37", command: ["sh", "-c", "sleep 3600"], volumeMounts: [{name: up, mountPath: /uploads}]}
EOF
