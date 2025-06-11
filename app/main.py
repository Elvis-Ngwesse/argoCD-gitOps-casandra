from flask import Flask
from faker import Faker
from pymongo import MongoClient
import threading
import time
import uuid
import os
from datetime import datetime

app = Flask(__name__)
fake = Faker()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongo-service:27017")
mongo_client = MongoClient(MONGO_URI)
db = mongo_client['customerdb']
customers_collection = db['customers']

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
            "basket": basket,
        }
        customers_collection.insert_one(customer_data)
        time.sleep(5)

@app.route('/')
def index():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    location = fake.city()
    country = fake.country()

    html = f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8" />
        <meta http-equiv="refresh" content="5">
        <title>Customer Generator Status</title>
        <style>
            body {{
                background-color: #87CEEB; /* sky blue */
                font-family: Arial, sans-serif;
                color: #03396c;
                text-align: center;
                padding: 50px;
            }}
            h1 {{
                font-size: 4em;   /* bigger text */
                margin-bottom: 0;
            }}
            p {{
                font-size: 2em;   /* bigger text */
                margin: 15px 0;
            }}
            .symbols {{
                font-size: 3em;  /* bigger symbols */
                margin-top: 20px;
            }}
            .box {{
                background: rgba(255, 255, 255, 0.7);
                padding: 25px;
                border-radius: 15px;
                display: inline-block;
                margin-top: 20px;
                box-shadow: 2px 2px 8px rgba(0,0,0,0.2);
            }}
        </style>
    </head>
    <body>
        <div class="box">
            <h1>🚀 Customer Generator</h1>
            <p>Status: ✅ Active and Running</p>
            <p>Current Date & Time: <strong>{now}</strong></p>
            <p>Location: <strong>{location}</strong></p>
            <p>Country: <strong>{country}</strong></p>
            <div class="symbols">
                &#127822; &#127823; &#127824; &#127825; &#127826; &#127827;
            </div>
            <p>Generating fake customers every 5 seconds...</p>
        </div>
    </body>
    </html>
    '''
    return html

# Start customer generation in a background thread
threading.Thread(target=generate_customer, daemon=True).start()

if __name__ == '__main__':
    print("Customer Generator Service is running at http://localhost:5000")
    app.run(host='0.0.0.0', port=5000)
