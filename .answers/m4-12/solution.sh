#!/usr/bin/env bash
# Solution de référence : m4-12 — SecurityContext
kubectl config use-context ckad-b

cat > runner.yaml <<'EOF'
apiVersion: v1
kind: Pod
metadata: {name: runner, namespace: m4-12}
spec:
  securityContext:
    runAsUser: 1500
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
kubectl apply -f runner.yaml
kubectl -n m4-12 wait --for=condition=Ready pod/runner --timeout=60s
