# Build Docker Image
```
docker build -t api-exam . 
```

# Push image to registry
```
docker login registry.firegroup.exam -u username-xxx -p password-xxx
docker tag api-exam:latest registry.firegroup.exam/api-exam:v1.0
docker push registry.firegroup.exam/api-exam:v1.0
```

# Deploy Kubernetes
```
helm registry login registry.firegroup.exam --username username-xxx --password password-xxx
helm package chart --version v1.0
helm push api-exam-v1.0.tgz oci://registry.firegroup.exam/api-exam
helm upgrade --install api-exam oci://registry.firegroup.exam/api-exam --version v1.0 --namespace exam --values chart/values.yml
```
# Checking Kubernetes objects
```
kubectl get pod -n exam
kubectl get svc -n exam
kubectl get ingress -n exam
```




