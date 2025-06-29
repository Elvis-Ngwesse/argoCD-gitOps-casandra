*********************
To Test on Your Local
*********************
---
## ⚙️ Run MongoDB Using Docker
```bash
docker run -d --name mongodb -p 27017:27017 mongo:latest
```
---
### 📄 Build minio-url-app and customer-app Image
```bash
COMMIT_SHA=$(git rev-parse --short HEAD)

docker buildx build \
  --platform linux/amd64 \   # or `linux/arm64` depending on your machine
  -t dockerelvis/customer-app:latest \
  -t dockerelvis/customer-app:$COMMIT_SHA \
  -f docker/Dockerfile \
  . \
  --load

echo $COMMIT_SHA

COMMIT_SHA=$(git rev-parse --short HEAD)

docker buildx build \
  --platform linux/amd64,linux/arm64 \
  -t dockerelvis/minio-url-app:latest \
  -t dockerelvis/minio-url-app:$COMMIT_SHA \
  -f docker2/Dockerfile \
  . \
  --load
echo $COMMIT_SHA
```

---
### Build and run containers
- docker run --rm -p 5003:5000 dockerelvis/customer-app:$COMMIT_SHA
- - docker run --rm -p 5004:5002 dockerelvis/minio-url-app:$COMMIT_SHA
---

---
### 📄 Build and push Minio-url-app Image
```bash

# Multi platform
docker buildx create --use

COMMIT_SHA=$(git rev-parse --short HEAD)
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  -t dockerelvis/minio-url-app:latest \
  -t dockerelvis/minio-url-app:$COMMIT_SHA \
  -f docker2/Dockerfile . --push
echo $COMMIT_SHA

```

## 📄 Build & Push Argocd-App Image
```bash
docker build -t dockerelvis/customer-app:latest -f docker/Dockerfile .
docker login
docker push dockerelvis/customer-app:latest

# Multi platform
docker buildx create --use
COMMIT_SHA=$(git rev-parse --short HEAD)
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  -t dockerelvis/customer-app:latest \
  -t dockerelvis/customer-app:$COMMIT_SHA \
  -f docker/Dockerfile . --push
echo $COMMIT_SHA

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