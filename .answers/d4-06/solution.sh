#!/usr/bin/env bash
# Solution de référence : d4-06 — SecurityContext durci
kubectl config use-context ckad-a
cat > secure.yaml <<'EOF'
apiVersion: v1
kind: Pod
metadata:
  name: secure
  namespace: d4-06
spec:
  securityContext:            # niveau Pod
    runAsUser: 1000
    runAsGroup: 3000
    fsGroup: 2000
  containers:
  - name: secure
    image: busybox:1.37
    command: ["sh", "-c", "sleep 3600"]
    securityContext:          # niveau conteneur
      allowPrivilegeEscalation: false
      readOnlyRootFilesystem: true
      capabilities:
        drop: ["ALL"]
EOF
kubectl apply -f secure.yaml
kubectl -n d4-06 wait --for=condition=Ready pod/secure --timeout=60s
kubectl -n d4-06 exec secure -- id
