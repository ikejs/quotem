from flask import Flask, render_template
from dotenv import load_dotenv
from flask_pymongo import PyMongo
from bson.json_util import dumps

app = Flask(__name__, static_url_path='')

# MongoDB location
app.config['MONGO_URI'] = 'mongodb://localhost:27017/quotem'
mongo = PyMongo(app)
db = mongo.db
# Title string placed after each page name
title = " | Quotem - Quotes for days 🤡"

@app.route('/')
def index():
    featuredQuotes = db.quotes.aggregate([
    {
        "$project" : { "likes_count": { "$size": { "$ifNull": [ "$likes", [] ] } } }
    },
    {
        "$sort":  { "likes_count": 1 }
    }
    ])
    recentQuotes = db.quotes.find().sort([('_id', -1)])
    categories = db.categories.find({ 'featured': True })
    return render_template(
        'index.html',
        title='Home' + title,
        featuredQuotes=featuredQuotes,
        recentQuotes=recentQuotes,
        categories=categories,
        index=True
        )

@app.route('/categories')
def categories():
    # https://stackoverflow.com/questions/9040161/mongo-order-by-length-of-array
    # Sort by category with the most quotes
    categories = db.categories.aggregate([
    {
        "$project" : { "quotes_count": { "$size": { "$ifNull": [ "$quotes", [] ] } } }
    },
    {
        "$sort": { "quotes_count": 1 }
    }
    ])
    return render_template(
        'categories.html',
        title='Categories' + title,
        categories=dumps(categories)
        )

if __name__ == '__main__':
    app.run(debug=True)
