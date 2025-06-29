# 🚀 DevOps Setup & Deployment Guide


*********************
To Test on Your Local
*********************
---
## ⚙️ Run MongoDB Using Docker
```bash
docker run -d --name mongodb -p 27017:27017 mongo:latest
```
---
### 📄 Push Flask-MinIO Presigned Image
```bash
# Build the image
docker build -t flask-minio-presigned .
# Load image into Minikube
docker save flask-minio-presigned | minikube image load -
```
---
### 📄 Push Flask-MinIO Image
```bash
docker build -t dockerelvis/presigned-app:latest -f docker2/Dockerfile .
docker login
docker push dockerelvis/presigned-app:latest

# Multi platform
docker buildx create --use

minio_version=$(git rev-parse --short HEAD)-$(date +%Y%m%d%H%M%S)
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  -t dockerelvis/report-url-generator:latest \
  -t dockerelvis/report-url-generator:$minio_version \
  -f docker2/Dockerfile \
  . \
  --push

 - echo $minio_version
 - The image is not stored locally. It's built remotely (via buildx) and pushed directly to Docker Hub.
 - docker pull dockerelvis/presigned-app:latest to test locally
 - docker run --rm -p 5004:5002 dockerelvis/argocd-app:latest

```

## 📄 Build & Push Argocd-App Image
```bash
docker build -t dockerelvis/argocd-app:latest -f docker/Dockerfile .
docker login
docker push dockerelvis/argocd-app:latest

# Multi platform
docker buildx create --use

argocd_version=$(git rev-parse --short HEAD)-$(date +%Y%m%d%H%M%S)
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  -t dockerelvis/customer-app:latest \
  -t dockerelvis/customer-app:$argocd_version \
  -f docker/Dockerfile \
  . \
  --push

 - echo $argocd_version
 - The image is not stored locally. It's built remotely (via buildx) and pushed directly to Docker Hub.
 - docker pull dockerelvis/argocd-app:latest to test locally
 - docker run --rm -p 5002:5000 dockerelvis/argocd-app:latest

```
---
### 📄 Build and Run Flask-Customer Container
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
Visit: [http://localhost:5002]
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
********************
## 💻 Start Minikube
********************
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

Access: (https://localhost:8080)
### 🔑 Get password

```bash
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d; echo
```

### 🔑 Default Login
```bash
argocd login localhost:8080 --username admin --password $(kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d)
```

---
## 🔗 Connect Git Repository
```bash
argocd repo add git@github.com:Elvis-Ngwesse/argoCD-mongodb.git \
  --ssh-private-key-path ~/.ssh/id_rsa
```

---
## ✅ Create the App
```bash
argocd app create test-app \
  --repo https://github.com/Elvis-Ngwesse/argoCD-mongodb.git \
  --path k8s/test \
  --revision HEAD \
  --dest-server https://kubernetes.default.svc \
  --dest-namespace test-env \
  --sync-policy automated \
  --self-heal \
  --auto-prune \
  --directory-recurse \
  --sync-option CreateNamespace=true

```

---
## ✅ Trigger First Sync
```bash
argocd app sync test-app
```
---

## ✅ Delete App
```bash
argocd app delete test-app --cascade
argocd app sync test-app --prune
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

## ⌚ Access Apps
minikube service grafana -n logging --url 
    username: admin
    password: admin
minikube service flask-service -n test --url
minikube service prometheus -n logging --url
    go to /targets
minikube service loki -n logging --url
minikube service flask-service -n test --url
---
> End of Deployment Guide ✨


📦 Deployment Plan (Incremental Testing)
--------------
| Step | Component          | Dependency                  | Purpose                                           |
|------|--------------------|-----------------------------|---------------------------------------------------|
| 1    | Loki               | None                        | Central log storage and query engine              |
| 2    | Promtail           | Loki                        | Collect logs from nodes → send to Loki            |
| 3    | Grafana Agent      | Loki, Prometheus (optional) | Scrape app logs/metrics → send to Loki/Prometheus |
| 4    | Prometheus         | Grafana Agent               | Scrape metrics from Grafana Agent                 |
| 5    | Grafana (optional) | All                         | Visualize logs and metrics                        |

---
## Grafana “Create Dashboard”
🟢 “Add visualization”
🟢 “Add a library panel”
🟢 “Import a dashboard”

Click on: Add visualization
🟩 1. Select Data Source: Choose your Prometheus
🟩 2. Click on Code on
🟩 3. Enter query:
        process_resident_memory_bytes / 1024 / 1024
        sum by (instance) (process_resident_memory_bytes) / 1024 / 1024
🟩 4. Click on Run Queries
🟩 5. You can select Time Range at the top
🟩 6. On the right, choose one:
        Time series: Shows memory usage over time
        Stat: Shows total memory per instance as a single number
        Table: Shows memory per instance in a table
🟩 7. Configure Display
        Panel Title: Process Memory by Instance
        Click Standard options
        Choose Data → bytes
🟩 8. Click “Apply” (top right)
🟩 9. Click the disk/save icon to save your dashboard
🟩 10. Name it: Process Memory Dashboard
✅ Done!
---