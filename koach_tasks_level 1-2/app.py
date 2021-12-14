from flask import Flask, render_template, session, request, redirect, url_for
from flask_pymongo import PyMongo
import bcrypt

app=Flask(__name__)
mongo=PyMongo(app,uri= "mongodb://localhost:27017/LEVEL1")

@app.route('/')
def index():
    if 'email' in session:
        return 'You are logged in as' + session['email']
    return render_template('home2.html')


@app.route('/login', methods= ['POST'])
def login():
    users = mongo.db.users
    login_email=users.find_one({ 'email' : request.form['email']})
    
    if login_email:
        if bcrypt.hashpw(request.form['password'].encode('utf-8'), login_email['password'].encode('utf-8'))==login_email['password'].encode('utf-8'):
            session['email']=request.form['email'] 
            return redirect(url_for('index'))
    return "Invalid email/password combination"




@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        #collection - user
        users = mongo.db.users
        existing_user= users.find_one({'name': request.form['username']})
        
        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
            users.insert({'name': request.form['username'], 'password' : hashpass})
            session['username']= request.form['username']
            return redirect(url_for('register'))
        return 'That username already exists!'
    return render_template('home2.html')
    
    

if __name__ == '__main__':
    app.run(debug= False)








    
