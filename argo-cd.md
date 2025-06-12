
## ⚙️ Test using docker local host
- Install Mongodb Locally (Docker)
    - docker run -d --name mongodb -p 27017:27017 mongo:latest
- 🐳 Test It (In Docker)
     - docker build -t customer-generator -f docker/Dockerfile .
     - docker run -d --name customer-generator \
       --link mongodb:mongo \
       -p 5002:5000 \
       -e MONGO_URI="mongodb://mongo:27017/" \
       customer-generator
- Visit http://localhost:5002 to confirm it’s running.

## ✅ Query Mongo localhost
- docker exec -it mongodb mongosh
- show dbs;
- use customerdb;
- show collections;
- db.customers.find().pretty();
- db.customers.find({status: "active"}).pretty();
- db.customers.find().limit(5).pretty();

## 📖 Docker push
- Build and Push Docker Image
    docker build -t dockerelvis/argocd-app:latest -f docker/Dockerfile .
    docker login
    docker push dockerelvis/argocd-app:latest

## 👨‍🏫  Start Minikube
- Go to README.md file

## ⚙️  Install Argo CD
    kubectl create namespace argocd
    kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

## 🌐 Port-forward Argo CD UI
- kubectl port-forward svc/argocd-server -n argocd 8080:443
- Access: https://localhost:8080
# 🔑 Default Login
    Username: admin
    Password: kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d

## 🔗 Connect Git Repository
- argocd login localhost:8080

# ✅ Add repo
    argocd repo add git@github.com:Elvis-Ngwesse/argoCD-mongodb.git \
    --ssh-private-key-path ~/.ssh/id_rsa

# ✅ Create the app
    argocd app create python-mongodb-test \
    --repo git@github.com:Elvis-Ngwesse/argoCD-mongodb.git \
    --path k8s/test \
    --dest-server https://kubernetes.default.svc \
    --dest-namespace test \
    --sync-policy automated

# ✅ Enable prune, self-heal, and sync options
    argocd app set python-mongodb-test \
    --sync-policy automated \
    --self-heal \
    --sync-option CreateNamespace=true


# ✅ Trigger first sync
    argocd app sync python-mongodb-test

# ✅ Delete app
    argocd app delete python-mongo-app --cascade

# ✅ 🚀 Deploy with Argo CD
    Argo will auto-sync your manifests and deploy the app.

# ✅ 🛡️ Verify
    kubectl get pods
    kubectl get svc argocd-server -n argocd

# ✅ Use minikube service argocd-app to access the app.
    🔄 Make a Code Change
    Push to GitHub
    Argo CD syncs automatically and redeploys

# ✅ Get app history
    argocd app history python-mongodb-test

# ✅ Roll back deployment
    argocd app rollback python-mongodb-test 0


Metrics + Grafana for visibility
Ingress setup with TLS


# Build the image with a tag
docker build -t flask-minio-presigned .

# Load the image into Minikube's Docker daemon
minikube image load flask-minio-presigned

## 📖 Docker push flask-minio image
- Build and Push Docker Image
  docker build -t dockerelvis/presigned-app:latest -f docker2/Dockerfile .
  docker login
  docker push dockerelvis/presigned-app:latest

## Get pre-signed Url
- Use port forwarding
- kubectl port-forward svc/flask-minio-service 5002:80 -n test
- http://localhost:5002/presigned-urls
- enter in browser to download pre-signed url as below

{
"results/results_20250611224950.html": "http://minio-service:9000/test-reports/results/results_20250611224950.html?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=minioadmin%2F20250612%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20250612T054129Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=cdf6960de4923d4a6d7e1e48935e2c24ed6a0b472264345f3b19cecd915ff622",
"results/results_20250611224950.xml": "http://minio-service:9000/test-reports/results/results_20250611224950.xml?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=minioadmin%2F20250612%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20250612T054129Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=b436169b5d1cfe2cf8c8c6fc764ac85aaa38e21dd052785180e2da4733f41a4c"
}
- kubectl port-forward svc/minio-service 9000:9000 -n test
- wget "http://localhost:9000/test-reports/results/results_20250611224950.html?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=minioadmin%2F20250612%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20250612T054129Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=cdf6960de4923d4a6d7e1e48935e2c24ed6a0b472264345f3b19cecd915ff622"
- curl --resolve minio-service:9000:127.0.0.1 -o results.html "http://localhost:9000/test-reports/results/results_20250611224950.html?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=minioadmin%2F20250612%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20250612T054129Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=cdf6960de4923d4a6d7e1e48935e2c24ed6a0b472264345f3b19cecd915ff622"
