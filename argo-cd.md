# 🚀 DevOps Setup & Deployment Guide

---

## ⚙️ Run MongoDB Using Docker

```bash
docker run -d --name mongodb -p 27017:27017 mongo:latest
```

---

## 🧪 Test App in Docker

```bash
# Build the image
docker build -t customer-generator -f docker/Dockerfile .

# Run the container
docker run -d --name customer-generator \
  --link mongodb:mongo \
  -p 5002:5000 \
  -e MONGO_URI="mongodb://mongo:27017/" \
  customer-generator
```

Visit: [http://localhost:5002](http://localhost:5002)

---

## 📊 Query MongoDB Locally

```bash
docker exec -it mongodb mongosh
```

MongoDB Shell Commands:

```bash
show dbs;
use customerdb;
show collections;
db.customers.find().pretty();
db.customers.find({status: "active"}).pretty();
db.customers.find().limit(5).pretty();
```

---

## 📄 Build & Push Docker Image

```bash
docker build -t dockerelvis/argocd-app:latest -f docker/Dockerfile .
docker login
docker push dockerelvis/argocd-app:latest
```

---

## 💻 Start Minikube

Refer to `README.md` for Minikube setup instructions.

---

## ⚙️ Install Argo CD

```bash
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

---

## 🌐 Port-forward Argo CD UI

```bash
kubectl port-forward svc/argocd-server -n argocd 8080:443
```

Access: [https://localhost:8080](https://localhost:8080)

### 🔑 Default Login

```bash
Username: admin
Password:
  kubectl -n argocd get secret argocd-initial-admin-secret \
  -o jsonpath="{.data.password}" | base64 -d
```

---

## 🔗 Connect Git Repository

```bash
argocd login localhost:8080

argocd repo add git@github.com:Elvis-Ngwesse/argoCD-mongodb.git \
  --ssh-private-key-path ~/.ssh/id_rsa
```

---

## ✅ Create the App

```bash
argocd app create python-mongodb-test \
  --repo git@github.com:Elvis-Ngwesse/argoCD-mongodb.git \
  --path k8s/test \
  --dest-server https://kubernetes.default.svc \
  --dest-namespace test \
  --sync-policy automated
```

---

## ✅ Enable Prune, Self-Heal, and Sync Options

```bash
argocd app set python-mongodb-test \
  --sync-policy automated \
  --self-heal \
  --sync-option CreateNamespace=true
```

---

## ✅ Trigger First Sync

```bash
argocd app sync python-mongodb-test
```

---

## ✅ Delete App

```bash
argocd app delete python-mongo-app --cascade
```

---

## ✅ 🚀 Deploy with Argo CD

Argo CD will auto-sync your manifests and deploy the app.

---

## ✅ 🛡️ Verify Deployment

```bash
kubectl get pods
kubectl get svc argocd-server -n argocd
```

---

## ✅ Access App via Minikube

* Use `minikube service argocd-app` to access the deployed app.
* Make a code change and push to GitHub.
* Argo CD will automatically sync and redeploy.

---

## ✅ Get App History

```bash
argocd app history python-mongodb-test
```

---

## ✅ Rollback Deployment

```bash
argocd app rollback python-mongodb-test 0
```

---

## 📚 Flask MinIO Presigned URL Setup

```bash
# Build the image
docker build -t flask-minio-presigned .

# Load image into Minikube
docker save flask-minio-presigned | minikube image load -
```

### 📄 Push Flask-MinIO Image

```bash
docker build -t dockerelvis/presigned-app:latest -f docker2/Dockerfile .
docker login
docker push dockerelvis/presigned-app:latest
```

---

## ✉️ Get Pre-Signed URL

```bash
kubectl port-forward svc/flask-minio-service 5002:80 -n test
```

Visit: [http://localhost:5002/presigned-urls](http://localhost:5002/presigned-urls)

Example response:

```json
{
  "results/results_20250611224950.html": "http://minio-service:9000/test-reports/...",
  "results/results_20250611224950.xml": "http://minio-service:9000/test-reports/..."
}
```

---

## 💾 Download Test Results from Pre-Signed URLs

```bash
kubectl port-forward svc/minio-service 9000:9000 -n test

curl --resolve minio-service:9000:127.0.0.1 -o results.html "http://minio-service:9000/test-reports/..."
curl --resolve minio-service:9000:127.0.0.1 -o results.xml "http://minio-service:9000/test-reports/..."
```

---

## 🔒 Access MinIO via Client

```bash
kubectl port-forward svc/minio-service 9002:9001 -n test
```

Login:

* **Username**: `minioadmin`
* **Password**: `minioadmin`

Download test results from the MinIO web interface.

---

## ⌚ Metrics + Grafana for Visibility

> Set up monitoring using Grafana. Configure Prometheus scrapers if needed.

---

## 🌐 Ingress with TLS

> Configure ingress rules and TLS certificates for secure external access.

---
> End of Deployment Guide ✨
