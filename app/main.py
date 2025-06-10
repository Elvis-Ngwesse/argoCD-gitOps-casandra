from flask import Flask
from faker import Faker
from pymongo import MongoClient
import threading
import time
import uuid
import os

app = Flask(__name__)
fake = Faker()

# MongoDB connection URI (use env var or default localhost)
MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongo-service:27017")

# Connect to MongoDB
mongo_client = MongoClient(MONGO_URI)
db = mongo_client['customerdb']      # Database name
customers_collection = db['customers']  # Collection name

# Predefined food items
food_items = [
    "apple", "banana", "bread", "butter", "carrot", "cheese", "chicken", "chocolate",
    "coffee", "cookie", "egg", "fish", "grapes", "hamburger", "juice", "lettuce", "milk",
    "onion", "orange", "pasta", "pepper", "pizza", "potato", "rice", "salad", "soda",
    "steak", "tomato", "water", "yogurt", "beef", "turkey", "peach", "pear", "spinach",
    "broccoli", "cucumber", "mushroom", "mango", "blueberries", "strawberries", "pineapple",
    "avocado", "corn", "beans", "lentils", "tofu", "pancake", "waffle", "bacon", "sausage",
    "shrimp", "crab", "lobster", "noodles", "cereal", "granola", "kale", "zucchini", "plum",
    "cherry", "lemon", "lime", "bagel", "toast", "muffin", "donut", "syrup", "honey", "jam",
    "mustard", "ketchup", "mayonnaise", "pickles", "olives", "nachos", "taco", "burrito",
    "quinoa", "barley", "coconut", "almond", "walnut", "cashew", "hazelnut", "chili", "soup"
]

def generate_customer():
    while True:
        customer_id = str(uuid.uuid4())
        basket = [fake.random_element(elements=food_items) for _ in range(30)]
        customer_data = {
            "_id": customer_id,
            "username": fake.user_name(),
            "address": fake.address(),
            "status": fake.random_element(['active', 'inactive']),
            "country": fake.country(),
            "basket": basket,  # store as list directly
        }
        customers_collection.insert_one(customer_data)
        time.sleep(5)

@app.route('/')
def index():
    return '''
    <pre>
     _______           _                             _____                           _             
    |__   __|         | |                           / ____|                         | |            
       | | ___   ___ | | ___   _ _ __   ___ _ __   | |     ___  _ ____   _____ _ __ | |_ ___  _ __ 
       | |/ _ \ / _ \| |/ / | | | '_ \ / _ \ '__|  | |    / _ \| '_ \ \ / / _ \ '_ \| __/ _ \| '__|
       | | (_) | (_) |   <| |_| | |_) |  __/ |     | |___| (_) | | | \ V /  __/ | | | || (_) | |   
       |_|\___/ \___/|_|\_\\__, | .__/ \___|_|      \_____\___/|_| |_|\_/ \___|_| |_|\__\___/|_|   
                            __/ | |                                                              
                           |___/|_|       🚀 Customer Generator is Running...
    </pre>
    <p>Status: ✅ Active</p>
    <p>Generating fake customers every 5 seconds</p>
    '''

# Start background thread to generate customers
threading.Thread(target=generate_customer, daemon=True).start()

if __name__ == '__main__':
    print(r"""
  ____           _                   _                   _____                         
 / ___|___ _ __ | |_ _   _ _ __ ___ | |__   ___ _ __    |  ___|__  _ __ ___ ___  ___  
| |   / _ \ '_ \| __| | | | '_ ` _ \| '_ \ / _ \ '__|   | |_ / _ \| '__/ __/ _ \/ __| 
| |__|  __/ | | | |_| |_| | | | | | | |_) |  __/ |      |  _| (_) | | | (_|  __/\__ \ 
 \____\___|_| |_|\__|\__,_|_| |_| |_|_.__/ \___|_|      |_|  \___/|_|  \___\___||___/ 

🚀 Customer Generator Service is running at http://localhost:5000
""")
    app.run(host='0.0.0.0', port=5000)
