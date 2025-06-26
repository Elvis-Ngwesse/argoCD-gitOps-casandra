## Documentation Part 1: Flask App → Prometheus → Grafana
Flask app exposes metrics on a Prometheus-compatible endpoint (/metrics on port 8001), which are scraped by 
Prometheus and visualized in Grafana.
# Workflow
- Flask app uses the prometheus_client Python library to expose metrics on /metrics (port 8001). 
- Prometheus automatically discovers pods via Kubernetes service discovery and scrapes their metrics endpoints. 
- Metrics are stored in Prometheus’s time-series database. 
- Grafana queries Prometheus to build dashboards and alerts.
# Key Concepts in Prometheus Scrape Config
- kubernetes_sd_configs: Enables Prometheus to discover all pods in the cluster automatically. 
- Namespace filter: Only pods in the test namespace are considered (regex: test). 
- Label filter: Limits scraping to pods labeled app as one of argocd-app, flask-minio, minio, or mongo. 
- Annotation filter: Only pods annotated with prometheus.io/scrape: "true" are scraped. This annotation is important 
to avoid scraping all pods. 
- Dynamic path and port: The metrics endpoint path and port are extracted from pod annotations 
(prometheus.io/path, prometheus.io/port) to allow flexibility. 
- Target rewriting: The final scrape target URL is constructed from the pod IP and port.
# Add these annotations in your pod or deployment manifest:
---
annotations:
    prometheus.io/scrape: "true"
    prometheus.io/port: "8001"
    prometheus.io/path: "/metrics"
---


## Documentation Part 2: Flask App → Grafana Agent → Loki → Grafana
- Flask app outputs structured logs to stdout, which are collected by Grafana Agent and shipped to Loki for 
centralized log storage and querying. Grafana then visualizes logs alongside metrics.
# Workflow
- Flask app writes logs to stdout in a format compatible with Loki. 
- Grafana Agent runs as a DaemonSet on each node, scraping logs from pod log files and scraping Prometheus metrics. 
- Grafana Agent forwards logs to Loki, which stores and indexes them efficiently. 
- Grafana connects to Loki as a datasource and allows log queries, filtering, and dashboards alongside metrics.
# Key Points
- Logs are discovered and scraped based on Kubernetes metadata and pod labels. 
- Metrics scraped by Grafana Agent supplement the Prometheus metrics pipeline or provide an alternative. 
- Loki retention and storage are managed via persistent storage and compaction. 
- Grafana provisions the Loki datasource automatically for seamless integration.
# Metrics scraping:
- Uses Kubernetes service discovery (role: pod) to find pods in test and logging namespaces. 
- Filters pods by labels: flask-minio, argocd-app, or minio. 
- Scrapes metrics on specific container ports (8001, 8002, 9000, 9001). 
- Builds scrape target URLs dynamically from pod IP and container port.
# Logs scraping:
- Tracks log reading positions in /tmp/positions.yaml to avoid re-reading logs. 
- Collects logs from pods matching specific namespaces and labels. 
- Reads pod container logs from /var/log/containers/ on nodes.
- Sends logs to Loki service endpoint.


## Quick overview before we dive in
- Each pod runs one or more containers.
- Containers write logs to stdout and stderr.
- The container runtime (like containerd or Docker) captures these logs and stores them on the node's filesystem.
- Kubernetes exposes logs via kubectl logs by reading those files.
- On each node, logs for pods are usually stored under /var/log/containers/ and /var/log/pods/.
- Logs in /var/log/containers/ are symlinks to files under /var/log/pods/ or container runtime log paths.