# Préparation de m5-12 (CTX, NS, OUT fournis par le lanceur)
kubectl --context "$CTX" apply -f - <<'EOF'
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata: {name: pipelines.data.m5.lab}
spec:
  group: data.m5.lab
  scope: Namespaced
  names: {plural: pipelines, singular: pipeline, kind: Pipeline}
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
              source: {type: string}
EOF
kubectl --context "$CTX" wait --for=condition=Established crd/pipelines.data.m5.lab --timeout=30s
