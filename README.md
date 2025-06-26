## argoCD-gitOps-casandra
Deploy a Python FastAPI app with a Cassandra database using Kubernetes and Argo CD. Learn GitOps, 
containerization, and declarative infrastructure in a hands-on, cloud-native setup ideal for DevOps 
and platform engineering skills.

## 📖 What is Argo CD?
Argo CD is a declarative, GitOps continuous delivery tool for Kubernetes. It Monitors Git repositories 
for Kubernetes manifests. Synchronizes Kubernetes clusters with the Git state.
Offers a web UI and CLI for application lifecycle management.

## 🧰 Prerequisites
Install the following (all open-source):
- Minikube (local Kubernetes cluster)
- kubectl
- GitHub account
- Argo CD CLI
- Docker

## 🏗️ Project Structure
argoCD-gitOps-casandra/
├── app/
│   ├── main.py
│   └── requirements.txt
├── docker/
│   ├── Dockerfile
├── k8s/
│   ├── deployment.yaml
│   ├── service.yaml
│   └── cassandra.yaml
├── manifests/
│   ├── app.yaml  # Argo CD application manifest
├── README.md


## Create venv
- python3 -m venv venv
- source myenv/bin/activate
- deactivate

## install argocd
- sudo curl -sSL -o /usr/local/bin/argocd https://github.com/argoproj/argo-cd/releases/latest/download/argocd-darwin-arm64
- sudo chmod +x /usr/local/bin/argocd
- argocd version

## 👨‍🏫  Start Minikube
- minikube start --nodes 3
- kubectl get nodes
- minikube ssh --node=minikube
- minikube ssh --node=minikube-m02
- minikube ssh --node=minikube-m03

# Taint the master node so it won't run workloads:
- kubectl taint nodes minikube node-role.kubernetes.io/master=:NoSchedule

# 🚀 (Optional) Enable Dashboard and Ingress
- minikube addons enable dashboard
- minikube addons enable ingress

# 📊 Open Minikube Dashboard
- minikube dashboard

# 🗑️ Delete Minikube
- minikube stop minikube delete --all
- minikube delete --all --purge

# 🔧 Uninstall 
- brew uninstall minikube
  minikube delete --all
  rm -rf ~/.minikube
  rm -rf ~/.kube
# 📦 Install minikube
- brew install minikube

# 📦 Install gcp
- https://cloud.google.com/sdk/docs/install
- gcloud components install kubectl 
- gcloud auth login 
- gcloud config set account aws.gcp.devops.elvis@gmail.com
- gcloud projects create argocd-project-1 \
  --name="Argo CD MongoDB Demo"
- gcloud billing accounts list
- gcloud beta billing projects link argocd-project-1 \
  --billing-account=YOUR_BILLING_ACCOUNT_ID
- gcloud config set project argocd-project-1

✅ 1. Enable Required APIs
gcloud services enable \
container.googleapis.com \
compute.googleapis.com \
iam.googleapis.com

✅ 2. Create a GKE Cluster
gcloud container clusters create argocd-cluster \
--zone=europe-west2-b \
--num-nodes=2 \
--machine-type=e2-medium \
--enable-ip-alias \
--enable-autoscaling \
--min-nodes=1 \
--max-nodes=4 \
--enable-autoupgrade \
--enable-autorepair \
--metadata disable-legacy-endpoints=true \
--workload-pool=argocd-project-1.svc.id.goog \
--labels=environment=production,team=devops

✅ 3. Get Cluster Credentials
gcloud container clusters get-credentials argocd-cluster \
--zone=europe-west2-b

✅ 4. Verify kubectl Access
kubectl config current-context
kubectl get nodes

✅ 5. Install Argo CD in a Namespace
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

✅ 6. Get Argo CD Initial Admin Password
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d; echo

✅ 7. Expose Argo CD via LoadBalancer or Ingress
kubectl port-forward svc/argocd-server -n argocd 8080:443

✅ 8. Login to Argo CD UI
Open the external IP in your browser: (https://localhost:8080)
Username: admin
Password: (from step 7 command)

✅ 9. Login to Argo CD CLI
argocd login localhost:8080 --username admin --password $(kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d)

✅ 10. Add repo
argocd repo add git@github.com:Elvis-Ngwesse/argoCD-mongodb.git \
--ssh-private-key-path ~/.ssh/id_rsa

✅ 11. Deploy Your App (Mongo + Flask)
argocd app create prod-app \
--repo git@github.com:Elvis-Ngwesse/argoCD-mongodb.git \
--path k8s/prod \
--dest-server https://kubernetes.default.svc \
--dest-namespace prod \
--sync-policy automated \
--self-heal \
--sync-option CreateNamespace=true

✅ Delete the cluster
gcloud container clusters delete argocd-cluster \
--zone=europe-west2-b

🕒 Scale node pool to zero
gcloud container clusters resize argocd-cluster \
--zone=europe-west2-b \
--node-pool=default-pool \
--num-nodes=0
