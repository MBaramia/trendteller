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
app.config["SECRET_KEY"] = "fdhsbfdsh3274y327432"

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

def queryFollowedCompanies(userID):
    gettingCompaniesQry = text("SELECT companyID FROM FollowedCompanies WHERE userID=:userID")
    followedCompaniesQry = gettingCompaniesQry.bindparams(userID = userID)
    resultset = db.session.execute(followedCompaniesQry)
    values = resultset.fetchall()
    print(values)

def queryAllNews():
    getNews = text("SELECT * FROM ORDER BY datetime DESC LIMIT = 15")
    getNewsQry = getNews.bindparams()
    resultset = db.session.execute(getNewsQry)
    values = resultset.fetchall()

def queryAllCompanies():
    getCompanies = text("SELECT * FROM Companies")
    getCompaniesQry = getCompanies.bindparams()
    resultset = db.session.execute(getCompaniesQry)
    values = resultset.fetchall()
    print(values)


def queryNotifications(userID):
    notifications = text("SELECT * FROM Notifications WHERE userID=:uerID AND viewed=False")
    notificationsQry = notifications.bindparams(userID=userID)
    resultset = db.session.execute(notificationsQry)
    values = resultset.fetchall()

def queryCompanyInfo(companyID):
    getCompanies = text("SELECT * FROM Companies WHERE companyID=:companyID")
    getCompaniesQry = getCompanies.bindparams(companyID = companyID)
    resultset = db.session.execute(getCompaniesQry)
    values = resultset.fetchall()

def queryCompanyNews(companyID):
    getCompaniesNews = text("SELECT * FROM Articles")
    getCompaniesNewsQry = getCompaniesNews.bindparams()
    resultset = db.session.execute(getCompaniesNewsQry)
    values = resultset.fetchall()

def queryArticleInfo(articleID, companyID):
    getArticles = text("SELECT * FROM Articles JOIN AffectedCompanies ON Articles.ArticleID = AffectedCompanies.ArticleID WHERE AffectedCompanies.CompanyID=:companyID")
    getArticlesQry = getArticles.bindparams(companyID = companyID)
    resultset = db.session.execute(getArticlesQry)
    values = resultset.fetchall()

def querySearchCompanies(query):
    query = db.session.query(CompanyData).filter(CompanyData.name.like(f"%{query}%")) # find all of the instances where the name has the query string as a substring
    results = query.all()


