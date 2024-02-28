#from flask import 

from db_schema import db, dbinit, UserData, CompanyData, Articles, FollowedCompanies, Notifications, AffectedCompanies

# import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from sqlalchemy.exc import IntegrityError
from sqlalchemy import text
import random

# create the Flask app
from flask import Flask, render_template,request,session,redirect,flash, jsonify
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

resetdb = True
if resetdb:
    with app.app_context():
        # drop everything, create all the tables, then put some data into the tables
        db.drop_all()
        db.create_all()
        dbinit()
login_manager = LoginManager()
login_manager.init_app(app)

@app.route('/processLogin', methods=['POST'])
def processLogin():
    username = request.form["username"]
    password = request.form["password"]
    qrytext = text("SELECT * FROM UserData WHERE username=:username;")
    qry = qrytext.bindparams(username = username)
    resultset = db.session.execute(qry)
    values = resultset.fetchall()
    if len(values) == 0:
        return jsonify({"message": "No such user exists"}), 401
    if not check_password_hash(values[0][2],password): # this means that the password provided upon registering and the password entered are different
        return jsonify({"message": "Incorrect password"}), 401
    user = UserData(values[0][0], values[0][1], values[0][2]) # setting all the information about the user
    login_user(user)
    return jsonify({"message": "Login successful"})


# Members API route - delete
@app.route("/members")
def members():
    qrytext = text("SELECT * FROM CompanyWeights")
    qry = qrytext.bindparams()
    resultset = db.session.execute(qry)

    for item in resultset:
        # Assuming the order of columns in the SELECT statement is relationOne, relationTwo, mutualFollowers
        newText = f"{item[0]} {item[1]} {item[2]}"
        print(newText)
    return {"members": ["member1", "member2", "member3"]}

if __name__ == "__main__":
    app.run(debug=True)
