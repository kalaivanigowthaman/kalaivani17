from flask import Flask,render_template,url_for,redirect,request,flash
from flask_mysqldb import MySQL
app=Flask(__name__)

#mysql connection 
app.config["MYSQL_HOST"]="localhost"
app.config["MYSQL_USER"]="root"
app.config["MYSQL_PASSWORD"]="root"
app.config["MYSQL_DB"]="user"
app.config["MYSQL_CURSORCLASS"]="DictCursor"
mysql=MySQL(app)

#Loading Home Page
@app.route("/")
def home():
	con=mysql.connection.cursor()
	sql="SELECT * FROM users"
	con.execute(sql)
	res=con.fetchall()
	return render_template("home.html",datas=res)

#New User
@app.route("/addusers",methods=['GET','POST'])
def addusers():
	if request.method=='POST':
		name=request.form['name']
		age=request.form['age']
		city=request.form['city']
		con=mysql.connection.cursor()
		sql="insert into users(NAME,AGE,CITY)values(%s,%s,%s)"
		con.execute(sql,[name,age,city])
		mysql.connection.commit()
		con.close()
		flash('User Details Added!')
		return redirect(url_for("home"))
	return render_template("addusers.html")

#update
@app.route("/edituser/<string:id>",methods=['GET','POST'])
def edituser(id):
	con = mysql.connection.cursor()
	if request.method=='POST':
		name=request.form['name']
		age=request.form['age']
		city=request.form['city']
		sql="update users set Name=%s,Age=%s,city=%s Where ID=%s"
		con.execute(sql,[name,age,city,id])
		mysql.connection.commit()
		con.close()
		flash('User Details Updated!')
		return redirect(url_for("home"))
		con=mysql.connection.cursor()
	sql="select * from users where ID=%s"
	con.execute(sql,[id])
	res=con.fetchone()
	return render_template("edit.html",datas=res)

#delete user
@app.route("/deleteUser/<string:id>",methods=['GET','POST'])
def deleteUser(id):
	con = mysql.connection.cursor()
	sql="delete from users where ID=%s"
	con.execute(sql,[id])
	mysql.connection.commit()
	con.close()
	flash('User Details Deleted!')
	return redirect(url_for("home"))


if(__name__=='__main__'):
	app.secret_key="kalai123"
	app.run(debug=True)
