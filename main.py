#init.py
##librerias
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors


##Inicializacion
app = Flask(__name__)
app.secret_key = 'mysecretkey'

##Configuracion MySQL (DB)
app.config['MYSQL_HOST'] = 'us-cdbr-east-02.cleardb.com'
app.config['MYSQL_USER'] = 'b629ab6019ca38'
app.config['MYSQL_PASSWORD'] = '6ba7734f'
app.config['MYSQL_DB'] = 'heroku_b7bee2d28031202'

##Inicializacion de MySQL
mysql = MySQL(app)

##Rutas
###Index

###Login
@app.route('/', methods=['GET', 'POST']) #(index.html)
def login():
    msg = ''
    if request.method == 'POST' and ('username' in request.form and 'password' in request.form):
        username = request.form['username']
        password = request.form['password']
        # Validacion de los datos
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password))
        global account 
        account = cursor.fetchone()
        cursor.close()
        if account == None:
            msg = 'Username o password incorrectos'     
        else:
            session['username'] = account['username']
            print (session['username'])
            return redirect(url_for('home'))
    return render_template('index.html', msg = msg)

@app.route('/register', methods=['GET', 'POST']) #(register.html)
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        # Agregar datos 
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO accounts(username, password, email) VALUES ( %s, %s, %s)', (username, password, email))
        mysql.connection.commit()
        msg = 'Registro completo'
    return render_template('register.html', msg = msg)

###Home
@app.route('/home')
def home():
    return render_template('home.html', data = account)

@app.route('/profile')
def profile():
    return render_template('procfile.html', data = account)

@app.route('/logout')
def logout():
    session.clear()
    return render_template('index.html')
##run
if __name__ == '__main__':
    app.run(port=3000, debug=True)