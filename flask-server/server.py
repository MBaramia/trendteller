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

# fake stock data
from fake_data import fakeData, fakePredicton, dates, combinedData

# websocket
from flask_socketio import SocketIO, emit

# cors
from flask_cors import CORS


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
    allCompanies.append({"id":0, "name":"Tesla", "code":"TSLA", "price":147.9400, "change": "-14.9%", "perception":0, "following":True})
    allCompanies.append({"id":1, "name":"Google", "code":"GOOGL", "price":132.6500, "change": "+9.3%", "perception":2, "following":True})
    allCompanies.append({"id":2, "name":"PayPal", "code":"PYPL", "price":152.6500, "change": "+2.1%", "perception":1, "following":True})
    allCompanies.append({"id":3, "name":"Apple", "code":"AAPL", "price":148.3600, "change": "+1.5%", "perception":1, "following":True})
    allCompanies.append({"id":4, "name":"Amazon", "code":"AMZN", "price":3342.8800, "change": "+0.8%", "perception":2, "following":True})
    allCompanies.append({"id":5, "name":"Microsoft", "code":"MSFT", "price":305.2200, "change": "-0.5%", "perception":0, "following":True})
    allCompanies.append({"id":6, "name":"Facebook", "code":"FB", "price":369.7900, "change": "+2.3%", "perception":2, "following":True})
    allCompanies.append({"id":7, "name":"Netflix", "code":"NFLX", "price":574.1300, "change": "-1.2%", "perception":0, "following":True})
    allCompanies.append({"id":11, "name":"Intel", "code":"INTC", "price":54.1800, "change": "-0.9%", "perception":0, "following":True})
    allCompanies.append({"id":12, "name":"Nvidia", "code":"NVDA", "price":220.0500, "change": "+3.7%", "perception":2, "following":True})
    allCompanies.append({"id":13, "name":"IBM", "code":"IBM", "price":139.2800, "change": "-0.3%", "perception":1, "following":True})
    allCompanies.append({"id":14, "name":"Twitter", "code":"TWTR", "price":69.4200, "change": "+1.8%", "perception":2, "following":True})
    #Testing - delete above
    result = {"data":allCompanies}
    return result


def queryAllNews():
    getNews = text("SELECT * FROM Articles ORDER BY datetime DESC LIMIT 15")
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
        getCode = text("SELECT symbol FROM CompanyData WHERE id=:companyID")
        getCodeQry = getCode.bindparams(companyID = affectedValue[0][0])
        codeResult = db.session.execute(getCodeQry)
        codeValue = codeResult.fetchall()

        item = {"id":article[0], "title":article[3], "companyID":affectedValue[0][0], "companyCode":codeValue[0][0], "source":"", "date":article[1], "perception":article[5]}
        resultList.append(item)

    #Testing - delete below
    resultList.append({"id":1, "title":"Microsoft unveils new Windows 12 operating system", "companyID":7, "companyCode":"MSFT", "source":"BBC", "date":"20/02/2024", "perception":2})
    resultList.append({"id":2, "title":"Apple announces new iPhone 13 with advanced features", "companyID":3, "companyCode":"AAPL", "source":"TechCrunch", "date":"09/15/2021", "perception":1})
    resultList.append({"id":3, "title":"Amazon launches new delivery drone technology", "companyID":4, "companyCode":"AMZN", "source":"CNN", "date":"09/14/2021", "perception":2})
    resultList.append({"id":4, "title":"Microsoft acquires leading AI startup", "companyID":5, "companyCode":"MSFT", "source":"The Verge", "date":"09/13/2021", "perception":2})
    resultList.append({"id":5, "title":"Facebook introduces new privacy features", "companyID":6, "companyCode":"FB", "source":"Reuters", "date":"09/12/2021", "perception":1})
    resultList.append({"id":6, "title":"Netflix announces partnership with top Hollywood studio", "companyID":7, "companyCode":"NFLX", "source":"Variety", "date":"09/11/2021", "perception":0})
    resultList.append({"id":7, "title":"Intel unveils breakthrough processor technology", "companyID":11, "companyCode":"INTC", "source":"PCMag", "date":"09/10/2021", "perception":0})
    #Testing - delete above
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
        item = {"id":company[0], "name":company[1], "code":company[3], "price":str(company[4]), "change":"+1.0", "perception":1, "following":following} # need stock data and perception data for change and perception
        allCompanies.append(item)
    #Testing - delete below
    allCompanies.append({"id":5, "name":"PayPal", "code":"PYPL", "price":152.6500, "change": "+2.1%", "perception":1, "following":True})
    allCompanies.append({"id":6, "name":"Amazon", "code":"AMZN", "price":3342.8800, "change": "+0.8%", "perception":2, "following":True})
    allCompanies.append({"id":7, "name":"Facebook", "code":"FB", "price":369.7900, "change": "+2.3%", "perception":2, "following":True})
    allCompanies.append({"id":8, "name":"Netflix", "code":"NFLX", "price":574.1300, "change": "-1.2%", "perception":0, "following":True})
    allCompanies.append({"id":9, "name":"Intel", "code":"INTC", "price":54.1800, "change": "-0.9%", "perception":0, "following":True})
    allCompanies.append({"id":10, "name":"Nvidia", "code":"NVDA", "price":220.0500, "change": "+3.7%", "perception":2, "following":True})
    allCompanies.append({"id":11, "name":"IBM", "code":"IBM", "price":139.2800, "change": "-0.3%", "perception":1, "following":True})
    allCompanies.append({"id":12, "name":"Twitter", "code":"TWTR", "price":69.4200, "change": "+1.8%", "perception":2, "following":True})
    #Testing - delete above
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


        item = {"id":notification[0],"companyCode":companyDataValue[0][1],"companyID":companyDataValue[0][0],"title":getTitleQryValues[0][0],"source":getTitleQryValues[0][1],"date":getTitleQryValues[0][2], "perception":getTitleQryValues[0][3]}
        notifications.append(item)
    #Testing - delete below
    notifications.append({"id":0,"companyCode":"MSFT","companyID":5,"title":"Microsoft unveils new Windows 12 operating system","source":"BBC","date":"20/02/2024", "perception":1})
    notifications.append({"id":1,"companyCode":"AAPL","companyID":3,"title":"Apple announces new iPhone 13 with advanced features","source":"TechCrunch","date":"09/15/2021", "perception":1})
    notifications.append({"id":2,"companyCode":"AMZN","companyID":4,"title":"Amazon launches new delivery drone technology","source":"CNN","date":"09/14/2021", "perception":2})
    notifications.append({"id":3,"companyCode":"MSFT","companyID":5,"title":"Microsoft acquires leading AI startup","source":"The Verge","date":"09/13/2021", "perception":2})
    notifications.append({"id":4,"companyCode":"FB","companyID":6,"title":"Facebook introduces new privacy features","source":"Reuters","date":"09/12/2021", "perception":1})
    notifications.append({"id":5,"companyCode":"NFLX","companyID":7,"title":"Netflix announces partnership with top Hollywood studio","source":"Variety","date":"09/11/2021", "perception":0})
    notifications.append({"id":6,"companyCode":"INTC","companyID":11,"title":"Intel unveils breakthrough processor technology","source":"PCMag","date":"09/10/2021", "perception":0})
    notifications.append({"id":7,"companyCode":"PYPL","companyID":2,"title":"PayPal introduces new payment platform","source":"Forbes","date":"09/09/2021", "perception":1})
    notifications.append({"id":8,"companyCode":"NVDA","companyID":12,"title":"Nvidia launches new graphics card series","source":"Tom's Hardware","date":"09/08/2021", "perception":2})
    notifications.append({"id":9,"companyCode":"IBM","companyID":13,"title":"IBM announces breakthrough in quantum computing","source":"ZDNet","date":"09/07/2021", "perception":1})
    notifications.append({"id":10,"companyCode":"TWTR","companyID":14,"title":"Twitter introduces new feature to combat misinformation","source":"The Guardian","date":"09/06/2021", "perception":2})
    #Testing - delete above
    finalResult = {"data":notifications}
    return finalResult     

def queryCompanyInfo(companyID, userID):
    getCompanies = text("SELECT * FROM CompanyData WHERE id=:companyID")
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
    getCompaniesNews = text("SELECT * FROM Articles JOIN AffectedCompanies ON Articles.id = AffectedCompanies.articleID JOIN CompanyData ON AffectedCompanies.companyID = CompanyData.id WHERE CompanyData.id=:companyID")
    getCompaniesNewsQry = getCompaniesNews.bindparams(companyID = companyID)
    resultset = db.session.execute(getCompaniesNewsQry)
    values = resultset.fetchall()
    allArticles = []
    for article in values:
        item = {"id":article[0], "title":article[3], "companyID":companyID, "companyCode":article[16], "source":article[4], "date":article[1], "perception":article[6]}
        allArticles.append(item)
    #Testing - delete below
    print(len(allArticles))
    allArticles.append({"id":1, "title":"Microsoft unveils new Windows 12 operating system", "companyID":7, "companyCode":"MSFT", "source":"BBC", "date":"20/02/2024", "perception":2})
    allArticles.append({"id":2, "title":"Apple announces new iPhone 13 with advanced features", "companyID":3, "companyCode":"AAPL", "source":"TechCrunch", "date":"09/15/2021", "perception":1})
    allArticles.append({"id":3, "title":"Amazon launches new delivery drone technology", "companyID":4, "companyCode":"AMZN", "source":"CNN", "date":"09/14/2021", "perception":2})
    allArticles.append({"id":4, "title":"Microsoft acquires leading AI startup", "companyID":5, "companyCode":"MSFT", "source":"The Verge", "date":"09/13/2021", "perception":2})
    allArticles.append({"id":5, "title":"Facebook introduces new privacy features", "companyID":6, "companyCode":"FB", "source":"Reuters", "date":"09/12/2021", "perception":1})
    allArticles.append({"id":6, "title":"Netflix announces partnership with top Hollywood studio", "companyID":7, "companyCode":"NFLX", "source":"Variety", "date":"09/11/2021", "perception":0})
    allArticles.append({"id":7, "title":"Intel unveils breakthrough processor technology", "companyID":11, "companyCode":"INTC", "source":"PCMag", "date":"09/10/2021", "perception":0})
    #Testing - delete above
    finalResult = {"data":allArticles}
    return finalResult


def queryArticleInfo(articleID, companyID):
    getArticles = text("SELECT * FROM Articles JOIN AffectedCompanies ON Articles.id = AffectedCompanies.articleID WHERE AffectedCompanies.companyID=:companyID")
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
    #Testing - delete below
    item = {"title":"Elon Musk eats humble pie over unpaid bakery bill","source":"BBC","companyID":0,"companyName":"Tesla", "companyCode":"TSLA", "date":"28/02/2024", "summary":"Elon Musk has covered the cost of 4,000 mini pies for Giving Pies bakery in San Jose after Tesla canceled a last-minute order, leaving the small business $2,000 short. Musk responded to the bakery's social media complaint, stating he would resolve the issue. Tesla placed a new order for 3,600 pies, but the overwhelmed bakery, flooded with business from well-wishers, had to decline. The owner expressed gratitude, and even the mayor of San Jose acknowledged the community's support and thanked Musk for covering the cost.", "perception":2, "analysis":"This article may elicit a mixed response regarding public opinion of Tesla. Elon Musk's prompt intervention and willingness to cover the cost of the canceled bakery order could be viewed positively, showcasing a sense of responsibility and commitment to customer satisfaction. However, the initial cancellation might raise concerns about Tesla's reliability and communication with suppliers. The overwhelming support the bakery received after Musk's involvement may shed light on the power dynamics between large corporations and small businesses, potentially sparking discussions about fair business practices. Ultimately, while the incident highlights the scrutiny faced by prominent companies like Tesla, Musk's swift resolution is likely to leave a more positive impression on public perception.", "link":"https://www.bbc.co.uk/news/technology-68404698"}
    return item
    #Testing - delete above

def querySearchCompanies(query, userID):
    query = db.session.query(CompanyData).filter(CompanyData.name.like(f"%{query}%")) # find all of the instances where the name has the query string as a substring
    results = query.all()
    companies = []
    for company in results:
        companies.append(queryCompanyInfo(company.id, userID))
    result = {"data":companies}
    return result

def queryRecommendedCompanies(userID):
    #Placeholder - replace with actual logic (should return exactly 3 companies)
    allCompanies = []
    allCompanies.append({"id":5, "name":"PayPal", "code":"PYPL", "price":152.6500, "change": "+2.1%", "perception":1, "following":False})
    allCompanies.append({"id":6, "name":"Amazon", "code":"AMZN", "price":3342.8800, "change": "+0.8%", "perception":0, "following":False})
    allCompanies.append({"id":7, "name":"Facebook", "code":"FB", "price":369.7900, "change": "+2.3%", "perception":2, "following":False})
    #Placeholder - replace with actual logic
    finalResult = {"data":allCompanies}
    return finalResult

def switchFollowing(userID, companyID):
    getFollowing = text("SELECT * FROM FollowedCompanies WHERE userID=:userID AND companyID=:companyID")
    getFollowingQry = getFollowing.bindparams(userID = userID, companyID = companyID)
    followingResult = db.session.execute(getFollowingQry)
    followingValues = followingResult.fetchall()
    if len(followingValues) != 0:
        # Entry exists, delete it
        deleteFollowing = text("DELETE FROM FollowedCompanies WHERE userID=:userID AND companyID=:companyID")
        deleteFollowingQry = deleteFollowing.bindparams(userID=userID, companyID=companyID)
        db.session.execute(deleteFollowingQry)
        db.session.commit()
        socketio.emit("database_updated", {"data": "Company unfollowed"})
        return "Company unfollowed"
    insertFollowing = text("INSERT INTO FollowedCompanies (userID, companyID) VALUES (:userID, :companyID)")
    insertFollowingQry = insertFollowing.bindparams(userID=userID, companyID=companyID)
    db.session.execute(insertFollowingQry)
    db.session.commit()
    socketio.emit("database_updated", {"data": "Company followed"})
    return "Company followed"

def queryStockData(companyID):
    return combinedData

def queryPredictedStockData(companyID):
    return fakePredicton

def queryMainStockData(companyID):
    #Placeholder - replace with actual logic
    data = {
        "open": "145.4100",  
        "high": "148.1000", 
        "low": "145.2100", 
        "price": "147.9400", 
        "volume": "15198607"
    }
    #Placeholder - replace with actual logic
    return data

def queryStockChanges(companyID):
    #Placeholder - replace with actual logic
    data = {
        "data": [
            "+18.32 (0.49%)", "+12.04 (6.38%)", "-1.87 (-0.92%)", "+181.25 (922.39%)",
            "+18.32 (0.49%)", "+12.04 (6.38%)", "-1.87 (-0.92%)", "+181.25 (922.39%)"
        ]
    }
    #Placeholder - replace with actual logic
    return data

def queryStockDates(companyID):
    return dates

app = Flask(__name__)

# add cors policy
CORS(app)

# create websocket
socketio = SocketIO(app, cors_allowed_origins="http://localhost:3000")

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
    return jsonify({"message": "Update successful", "success":True})

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

@app.route('/getAllNews', methods=['POST'])
@login_required
def getAllNews():
    query = queryAllNews()
    return jsonify(query)

@app.route('/getAllCompanies', methods=['POST'])
@login_required
def getAllCompanies():
    query = queryAllCompanies(current_user.id)
    return jsonify(query)

@app.route('/getNotifications', methods=['POST'])
@login_required
def getNotifications():
    query = queryNotifications(current_user.id)
    return jsonify(query)

@app.route('/getCompanyInfo', methods=['POST'])
@login_required
def getCompanyInfo():
    data = request.get_json()
    companyID = data.get("companyID")

    query = queryCompanyInfo(companyID, current_user.id)
    return jsonify(query)

@app.route('/getCompanyNews', methods=['POST'])
@login_required
def getCompanyNews():
    data = request.get_json()
    companyID = data.get("companyID")

    query = queryCompanyNews(companyID)
    return jsonify(query)

@app.route('/getArticleInfo', methods=['POST'])
@login_required
def getArticleInfo():
    data = request.get_json()
    articleID = data.get("articleID")
    companyID = data.get("companyID")

    query = queryArticleInfo(articleID, companyID)
    return jsonify(query)

@app.route('/searchCompanies', methods=['POST'])
@login_required
def searchCompanies():
    data = request.get_json()
    query= data.get("query")

    result = querySearchCompanies(query, current_user.id)
    return jsonify(result)

@app.route('/getRecommendedCompanies', methods=['POST'])
@login_required
def getRecommendedCompanies():
    query = queryRecommendedCompanies(current_user.id)
    return jsonify(query)

@app.route('/getStockData', methods=['POST'])
@login_required
def getStockData():
    data = request.get_json()
    companyID = data.get("companyID")

    query = queryStockData(companyID)
    return jsonify(query)

@app.route('/getPredictedStockData', methods=['POST'])
@login_required
def getPredictedStockData():
    data = request.get_json()
    companyID = data.get("companyID")

    query = queryPredictedStockData(companyID)
    return jsonify(query)

@app.route('/getMainStockData', methods=['POST'])
@login_required
def getMainStockData():
    data = request.get_json()
    companyID = data.get("companyID")

    query = queryMainStockData(companyID)
    return jsonify(query)

@app.route('/getStockChanges', methods=['POST'])
@login_required
def getStockChanges():
    data = request.get_json()
    companyID = data.get("companyID")

    query = queryStockChanges(companyID)
    return jsonify(query)

@app.route('/getStockDates', methods=['POST'])
@login_required
def getStockDates():
    data = request.get_json()
    companyID = data.get("companyID")

    query = queryStockDates(companyID)
    return jsonify(query)

@app.route('/toggleFollowing', methods=['POST'])
@login_required
def toggleFollowing():
    data = request.get_json()
    companyID = data.get("companyID")

    query = switchFollowing(current_user.id, companyID)
    return jsonify(query)

if __name__ == "__main__":
    app.run(debug=True)
