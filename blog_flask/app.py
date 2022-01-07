from flask import Flask ,render_template , url_for , redirect , request , session
from datetime import date
import json , hashlib , time 
import os 

app=Flask(__name__)

def write_json(data,filename="main.json"):
	with open(filename , "w") as f :
		json.dump(data,f,indent = 4)

def CreateAccount_db(username , password , birth):
	with open("main.json") as json_file:
		data = json.load(json_file)
		temp = data["account"]     # temp is the obj ( array ) ,  
		n = {"username":username , "password":password , "birth" : birth , "post":[]}
		temp.append(n)
	write_json(data)

def IfAccountNotExist(AccountName):
	with open("main.json") as json_file:
		data = json.load(json_file)
		temp = data["account"]
		for i in range(len(temp)):
			if AccountName == temp[i]['username']:
				return False 
	return True

def GetPersonalInfomation(username):
	with open("main.json") as file:
		data = json.load(file)
		temp = data["account"]
		for i in range(len(temp)):
			if username == temp[i]['username']:
				return temp[i]['birth']
	return False 

def CheckAccount(username,password):
	with open("main.json") as file:
		data = json.load(file)
		temp = data["account"]
		for i in range(len(temp)):
			if username == temp[i]['username'] and password == temp[i]['password']:
				return True
	return False  

def IsValidDate(datestr):
	if len(datestr) == 8 :
		datestr = datestr[0:4] + '-' + datestr[4:6] + '-' + datestr[6:]
	print(datestr)
	try:
		date.fromisoformat(datestr)
	except:
		return False 
	else:
		return True 

def CreatePost(who,content):
	pass

@app.route("/")
def home():
	return render_template('index.html')

@app.route("/content")
def content():
	return render_template('content.html')

@app.route("/login",methods = ["POST","GET"])
def Login():
	if request.method == "POST":
		if CheckAccount(request.form['nm'],request.form['pd']):
			now = GetPersonalInfomation(request.form['nm'])
			#return f"<h1> hello " + str(request.form['nm']) + " ! \n your birthday is " + str(now) +"</h1> " 
			return render_template('content.html') 
		else:
			return f"<h1> username or password was wrong , check it again" 
	else:
		return render_template('login.html')
		#if request.form["nm"] in database and database[request.form["nm"]] == request.form["pd"]: # see if username and password wright
		#	return mainpage #after login , see the personal page 
		#else :
		#	return f"<h1>your password or username was wrong<h1>"

@app.route("/CreateAccount",methods = ["POST","GET"])
def CreateAccount():
	if request.method == "POST":
		if request.form["pd"] == request.form["pd1"] and IsValidDate(request.form["birth"]) and IfAccountNotExist(request.form["nm"]):
			CreateAccount_db(request.form["nm"] , request.form["pd"] , request.form["birth"])
			return f"<h1> create account successful , you can login now!" 
		else:
			return f"<h1> this user name has been used !" 
	else:
		return render_template('CreateAccount.html')

@app.route("/<usr>")
def user(usr):
	return f"<h1>{usr}</h1>"

if __name__ == '__main__':
	app.run(debug=True)

