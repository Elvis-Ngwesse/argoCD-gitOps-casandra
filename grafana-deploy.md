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