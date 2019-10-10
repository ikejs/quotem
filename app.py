# -*- coding: utf-8 -*-9

from flask import Flask, render_template, request, redirect
from dotenv import load_dotenv
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId
import os
import pprint

host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/Quotem')
client = MongoClient(host=f'{host}?retryWrites=false')
data_b = client.get_default_database()
db = data_b.db

app = Flask(__name__)

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
        title='Recent Quotes' + title,
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
    tags = db["tags"].find({ 'featured': True })
    tag = db['tags'].find_one({ 'slug': slug })
    quotesList = db['quotes'].find({ 'tags': { '$in' : [ str(tag['_id']) ]}})
    quotes=[]
    for quote in quotesList:
        quotes.append([quote, db.users.find_one({ '_id': ObjectId(quote['author']) })])
    return render_template(
        'tag.html',
        tag=tag,
        tags=tags,
        quotes=quotes,
        title=tag['name'] + ' Quotes' + title
        )


@app.route('/u/<username>')
def user(username):
    tags = db["tags"].find({ 'featured': True })
    user = db['users'].find_one({ 'username': username })
    quotesList = db['quotes'].find({ 'author': str(user['_id']) }).sort([('_id', -1)])
    quotes=[]
    for quote in quotesList:
        quotes.append([quote, user])
    return render_template(
        'user.html',
        user=user,
        quotes=quotes,
        tags=tags,
        title=user['name'] +  "'s Quotes'" + title
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


@app.route('/new', methods=['GET', 'POST'])
def new():
    if request.method == 'GET':
        tags = db["tags"].find({ 'featured': True })
        if request.args.get('user'):
            user = db.users.find_one({ 'username': request.args.get('user') })
            return render_template(
            'new.html',
            title='New Quote' + title,
            user=user,
            tags=tags,
            index=True
            )
    elif request.method == 'POST':
        quote = {
            'author': request.form.get('userId'),
            'quote': request.form.get('quote'),
            'likes': [],
            'requotes': [],
            'tags': []
        }
        inserttedQuote = db.quotes.insert_one(quote)
        print(inserttedQuote)
        return redirect('/')


@app.route('/edit/<quoteId>')
def edit(quoteId):
    tags = db["tags"].find({ 'featured': True })
    quote = db["quotes"].find_one({ '_id': ObjectId(quoteId) })
    user = db.users.find_one({ '_id': ObjectId(quote['author']) })
    return render_template(
    'edit.html',
    title='Edit Quote' + title,
    user=user,
    tags=tags,
    quote=quote,
    index=True
    )


@app.route('/edit/<quoteId>', methods=['POST'])
def post_edit(quoteId):
    quote = db["quotes"].find_one({ '_id': ObjectId(quoteId) })
    user = db.users.find_one({ '_id': ObjectId(quote['author']) })
    quoteObj = {
        'quote': request.form.get('quote'),
        'author': str(user["_id"])
    }
    db["quotes"].update_one(
        {'_id': ObjectId(quote['_id'])},
        {'$set': quoteObj })
    return redirect("/u/"+user['username'])


@app.route('/delete/<quoteId>', methods=['POST'])
def post_delete(quoteId):
    db['quotes'].delete_one({'_id': ObjectId(quoteId)})
    return redirect('/u/ikeholzmann')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))
