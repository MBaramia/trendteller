#from flask import 

from db_schema import db, dbinit, UserData, CompanyData, Articles, FollowedCompanies, Notifications, AffectedCompanies

# import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from sqlalchemy.exc import IntegrityError
from sqlalchemy import text
import random
import json

# create the Flask app
from flask import Flask, render_template,request,session,redirect,flash, jsonify
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash


def queryFollowedCompanies(userID):
    gettingCompaniesQry = text("SELECT * FROM FollowedCompanies JOIN CompanyData WHERE userID=:userID")
    followedCompaniesQry = gettingCompaniesQry.bindparams(userID = userID)
    resultset = db.session.execute(followedCompaniesQry)
    values = resultset.fetchall()
    allCompanies = []
    for company in values:
        getFollowing = text("SELECT * FROM FollowedCompanies WHERE userID=:userID AND companyID=:companyID")
        getFollowingQry = getFollowing.bindparams(userID = userID, companyID = company[0])
        followingResult = db.session.execute(getFollowingQry)
        followingValues = followingResult.fetchall()
        following = False
        if len(followingValues) != 0:
            following = True
        item = {"id":company[0], "name":company[3], "code":company[5], "price":company[6], "perception":"", "following":following}
        allCompanies.append(item)
    #Testing - delete below
    allCompanies.append({"id":0, "name":"Tesla", "code":"TSLA", "price":147.9400, "change": "-14.9%", "perception":-1, "following":True})
    allCompanies.append({"id":1, "name":"Google", "code":"GOOGL", "price":132.6500, "change": "+9.3%", "perception":1, "following":True})
    allCompanies.append({"id":2, "name":"PayPal", "code":"PYPL", "price":152.6500, "change": "+2.1%", "perception":0, "following":True})
    allCompanies.append({"id":3, "name":"Apple", "code":"AAPL", "price":148.3600, "change": "+1.5%", "perception":0, "following":True})
    allCompanies.append({"id":4, "name":"Amazon", "code":"AMZN", "price":3342.8800, "change": "+0.8%", "perception":1, "following":True})
    allCompanies.append({"id":5, "name":"Microsoft", "code":"MSFT", "price":305.2200, "change": "-0.5%", "perception":-1, "following":True})
    allCompanies.append({"id":6, "name":"Facebook", "code":"FB", "price":369.7900, "change": "+2.3%", "perception":1, "following":True})
    allCompanies.append({"id":7, "name":"Netflix", "code":"NFLX", "price":574.1300, "change": "-1.2%", "perception":-1, "following":True})
    allCompanies.append({"id":11, "name":"Intel", "code":"INTC", "price":54.1800, "change": "-0.9%", "perception":-1, "following":True})
    allCompanies.append({"id":12, "name":"Nvidia", "code":"NVDA", "price":220.0500, "change": "+3.7%", "perception":1, "following":True})
    allCompanies.append({"id":13, "name":"IBM", "code":"IBM", "price":139.2800, "change": "-0.3%", "perception":0, "following":True})
    allCompanies.append({"id":14, "name":"Twitter", "code":"TWTR", "price":69.4200, "change": "+1.8%", "perception":1, "following":True})
    #Testing - delete above
    result = {"data":allCompanies}
    return result


def queryAllNews():
    getNews = text("SELECT * FROM ORDER BY datetime DESC LIMIT = 15")
    getNewsQry = getNews.bindparams()
    resultset = db.session.execute(getNewsQry)
    values = resultset.fetchall()
    resultList = []
    for article in values:
        # this query gets the affected companies by an article
        getAffected = text("SELECT * FROM AffectedCompanies WHERE articleID=:articleID")
        getAffectedQry = getAffected.bindparams(articleID = article[0])
        affectedResult = db.session.execute(getAffectedQry)
        affectedValue = affectedResult.fetchall()

        #getting the company code based on the affected company ID
        getCode = text("SELECT symbol FROM CompanyData WHERE companyID=:companyID")
        getCodeQry = getCode.bindparams(companyID = affectedValue[0][0])
        codeResult = db.session.execute(getCodeQry)
        codeValue = codeResult.fetchall()

        item = {"id":article[0], "title":article[3], "companyID":affectedValue[0][0], "companyCode":codeValue[0][0], "source":"", "date":article[1], "perception":article[5]}
        jsonObject = json.dumps(item)
        resultList.append(jsonObject)
    finalResult = {"data":resultList}
    return finalResult
        

def queryAllCompanies(userID):
    getCompanies = text("SELECT * FROM CompanyData")
    getCompaniesQry = getCompanies.bindparams()
    resultset = db.session.execute(getCompaniesQry)
    values = resultset.fetchall()
    allCompanies = []
    for company in values:
        getFollowing = text("SELECT * FROM FollowedCompanies WHERE userID=:userID AND companyID=:companyID")
        getFollowingQry = getFollowing.bindparams(userID = userID, companyID = company[0])
        followingResult = db.session.execute(getFollowingQry)
        followingValues = followingResult.fetchall()
        following = False
        if len(followingValues) != 0:
            following = True
        item = {"id":company[0], "name":company[1], "code":company[3], "price":str(company[4]), "change":"change", "perception":"perception", "following":following} # need stock data and perception data for change and perception
        jsonObject = json.dumps(item, indent = 2)
        allCompanies.append(jsonObject)
    finalResult = {"data":allCompanies}
    return finalResult



def queryNotifications(userID):
    notifications = text("SELECT * FROM Notifications WHERE userID=:userID AND viewed=False")
    notificationsQry = notifications.bindparams(userID=userID)
    resultset = db.session.execute(notificationsQry)
    values = resultset.fetchall()
    notifications = []
    for notification in values:
        #gets title of article
        getTitle = text("SELECT title, source, date, effect FROM Articles WHERE articleID=:articleID")
        getTitleQry = getTitle.bindparams(articleID = notification[1])
        getTitleResult = db.session.execute(getTitleQry)
        getTitleQryValues = getTitleResult.fetchall()


        #get companyID and code
        getCompanyData = text("SELECT CompanyData.id, CompanyData.symbol FROM AffectedCompanies JOIN CompanyData ON AffectedCompanies.companyID = CompanyData.id WHERE articleID=:articleID")
        companyDataQry = getCompanyData.bindparams(articleID = notification[1])
        companyDataResult = db.session.execute(companyDataQry)
        companyDataValue = companyDataResult.fetchall()


        item = {"id":notification[0],"code":companyDataValue[0][1],"id":companyDataValue[0][0],"title":getTitleQryValues[0][0],"source":getTitleQryValues[0][1],"date":getTitleQryValues[0][2], "effect":getTitleQryValues[0][3]}
        jsonObject = json.dumps(item, indent = 2)
        notifications.append(jsonObject)
    finalResult = {"data":notifications}
    return finalResult     

def queryCompanyInfo(companyID, userID):
    getCompanies = text("SELECT * FROM CompanyData WHERE companyID=:companyID")
    getCompaniesQry = getCompanies.bindparams(companyID = companyID)
    resultset = db.session.execute(getCompaniesQry)
    values = resultset.fetchall()
    for company in values:
        getFollowing = text("SELECT * FROM FollowedCompanies WHERE userID=:userID AND companyID=:companyID")
        getFollowingQry = getFollowing.bindparams(userID = userID, companyID = company[0])
        followingResult = db.session.execute(getFollowingQry)
        followingValues = followingResult.fetchall()
        following = False
        if len(followingValues) != 0:
            following = True
        item = {"id":company[0], "code":company[3], "name":company[1], "overview":company[2], "perception":company[5],"following":following}
        return item

def queryCompanyNews(companyID):
    getCompaniesNews = text("SELECT * FROM Articles JOIN AffectedCompanies ON Articles.articleID = AffectedCompanies.articleID JOIN CompanyData ON AffectedCompanies.companyID = CompanyData.companyID WHERE companyID=:companyID")
    getCompaniesNewsQry = getCompaniesNews.bindparams(companyID = companyID)
    resultset = db.session.execute(getCompaniesNewsQry)
    values = resultset.fetchall()
    allArticles = []
    for article in values:
        item = {"id":article[0], "title":article[3], "companyID":companyID, "companyCode":article[16], "source":article[4], "date":article[1], "perception":article[6]}
        jsonObject = json.dumps(item, indent=2)
        allArticles.append(jsonObject)
    finalResult = {"data":allArticles}
    return finalResult


def queryArticleInfo(articleID, companyID):
    getArticles = text("SELECT * FROM Articles JOIN AffectedCompanies ON Articles.articleID = AffectedCompanies.articleID WHERE AffectedCompanies.companyID=:companyID")
    getArticlesQry = getArticles.bindparams(companyID = companyID)
    resultset = db.session.execute(getArticlesQry)
    values = resultset.fetchall()

    getCompanyData = text("SELECT * FROM CompanyData WHERE id=:id")
    getCompanyDataQry = getCompanyData.bindparams(id = companyID)
    companyResults = db.session.execute(getCompanyDataQry)
    companyValues = companyResults.fetchall()
    for article in values:
        item = {"title":article[3],"source":article[4],"companyID":str(companyID),"companyName":companyValues[1], "companyCode":companyValues[3], "date":article[1], "summary":article[6], "perception":article[7], "analysis":article[11], "link":article[2]}
    return item

def searchCompanies(query, userID):
    query = db.session.query(CompanyData).filter(CompanyData.name.like(f"%{query}%")) # find all of the instances where the name has the query string as a substring
    results = query.all()
    companies = []
    for company in results:
        companies.append(getCompanyInfo(company[0], userID))
    result = {"data":companies}
    return result



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



@login_manager.user_loader
def load_user(user_id):
    return UserData.query.get(int(user_id))

@app.route('/processLogin', methods=['POST'])
def processLogin():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    user = UserData.query.filter(UserData.username == username).first()
    if (not user):
        return jsonify({"message": "No such user exists"}), 401
    if not check_password_hash(user.password,password): # this means that the password provided upon registering and the password entered are different
        return jsonify({"message": "Incorrect password"}), 401
    login_user(user)
    return jsonify({"message": "Login successful"})

@app.route("/processLogout", methods=["POST"])
@login_required
def processLogout():
    logout_user()
    return jsonify({"message": "Logout successful"})

@app.route("/processRegister", methods=["POST"])
def processRegister():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    try:
        user = UserData(username, password)
        db.session.add(user)
        db.session.commit()
        login_user(user)
    except:
        return jsonify({"message": "Username is taken"}), 401
    
    return jsonify({"message": "Registration successful"})

@app.route('/processUpdate', methods=['POST'])
@login_required
def processUpdate():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    user = UserData.query.filter(UserData.id == current_user.id).first()
    user.updateDetails(username, password)
    db.session.commit()
    return jsonify({"message": "Update successful"})

@app.route('/getUserData', methods=['POST'])
@login_required
def getUserData():
    user = UserData.query.filter(UserData.id == current_user.id).first()
    username = user.username
    return jsonify({"username": username})

@app.route("/checkLoggedIn", methods=["POST"])
@login_required
def checkLoggedIn():
    return jsonify({"message": "Is logged in"})

@app.route('/getFollowedCompanies', methods=['POST'])
@login_required
def getFollowedCompanies():
    query = queryFollowedCompanies(current_user.id)
    return jsonify(query)

if __name__ == "__main__":
    app.run(debug=True)
