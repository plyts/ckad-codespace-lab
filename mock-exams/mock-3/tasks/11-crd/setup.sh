# Préparation de m3-11 (CTX, NS, OUT fournis par le lanceur)
kubectl --context "$CTX" apply -f - <<'EOF'
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata: {name: maintenances.ops.m3.lab}
spec:
  group: ops.m3.lab
  scope: Namespaced
  names: {plural: maintenances, singular: maintenance, kind: Maintenance}
  versions:
  - name: v1alpha1
    served: true
    storage: true
    schema:
      openAPIV3Schema:
        type: object
        properties:
          spec:
            type: object
            properties:
              window: {type: string}
EOF
kubectl --context "$CTX" wait --for=condition=Established crd/maintenances.ops.m3.lab --timeout=30s
