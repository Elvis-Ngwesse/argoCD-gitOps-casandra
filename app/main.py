from flask import Flask, jsonify
from faker import Faker
from pymongo import MongoClient
import threading
import time
import uuid
import os
import sys
import logging
from datetime import datetime
from prometheus_flask_exporter import PrometheusMetrics

# ---------------------------------------
# ✅ Logging Setup
# ---------------------------------------
logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger("customer-generator")

# ---------------------------------------
# 🌐 Flask App Setup
# ---------------------------------------
app = Flask(__name__)
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.INFO)

# ✅ Prometheus Metrics
metrics = PrometheusMetrics(app)

# ---------------------------------------
# 🧱 MongoDB Setup
# ---------------------------------------
MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongo-service:27017")
mongo_client = MongoClient(MONGO_URI)
db = mongo_client['customerdb']
customers_collection = db['customers']

logger.info("✅ Connected to MongoDB at %s", MONGO_URI)

# ---------------------------------------
# 🍎 Basket Items & Faker
# ---------------------------------------
fake = Faker()
food_items = [...]  # same food list (shortened here to save space, keep yours intact)

# ---------------------------------------
# 🔄 Background Generator
# ---------------------------------------
def generate_customer():
    logger.info("🧵 Starting background customer generation thread...")
    while True:
        customer_id = str(uuid.uuid4())
        basket = [fake.random_element(elements=food_items) for _ in range(30)]
        customer_data = {
            "_id": customer_id,
            "username": fake.user_name(),
            "address": fake.address(),
            "status": fake.random_element(['active', 'inactive']),
            "country": fake.country(),
            "basket": basket,
        }
        try:
            customers_collection.insert_one(customer_data)
            logger.info("🆕 Inserted customer: %s", customer_data["username"])
        except Exception as e:
            logger.error("❌ Failed to insert customer: %s", str(e))
        time.sleep(5)

# ---------------------------------------
# 🌍 Web UI Route
# ---------------------------------------
@app.route('/')
def index():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    location = fake.city()
    country = fake.country()
    app.logger.info("🌐 Page hit at %s from %s, %s", now, location, country)

    html = f'''...'''  # same HTML block you have (shortened here for brevity)
    return html

# ---------------------------------------
# ✅ Health Route for Kubernetes
# ---------------------------------------
@app.route('/healthz')
def health():
    return jsonify({"status": "ok"}), 200

# ---------------------------------------
# 🧾 Optional: Last Customer API
# ---------------------------------------
@app.route('/customers/latest')
def latest_customer():
    try:
        customer = customers_collection.find().sort([("_id", -1)]).limit(1)[0]
        return jsonify(customer)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ---------------------------------------
# 🚀 Run App
# ---------------------------------------
if __name__ == '__main__':
    logger.info("🚀 Customer Generator Service is starting on http://0.0.0.0:5000")
    threading.Thread(target=generate_customer, daemon=True).start()
    app.run(host='0.0.0.0', port=5000)
