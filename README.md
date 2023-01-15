# Build Docker Image
```
docker build -t api-exam . 
```

# Push image to registry
```
docker login registry.firegroup.com -u username-xxx -p password-xxx
docker tag api-exam:latest registry.firegroup.com/api-exam:v1.0
docker push registry.firegroup.com/api-exam:v1.0
```

# Deploy Kubernetes
## Assuming the ingress-nginx and metallb had been installed in kubernetes cluster
```
helm registry login registry.firegroup.com --username username-xxx --password password-xxx
helm package chart --version v1.0
helm push api-exam-v1.0.tgz oci://registry.firegroup.com/api-exam
helm upgrade --install api-exam oci://registry.firegroup.com/api-exam --version v1.0 --namespace exam --values chart/values.yml
```
# Checking Kubernetes objects
```
kubectl get pod -n exam
kubectl get svc -n exam
kubectl get ingress -n exam
```
# How to use api
Mapping domain exam.firegroup.com IP loadbalance on ingress-nginx
Excuting curl command
```
Curl https://exam.firegroup.com/exam
```
The result should be success then repose as below:
```
[
  "20230115-1014",
  "true"
]
```




