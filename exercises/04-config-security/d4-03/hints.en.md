## Hint 1

The ServiceAccount is one imperative command (`kubectl create serviceaccount --help`); the Pod needs YAML.

## Hint 2

In the Pod: `serviceAccountName: deployer` and `automountServiceAccountToken: false` under `spec`.

## Hint 3

That Pod field is immutable: delete and recreate the Pod if you got it wrong.

