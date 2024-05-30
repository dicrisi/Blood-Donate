from audioop import rms
from datetime import date, datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime

from mailbox import Message
from unittest import result
from flask import Flask, render_template, request,session
from flask import Flask, render_template, json, request
#from flask_mysqldb import MySQL
#from werkzeug import generate_password_hash, check_password_hash
from flask import Flask, render_template, request, jsonify, url_for
import pymysql
import sys
import json
import random
import pymysql.cursors
from flask import Flask, render_template, request, redirect
from flask import Flask, render_template, request
from flask import flash
from werkzeug.utils import secure_filename
#from werkzeug import secure_filename
from flask import Flask, session, redirect, url_for, request
#from settings import PROJECT_ROOT
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
#import mysql.connector
app = Flask(__name__)

#UPLOAD_FOLDER = url_for('static',='/uploads')
UPLOAD_FOLDER = '/static/uploads/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'wav', 'mp3'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

connection = pymysql.connect(host='localhost',
                             user='root',
                             password='',
                             db='blooddonate',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)




@app.route('/')
def student():
   return render_template('index.html')

@app.route('/showusersignin',methods = ['POST', 'GET'])
def showusersignin():
    return render_template("usersignin.html",result = result)

@app.route('/donarsignin',methods = ['POST', 'GET'])
def donarsignin():
    return render_template("donarsignin.html",result = result)




@app.route('/services',methods = ['POST', 'GET'])
def services():
    return render_template("services.html",result = result)

@app.route('/contactus',methods = ['POST', 'GET'])
def contactus():
    return render_template("contactus.html",result = result)

@app.route('/about',methods = ['POST', 'GET'])
def aboutus():
    return render_template("about.html",result = result)



@app.route('/showuserhome',methods = ['POST', 'GET'])
def showuserhome():
    return render_template("userhome.html",result = result)



@app.route('/logout',methods = ['POST', 'GET'])
def logout():
    try:
        return render_template("index.html")
    except Exception as e:
        return json.dumps({'error': str(e)})
    

@app.route('/asigninclick',methods = ['POST', 'GET'])
def asigninclick():
   if request.method == 'POST':
      try:
          email = request.form["email"]
          pwd = request.form["pwd"]
          # validate the received values
          if email and pwd:
              connection = pymysql.connect(host='localhost',
                                           user='root',
                                           password='',
                                           db='blooddonate',
                                           charset='utf8mb4',
                                           cursorclass=pymysql.cursors.DictCursor)
              with connection.cursor() as cursor:
                  # Read a single record
                  #res = "select * from signup where email=%s and pwd=%s"
                  sql = "select * from adminlogin where user=%s and psw=%s"
                  cursor.execute(sql, (email, pwd))
                  res = cursor.fetchall()
                  if len(res) == 1:
                      connection.commit()
                      #connection.close()
                      return render_template('adminhome.html')

                  else:
                      error ="Invalid login"
                      connection.commit()
                    #  connection.close()
                      return "Invalid login"

      except Exception as e:
          return json.dumps({'error': str(e)})



@app.route('/donarsigninn', methods=['POST', 'GET'])
def donar_signin():
    if request.method == 'POST':
        try:
            dname = request.form["dname"]
            pwd = request.form["pwd"]
            
            if dname and pwd:
                connection = pymysql.connect(host='localhost',
                                             user='root',
                                             password='',
                                             db='blooddonate',
                                             charset='utf8mb4',
                                             cursorclass=pymysql.cursors.DictCursor)
                with connection.cursor() as cursor:
                    sql = "SELECT did, dname, email, blood FROM donar WHERE dname = %s AND pwd = %s"
                    cursor.execute(sql, (dname, pwd))
                    res = cursor.fetchone()

                    if res:
                        session['dname'] = res['dname']
                        session['did'] = res['did']
                        session['email'] = res['email']
                        session['blood'] = res['blood']
                        connection.commit()
                        return redirect(url_for('donar_home'))
                    else:
                        flash('Invalid Donor ID or Password', 'error')
                        return render_template('donarsignin.html')
            else:
                flash('Please enter both Donor ID and Password', 'error')
                return render_template('donarsignin.html')
        except Exception as e:
            return json.dumps({'error': str(e)})
    else:
        return render_template('donarsignin.html')


@app.route('/donarhome')
def donar_home():
    if 'dname' in session:
        return render_template('donorhome.html', dname=session['dname'])
    else:
        return redirect(url_for('donarsignin'))


@app.route('/addblood', methods=['GET', 'POST'])
def add_blood():
    if 'did' not in session:
        flash('Please log in as a donor first', 'error')
        return redirect(url_for('donar_signin'))
    
    if request.method == 'POST':
        try:
            units = request.form.get("units")
            dat = request.form.get("dat")
            
            if units and dat:
                connection = pymysql.connect(
                    host='localhost',
                    user='root',
                    password='',
                    db='blooddonate',
                    charset='utf8mb4',
                    cursorclass=pymysql.cursors.DictCursor
                )
                try:
                    with connection.cursor() as cursor:
                        sql = """
                        INSERT INTO bloodstock (did, dname, email, blood, units, dat) 
                        VALUES (%s, %s, %s, %s, %s, %s)
                        """
                        cursor.execute(sql, (session['did'], session['dname'], session['email'], session['blood'], units, dat))
                        connection.commit()
                        flash('Blood units added successfully', 'success')
                        return redirect(url_for('add_blood'))
                finally:
                    connection.close()
            else:
                flash('Please enter the number of units and date', 'error')
        except Exception as e:
            flash('An error occurred while adding blood units: ' + str(e), 'error')
    
    return render_template('addblood.html')

@app.route('/viewdonar',methods = ['POST', 'GET'])
def adminviewdonor():
    try:
        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='',
                                     db='blooddonate',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        with connection.cursor() as cursor:
            sql = "select * from donar"
            cursor.execute(sql)
            data = cursor.fetchall()
            return render_template("adminviewdonar.html",data=data,id=0)
    except Exception as e:
        return json.dumps({'error': str(e)})
    


@app.route('/viewdonar/<int:bid>',methods = ['POST', 'GET'])
def admindonar(bid):
    try:
        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='',
                                     db='blooddonate',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        with connection.cursor() as cursor:
            sql = "select * from donar"
            cursor.execute(sql)
            data = cursor.fetchall()
            return render_template("adminviewdonar.html",data=data,id=bid)
    except Exception as e:
        return json.dumps({'error': str(e)})



@app.route('/viewdonorblood', methods=['POST', 'GET'])
def donorblood():
    try:
        if 'email' not in session:
            return redirect(url_for('login'))  # Redirect to login if not logged in

        email = session['email']

        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='',
                                     db='blooddonate',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        with connection.cursor() as cursor:
            sql = "SELECT * FROM bloodstock WHERE email = %s"
            cursor.execute(sql, (email,))
            data = cursor.fetchall()
            return render_template("viewdonarblood.html", data=data, id=0)
    except Exception as e:
        return json.dumps({'error': str(e)})

@app.route('/viewdonorblood/<int:bid>', methods=['POST', 'GET'])
def eituser(bid):
    try:
        if 'email' not in session:
            return redirect(url_for('login'))  # Redirect to login if not logged in

        email = session['email']

        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='',
                                     db='blooddonate',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        with connection.cursor() as cursor:
            sql = "SELECT * FROM bloodstock WHERE id = %s AND email = %s"
            cursor.execute(sql, (bid, email))
            data = cursor.fetchall()
            return render_template("viewdonarblood.html", data=data, id=bid)
    except Exception as e:
        return json.dumps({'error': str(e)})



@app.route('/viewbloodstock',methods = ['POST', 'GET'])
def view_bloodstock():
    try:
        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='',
                                     db='blooddonate',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        with connection.cursor() as cursor:
            sql = "select * from bloodstock"
            cursor.execute(sql)
            data = cursor.fetchall()
            return render_template("adminbloodstock.html",data=data,id=0)
    except Exception as e:
        return json.dumps({'error': str(e)})

@app.route('/viewbloodstock/<int:bid>',methods = ['POST', 'GET'])
def adminitblood(bid):
    try:
        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='',
                                     db='blooddonate',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        with connection.cursor() as cursor:
            sql = "select * from bloodstock"
            cursor.execute(sql)
            data = cursor.fetchall()
            return render_template("adminbloodstock.html",data=data,id=bid)
    except Exception as e:
        return json.dumps({'error': str(e)})



@app.route('/viewpatientblood',methods = ['POST', 'GET'])
def view_patientblood():
    try:
        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='',
                                     db='blooddonate',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        with connection.cursor() as cursor:
            sql = "select * from donar"
            cursor.execute(sql)
            data = cursor.fetchall()
            return render_template("viewpatientblood.html",data=data,id=0)
    except Exception as e:
        return json.dumps({'error': str(e)})

@app.route('/viewpatientblood/<int:did>',methods = ['POST', 'GET'])
def ituser(did):
    try:
        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='',
                                     db='blooddonate',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        with connection.cursor() as cursor:
            sql = "select * from donar"
            cursor.execute(sql)
            data = cursor.fetchall()
            return render_template("viewpatientblood.html",data=data,id=did)
    except Exception as e:
        return json.dumps({'error': str(e)})



@app.route('/viewpatient',methods = ['POST', 'GET'])
def viewpatient():
    try:
        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='',
                                     db='blooddonate',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        with connection.cursor() as cursor:
            sql = "select * from patient"
            cursor.execute(sql)
            data = cursor.fetchall()
            return render_template("adminpatient.html",data=data,id=0)
    except Exception as e:
        return json.dumps({'error': str(e)})

@app.route('/viewpatient/<int:pid>',methods = ['POST', 'GET'])
def patient__blood(pid):
    try:
        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='',
                                     db='blooddonate',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        with connection.cursor() as cursor:
            sql = "select * from patient"
            cursor.execute(sql)
            data = cursor.fetchall()
            return render_template("adminpatient.html",data=data,id=pid)
    except Exception as e:
        return json.dumps({'error': str(e)})





# Route to render the create new donor account page
@app.route('/newaccount', methods=['GET'])
def new_account():
    return render_template('donarnewaccount.html')


@app.route('/newaccount', methods=['POST'])
def create_new_account():
    
    dname = request.form['dname']
    
    pwd = request.form['Pwd']
    email = request.form['emailid']
    mbl = request.form['mbl']
    blood = request.form['blood']
    dob = request.form['dob']
    addr = request.form['addr']
    

    connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='',
                                     db='blooddonate',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)

    with connection.cursor() as cursor:
            sql = "INSERT INTO donar (dname, pwd, email, mbl, blood,dob,addr) VALUES (%s, %s, %s,%s, %s, %s, %s)"
            cursor.execute(sql, (dname, pwd, email, mbl, blood,dob,addr))
            connection.commit()
   
    return render_template('donarnewaccount.html', dname=dname)



@app.route('/donardetails', methods=['POST', 'GET'])
def donar():
    if 'email' not in session:
        flash('Please log in as a donor first', 'error')
        return redirect(url_for('donarsignin'))
    
    try:
        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='',
                                     db='blooddonate',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        with connection.cursor() as cursor:
            sql = "SELECT * FROM donar WHERE email = %s"
            cursor.execute(sql, (session['email'],))
            data = cursor.fetchall()
            return render_template("donardetails.html", data=data, id=0)
    except Exception as e:
        return json.dumps({'error': str(e)})

@app.route('/donardetails/<int:did>', methods=['POST', 'GET'])
def aeituser(did):
    if 'email' not in session:
        flash('Please log in as a donor first', 'error')
        return redirect(url_for('donarsignin'))

    try:
        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='',
                                     db='blooddonate',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        with connection.cursor() as cursor:
            sql = "SELECT * FROM donar WHERE email = %s"
            cursor.execute(sql, (session['email'],))
            data = cursor.fetchall()
            return render_template("donardetails.html", data=data, id=did)
    except Exception as e:
        return json.dumps({'error': str(e)})


@app.route('/patientnewaccount', methods=['GET'])
def patient_new_account():
    return render_template('patientaccount.html')


@app.route('/patientnewaccount', methods=['POST'])
def create_patient_account():
   
    pname = request.form['pname']
    psw = request.form['Psw']
    email = request.form['email']
    mob = request.form['mob']
    blood = request.form['blood']
    dat = request.form['dat']
    address = request.form['address']

    # Add logic to store the new patient account details in the database or perform other operations as needed
    # For example, you can use SQLAlchemy to interact with the database
    connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='',
                                     db='blooddonate',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)

    with connection.cursor() as cursor:
            sql = "INSERT INTO patient (pname, psw, email, mob, blood,dat,address) VALUES (%s, %s, %s,%s, %s, %s, %s)"
            cursor.execute(sql, (pname, psw, email, mob, blood,dat,address))
            connection.commit()
    # Redirect to a success page or render a success message
    return render_template('patientaccount.html', pname=pname)




@app.route('/patientdetails', methods=['POST', 'GET'])
def patient_details():
    if 'pname' not in session:
        flash('Please log in as a patient first', 'error')
        return redirect(url_for('usersignin'))
    
    try:
        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='',
                                     db='blooddonate',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        with connection.cursor() as cursor:
            sql = "SELECT * FROM patient WHERE pname = %s"
            cursor.execute(sql, (session['pname'],))
            data = cursor.fetchall()
            return render_template("patientdetails.html", data=data, pid=0)
    except Exception as e:
        return json.dumps({'error': str(e)})

@app.route('/patientdetails/<int:pid>', methods=['POST', 'GET'])
def patient(pid):
    if 'pname' not in session:
        flash('Please log in as a donor first', 'error')
        return redirect(url_for('usersignin'))

    try:
        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='',
                                     db='blooddonate',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        with connection.cursor() as cursor:
            sql = "SELECT * FROM patient WHERE pname = %s"
            cursor.execute(sql, (session['pname'],))
            data = cursor.fetchall()
            return render_template("patientdetails.html", data=data, pid=pid)
    except Exception as e:
        return json.dumps({'error': str(e)})

    


@app.route('/showadminsignin',methods = ['POST', 'GET'])
def showadminsignin():
    return render_template("adminsignin.html",result = result)



@app.route('/usigninclick', methods=['POST', 'GET'])
def usigninclick():
    if request.method == 'POST':
        try:
            p1 = request.form["p1"]
            p2 = request.form["p2"]
            # Validate the received values
            if p1 and p2:
                connection = pymysql.connect(host='localhost',
                                             user='root',
                                             password='',
                                             db='blooddonate',
                                             charset='utf8mb4',
                                             cursorclass=pymysql.cursors.DictCursor)
                with connection.cursor() as cursor:
                    # Read a single record
                    sql = "SELECT pid FROM patient WHERE pname = %s AND psw = %s"
                    cursor.execute(sql, (p1, p2))
                    res = cursor.fetchone()  # Assuming there's only one matching record

                    if res:  # If a matching record is found
                        session['pname'] = p1
                        session['pid'] = res['pid']  # Store the id in session
                        connection.commit()
                        return render_template('userhome.html')
                    else:
                        error = "Invalid login"
                        return "Invalid login"
        except Exception as e:
            return json.dumps({'error': str(e)})
    else:
        return "Method not allowed"





@app.route('/')
def index():
    # Generate the URL for the image
    gif = url_for('static', filename='images/vutura-chatbot.gif')
    return render_template("index.html", chat_gif=gif)  # Pass images to the template

@app.route('/adminhome',methods = ['POST', 'GET'])
def adminhome():
    return render_template("adminhome.html",result = result)



if __name__ == '__main__':
   app.secret_key = "sadfsdfdfssdfadsfsdfsd"
   app.run(port=5020)