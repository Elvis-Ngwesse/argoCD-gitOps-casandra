
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
--machine-type=e2-standard-4 \
--enable-ip-alias \
--enable-autoscaling \
--min-nodes=1 \
--max-nodes=4 \
--enable-autoupgrade \
--enable-autorepair \
--metadata disable-legacy-endpoints=true \
--workload-pool=argocd-project-1.svc.id.goog \
--labels=environment=test-stage,team=devops

✅ 3. Get Cluster Credentials
gcloud container clusters get-credentials argocd-cluster \
--zone=europe-west2-b

✅ 4. Get API Server URL
kubectl config view --minify -o jsonpath='{.clusters[0].cluster.server}'

✅ 5. Verify kubectl Access
kubectl config current-context
kubectl get nodes

✅ 6. Install Argo CD in a Namespace
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

✅ 7. Get Argo CD Initial Admin Password
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d; echo

✅ 8. Expose Argo CD via LoadBalancer or Ingress
kubectl port-forward svc/argocd-server -n argocd 8080:443

✅ 9. Login to Argo CD UI
Open the external IP in your browser: (https://localhost:8080)
Username: admin
Password: (from step 7 command)

✅ 10. Login to Argo CD CLI
argocd login localhost:8080 --username admin --password $(kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d)

✅ 11. Add repo
argocd repo add git@github.com:Elvis-Ngwesse/argoCD-mongodb.git \
--ssh-private-key-path ~/.ssh/id_rsa

✅ 12. Deploy Your App (Mongo + Flask)
argocd app create prod-app \
--repo git@github.com:Elvis-Ngwesse/argoCD-mongodb.git \
--path k8s/base \
--dest-server https://kubernetes.default.svc \
--dest-namespace test-stage \
--sync-policy automated \
--self-heal \
--sync-option CreateNamespace=true

✅ 13. Sync your app
argocd app sync prod-app

✅ Delete the cluster
gcloud container clusters delete argocd-cluster \
--zone=europe-west2-b

🕒 Scale node pool to zero
gcloud container clusters resize argocd-cluster \
--zone=europe-west2-b \
--node-pool=default-pool \
--num-nodes=2

gcloud compute machine-types list \
--filter="zone:europe-west2-b AND name~'e2'" \
--format="table(name, guestCpus, memoryMb)"


## ⌚ Access Apps
kubectl get svc flask-service -n test-stage
http://<external-ip>:5000
kubectl get svc flask-minio-service -n test-stage
http://<external-ip>:5002



| **Option**                     | **What it means**                                | **Recommended Setting**       | **Why / Notes**                                       |
|--------------------------------|--------------------------------------------------|-------------------------------|-------------------------------------------------------|
| **Revision**                   | Git branch, tag, or commit to sync from          | `main` or specific commit SHA | Choose the version of manifests you want deployed     |
| **PRUNE**                      | Delete resources removed from Git repo           | ✅ Enabled                     | Keeps cluster clean by removing deleted resources     |
| **DRY RUN**                    | Simulate sync without applying changes           | ❌ Disabled                    | You want to actually apply changes, not just simulate |
| **APPLY ONLY**                 | Only apply new/changed resources, no deletes     | ❌ Disabled                    | Allow pruning (deletes) to clean up removed resources |
| **FORCE**                      | Force apply by deleting & recreating resources   | ❌ Disabled (unless needed)    | Use only if normal apply fails or resources get stuck |
| **SKIP SCHEMA VALIDATION**     | Skip Kubernetes resource validation              | ❌ Disabled                    | Usually keep validation to avoid bad manifests        |
| **AUTO-CREATE NAMESPACE**      | Create namespace if it doesn’t exist             | ✅ Enabled (if needed)         | Helpful if deploying to a new namespace               |
| **PRUNE LAST**                 | Delete resources after applying changes          | ✅ Enabled                     | Safer deletion sequence                               |
| **APPLY OUT OF SYNC ONLY**     | Only apply if resource differs from Git manifest | ✅ Enabled                     | Speeds up sync by skipping unchanged resources        |
| **RESPECT IGNORE DIFFERENCES** | Honor ignoreDifferences settings                 | ✅ Enabled                     | Avoids unnecessary sync for ignored differences       |
| **SERVER-SIDE APPLY**          | Use Kubernetes server-side apply                 | ✅ Enabled                     | More reliable, recommended method                     |
| **PRUNE PROPAGATION POLICY**   | How deletes are propagated                       | `foreground` (default)        | Default safe setting for pruning resources            |
