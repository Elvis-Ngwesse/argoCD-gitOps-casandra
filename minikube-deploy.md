# 🚀 DevOps Setup & Deployment Guide

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

## 🔑 Get password 🌐 Port-forward Argo CD UI
```bash
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d; echo
kubectl port-forward svc/argocd-server -n argocd 8080:443
```
Access: (https://localhost:8080)

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
  --dest-namespace test-stage \
  --directory-recurse \
  --sync-policy automated \
  --sync-option CreateNamespace=true \
  --sync-option SelfHeal=true \
  --sync-option Prune=true

```

---
## ✅ Trigger First Sync
```bash
argocd app get test-app
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

* Use `minikube service customer-app` to access the deployed app.
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

