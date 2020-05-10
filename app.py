from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.utils import secure_filename
import hashlib, sqlite3, random, string, os, time, shutil
from datetime import datetime, timedelta
from Split import responsive

def randomString(stringLength):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(stringLength))

app = Flask(__name__)

@app.route('/') #, methods=['GET', 'POST'])
def landingPage():
    if 'name' in session:
        return redirect('/dashboard')
    else:
        return render_template('landing-page.html')

    # return("Bismillah")

@app.route('/login', methods=['GET', 'POST'])
def loginPage():
    if 'name' in session:
        return redirect('/dashboard')

    if request.method == 'GET':
        return render_template('login-page.html')
    else:
        # print('login post working')
        userInput = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('AiDdatabase.db')
        c = conn.cursor()
        c.execute("SELECT username, email, password_salt, password_hash FROM Login_DB")
        for row in c.fetchall():
            # print('Inside the row is = ',row)
            if row[0]==userInput or row[1]==userInput:
                salt = row[2].encode('utf-8')
                passw = password.encode('utf-8')
                hash = hashlib.sha512(salt + passw).hexdigest()
                if hash==row[3]:
                    #Logged in
                    # print('logged in')
                    c.close()
                    session['name'] = row[0]
                    session.permanent = True
                    return redirect(url_for('dashboard'))
                else:
                    # print('wrong password')
                    c.close()
                    flash('Wrong password')
                    return redirect(request.url)

            # else:
        # print('username not match')
        c.close()
        # session.clear()
        flash('Login failed : Username/email not registered')
        return redirect(request.url)

@app.route('/register', methods=['GET', 'POST'])
def registerPage():
    if 'name' in session:
        return redirect('/dashboard')

    if request.method == 'GET':
        # print('register - get method')
        return render_template('sign-up.html')
    else:
        # print('register - post method')

        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        passw = password.encode('utf-8')
        dateToday = datetime.now()
        salt = randomString(10).encode('utf-8')
        hash = hashlib.sha512(salt+passw).hexdigest()
        salt = salt.decode('utf-8')
        hash = str(hash)

        isActive = 0
        # print('Value is : ',username, email, salt, hash, dateToday, isActive)

        conn = sqlite3.connect('AiDdatabase.db')
        c = conn.cursor()

        c.execute("SELECT username FROM Login_DB")
        names = {name[0] for name in c.fetchall()}
        c.execute("SELECT email FROM Login_DB")
        emails = {em[0] for em in c.fetchall()}

        if username in names:
            # print("Username taken, break.")
            c.close()
            flash('username already taken by other user')
            return redirect(request.url)
            # return redirect('/register')

        elif email in emails:
            # print("Email taken, break.")
            c.close()
            flash('email already used')
            return redirect(request.url)
            # return redirect('/register')

        else:
            insert_query = "INSERT INTO Login_DB \
                                (username, email, password_salt, password_hash, date_register, isActive) \
                                VALUES ('{}','{}','{}','{}','{}','{}')".format(username, email, salt, hash, dateToday,
                                                                               isActive)
            c = c.execute((insert_query))
            conn.commit()
            # print("Done commit to database")
            c.close()
            return redirect('/login')


@app.route('/dashboard') #, methods=['GET', 'POST'])
def dashboard():
    # print('Session now is : ', session)
    if 'name' in session:
        # session.clear()
        # return render_template('landing-page.html')
        return render_template('quick-start.html')
    elif not session:
        return redirect('/')
        # return render_template('landing-page.html')
    else:
        session.clear()
        # return render_template('quick-start.html')
        return redirect('/')
        # return render_template('landing-page.html')

@app.route('/image-splitter', methods=['GET', 'POST'])
def imageSplitter():

    if 'name' in session:
        if request.method == 'GET':
            return render_template('image-splitter.html', list_file = None, result_folder=None, isResult=False)

        else:
            numX = request.form['horizontal-input']
            numY = request.form['vertical-input']
            file = request.files['file']
            filename = secure_filename(file.filename)
            # print('the file isss.............')
            # print(file)
            # print(filename)
            if filename=='':
                flash('Input file first')
                return redirect(request.url)
            nowTime = int(time.time())
            username = session['name']
            UPLOAD_FOLDER = str('static/user/' + username + '/splitter/' + str(nowTime) + '/')
            RES_FOLDER = str('static/user/' + username + '/splitter/' + str(nowTime) + '/result/')
            # print('UPLOAD_FOLDER = ', UPLOAD_FOLDER)

            if not os.path.isdir(UPLOAD_FOLDER):
                os.makedirs(UPLOAD_FOLDER)
                os.makedirs(RES_FOLDER)

            full_filename = os.path.join((UPLOAD_FOLDER), filename)
            file.save(full_filename)

            responsive(img_src=full_filename,
                       numX=numX,
                       numY=numY,
                       saveIn=RES_FOLDER)

            result_files = os.listdir(RES_FOLDER)

            shutil.make_archive(full_filename, 'zip', RES_FOLDER)
            zipFileName = str(full_filename+'.zip')
            # return redirect('#')
            return render_template('image-splitter.html', list_file=result_files,
                                   result_folder=RES_FOLDER, isResult=True, zipFile=zipFileName)

    elif not session:
        return redirect('/')
    else:
        session.clear()
        return redirect('/')


@app.route('/logout') #, methods=['GET', 'POST'])
def logout():
    session.clear()
    return redirect('/')

@app.errorhandler(404)
def page_not_found(error):
    return redirect('/')
    # return 'This page does not exist', 777

app.secret_key = 'Nh9huif8GV^Gs68D$A@#%S$fsgha'
if __name__ == '__main__':
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=1440)
    app.config['SESSION_TYPE'] = 'filesystem'
    # app.config['SECRET_KEY'] = 'Nh9huif8GV^Gs68D$A@#%S$fsgha'
    # session.init_app(app)
    app.run(debug=True)

# To run on windows
# set FLASK_APP=main_flask.py
# set FLASK_ENV=development

# http://www.rahmatsiswanto.com/2018/04/python-flask-mysqldb-simple-login.html