from flask import Flask, render_template, request, redirect, url_for, session
import bcrypt
import sqlite3
from datetime import date

dateToday = date.today().isoformat()

app = Flask(__name__)

@app.route('/') #, methods=['GET', 'POST'])
def landingPage():
    return render_template('landing-page.html')
    # return("Bismillah")

@app.route('/login') #, methods=['GET', 'POST'])
def loginPage():
    if request.method == 'POST':
        session['name'] = request.form['name']
        session['email'] = request.form['email']


    return render_template('login-page.html')

@app.route('/register', methods=['GET', 'POST'])
def registerPage():
    if request.method == 'GET':
        return render_template('sign-up.html')
    else:
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        passw = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hash = bcrypt.hashpw(passw, salt)
        isActive = 0
        try:
            conn = sqlite3.connect('AiDdatabase.db')
            c = conn.cursor()
            insert_query = """INSERT INTO Login_DB
                                      (username, email, password_salt, password_hash, date_register, isActive) 
                                       VALUES 
                                      ({}, {}, {}, {}, {}, {}""".format(username, email, salt, hash, dateToday, isActive)
            c = c.execute((insert_query))
            conn.commit()
            c.close()
        except:
            print('error')



@app.route('/dashboard') #, methods=['GET', 'POST'])
def dashboard():
    return render_template('quick-start.html')

@app.route('/image-splitter') #, methods=['GET', 'POST'])
def imageSplitter():
    return render_template('image-splitter.html')

app.secret_key = 'super secret key'
if __name__ == '__main__':
    app.config['SESSION_TYPE'] = 'filesystem'
    # app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    # session.init_app(app)
    app.run(debug=True)

# To run on windows
# set FLASK_APP=main_flask.py
# set FLASK_ENV=development

# http://www.rahmatsiswanto.com/2018/04/python-flask-mysqldb-simple-login.html