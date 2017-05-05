import sqlite3 as sql

def insertDoc(dname,dusername,demail,dpassword,dphone,ddob,daddress,dspecialization):
		con=sql.connect("icmr.db")
		cur=con.cursor()
		cur.execute("INSERT INTO doctor (name,username,email_id,password,phone_number,dob,address,specialisation) VALUES (?,?,?,?,?,?,?,?)",(dname,dusername,demail,dpassword,dphone,ddob,daddress,dspecialization))
		con.commit()
		con.close()