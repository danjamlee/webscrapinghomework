from flask_pymongo import PyMongo
from flask import Flask, render_template
import scrape2


app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Or set inline
# mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")


@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars=mars)


@app.route("/scrape")
def scrape_data():
    mars = mongo.db.mars
    mars_data = scrape2.scrape()
    mars.update({}, mars_data, upsert=True)
    return "How do I return to the scraped page?"

if __name__ == "__main__":
    app.run()
