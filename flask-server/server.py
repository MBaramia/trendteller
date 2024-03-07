#from flask import 

from db_schema import db, dbinit, UserData, CompanyData, Articles, FollowedCompanies, Notifications, AffectedCompanies, Prediction

# import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from sqlalchemy.exc import IntegrityError
from sqlalchemy import text
import random
import json
from apscheduler.schedulers.background import BackgroundScheduler
import atexit
# create the Flask app
from flask import Flask, render_template,request,session,redirect,flash, jsonify
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone

# fake stock data
from fake_data import fakeData, fakePredicton, dates, combinedData, predictedDates
from stock_price_prediction import fetch_stock_prediction

# websocket
from flask_socketio import SocketIO, emit

# cors
from flask_cors import CORS
scheduler = BackgroundScheduler()
scheduler.start()

def fetch_and_store_predictions(timeframe):
    company_ids = [0, 1, 2]  # Example company IDs
    for company_id in company_ids:
        fetch_stock_prediction(company_id, timeframe)

# Schedule jobs for different timeframes
scheduler.add_job(func=lambda: fetch_and_store_predictions('intraday'), trigger='interval', hours=1, id='intraday_prediction_job')
scheduler.add_job(func=lambda: fetch_and_store_predictions('daily'), trigger='interval', hours=24, id='daily_prediction_job')
scheduler.add_job(func=lambda: fetch_and_store_predictions('weekly'), trigger='interval', days=7, id='weekly_prediction_job')
scheduler.add_job(func=lambda: fetch_and_store_predictions('monthly'), trigger='interval', weeks=4, id='monthly_prediction_job')

# Ensure the scheduler is shut down properly on exit
atexit.register(lambda: scheduler.shutdown())

# integrated
# need stock data and perception data for change and perception
def queryFollowedCompanies(userID):
    gettingCompaniesQry = text("""
        SELECT CompanyData.id, name, symbol 
        FROM FollowedCompanies 
        JOIN CompanyData ON FollowedCompanies.companyID = CompanyData.id
        WHERE FollowedCompanies.userID = :userID
    """)
    followedCompaniesQry = gettingCompaniesQry.bindparams(userID = userID)
    resultset = db.session.execute(followedCompaniesQry)
    values = resultset.fetchall()
    allCompanies = []

    for company in values:
        # waiting for real data to produce price
        item = {
            "id":company[0], 
            "name":company[1], 
            "code":company[2], 
            "price":random.randint(50, 200), 
            "change": "-14.9%",
            "perception":random.randint(0, 2), 
            "following":True
        }
        allCompanies.append(item)

    #Testing - delete below
    # allCompanies.append({"id":0, "name":"Tesla", "code":"TSLA", "price":147.9400, "change": "-14.9%", "perception":0, "following":True})
    # allCompanies.append({"id":1, "name":"Google", "code":"GOOGL", "price":132.6500, "change": "+9.3%", "perception":2, "following":True})
    # allCompanies.append({"id":2, "name":"PayPal", "code":"PYPL", "price":152.6500, "change": "+2.1%", "perception":1, "following":True})
    # allCompanies.append({"id":3, "name":"Apple", "code":"AAPL", "price":148.3600, "change": "+1.5%", "perception":1, "following":True})
    # allCompanies.append({"id":4, "name":"Amazon", "code":"AMZN", "price":3342.8800, "change": "+0.8%", "perception":2, "following":True})
    # allCompanies.append({"id":5, "name":"Microsoft", "code":"MSFT", "price":305.2200, "change": "-0.5%", "perception":0, "following":True})
    # allCompanies.append({"id":6, "name":"Facebook", "code":"FB", "price":369.7900, "change": "+2.3%", "perception":2, "following":True})
    # allCompanies.append({"id":7, "name":"Netflix", "code":"NFLX", "price":574.1300, "change": "-1.2%", "perception":0, "following":True})
    # allCompanies.append({"id":11, "name":"Intel", "code":"INTC", "price":54.1800, "change": "-0.9%", "perception":0, "following":True})
    # allCompanies.append({"id":12, "name":"Nvidia", "code":"NVDA", "price":220.0500, "change": "+3.7%", "perception":2, "following":True})
    # allCompanies.append({"id":13, "name":"IBM", "code":"IBM", "price":139.2800, "change": "-0.3%", "perception":1, "following":True})
    # allCompanies.append({"id":14, "name":"Twitter", "code":"TWTR", "price":69.4200, "change": "+1.8%", "perception":2, "following":True})
    #Testing - delete above
    result = {"data":allCompanies}
    return result

# integrated
def queryAllNews():
    getNews = text("""
        SELECT id, dateTime, link, title, source, summary 
        FROM Articles ORDER BY datetime DESC LIMIT 20
    """)
    getNewsQry = getNews.bindparams()
    resultset = db.session.execute(getNewsQry)
    values = resultset.fetchall()
    resultList = []

    for article in values:
        # this query gets the affected companies by an article
        getAffected = text("""
            SELECT companyID, symbol, effect, justification
            FROM AffectedCompanies JOIN CompanyData
            ON AffectedCompanies.companyID = CompanyData.id
            WHERE articleID=:articleID
        """)
        getAffectedQry = getAffected.bindparams(articleID = article[0])
        affectedResult = db.session.execute(getAffectedQry)
        affectedValue = affectedResult.fetchall()[0]

        item = {
            "id":article[0],
            "date": datetime.strptime(article[1], '%Y-%m-%d %H:%M:%S.%f').strftime('%d/%m/%Y'),
            "title":article[3],
            "source":article[4],
            "summary":article[5],
            "companyID":affectedValue[0],
            "companyCode":affectedValue[1],
            "perception": affectedValue[2],
            "justification": affectedValue[3]
        }

        resultList.append(item)

    #Testing - delete below
    # resultList.append({"id":1, "title":"Microsoft unveils new Windows 12 operating system", "companyID":7, "companyCode":"MSFT", "source":"BBC", "date":"20/02/2024", "perception":2})
    # resultList.append({"id":2, "title":"Apple announces new iPhone 13 with advanced features", "companyID":3, "companyCode":"AAPL", "source":"TechCrunch", "date":"09/15/2021", "perception":1})
    # resultList.append({"id":3, "title":"Amazon launches new delivery drone technology", "companyID":4, "companyCode":"AMZN", "source":"CNN", "date":"09/14/2021", "perception":2})
    # resultList.append({"id":4, "title":"Microsoft acquires leading AI startup", "companyID":5, "companyCode":"MSFT", "source":"The Verge", "date":"09/13/2021", "perception":2})
    # resultList.append({"id":5, "title":"Facebook introduces new privacy features", "companyID":6, "companyCode":"FB", "source":"Reuters", "date":"09/12/2021", "perception":1})
    # resultList.append({"id":6, "title":"Netflix announces partnership with top Hollywood studio", "companyID":7, "companyCode":"NFLX", "source":"Variety", "date":"09/11/2021", "perception":0})
    # resultList.append({"id":7, "title":"Intel unveils breakthrough processor technology", "companyID":11, "companyCode":"INTC", "source":"PCMag", "date":"09/10/2021", "perception":0})
    #Testing - delete above

    finalResult = {"data":resultList}
    return finalResult
        
# integrated
# need stock data and perception data for change and perception
def queryAllCompanies(userID):
    getCompanies = text("SELECT id, name, symbol FROM CompanyData")
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
        
        # waiting for real data to produce price, change
        item = {
            "id":company[0], 
            "name":company[1], 
            "code":company[2], 
            "price":random.randint(50, 200), 
            "change": "-14.9%",
            "perception":random.randint(0, 2), 
            "following":following
        }
        allCompanies.append(item)

    #Testing - delete below
    # allCompanies.append({"id":5, "name":"PayPal", "code":"PYPL", "price":152.6500, "change": "+2.1%", "perception":1, "following":True})
    # allCompanies.append({"id":6, "name":"Amazon", "code":"AMZN", "price":3342.8800, "change": "+0.8%", "perception":2, "following":True})
    # allCompanies.append({"id":7, "name":"Facebook", "code":"FB", "price":369.7900, "change": "+2.3%", "perception":2, "following":True})
    # allCompanies.append({"id":8, "name":"Netflix", "code":"NFLX", "price":574.1300, "change": "-1.2%", "perception":0, "following":True})
    # allCompanies.append({"id":9, "name":"Intel", "code":"INTC", "price":54.1800, "change": "-0.9%", "perception":0, "following":True})
    # allCompanies.append({"id":10, "name":"Nvidia", "code":"NVDA", "price":220.0500, "change": "+3.7%", "perception":2, "following":True})
    # allCompanies.append({"id":11, "name":"IBM", "code":"IBM", "price":139.2800, "change": "-0.3%", "perception":1, "following":True})
    # allCompanies.append({"id":12, "name":"Twitter", "code":"TWTR", "price":69.4200, "change": "+1.8%", "perception":2, "following":True})
    #Testing - delete above

    finalResult = {"data":allCompanies}
    return finalResult

# hopefully integrated but not tested
# waiting on dummy data for news articles/analysis etc.
def queryNotifications(userID):
    notifications = text("SELECT articleID FROM Notifications WHERE userID=:userID AND viewed=False")
    notificationsQry = notifications.bindparams(userID=userID)
    resultset = db.session.execute(notificationsQry)
    values = resultset.fetchall()
    notifications = []
    
    for value in values:
        articleID = value[0]

        getInfo = text("""
            SELECT articleID, title, source, dateTime, effect, companyID, symbol
            FROM Articles           
            JOIN AffectedCompanies ON Articles.id = AffectedCompanies.articleID
            JOIN CompanyData ON AffectedCompanies.companyID = CompanyData.id
            WHERE Articles.id=:articleID
        """)
        getInfoQry = getInfo.bindparams(articleID = articleID)
        getInfoResult = db.session.execute(getInfoQry)
        notification = getInfoResult.fetchall()[0]

        #get companyID and code
        # getCompanyData = text("SELECT CompanyData.id, CompanyData.symbol FROM AffectedCompanies JOIN CompanyData ON AffectedCompanies.companyID = CompanyData.id WHERE articleID=:articleID")
        # companyDataQry = getCompanyData.bindparams(articleID = notification[1])
        # companyDataResult = db.session.execute(companyDataQry)
        # companyDataValue = companyDataResult.fetchall()

        item = {
            "id": notification[0],
            "title":notification[1],
            "source":notification[2],
            "date": datetime.strptime(notification[3], '%Y-%m-%d %H:%M:%S.%f').strftime('%d/%m/%Y'),
            "perception":notification[4],
            "companyID":notification[5],
            "companyCode":notification[6]
        }
        notifications.append(item)

    #Testing - delete below
    # notifications = []
    # notifications.append({"id":0,"companyCode":"MSFT","companyID":5,"title":"Microsoft unveils new Windows 12 operating system","source":"BBC","date":"20/02/2024", "perception":1})
    # notifications.append({"id":1,"companyCode":"AAPL","companyID":3,"title":"Apple announces new iPhone 13 with advanced features","source":"TechCrunch","date":"09/15/2021", "perception":1})
    # notifications.append({"id":2,"companyCode":"AMZN","companyID":4,"title":"Amazon launches new delivery drone technology","source":"CNN","date":"09/14/2021", "perception":2})
    # notifications.append({"id":3,"companyCode":"MSFT","companyID":5,"title":"Microsoft acquires leading AI startup","source":"The Verge","date":"09/13/2021", "perception":2})
    # notifications.append({"id":4,"companyCode":"FB","companyID":6,"title":"Facebook introduces new privacy features","source":"Reuters","date":"09/12/2021", "perception":1})
    # notifications.append({"id":5,"companyCode":"NFLX","companyID":7,"title":"Netflix announces partnership with top Hollywood studio","source":"Variety","date":"09/11/2021", "perception":0})
    # notifications.append({"id":6,"companyCode":"INTC","companyID":11,"title":"Intel unveils breakthrough processor technology","source":"PCMag","date":"09/10/2021", "perception":0})
    # notifications.append({"id":7,"companyCode":"PYPL","companyID":2,"title":"PayPal introduces new payment platform","source":"Forbes","date":"09/09/2021", "perception":1})
    # notifications.append({"id":8,"companyCode":"NVDA","companyID":12,"title":"Nvidia launches new graphics card series","source":"Tom's Hardware","date":"09/08/2021", "perception":2})
    # notifications.append({"id":9,"companyCode":"IBM","companyID":13,"title":"IBM announces breakthrough in quantum computing","source":"ZDNet","date":"09/07/2021", "perception":1})
    # notifications.append({"id":10,"companyCode":"TWTR","companyID":14,"title":"Twitter introduces new feature to combat misinformation","source":"The Guardian","date":"09/06/2021", "perception":2})
    # Testing - delete above

    finalResult = {"data":notifications}
    # UNCOMMENT EVENTUALLY
    notificationUpdate = text("UPDATE Notifications SET viewed = :viewed WHERE userID = :userID")
    notificationQry = notificationUpdate.bindparams(viewed = True, userID = userID)
    db.session.execute(notificationQry)
    db.session.commit()

    if len(values) != 0:
        socketio.emit("database_updated", {"data": "News viewed"})

    return finalResult     

def queryNoOfNotifications(userID):
    notifications = text("SELECT articleID FROM Notifications WHERE userID=:userID AND viewed=False")
    notificationsQry = notifications.bindparams(userID=userID)
    resultset = db.session.execute(notificationsQry)
    values = resultset.fetchall()
    notifications = []
    return len(values) 

# integrated (need to change)
# need perception data for perception
def queryCompanyInfo(companyID, userID):
    getCompanies = text("SELECT id, name, symbol, description FROM CompanyData WHERE id=:companyID")
    getCompaniesQry = getCompanies.bindparams(companyID = companyID)
    resultset = db.session.execute(getCompaniesQry)
    company = resultset.fetchall()[0]

    getFollowing = text("SELECT * FROM FollowedCompanies WHERE userID=:userID AND companyID=:companyID")
    getFollowingQry = getFollowing.bindparams(userID = userID, companyID = company[0])
    followingResult = db.session.execute(getFollowingQry)
    followingValues = followingResult.fetchall()

    following = False
    if len(followingValues) != 0:
        following = True

    item = {
        "id":company[0],
        "name":company[1],
        "code":company[2],
        "overview":company[3],
        "perception":random.randint(0, 2),
        "following":following
    }
    return item

# integrated
def queryCompanyNews(companyID):
    getCompaniesNews = text("""
        SELECT articleID, dateTime, title, source, effect, symbol
        FROM Articles
        JOIN AffectedCompanies ON Articles.id = AffectedCompanies.articleID
        JOIN CompanyData ON AffectedCompanies.companyID = CompanyData.id
        WHERE CompanyData.id=:companyID
    """)
    getCompaniesNewsQry = getCompaniesNews.bindparams(companyID = companyID)
    resultset = db.session.execute(getCompaniesNewsQry)
    values = resultset.fetchall()
    allArticles = []

    for article in values:
        item = {
            "id":article[0],
            "date":datetime.strptime(article[1], '%Y-%m-%d %H:%M:%S.%f').strftime('%d/%m/%Y'),
            "title":article[2],
            "source":article[3],
            "perception":article[4],
            "companyID":companyID,
            "companyCode":article[5]
        }
        allArticles.append(item)

    #Testing - delete below
    # allArticles = []
    # allArticles.append({"id":1, "title":"Microsoft unveils new Windows 12 operating system", "companyID":companyID, "companyCode":"MSFT", "source":"BBC", "date":"20/02/2024", "perception":2})
    # allArticles.append({"id":2, "title":"Apple announces new iPhone 13 with advanced features", "companyID":companyID, "companyCode":"AAPL", "source":"TechCrunch", "date":"09/15/2021", "perception":1})
    # allArticles.append({"id":3, "title":"Amazon launches new delivery drone technology", "companyID":companyID, "companyCode":"AMZN", "source":"CNN", "date":"09/14/2021", "perception":2})
    # allArticles.append({"id":4, "title":"Microsoft acquires leading AI startup", "companyID":companyID, "companyCode":"MSFT", "source":"The Verge", "date":"09/13/2021", "perception":2})
    # allArticles.append({"id":5, "title":"Facebook introduces new privacy features", "companyID":companyID, "companyCode":"FB", "source":"Reuters", "date":"09/12/2021", "perception":1})
    # allArticles.append({"id":6, "title":"Netflix announces partnership with top Hollywood studio", "companyID":companyID, "companyCode":"NFLX", "source":"Variety", "date":"09/11/2021", "perception":0})
    # allArticles.append({"id":7, "title":"Intel unveils breakthrough processor technology", "companyID":companyID, "companyCode":"INTC", "source":"PCMag", "date":"09/10/2021", "perception":0})
    #Testing - delete above

    finalResult = {"data":allArticles}
    return finalResult

# integrated
def queryArticleInfo(articleID, companyID):
    getInfo = text("""
        SELECT dateTime, link, title, source, summary, effect, justification, name, symbol
        FROM Articles
        JOIN AffectedCompanies ON Articles.id = AffectedCompanies.articleID
        JOIN CompanyData ON AffectedCompanies.companyID = CompanyData.id
        WHERE AffectedCompanies.articleID=:articleID AND AffectedCompanies.companyID=:companyID
    """)
    getInfoQry = getInfo.bindparams(articleID=articleID, companyID=companyID)
    resultset = db.session.execute(getInfoQry)
    info = resultset.fetchall()[0]
    
    item = {
        "date": datetime.strptime(info[0], '%Y-%m-%d %H:%M:%S.%f').strftime("%d %B %Y"), 
        "link": info[1],
        "title": info[2],
        "source": info[3],
        "summary": info[4],
        "perception": info[5],
        "analysis": info[6],
        "companyID": str(companyID),
        "companyName": info[7],
        "companyCode": info[8],
    }

    #Testing - delete below
    # item = {"title":"Elon Musk eats humble pie over unpaid bakery bill","source":"BBC","companyID":0,"companyName":"Tesla", "companyCode":"TSLA", "date":"28/02/2024", "summary":"Elon Musk has covered the cost of 4,000 mini pies for Giving Pies bakery in San Jose after Tesla canceled a last-minute order, leaving the small business $2,000 short. Musk responded to the bakery's social media complaint, stating he would resolve the issue. Tesla placed a new order for 3,600 pies, but the overwhelmed bakery, flooded with business from well-wishers, had to decline. The owner expressed gratitude, and even the mayor of San Jose acknowledged the community's support and thanked Musk for covering the cost.", "perception":2, "analysis":"This article may elicit a mixed response regarding public opinion of Tesla. Elon Musk's prompt intervention and willingness to cover the cost of the canceled bakery order could be viewed positively, showcasing a sense of responsibility and commitment to customer satisfaction. However, the initial cancellation might raise concerns about Tesla's reliability and communication with suppliers. The overwhelming support the bakery received after Musk's involvement may shed light on the power dynamics between large corporations and small businesses, potentially sparking discussions about fair business practices. Ultimately, while the incident highlights the scrutiny faced by prominent companies like Tesla, Musk's swift resolution is likely to leave a more positive impression on public perception.", "link":"https://www.bbc.co.uk/news/technology-68404698"}
    #Testing - delete above

    return item

# almost integrated
# yet to be integrated with perception
def querySearchCompanies(query, userID):  
    getInfo = text("""
        SELECT id, name, symbol
        FROM CompanyData
        WHERE name LIKE CONCAT('%', :query, '%')
    """)
    getInfoQry = getInfo.bindparams(query=query)
    resultset = db.session.execute(getInfoQry)
    values = resultset.fetchall()
    companies = []

    for info in values:
        getFollowing = text("SELECT * FROM FollowedCompanies WHERE userID=:userID AND companyID=:companyID")
        getFollowingQry = getFollowing.bindparams(userID = userID, companyID = info[0])
        followingResult = db.session.execute(getFollowingQry)
        followingValues = followingResult.fetchall()

        following = False
        if len(followingValues) != 0:
            following = True

        item = {
            "id":info[0], 
            "name":info[1], 
            "code":info[2], 
            "price":random.randint(50, 200), 
            "change": "-14.9%",
            "perception":random.randint(0, 2), 
            "following":following
        }      
        companies.append(item)

    # query = db.session.query(CompanyData).filter(CompanyData.name.like(f"%{query}%")) # find all of the instances where the name has the query string as a substring
    # results = query.all()
    # companies = []
    # for company in results:
    #     companies.append(queryCompanyInfo(company.id, userID))
        
    result = {"data":companies}
    return result

# kind of integrated
# waiting on recommendation system to be finished
def queryRecommendedCompanies(userID):
    gettingCompaniesQry = text("""
        SELECT *
        FROM CompanyData
        LIMIT 3;
    """)   
    # followedCompaniesQry = gettingCompaniesQry.bindparams(userID = userID)
    resultset = db.session.execute(gettingCompaniesQry)
    values = resultset.fetchall()
    allCompanies = []
    # print(userID)
    # print(values)

    for company in values:
        getFollowing = text("SELECT * FROM FollowedCompanies WHERE userID=:userID AND companyID=:companyID")
        getFollowingQry = getFollowing.bindparams(userID = userID, companyID = company[0])
        followingResult = db.session.execute(getFollowingQry)
        followingValues = followingResult.fetchall()
        following = False
        if len(followingValues) != 0:
            following = True
        # print(company)

        # waiting for real data to produce price
        item = {
            "id":company[0], 
            "name":company[1], 
            "code":company[2], 
            "price":random.randint(50, 200), 
            "change": "-14.9%",
            "perception":random.randint(0, 2), 
            "following":following
        }
        allCompanies.append(item)

    #Placeholder - replace with actual logic (should return exactly 3 companies)
    # allCompanies = []
    # allCompanies.append({"id":20, "name":"PayPal", "code":"PYPL", "price":152.6500, "change": "+2.1%", "perception":1, "following":False})
    # allCompanies.append({"id":21, "name":"Amazon", "code":"AMZN", "price":3342.8800, "change": "+0.8%", "perception":0, "following":False})
    # allCompanies.append({"id":22, "name":"Facebook", "code":"FB", "price":369.7900, "change": "+2.3%", "perception":2, "following":False})
    #Placeholder - replace with actual logic
    finalResult = {"data":allCompanies}
    return finalResult

# integrated
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
    else:
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

# waiting on dummy data for news articles/analysis etc.
def queryRecentAnalysis(companyID):
    getAnalysis = text("""
        SELECT justification
        FROM Articles
        JOIN AffectedCompanies ON Articles.id = AffectedCompanies.articleID
        WHERE AffectedCompanies.companyID=:companyID
        ORDER BY Articles.dateTime DESC LIMIT 1
    """)
    getAnalysisQry = getAnalysis.bindparams(companyID = companyID)
    results = db.session.execute(getAnalysisQry)
    values = results.fetchall()
    # print(values)
    if len(values) != 0:
        return values[0][0]
    return "No analysis"

def queryPredictedStockDates(companyID):
    return predictedDates

app = Flask(__name__)
app.config["SECRET_KEY"] = "fdhsbfdsh3274y327432"

# add cors policy
CORS(app, resources={r"/*":{"origins":"*"}})

# create websocket
socketio = SocketIO(app, cors_allowed_origins="*")

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

@app.route('/getNoOfNotifications', methods=['POST'])
@login_required
def getNoOfNotifications():
    query = queryNoOfNotifications(current_user.id)
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

@app.route('/getPredictedStockDates', methods=['POST'])
@login_required
def getPredictedStockDates():
    data = request.get_json()
    companyID = data.get("companyID")

    query = queryPredictedStockDates(companyID)
    return jsonify(query)

@app.route('/getCompanyAnalysis', methods=['POST'])
@login_required
def getCompanyAnalysis():
    data = request.get_json()
    companyID = data.get("companyID")

    query = queryRecentAnalysis(companyID)
    return jsonify(query)
    
@app.route('/getPredictions/<int:company_id>', methods=['GET'])
def get_predictions(company_id):
    # Query the database for predictions related to the company_id
    predictions = Prediction.query.filter_by(companyID=company_id).order_by(Prediction.date_predicted.desc()).limit(7).all()

    # Format the predictions into a JSON-serializable list
    predictions_list = []
    for prediction in predictions:
        prediction_data = {
            'date_predicted': prediction.date_predicted.strftime("%Y-%m-%d %H:%M:%S"),
            'open': prediction.open,
            'high': prediction.high,
            'low': prediction.low,
            'close': prediction.close,
            'volume': prediction.volume
        }
        predictions_list.append(prediction_data)

    # Return the data as a JSON response
    return jsonify(predictions_list)

if __name__ == "__main__":
    socketio.run(app, debug=True, port=5001)
