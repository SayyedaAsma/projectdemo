

from flask import Flask, render_template, request,url_for,session,redirect
from flask.helpers import flash
from flask_mysqldb import MySQL

import MySQLdb.cursors
from werkzeug.utils import secure_filename
import os
import re

app = Flask(__name__)

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'zarnish'

# Enter your database connection details below
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Asma123@'
app.config['MYSQL_DB'] = 'registration_form'


# making connection with another database



# Intialize MySQL
mysql = MySQL(app)
 
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
  
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 
def allowed_file(filename):
  return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

   

@app.route('/',methods=['GET','POST'])
def login():

    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'Email' in request.form and 'password' in request.form:
        # Create variables for easy access
        Email = request.form['Email']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE Email = %s AND password = %s', (Email, password,))
        # Fetch one record and return result
        user = cursor.fetchone()
        # If account exists in accounts table in out database
        if user == {'userID': 1, 'Name': 'Asma', 'Email': 'sayyedaasma@gmail.com', 'password': 'asma123'}:
            # Create session data, we can access this data in other routes
            session.modified = True
            session['Name']=user['Name']
            session['userID']=user['userID']
            session['password'] = user['password']
            session['Email'] = user['Email']
            # Redirect to home page
           
            return render_template('admin.html')
            
       
        if user:
                session.modified = True
                session['password'] = user['password']
                session['Name'] = user['Name']
               
                session['userID']=user['userID']
                session['Email'] = user['Email']
                # Redirect to home page
                
                
                return render_template('front.html')

        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username or password!'
    # Show the login form with message (if any)
            return render_template('login.html', msg=msg)
    return render_template('login.html')
@app.route('/register',methods=['GET','POST'])
def register():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'Name' in request.form and 'password' in request.form and 'Email' in request.form:
        # Create variables for easy access
        Name = request.form['Name']
        password = request.form['password']
        Email = request.form['Email']
            # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE Name = %s', [Name])
        user = cursor.fetchone()
        # If account exists show error and validation checks
        if user:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', Email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', Name):
            msg = 'Name must contain only characters and numbers!'
        elif not Name or not password or not Email:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO users VALUES (NULL,%s, %s, %s)', [Name, Email, password])
            mysql.connection.commit()
            msg = 'You have successfully registered!'    
    else:
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)
      

@app.route('/home')
def home():
    return render_template('admin.html')


@app.route('/userrecord')
def userrecord():
     cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
     cursor.execute('SELECT * FROM users')
     data = cursor.fetchall()
     cursor.close()
     return render_template('userrecord.html', users=data)    

@app.route('/recipierecord')
def recipie():
     cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
     cursor.execute('SELECT * FROM bakeryproducts')
     data = cursor.fetchall()
     cursor.close()
     return render_template('recepie.html', bakeryproducts=data)


@app.route('/deserts')
def deserts():
     cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
     cursor.execute('SELECT * FROM deserts')
     data = cursor.fetchall()
     cursor.close()
     return render_template('deserts.html', deserts=data)


@app.route('/chinese')
def chinese():
     cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
     cursor.execute('SELECT * FROM chinesecuisine')
     data = cursor.fetchall()
     cursor.close()
     return render_template('chinese.html', chinesecuisine=data)

@app.route('/pakistani')
def pakistani():
     cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
     cursor.execute('SELECT * FROM pakistanicuisine')
     data = cursor.fetchall()
     cursor.close()
     return render_template('pakistani.html', pakistanicuisine=data)  

@app.route('/indian')
def indian():
     cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
     cursor.execute('SELECT * FROM indiancuisine')
     data = cursor.fetchall()
     cursor.close()
     return render_template('indian.html', indiancuisine=data)         

@app.route('/snacks')
def snacks():
     cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
     cursor.execute('SELECT * FROM snacks')
     data = cursor.fetchall()
     cursor.close()
     return render_template('snacks.html', snacks=data)

@app.route('/drinks')
def drinks():
     cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
     cursor.execute('SELECT * FROM drinksandshakes')
     data = cursor.fetchall()
     cursor.close()
     return render_template('drinks.html',drinksandshakes=data)
#for pakistanicuisine
@app.route('/update/<string:ID>',methods=['GET','POST'])
def update(ID):
     cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
     if request.method=='POST':
          ID=request.form['ID']
          title=request.form['title']
          Description=request.form['Description']        
          ingredients=request.form['ingredients']
          files = request.files.getlist('files[]')
          youtubelink=request.form['youtubelink']
          for file in files:
              if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename)) 
                cur.execute('UPDATE pakistanicuisine Set imagepath=%s WHERE ID=%s',(filename,ID))      
                flash('updated successfully')
                mysql.connection.commit()
                flash('updated successfully')
          cur.execute('UPDATE pakistanicuisine Set title=%s,Description=%s,ingredients=%s,youtubelink=%s WHERE ID=%s', (title,Description,ingredients,youtubelink,ID))
          mysql.connection.commit()
          cur.close()
          return redirect(url_for('pakistani'))
     cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)       
     query='SELECT * FROM pakistanicuisine WHERE ID=%s'
     cur.execute(query,(ID))
     data = cur.fetchone()
     cur.connection.commit()
     return render_template('update.html',pakistanicuisine=data)

@app.route('/insert', methods=['GET','POST'])
def insert():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
 
    if request.method=='POST':
      
      ingredients=request.form['ingredients']
      title=request.form['title']
      Description=request.form['Description']
      files = request.files.getlist('files[]')
      youtubelink=request.form['youtubelink']
      for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename)) 
            cur.execute('INSERT INTO pakistanicuisine (title,Description,ingredients,imagepath,youtubelink) VALUES (%s,%s,%s,%s,%s)', (title,Description,ingredients,filename,youtubelink)) 
            flash('inserted successfully')
            mysql.connection.commit()
      flash('inserted  successfully')
      cur.close()
      return redirect(url_for('pakistani'))
    return render_template("insert.html")


@app.route('/delete/<string:ID>',methods=['GET','POST'])
def delete(ID):
    cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute('Delete FROM pakistanicuisine WHERE ID LIKE %s',[ID])
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('pakistani'))



#for chinese 
@app.route('/updatec/<string:ID>',methods=['GET','POST'])
def updatec(ID):
     cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
     if request.method=='POST':
          
          ID=request.form['ID']
          title=request.form['title']
          Description=request.form['Description']
          ingredients=request.form['ingredients']
          files = request.files.getlist('files[]')
          youtubelink=request.form['youtubelink']
          for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                cur.execute('UPDATE chinesecuisine Set title=%s,Description=%s,ingredients=%s,youtubelink=%s WHERE ID=%s', (title,Description,ingredients,youtubelink,ID))
                mysql.connection.commit()
               
          cur.execute('UPDATE chinesecuisine Set title=%s,Description=%s,ingredients=%s,youtubelink=%s WHERE ID=%s', (title,Description,ingredients,youtubelink,ID))
          mysql.connection.commit()
          cur.close()   
          flash('File(s) successfully uploaded')    
          return redirect(url_for('chinese'))
     cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)       
     query='SELECT * FROM chinesecuisine WHERE ID=%s'
     cur.execute(query,(ID))
     data = cur.fetchone()
     cur.connection.commit()
     return render_template('updatec.html',chinesecuisine=data)

@app.route('/deletec/<string:ID>',methods=['GET','POST'])
def deletec(ID):
    cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute('Delete FROM chinesecuisine WHERE ID LIKE %s',[ID])
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('chinese'))

@app.route('/insertc', methods=['GET','POST'])
def insertc():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
 
    if request.method=='POST':
      youtubelink=request.form['youtubelink']
      title=request.form['title']
      Description=request.form['Description']
      ingredients=request.form['ingredients']
      cur.execute('INSERT INTO chinesecuisine (title,Description,ingredients,youtubelink) VALUES (%s,%s,%s,%s)', (title,Description,ingredients,youtubelink)) 
      flash('updated successfully')
      mysql.connection.commit()
      flash('inserted  successfully')
      cur.close()
      return redirect(url_for('chinese'))
    return render_template("insertc.html")

#for indian

 
@app.route('/updatei/<string:ID>',methods=['GET','POST'])
def updatei(ID):
     cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
     if request.method=='POST':
          ID=request.form['ID']
          title=request.form['title']
          Description=request.form['Description']
          ingredients=request.form['ingredients']
          files = request.files.getlist('files[]')
          youtubelink=request.form['youtubelink']
          for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                cur.execute('UPDATE indiancuisine Set imagepath=%s WHERE ID=%s',(filename,ID))  
                flash('updated successfully')
                mysql.connection.commit()
                flash('updated successfully')
          cur.execute('UPDATE indiancuisine Set title=%s,Description=%s,ingredients=%s,youtubelink=%s WHERE ID=%s', (title,Description,ingredients,youtubelink,ID))
          mysql.connection.commit()      
          cur.close()
          return redirect(url_for('indian'))
     cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)       
     query='SELECT * FROM indiancuisine WHERE ID=%s'
     cur.execute(query,(ID))
     data = cur.fetchone()
     cur.connection.commit()
     return render_template('updatei.html',indiancuisine=data)

@app.route('/deletei/<string:ID>',methods=['GET','POST'])
def deletei(ID):
    cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute('Delete FROM indiancuisine WHERE ID LIKE %s',[ID])
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('indian'))

@app.route('/inserti', methods=['GET','POST'])
def inserti():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
 
    if request.method=='POST':
      
      title=request.form['title']
      Description=request.form['Description']
      ingredients=request.form['ingredients']
      youtubelink=request.form['youtubelink']
      cur.execute('INSERT INTO indiancuisine (title,Description,ingredients,youtubelink) VALUES (%s,%s,%s,%s)', (title,Description,ingredients,youtubelink)) 
      mysql.connection.commit()
      flash('inserted  successfully')
      cur.close()
      return redirect(url_for('indian'))
    return render_template("inserti.html")

#snacks
@app.route('/updates/<string:ID>',methods=['GET','POST'])
def updates(ID):
     cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
     if request.method=='POST':
        ID=request.form['ID']
        title=request.form['title']
        Description=request.form['Description']
        ingredients=request.form['ingredients']
        files = request.files.getlist('files[]')
        youtubelink=request.form['youtubelink']
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                cur.execute('UPDATE snacks Set imagepath=%s WHERE ID=%s',(filename,ID))       
                flash('updated successfully')
                mysql.connection.commit()
          
                flash('updated successfully')
        cur.execute('UPDATE snacks Set title=%s,Description=%s,ingredients=%s,youtubelink=%s WHERE ID=%s', (title,Description,ingredients,youtubelink,ID))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('snacks'))
     cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)       
     query='SELECT * FROM snacks WHERE ID=%s'
     cur.execute(query,(ID))
     data = cur.fetchone()
     cur.connection.commit()
     return render_template('updates.html',snacks=data)

@app.route('/deletes/<string:ID>',methods=['GET','POST'])
def deletes(ID):
    cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute('Delete FROM snacks WHERE ID LIKE %s',[ID])
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('snacks'))

@app.route('/inserts', methods=['GET','POST'])
def inserts():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method=='POST':
      title=request.form['title']
      Description=request.form['Description']
      ingredients=request.form['ingredients']
      youtubelink=request.form['youtubelink']
      cur.execute('INSERT INTO snacks (title,Description,ingredients,youtubelink) VALUES (%s,%s,%s,%s)', (title,Description,ingredients,youtubelink)) 
      mysql.connection.commit()
      flash('inserted  successfully')
      cur.close()
      return redirect(url_for('snacks'))
    return render_template("inserts.html")

#for drinks
@app.route('/updated/<string:ID>',methods=['GET','POST'])
def updated(ID):
     cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
     if request.method=='POST':
          ID=request.form['ID']
          title=request.form['title']
          Description=request.form['Description']
          ingredients=request.form['ingredients']
          files = request.files.getlist('files[]')
          youtubelink=request.form['youtubelink']
          for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                cur.execute('UPDATE drinksandshakes Set imagepath=%s WHERE ID=%s',(filename,ID))     
                flash('updated successfully')
                mysql.connection.commit()
          flash('updated successfully')
          cur.execute('UPDATE drinksandshakes Set title=%s,Description=%s,ingredients=%s,youtubelink=%s WHERE ID=%s', (title,Description,ingredients,youtubelink,ID))
          mysql.connection.commit()
          cur.close()
          return redirect(url_for('drinks'))
     cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)       
     query='SELECT * FROM drinksandshakes WHERE ID=%s'
     cur.execute(query,(ID))
     data = cur.fetchone()
     cur.connection.commit()
     return render_template('updated.html',drinksandshakes=data)

@app.route('/deleted/<string:ID>',methods=['GET','POST'])
def deleted(ID):
    cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute('Delete FROM drinksandshakes WHERE ID LIKE %s',[ID])
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('drinks'))

@app.route('/insertd', methods=['GET','POST'])
def insertd():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method=='POST':
      title=request.form['title']
      Description=request.form['Description']
      ingredients=request.form['ingredients']
      youtubelink=request.form['youtubelink']
      cur.execute('INSERT INTO drinksandshakes (title,Description,ingredients, youtubelink) VALUES (%s,%s,%s,%s)', (title,Description,ingredients,youtubelink)) 
      mysql.connection.commit()
      flash('inserted  successfully')
      cur.close()
      return redirect(url_for('drinks'))
    return render_template("insertd.html")

#for deserts
@app.route('/updateds/<string:ID>',methods=['GET','POST'])
def updateds(ID):
     cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
     if request.method=='POST':
          ID=request.form['ID']
          title=request.form['title']
          Description=request.form['Description']
          ingredients=request.form['ingredients']
          
          files = request.files.getlist('files[]')
          youtubelink=request.form['youtubelink']
          for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                cur.execute('UPDATE deserts Set imagepath=%s WHERE ID=%s',(filename,ID))
                flash('updated successfully')
                mysql.connection.commit()
                flash('updated successfully')
          cur.execute('UPDATE deserts Set title=%s,Description=%s,ingredients=%s,youtubelink=%s WHERE ID=%s', (title,Description,ingredients,youtubelink,ID))
          mysql.connection.commit()     
          cur.close()
          return redirect(url_for('deserts'))
     cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)       
     query='SELECT * FROM deserts WHERE ID=%s'
     cur.execute(query,(ID))
     data = cur.fetchone()
     cur.connection.commit()
     return render_template('updateds.html',deserts=data)

@app.route('/deleteds/<string:ID>',methods=['GET','POST'])
def deleteds(ID):
    cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute('Delete FROM deserts WHERE ID LIKE %s',[ID])
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('deserts'))

@app.route('/insertds', methods=['GET','POST'])
def insertds():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method=='POST':
      title=request.form['title']
      youtubelink=request.form['youtubelink']
      Description=request.form['Description']
      ingredients=request.form['ingredients']
      cur.execute('INSERT INTO deserts (title,Description,ingredients,youtubelink) VALUES (%s,%s,%s,%s)', (title,Description,ingredients,youtubelink)) 
      mysql.connection.commit()
      flash('inserted  successfully')
      cur.close()
      return redirect(url_for('deserts'))
    return render_template("insertds.html")



#for bakeryproducts
@app.route('/updateb/<string:ID>',methods=['GET','POST'])
def updateb(ID):
     cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
     if request.method=='POST':
          ID=request.form['ID']
          title=request.form['title']
          Description=request.form['Description']
          ingredients=request.form['ingredients']
          files = request.files.getlist('files[]')
          youtubelink=request.form['youtubelink']
          
          for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                cur.execute('UPDATE bakeryproducts Set imagepath=%s WHERE ID=%s',(filename,ID)) 
                flash('updated successfully')
                mysql.connection.commit()
          flash('updated successfully')
          cur.execute('UPDATE bakeryproducts Set title=%s,Description=%s,ingredients=%s,youtubelink=%s WHERE ID=%s', (title,Description,ingredients,youtubelink,ID))
          mysql.connection.commit()
          cur.close()
          return redirect(url_for('recipie'))
     cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)       
     query='SELECT * FROM bakeryproducts WHERE ID=%s'
     cur.execute(query,(ID))
     data = cur.fetchone()
     cur.connection.commit()
     return render_template('updateb.html',bakeryproducts=data)

@app.route('/deleteb/<string:ID>',methods=['GET','POST'])
def deleteb(ID):
    cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute('Delete FROM bakeryproducts WHERE ID LIKE %s',[ID])
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('recipie'))

@app.route('/insertb', methods=['GET','POST'])
def insertb():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method=='POST':
      title=request.form['title']
      Description=request.form['Description']
      ingredients=request.form['ingredients']
      youtubelink=request.form['youtubelink']
      cur.execute('INSERT INTO bakeryproducts (title,Description,ingredients,youtubelink) VALUES (%s,%s,%s,%s)', (title,Description,ingredients,youtubelink)) 
      mysql.connection.commit()
      flash('inserted  successfully')
      cur.close()
      return redirect(url_for('recipie'))
    return render_template("insertb.html")    


@app.route('/front')
def front():
    return render_template('front.html')

@app.route('/categories')
def categories():
    return render_template('recipies.html')

@app.route('/dispp')
def dispp():
    return render_template('pakistanip.html')

@app.route('/dispc')    
def dispc():
     cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
     cursor.execute('SELECT * FROM chinesecuisine')
     data = cursor.fetchall()
     cursor.close()
     return render_template('chinesed.html', chinesecuisine=data)

@app.route('/dispd')    
def dispd():
     cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
     cursor.execute('SELECT * FROM deserts')
     data = cursor.fetchall()
     cursor.close()
     return render_template('desertsd.html', deserts=data)  

@app.route('/dispds')    
def dispds():
     cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
     cursor.execute('SELECT * FROM drinksandshakes')
     data = cursor.fetchall()
     cursor.close()
     return render_template('drinksd.html', drinksandshakes=data) 

@app.route('/dispb')    
def dispb():
     cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
     cursor.execute('SELECT * FROM bakeryproducts')
     data = cursor.fetchall()
     cursor.close()
     return render_template('bakeryb.html',  bakeryproducts=data)

@app.route('/dispi')    
def dispi():
     cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
     cursor.execute('SELECT * FROM indiancuisine')
     data = cursor.fetchall()
     cursor.close()
     return render_template('indid.html', indiancuisine=data)


@app.route('/disps')    
def disps():
     cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
     cursor.execute('SELECT * FROM snacks')
     data = cursor.fetchall()
     cursor.close()
     return render_template('snackss.html', snacks=data) 

@app.route('/karahi')
def karahi():
     cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
     cursor.execute('SELECT * FROM pakistanicuisine Where ID=1')
     data = cursor.fetchall()
     cursor.close()
     return render_template('karahi.html', pakistanicuisine=data)

@app.route('/biryani')
def biryani():
     cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
     cursor.execute('SELECT * FROM pakistanicuisine Where ID=2')
     data = cursor.fetchall()
     cursor.close()
     return render_template('biryani.html', pakistanicuisine=data)

@app.route('/paye')
def paye():
     cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
     cursor.execute('SELECT * FROM pakistanicuisine Where ID=3')
     data = cursor.fetchall()
     cursor.close()
     return render_template('paye.html', pakistanicuisine=data)

@app.route('/nihari')
def nihari():
     cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
     cursor.execute('SELECT * FROM pakistanicuisine Where ID=4')
     data = cursor.fetchall()
     cursor.close()
     return render_template('nihari.html', pakistanicuisine=data)

@app.route('/tandoori')
def tandoori():
     cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
     cursor.execute('SELECT * FROM pakistanicuisine Where ID=5')
     data = cursor.fetchall()
     cursor.close()
     return render_template('tandoori.html', pakistanicuisine=data)

#snacks
@app.route('/pakora')
def pakora():
     cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
     cursor.execute('SELECT * FROM snacks Where ID=1')
     data = cursor.fetchall()
     cursor.close()
     return render_template('pakora.html', snacks=data)


@app.route('/samosa')
def samosa():
     cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
     cursor.execute('SELECT * FROM snacks Where ID=2')
     data = cursor.fetchall()
     cursor.close()
     return render_template('samosa.html', snacks=data)

@app.route('/baray')
def baray():
     cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
     cursor.execute('SELECT * FROM snacks Where ID=3')
     data = cursor.fetchall()
     cursor.close()
     return render_template('baray.html', snacks=data)


@app.route('/chanachat')
def chanachat():
     cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
     cursor.execute('SELECT * FROM snacks Where ID=4')
     data = cursor.fetchall()
     cursor.close()
     return render_template('chana.html', snacks=data)               

@app.route('/fruitchat')
def fruitchat():
     cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
     cursor.execute('SELECT * FROM snacks Where ID=5')
     data = cursor.fetchall()
     cursor.close()
     return render_template('fruit.html', snacks=data)

#bakeryproducts
@app.route('/cookies')
def cookies():
     cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
     cursor.execute('SELECT * FROM bakeryproducts Where ID=1')
     data = cursor.fetchall()
     cursor.close()
     return render_template('cookie.html', bakeryproducts=data)

@app.route('/cake')
def cake():
     cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
     cursor.execute('SELECT * FROM bakeryproducts Where ID=2')
     data = cursor.fetchall()
     cursor.close()
     return render_template('cake.html', bakeryproducts=data)

@app.route('/brownie')
def brownie():
     cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
     cursor.execute('SELECT * FROM bakeryproducts Where ID=3')
     data = cursor.fetchall()
     cursor.close()
     return render_template('brownie.html', bakeryproducts=data)


@app.route('/cofee')
def cofee():
     cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
     cursor.execute('SELECT * FROM bakeryproducts Where ID=4')
     data = cursor.fetchall()
     cursor.close()
     return render_template('cofee.html', bakeryproducts=data)          

@app.route('/garlic')
def garlic():
     cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
     cursor.execute('SELECT * FROM bakeryproducts Where ID=5')
     data = cursor.fetchall()
     cursor.close()
     return render_template('garlic.html', bakeryproducts=data)


#deserts
@app.route('/falooda')
def falooda():
     cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
     cursor.execute('SELECT * FROM deserts Where ID=1')
     data = cursor.fetchall()
     cursor.close()
     return render_template('falooda.html', deserts=data)

@app.route('/firni')
def firni():
     cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
     cursor.execute('SELECT * FROM deserts Where ID=2')
     data = cursor.fetchall()
     cursor.close()
     return render_template('firni.html', deserts=data)


@app.route('/gulab')
def gulab():
     cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
     cursor.execute('SELECT * FROM deserts Where ID=3')
     data = cursor.fetchall()
     cursor.close()
     return render_template('gulab.html', deserts=data)


@app.route('/sohan')
def sohan():
     cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
     cursor.execute('SELECT * FROM deserts Where ID=4')
     data = cursor.fetchall()
     cursor.close()
     return render_template('sohan.html', deserts=data)


@app.route('/barfi')
def barfi():
     cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
     cursor.execute('SELECT * FROM deserts Where ID=5')
     data = cursor.fetchall()
     cursor.close()
     return render_template('barfi.html', deserts=data)

# for indian
@app.route('/butter')
def butter():
     cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
     cursor.execute('SELECT * FROM indiancuisine Where ID=1')
     data = cursor.fetchall()
     cursor.close()
     return render_template('butter.html', indiancuisine=data)

@app.route('/malai')
def malai():
     cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
     cursor.execute('SELECT * FROM indiancuisine Where ID=2')
     data = cursor.fetchall()
     cursor.close()
     return render_template('malai.html', indiancuisine=data)

@app.route('/panipuri')
def panipuri():
     cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
     cursor.execute('SELECT * FROM indiancuisine Where ID=3')
     data = cursor.fetchall()
     cursor.close()
     return render_template('panipuri.html', indiancuisine=data)

@app.route('/palak')
def palak():
     cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
     cursor.execute('SELECT * FROM indiancuisine Where ID=4')
     data = cursor.fetchall()
     cursor.close()
     return render_template('palak.html', indiancuisine=data)

#for chinese
@app.route('/soup')
def soup():
     cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
     cursor.execute('SELECT * FROM chinesecuisine Where ID=1')
     data = cursor.fetchall()
     cursor.close()
     return render_template('soup.html', chinesecuisine=data)

@app.route('/rolls')
def rolls():
     cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
     cursor.execute('SELECT * FROM chinesecuisine Where ID=2')
     data = cursor.fetchall()
     cursor.close()
     return render_template('rolls.html', chinesecuisine=data)

@app.route('/cashew')
def cashew():
     cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
     cursor.execute('SELECT * FROM chinesecuisine Where ID=3')
     data = cursor.fetchall()
     cursor.close()
     return render_template('cashew.html', chinesecuisine=data)

@app.route('/peri')
def peri():
     cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
     cursor.execute('SELECT * FROM chinesecuisine Where ID=4')
     data = cursor.fetchall()
     cursor.close()
     return render_template('peri.html',chinesecuisine=data)

@app.route('/egg')
def egg():
     cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
     cursor.execute('SELECT * FROM chinesecuisine Where ID=6')
     data = cursor.fetchall()
     cursor.close()
     return render_template('egg.html', chinesecuisine=data)

#drinksand shakes
@app.route('/mint')
def mint():
     cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
     cursor.execute('SELECT * FROM drinksandshakes Where ID=1')
     data = cursor.fetchall()
     cursor.close()
     return render_template('mint.html', drinksandshakes=data)

@app.route('/lemon')
def lemon():
     cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
     cursor.execute('SELECT * FROM drinksandshakes Where ID=2')
     data = cursor.fetchall()
     cursor.close()
     return render_template('lemon.html', drinksandshakes=data)

@app.route('/sour')
def sour():
     cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
     cursor.execute('SELECT * FROM drinksandshakes Where ID=4')
     data = cursor.fetchall()
     cursor.close()
     return render_template('sour.html', drinksandshakes=data)

@app.route('/cold')
def cold():
     cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
     cursor.execute('SELECT * FROM drinksandshakes Where ID=5')
     data = cursor.fetchall()
     cursor.close()
     return render_template('cold.html', drinksandshakes=data)


@app.route('/strawbry')
def strawbry():
     cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
     cursor.execute('SELECT * FROM drinksandshakes Where ID=6')
     data = cursor.fetchall()
     cursor.close()
     return render_template('strawbry.html', drinksandshakes=data)

@app.route('/blue')
def blue():
     cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
     cursor.execute('SELECT * FROM drinksandshakes Where ID=7')
     data = cursor.fetchall()
     cursor.close()
     return render_template('blue.html', drinksandshakes=data)

@app.route('/apple')
def apple():
     cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
     cursor.execute('SELECT * FROM drinksandshakes Where ID=8')
     data = cursor.fetchall()
     cursor.close()
     return render_template('apple.html', drinksandshakes=data)

@app.route('/choclate')
def choclate():
     cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
     cursor.execute('SELECT * FROM drinksandshakes Where ID=9')
     data = cursor.fetchall()
     cursor.close()
     return render_template('choclate.html', drinksandshakes=data)

@app.route('/aboutus')
def aboutus():
     return render_template('aboutus.html')



@app.route('/comment')
def comment():
     print(session['userID'])
     return render_template('front.html')


@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('Email', None)
   session.pop('Name', None)
   # Redirect to login page
   return redirect(url_for('login'))


if __name__=="__main__":
    app.run(debug=True)        