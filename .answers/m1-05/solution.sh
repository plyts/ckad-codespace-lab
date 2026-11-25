#!/usr/bin/env bash
# Solution de référence : m1-05 — Pod non root
kubectl config use-context ckad-a

cat > hardened.yaml <<'EOF'
apiVersion: v1
kind: Pod
metadata: {name: hardened, namespace: m1-05}
spec:
  securityContext:
    runAsUser: 2000
    runAsNonRoot: true
  containers:
  - name: app
    image: busybox:1.37
    command: ["sh", "-c", "sleep 3600"]
    securityContext:
      allowPrivilegeEscalation: false
      capabilities:
        drop: ["ALL"]
        add: ["NET_BIND_SERVICE"]
EOF
kubectl apply -f hardened.yaml
kubectl -n m1-05 wait --for=condition=Ready pod/hardened --timeout=60s
