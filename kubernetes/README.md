# Notes

Files that could be used to deploy this application in kubernetes


Scratch commands:
```
k create namespace fastapi
k annotate namespace/fastapi istio-injection=enabled
kubens fastapi
kubectl create secret generic aws-secret --from-env-file=.env
k apply -f deployment.yaml
k apply -f service-mesh.yaml
```