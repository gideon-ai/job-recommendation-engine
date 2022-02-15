#!/usr/bin/env python
# coding: utf-8

# In[10]:


import numpy as np
import os
from flask import Flask, render_template, session, request,send_from_directory,redirect,url_for,request
from oauth2client.contrib.flask_util import UserOAuth2
from flask_pymongo import PyMongo

from werkzeug.security import generate_password_hash, check_password_hash

UPLOAD_FOLDER = os.path.basename('uploads')

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config["MONGO_URI"] = "mongodb://username:password@cluster-ip"
app.config["MONGO_DBNAME"] = "joren"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mongo = PyMongo(app)
#bcrypt = Bcrypt(None)
users = mongo.db.users
@app.route('/')
def index():
    print (session)
    if 'username' in session:
        #return 'You are logged in as ' + session['username'] 
            welcome = "Welcome "+session['username']+"!"
            return render_template('index.html',trainee=welcome)

    return render_template('landings.html')
@app.route('/home')
def home():
    print (session)
    if 'email' in session:
        #return 'You are logged in as ' + session['username'] 
            login_user = users.find_one({'email' : session['email']})
            username = login_user['username']
            welcome = "Welcome "+username+"!"
            return render_template('index.html',trainee=welcome)

    return render_template('landings.html')

@app.route('/login')
def login():
    print (session)
    if 'email' in session:
        #return 'You are logged in as ' + session['username'] 
            login_user = users.find_one({'email' : session['email']})
            username = login_user['username']
            welcome = "Welcome "+username+"!"
            return render_template('index.html',trainee=welcome)
    return render_template('login.html')

@app.route('/create')
def create():
    print (session)
    if 'email' in session:
        #return 'You are logged in as ' + session['username'] 
            login_user = users.find_one({'email' : session['email']})
            print (login_user)
            username = login_user['username']
            welcome = "Welcome "+username+"!"
            return render_template('website.html')
    return render_template('wlogin.html')

@app.route('/web', methods=['POST','GET'])
def web():
    users = mongo.db.users
    
    #print (request.form['username'])
    login_user = users.find_one({'email' : request.form['email']})
    print (login_user)
    
    
    if login_user:
        matches = check_password_hash(login_user['password'],request.form['password'])
        print (matches)
        if matches:
            session['email'] = request.form['email']
            #return redirect(url_for('create'))
            return render_template('website.html')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/website', methods=['POST'] )
def website_details():
    username = "none"
    if 'email' in session:
        #return 'You are logged in as ' + session['username'] 
            login_user = users.find_one({'email' : session['email']})
            username = login_user['username']
    print (request.form['name'])
    print (request.form['bizmail'])
    print (request.form['phoneno'])
    #print (request.form['function'])
    #print (request.form['pages'])
    print (request.form.get('function'))
    print (request.form.getlist('pages'))
    website = mongo.db.website
    
    username = username
    webname = request.form['name']
    bizmail = request.form['bizmail']
    bizno = request.form['phoneno']
    function = request.form.get('function')
    pages = request.form.getlist('pages')
    
    print (website)
    website.insert_one({'name' : username, 'owner_mail':session['email'], 'webname' : webname, 'bizmail':bizmail, 'bizno':bizno, 'function':function,'pages':pages})
    return render_template('creation.html',appname=webname)


@app.route('/signin', methods=['POST'])
def signin():
    users = mongo.db.users
    print (users)
    login_user = users.find_one({'email' : request.form['email']})
    print (login_user)
    if login_user:
        matches = check_password_hash(login_user['password'],request.form['password'])
        print (matches)
        if matches:
            session['email'] = request.form['email']
            return redirect(url_for('home'))

 
    return render_template('login-error.html')

@app.route('/signup')
def create_account():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register():
    #if request.method == 'POST':
    users = mongo.db.users
    username = request.form['username']
    password = request.form['pass']
    password_hash = generate_password_hash(password)
    email = request.form['email']
    session['email'] = email
    print (username)
    print (password)
    print (email)
    users.insert({'username' : username, 'password' : password_hash, 'email':email})
    
   
    print (username)
    print (password)
    print (email)
    

    return render_template('index.html',trainee=username)

@app.route('/reset')
def reset():
    return render_template("password-reset.html")
@app.route('/resetstatus',methods=['POST'])
def reset_status():
    email = request.form['youremail']
    username = request.form['yourusername']
    password = request.form['newpass']
    users = mongo.db.users
    user_record = users.find_one({'name':request.form['yourusername']})
    existing_user = user_record['name']
    existing_user_email = user_record['email']
    print (existing_user)
    print (existing_user_email)
    print (email)
    print (username)
    
    if (email == existing_user_email and username == existing_user):
        password_hash = generate_password_hash(password)
        users.update({'name':username},{'$set':{'password':password_hash}})
        return render_template('password-reset-successful.html')
    return render_template("login-error.html")
if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run()







