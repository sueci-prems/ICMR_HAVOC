from flask import Flask,render_template,request,redirect,url_for
import easygui
import sqlite3 as sql
import csv
import random
import math
import numpy as np
from pysqlcipher import dbapi2 as sqlcipher
from sklearn import tree

app=Flask(__name__)
	
@app.route("/")
def index():
	#if request.method== 'POST':
	return render_template('index.html')


@app.route('/doctor', methods=['GET', 'POST'])
def doctor():
	#if request.method== 'POST':
	return render_template('doctor.html')

@app.route('/receptionist', methods=['GET', 'POST'])
def receptionist():
    #if request.method== 'POST':
    return render_template('receptionist.html')

@app.route('/home',methods=['GET','POST'])
def home():
	#if request.method== 'POST':
	return redirect(url_for('index')) 

@app.route('/adddoc',methods = ['POST', 'GET'])
def adddoc():
   if request.method == 'POST':
         dname = request.form['name']
         dusername = request.form['username']
         demail = request.form['email']
         dpassword = request.form['password']
         dphone = request.form['phone']
         ddob=request.form['birth']
         daddress=request.form['address']
         dspecialization=request.form['special']
         db=sqlcipher.connect('encrypted.db')
         db.executescript('pragma key="my password"; pragma kdf_iter=64000;')
         db.execute("INSERT INTO doctor (name,username,email_id,password,phone_number,dob,address,specialisation) VALUES (?,?,?,?,?,?,?,?)",(dname,dusername,demail,dpassword,dphone,ddob,daddress,dspecialization))
         easygui.msgbox("Successfully Registered ",title="Registration")
         return render_template("doctor.html")
   else:
         easygui.msgbox("Registeration failed ",title="Registration")

@app.route('/addrec',methods = ['POST', 'GET'])
def addrec():
   if request.method == 'POST':
         dname = request.form['name']
         dusername = request.form['username']
         demail = request.form['email']
         dpassword = request.form['password']
         dphone = request.form['phone']
         ddob=request.form['birth']
         daddress=request.form['address']
         dlang=request.form['language']
         db=sqlcipher.connect('encrypted.db')
         db.executescript('pragma key="my password";')
         db.execute("INSERT INTO receptionists (name,username,email_id,password,phone_number,dob,address,language) VALUES (?,?,?,?,?,?,?,?)",(dname,dusername,demail,dpassword,dphone,ddob,daddress,dlang))
         
         easygui.msgbox("Successfully Registered ",title="Registration")
         return render_template("receptionist.html")
   else:
         easygui.msgbox("Registeration failed ",title="Registration")

@app.route('/addpat',methods = ['POST', 'GET'])
def addpat():
   if request.method == 'POST':
         did = request.form['pid']
         dusername = request.form['did']
         dname = request.form['pname']
         demail = request.form['pemail']
         dphone = request.form['phone']
         daddress=request.form['paddress']
         ddob=request.form['birth']
         dblood=request.form['bg']
         db=sqlcipher.connect('encrypted.db')
         db.executescript('pragma key="my password"; pragma kdf_iter=64000;')
         db.execute("INSERT INTO patient (pid,username,name,email,contact,address,dob,bloodgrp) VALUES (?,?,?,?,?,?,?,?)",(did,dusername,dname,demail,dphone,daddress,ddob,dblood))
         easygui.msgbox("Successfully Registered ",title="Registration")
         return render_template("nurse-land.html")
   else:
         easygui.msgbox("Registeration failed ",title="Registration")



@app.route('/doclog',methods = ['POST', 'GET'])
def doclog():
	if request.method=='POST':
		dusername = request.form['username']
		dpassword = request.form['password']
		#con=sql.connect("encrypted.db")
		#cur=con.cursor()
		#cur.execute("SELECT * from doctor where username='"+dusername+"' and password='"+dpassword+"'")
		db=sqlcipher.connect('encrypted.db')
		db.executescript('pragma key="my password"; pragma kdf_iter=64000;')
		data=db.execute("SELECT * from doctor where username='"+dusername+"' and password='"+dpassword+"';").fetchone()


		#data=db.fetchone()
		if data is None:
			easygui.msgbox("Retry ",title="Login")
			return render_template("doctor.html")
		else:
			easygui.msgbox("Successfully Logged in.... ",title="Login")
			return render_template("doctor-land.html")

@app.route('/reclog',methods = ['POST', 'GET'])
def reclog():
	if request.method=='POST':
		dusername = request.form['username']
		dpassword = request.form['password']
		db=sqlcipher.connect('encrypted.db')
		db.executescript('pragma key="my password"; pragma kdf_iter=64000;')
		data=db.execute("SELECT * from receptionists where username='"+dusername+"' and password='"+dpassword+"';").fetchone()
		
		if data is None:
			easygui.msgbox("Retry ",title="Login")
			return render_template("receptionist.html")
		else:
			easygui.msgbox("Successfully Logged in.... ",title="Login")
			return render_template("nurse-land.html")


@app.route('/reclogout',methods=['POST','GET'])
def reclogout():
	return render_template("receptionist.html")

@app.route('/rechome',methods=['POST','GET'])
def rechome():
	return render_template("nurse-land.html")


@app.route('/newpat', methods=['GET', 'POST'])
def newpat():
	#if request.method== 'POST':
	return render_template('new-patient.html')

@app.route('/feedback', methods=['GET', 'POST'])			
def feedback():
	#if request.method== 'POST':
	return render_template('feedback.html')

def loadCsv(filename):
	lines = csv.reader(open(filename, "rb"))
	dataset = list(lines)
	for i in range(len(dataset)):
		dataset[i] = [float(x) for x in dataset[i]]
	return dataset

def loadCsv1(filename1):
	lines = csv.reader(open(filename1, "rb"))
	dataset1 = list(lines)
	for i in range(len(dataset1)):
		dataset1[i] = [float(x) for x in dataset1[i]]
	return dataset1


@app.route('/pred',methods=['GET', 'POST'])
def pred():
   if request.method == 'POST':
		filename = 'features.csv'
		features=loadCsv(filename)
		filename1 = 'label.csv'
		label = loadCsv1(filename1)
		X=features
		label=np.array(label)
		y=np.ravel(label)
		pid=request.form['pat-id']
		symp0 = request.form['age']
		symp1= request.form['sex']
		symp2 = request.form['cp']
		symp3 = request.form['trestbps']
		symp4 = request.form['chol']
		symp5 = request.form['fbs']
		symp6 = request.form['restecg']
		symp7 = request.form['thalach']
		symp8 = request.form['exang']
		symp9 = request.form['oldpeak']
		symp10 = request.form['slope']
		symp11 = request.form['ca']
		symp12 = request.form['thal']
		user_input=[]
		user_input.insert(0,symp0)
		user_input.insert(1,symp1)
		user_input.insert(2,symp2)
		user_input.insert(3,symp3)
		user_input.insert(4,symp4)
		user_input.insert(5,symp5)
		user_input.insert(6,symp6)
		user_input.insert(7,symp7)
		user_input.insert(8,symp8)
		user_input.insert(9,symp9)
		user_input.insert(10,symp10)
		user_input.insert(11,symp11)
		user_input.insert(12,symp12)
		clf=tree.DecisionTreeClassifier()
		clf=clf.fit(features,label)
		a=clf.predict(user_input)
		result= a[0]

		db=sqlcipher.connect('encrypted.db')
		db.executescript('pragma key="my password"; pragma kdf_iter=64000;')
		data=db.execute("SELECT * from patient where pid='"+pid+"';").fetchone()
		
		if data is None:
			easygui.msgbox("Patient already exists...",title="Prediction")
	   		return render_template("doctor-land.html")
	   	else:
	   		db.execute("INSERT INTO pat_health (pid,symp0,symp1,symp2,symp3,symp4,symp5,symp6,symp7,symp8,symp9,symp10,symp11,symp12,result) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);",(pid,symp0,symp1,symp2,symp3,symp4,symp5,symp6,symp7,symp8,symp9,symp10,symp11,symp12,result))
	   		return render_template("doctor-land.html",result=result)
	   		





if __name__=="__main__":
	app.run(debug=False)
