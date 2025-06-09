
## ⚙️ Test Locally Without Kubernetes
- Install Cassandra Locally (Docker)
    - docker run --name cassandra -d -p 9042:9042 cassandra:4.0
- Set Environment Variable in main.py
- Make sure Cassandra connects to localhost:
- cluster = Cluster(['localhost'])
- Create Virtual Environment and Install Dependencies
     - python3 -m venv venv 
     - source venv/bin/activate 
     - pip install -r app/requirements.txt
- 🧪 Test It (Locally)
     - python app/main.py
- 🐳 Test It (In Docker)
     - docker build -t customer-generator -f docker/Dockerfile .
     - docker run --rm -p 5002:5000 \
       --link cassandra \
       -e CASSANDRA_HOST=cassandra \
       customer-generator

- Visit http://localhost:5002 to confirm it’s running.

## ✅ Query Cassandra
- docker exec -it cassandra cqlsh
- USE shop;
- SELECT id, username, basket FROM customers LIMIT 5;
- DESCRIBE TABLE customers;

## 📖 GitOps Deployment
- Build and Push Docker Image

docker build -t your-dockerhub-username/autoshopper:latest .
docker push your-dockerhub-username/autoshopper:latest

Step 2: Start Minikube

minikube start

Step 3: Install Argo CD

kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

Step 4: Port-forward Argo CD UI

kubectl port-forward svc/argocd-server -n argocd 8080:443

Access: https://localhost:8080

Default login:

Username: admin

Password: run:

kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d

Step 5: Connect Git Repo

Login to Argo CD UI.

Create a new app:

Repo URL: your GitHub repo

Path: k8s

Cluster: in-cluster

Namespace: default

Step 6: Deploy with Argo CD

Argo will auto-sync your manifests and deploy the app.

Step 7: Verify

kubectl get pods
kubectl get svc autoshopper

Use minikube service autoshopper to access the app.

🔄 Make a Code Change

Change something in main.py

Push to GitHub

Argo CD syncs automatically and redeploys

Let me know if you'd like:

Helm charts version

Metrics + Grafana for visibility

Ingress setup with TLS

This setup gives students full hands-on experience with GitOps, containers, microservices, and cloud-native tech—all locally and free.