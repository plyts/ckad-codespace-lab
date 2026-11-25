# Préparation de d4-08 (CTX, NS, OUT fournis par le lanceur)
kubectl --context "$CTX" apply -f - <<'EOF'
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  name: backups.lab.ckad.io
spec:
  group: lab.ckad.io
  scope: Namespaced
  names: {plural: backups, singular: backup, kind: Backup, shortNames: [bk]}
  versions:
  - name: v1
    served: true
    storage: true
    schema:
      openAPIV3Schema:
        type: object
        properties:
          spec:
            type: object
            required: [schedule]
            properties:
              schedule: {type: string}
              retention: {type: integer, minimum: 1}
EOF
kubectl --context "$CTX" wait --for=condition=Established crd/backups.lab.ckad.io --timeout=30s
# Established ne suffit pas : le schéma OpenAPI (kubectl explain) est publié quelques secondes après.
for i in $(seq 1 60); do kubectl --context "$CTX" explain backup.spec >/dev/null 2>&1 && break; sleep 1; done
