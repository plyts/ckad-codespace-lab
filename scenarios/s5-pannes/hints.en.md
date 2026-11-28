## Hint 1

`kubectl -n pannes get pods`: each status (CreateContainerConfigError, Pending) points the diagnosis.

## Hint 2

`kubectl -n pannes describe pod -l app=orders` and `kubectl -n pannes describe pvc uploads`: read the Events.

## Hint 3

For the PVC: `kubectl -n pannes get pvc uploads -o yaml > pvc.yaml`, change the class to `standard`, then delete and recreate PVC and Pod.

