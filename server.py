""" server.py """
from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient

import json


MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017

app = Flask(__name__)
app.config.from_object(__name__)
app.config['MONGO_DBNAME'] = "mainAPP"

#connection = MongoClient('localhost', 27017)
connection = MongoClient(app.config['MONGODB_HOST'], app.config['MONGODB_PORT'])

@app.route('/')
def index():
    pass

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/users/', methods=['GET'])
def show_users():
    db = connection['mainAPP'] 
    collection = db.users
    users = collection.find()
    existing_users = []
    
    for user in users:
        usr = {'username': str(user['username']),
               'email': str(user['email']),
               'skills': user['skills']}
        existing_users.append(usr)

    return render_template("index.html", existingUsers=json.dumps(existing_users))
  
@app.route('/<username>')
def show_users_stuff(username):
    db = connection['mainAPP'] 
    collection = db.users
    users = collection.find_one({"username": str(username)})
    app.logger.info(users)
    if users:
        usr = {'username': str(username),
               'email': str(users['email']),
               'skills': users['skills']}

        return render_template("user.html", existingUser=json.dumps(usr))
    else:
        return "not found!"


@app.route('/<username>/add_skill', methods=['GET', 'POST'])
def add_user_skill(username):
    db = connection['mainAPP']
    collection = db.users
    user = collection.find_one({"username": str(username)})

    if user and request.method == 'POST':
        user[u'skills'].append(request.json)
        collection.update({"username": str(username)}, {"$set": user}, upsert=False)

    return "aa"

@app.route('/<username>/remove_skill', methods=['GET', 'POST'])
def remove_user_skill(username):
    db = connection['mainAPP']
    collection = db.users
    user = collection.find_one({"username": str(username)})

    if user and request.method == 'POST':
        for skill in user[u'skills']:
            if skill.keys()[0] == request.data:
                user[u'skills'].remove(skill)
                collection.update({"username": str(username)}, {"$set": user}, upsert=False)
    return "aa"

@app.route('/<username>/add_todo', methods=['GET', 'POST'])
def add_skill_todo(username):
    db = connection['mainAPP']
    collection = db.users
    user = collection.find_one({"username": str(username)})
    
    if user and request.method == 'POST':
        skill_in_use = request.json['skill_in_use']
        new_todo = request.json['newTodo']
        
        for skill in user[u'skills']:
            if skill.keys()[0] == skill_in_use:
                user[u'skills'][0][skill_in_use].append(new_todo)
                collection.update({"username": str(username)}, {"$set": user}, upsert=False)
    return "aa"

@app.route('/<username>/remove_todo', methods=['GET', 'POST'])
def remove_skill_todo(username):
    db = connection['mainAPP']
    collection = db.users
    user = collection.find_one({"username": str(username)})

    if user and request.method == 'POST':
        skill_in_use = request.json['skill_in_use']
        todo = request.json['Todo']
        
        for skill in user[u'skills']:
            if skill.keys()[0] == skill_in_use:
                user[u'skills'][0][skill_in_use].remove(todo)
                app.logger.info(user[u'skills'])
                collection.update({"username": str(username)}, {"$set": user}, upsert=False)
    return "aa"

#@app.route('/add/<username>', methods=['GET'])
#def add_user(username):
#    db = connection['mainAPP']
#    collection = db.users
#    r = collection.find_one({'username': username})
#    if r is None:
#        user = {'username': username, 
#                'email': u'root@localhost',
#                'skills': [{'skill_name1': ['todo1', 'todo2']}, {'skill_name2': ['todo3', 'todo4']}]}   
#        
#        collection.insert(user)
#        return "inserted"
#    else:
#        return "skipped because user exists!"
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)