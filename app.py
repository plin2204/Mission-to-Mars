## 10.5.1: Use Flask to Create a Web App
from flask import Flask, render_template
from flask_pymongo import PyMongo
import scraping

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = Pymongo(app)

# Homepage
@app.route("/")
def index():
    # Uses PyMongo to find “mars” collection in our database, which created when we converted our Jupyter scraping code to Python Script
    mars = mongo.db.mars.find_one()
    # Tells Flask to return an HTML template using an index.html file
    return render_template("index.html", mars=mars) # mars=mars tells Python to use the “mars” collection in MongoDB

# Scrape route
@app.route("/scrape")
def scrape():
    # Assign a new variable that points to our Mongo database
    mars = mongo.db.mars
    # Create a new variable to hold the newly scraped data by using scraping.py
    mars_data = scraping.scrape_all()
    # Update database by .update(), and upsert=True, which tells Mongo to create a new document if one doesn’t already exist
    mars.update({}, mars_data, upsert=True)
    # Add a message to let us know that the scraping was successful
    return "Scraping Successful!"