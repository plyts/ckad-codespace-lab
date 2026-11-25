# Contrôles de d5-02 (sourcé après lib/check.sh)
ck_eq "Type NodePort" "NodePort" 'jp svc web-np "{.spec.type}"' \
  "kubectl expose … --type=NodePort." "kubectl -n $NS get svc"
ck_eq "nodePort 30080" "30080" 'jp svc web-np "{.spec.ports[0].nodePort}"' \
  "kubectl expose ne permet pas de choisir le nodePort : édite le Service ou écris le YAML (plage 30000-32767)." "kubectl -n $NS get svc web-np -o yaml | grep -A5 ports"
ck_http "Accessible via l'IP d'un nœud sur 30080" "$NS" "" "http://$(k get nodes -o jsonpath='{.items[0].status.addresses[?(@.type=="InternalIP")].address}'):30080" "Welcome to nginx" \
  "Un NodePort ouvre le même port sur tous les nœuds." "kubectl get nodes -o wide"
