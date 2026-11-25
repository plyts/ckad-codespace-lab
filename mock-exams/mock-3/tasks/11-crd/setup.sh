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
# Established ne suffit pas : le schéma OpenAPI (kubectl explain) est publié quelques secondes après.
for i in $(seq 1 60); do kubectl --context "$CTX" explain maintenance.spec >/dev/null 2>&1 && break; sleep 1; done
