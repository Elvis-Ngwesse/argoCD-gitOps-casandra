from flask import Flask
from faker import Faker
from cassandra.cluster import Cluster
import threading
import time
import uuid
import os

app = Flask(__name__)
fake = Faker()

# Get Cassandra host from environment variable or default to 'cassandra'
CASSANDRA_HOST = os.getenv('CASSANDRA_HOST', 'cassandra')

# Connect to Cassandra
cluster = Cluster([CASSANDRA_HOST])
session = cluster.connect()

# Create keyspace and table
session.execute("""
    CREATE KEYSPACE IF NOT EXISTS shop WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '1'}
""")
session.set_keyspace('shop')
session.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        id UUID PRIMARY KEY,
        username TEXT,
        address TEXT,
        status TEXT,
        country TEXT,
        basket LIST<TEXT>
    )
""")

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
        basket = [fake.random_element(elements=food_items) for _ in range(30)]
        session.execute("""
            INSERT INTO customers (id, username, address, status, country, basket)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (uuid.uuid4(), fake.user_name(), fake.address(), fake.random_element(['active', 'inactive']),
              fake.country(), basket))
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


# Start background thread
threading.Thread(target=generate_customer, daemon=True).start()

# ASCII startup banner
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
