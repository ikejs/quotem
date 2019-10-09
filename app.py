# -*- coding: utf-8 -*-9


from flask import Flask, render_template, request
from dotenv import load_dotenv
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId
import pprint

app = Flask(__name__, static_url_path='')

# MongoDB location & secret key
app.config['MONGO_URI'] = 'mongodb://localhost:27017/quotem'
app.config['SECRET_KEY'] = 'shhhhhhhhhhhhhhhhhhhhhhhhhhhhh'
mongo = PyMongo(app)
db = mongo.db

# Title string placed after each page name
title = " | Quotem - Quotes for days 🤡".decode('utf-8')

@app.route('/')
def index():
    tags = db["tags"].find({ 'featured': True })
    popularQuotesList = db["quotes"].aggregate([
    {
        "$project" : { "likes_count": { "$size": { "$ifNull": [ "$likes", [] ] } } }
    },
    {
        "$sort":  { "likes_count": -1 }
    },
    {
        "$limit": 4
    }
    ])
    popularQuotes = []
    for quote in popularQuotesList:
        quoteObj = db["quotes"].find_one({ '_id': quote['_id'] })
        authorObj = db["users"].find_one({ '_id': ObjectId(quoteObj['author']) })
        popularQuotes.append([quoteObj, authorObj])
    recentQuotesList = db["quotes"].find().sort([('_id', -1)]).limit(4)
    recentQuotes = []
    for quote in recentQuotesList:
        quoteObj = db["quotes"].find_one({ '_id': quote['_id'] })
        authorObj = db["users"].find_one({ '_id': ObjectId(quoteObj['author']) })
        recentQuotes.append([quoteObj, authorObj])
    return render_template(
        'index.html',
        title='Home' + title,
        popularQuotes=popularQuotes,
        recentQuotes=recentQuotes,
        tags=tags,
        index=True,
        active='index'
        )


@app.route('/popular')
def popular():
    tags = db["tags"].find({ 'featured': True })
    popularQuotesList = db["quotes"].aggregate([
    {
        "$project" : { "likes_count": { "$size": { "$ifNull": [ "$likes", [] ] } } }
    },
    {
        "$sort":  { "likes_count": -1 }
    }
    ])
    popularQuotes = []
    for quote in popularQuotesList:
        quoteObj = db["quotes"].find_one({ '_id': quote['_id'] })
        authorObj = db["users"].find_one({ '_id': ObjectId(quoteObj['author']) })
        popularQuotes.append([quoteObj, authorObj])
    return render_template(
        'popular.html',
        title='Popular Quotes' + title,
        popularQuotes=popularQuotes,
        tags=tags,
        index=True,
        active='popular'
        )


@app.route('/recent')
def recent():
    tags = db["tags"].find({ 'featured': True })
    recentQuotesList = db["quotes"].find().sort([('_id', -1)])
    recentQuotes = []
    for quote in recentQuotesList:
        quoteObj = db["quotes"].find_one({ '_id': quote['_id'] })
        authorObj = db["users"].find_one({ '_id': ObjectId(quoteObj['author']) })
        recentQuotes.append([quoteObj, authorObj])
    return render_template(
        'recent.html',
        title='Popular Quotes' + title,
        recentQuotes=recentQuotes,
        tags=tags,
        index=True,
        active='recent'
        )

@app.route('/tags')
def tags():
    # https://stackoverflow.com/questions/9040161/mongo-order-by-length-of-array
    # Sort by tag with the most quotes, limit to 10
    tagsList = db["tags"].aggregate([
    {
        "$project" : { "quotes_count": { "$size": { "$ifNull": [ "$quotes", [] ] } } }
    },
    {
        "$sort": { "quotes_count": -1 }
    },
    {
        "$limit": 10
    }
    ])
    tags = []
    for tag in tagsList:
        tags.append(db["tags"].find_one({'_id': tag['_id']}))
    return render_template(
        'tags.html',
        title='tags' + title,
        tags=tags
        )


@app.route('/tag/<slug>')
def tag(slug):
    tag = db['tags'].find_one({ 'slug': slug })
    quotesList = db['quotes'].find({ 'tags': { '$in' : [ str(tag['_id']) ]}})
    quotes=[]
    for quote in quotesList:
        quotes.append([quote, db.users.find_one({ '_id': ObjectId(quote['author']) })])
    return render_template(
        'tag.html',
        tag=tag,
        quotes=quotes,
        title=tag['name'] + ' Quotes' + title
        )


@app.route('/signup')
def signup():
    return render_template(
    'signup.html',
    title='Sign Up' + title
    )



@app.route('/login')
def login():
    return render_template(
    'login.html',
    title='Login' + title
    )





if __name__ == '__main__':
    app.run(debug=True)
