from flask import Flask, render_template, flash, redirect, url_for, session, request
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps
from flask_mysqldb import MySQL
import urllib2
import re

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_DB'] = 'user'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)


dict = {'Canceling Units': 'http://www.purplemath.com/modules/units.htm', 'Distance Formula': 'http://www.purplemath.com/modules/distform.htm', 'Engineering Notation': 'http://www.purplemath.com/modules/exponent4.htm',
        'Evaluation': 'http://www.purplemath.com/modules/evaluate.htm','Intercepts': 'http://www.purplemath.com/modules/intrcept.htm',
        'Midpoint Formula': 'http://www.purplemath.com/modules/midpoint.htm','Order of Operations': 'http://www.purplemath.com/modules/orderops.htm',
        'Polynomials':'http://www.purplemath.com/modules/polydefs.htm','Simplifying with ':'http://www.purplemath.com/modules/simpexpo.htm',
        'Parentheses':'http://www.purplemath.com/modules/simparen.htm','Slope of a straight line':'http://www.purplemath.com/modules/slope.htm',
        'Slope and Graphing': 'http://www.purplemath.com/modules/slopgrph.htm','Slope and y-intercept':'http://www.purplemath.com/modules/slopyint.htm',
        'Solving Absolute Value':'http://www.purplemath.com/modules/solveabs.htm','Equations':'http://www.purplemath.com/modules/solveabs.htm',
        'Solving Linear Equations':'http://www.purplemath.com/modules/solvelin.htm',
        'Straight-line equations':'http://www.purplemath.com/modules/strtlneq.htm','Variables':'http://www.purplemath.com/modules/variable.htm',
        'Solving Radical Equations':'http://www.purplemath.com/modules/solverad.htm'
        }

# import mysql.connector as mariadb

# mariadb_connection = mariadb.connect(user='root', database='user')
# cursor = mariadb_connection.cursor()

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT user, host FROM mysql.user''')
    rv = cur.fetchall()
    return render_template("index.html")

@app.route('/login')
def login():

    return render_template("login.html")
@app.route('/main')
def main():
    dataAndTitle = []       
    for index in dict:    
        url = dict[index]
        req = urllib2.Request(url)
        f = urllib2.urlopen(req)
        html = f.read()
        titles = re.findall(r'<title>(.*?)</title>',html)
        paragraph = re.findall(r'<p class="text">(.*?)</p>',html)
        if not paragraph:
            continue
        # paragraph = re.sub(r'\<(.*?)\>', '', paragraph[0], re.DOTALL)

        case = { titles[0] : paragraph }
        dataAndTitle.append(case)
    
    return render_template("main.html",data = dataAndTitle)


class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))

        # Create cursor
        cur = mysql.connection.cursor()

        # Execute query
        cur.execute("INSERT INTO user1(name, email, username, password) VALUES(%s, %s, %s, %s)", (name, email, username, password))

        # Commit to DB
        mysql.connection.commit()

        # Close connection
        cur.close()

        flash('You are now registered and can log in', 'success')

        return redirect(url_for('login'))
    return render_template('register.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
