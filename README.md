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


