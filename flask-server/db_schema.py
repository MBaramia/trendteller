from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, Column, DateTime, Integer, MetaData, Table
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy import event 
import json
from sqlalchemy import text, UniqueConstraint
from datetime import datetime, timezone, timedelta
from stock_price_prediction import fetch_stock_prediction
from historic import fetch_historic_data
from news import process_articles
import requests

# create the database interface
db = SQLAlchemy()

# All of the data about a user
# All of the data about a user
class UserData(db.Model,UserMixin):
    __tablename__='UserData'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(20))
    def __init__(self,username,password): 
        self.username = username
        self.password = generate_password_hash(password)
    
    def updateDetails(self, username, password):
        if username != "":
            self.username = username
        if password != "":
            self.password = generate_password_hash(password)

# this table stores all of the data relating to a company
class CompanyData(db.Model):
    __tablename__='CompanyData'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    symbol = db.Column(db.String(4))
    description = db.Column(db.String(10000))
    # exchange = db.Column(db.Double)
    # currPerception = db.Column(db.Integer) # stores the current perception of the company
    def __init__(self,id,name,symbol,description): 
        self.id = id 
        self.name = name
        self.symbol = symbol
        self.description = description
        # self.exchange = exchange
        # self.currPerception = currPerception

# this table stores all of the data relating to an article
class Articles(db.Model):
    __tablename__ = 'Articles'
    id = db.Column(db.Integer, primary_key=True)
    dateTime = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    link = db.Column(db.String(255))
    title = db.Column(db.String(100))
    source = db.Column(db.String(100))
    summary = db.Column(db.String(500))

    def __init__(self, dateTime, link, title, source, summary, id=None): 
        self.id = id
        self.dateTime = dateTime
        self.link = link
        self.title = title
        self.source = source
        self.summary = summary

# this is a table of companies that a user tracks
class FollowedCompanies(db.Model):
    __tablename__ = 'FollowedCompanies'
    companyID = Column(Integer, db.ForeignKey('CompanyData.id'), primary_key=True)
    userID = Column(Integer, db.ForeignKey('UserData.id'), primary_key=True)
    def __init__(self, companyID, userID):
        self.companyID = companyID
        self.userID = userID

# these are the notifications that are alerts that a new news article has been published about a company that a user follows
class Notifications(db.Model):
    __tablename__ = 'Notifications'
    userID = Column(Integer, db.ForeignKey('UserData.id'), primary_key=True)
    articleID = Column(Integer, db.ForeignKey('Articles.id'), primary_key=True)
    viewed = Column(db.Boolean, default=False)

    def __init__(self,userID,articleID,viewed):
        self.userID = userID
        self.articleID = articleID
        self.viewed = viewed

# this takes the companies that are affected by an article 
class AffectedCompanies(db.Model):
    __tablename__ = 'AffectedCompanies'
    companyID = Column(Integer, db.ForeignKey('CompanyData.id'), primary_key=True)
    articleID = Column(Integer, db.ForeignKey('Articles.id'), primary_key=True)
    effect = Column(Integer)
    justification = Column(db.String(100))

    def __init__(self,companyID,articleID,effect,justification):
        self.companyID = companyID
        self.articleID = articleID
        self.effect = effect
        self.justification = justification

# this table takes two companies and stores the number of people that follow both of those companies 
class CompanyWeights(db.Model): 
    __tablename__ = 'CompanyWeights'
    relationOne = Column(Integer, db.ForeignKey('CompanyData.id'), primary_key = True) # one of the companies that are followed by users 
    relationTwo = Column(Integer, db.ForeignKey('CompanyData.id'), primary_key = True) # the other company that is followed by the user 
    mutualFollowers = Column(Integer, default = 0)
    def __init__(self,relationOne, relationTwo, mutualFollowers):
        self.relationOne = relationOne
        self.relationTwo = relationTwo
        self.mutualFollowers = mutualFollowers
        
# this table stores prediction data
class Prediction(db.Model):
    __tablename__ = 'Prediction'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    companyID = db.Column(db.Integer, db.ForeignKey('CompanyData.id'), nullable=False)
    date_predicted = db.Column(DateTime(timezone=True), default=func.now(), nullable=False)
    close = db.Column(db.Float)
    volume = db.Column(db.Float)
    open = db.Column(db.Float)
    high = db.Column(db.Float)
    low = db.Column(db.Float)
    timeframe = db.Column(db.String(50))  
    def __init__(self, companyID, date_predicted, close, volume, open, high, low, timeframe):
        self.companyID = companyID
        self.date_predicted = date_predicted
        self.close = close
        self.volume = volume
        self.open = open
        self.high = high
        self.low = low
        self.timeframe = timeframe

class HistoricData(db.Model):
    __tablename__ = 'HistoricData'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    companyID = db.Column(db.Integer, db.ForeignKey('CompanyData.id'), nullable=False)
    date = db.Column(DateTime, nullable=False)
    open = db.Column(db.Float, nullable=False)
    high = db.Column(db.Float, nullable=False)
    low = db.Column(db.Float, nullable=False)
    close = db.Column(db.Float, nullable=False)
    volume = db.Column(db.BigInteger, nullable=False)
    timeframe = db.Column(db.String(10), nullable=False)  # Intraday, Daily, Weekly, Monthly
    def __init__(self, companyID, date, open, high, low, close, volume, timeframe):
        self.companyID = companyID
        self.date = date
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.volume = volume
        self.timeframe = timeframe

  
@event.listens_for(FollowedCompanies, 'before_insert')
def before_followed_companies_insert(mapper, connection, target):
    print(f"Inserting FollowedCompanies: companyID={target.companyID}, userID={target.userID}")
     # Find all companies already followed by the user
    user_followed_companies = FollowedCompanies.query.filter_by(userID=target.userID).all()
    # Update CompanyWeights table
    for user_followed_company in user_followed_companies:
        # Check if CompanyWeights entry already exists for the relationship
        existing_entry = CompanyWeights.query.filter(
            (CompanyWeights.relationOne == user_followed_company.companyID) &
            (CompanyWeights.relationTwo == target.companyID)
            ).first()

        if existing_entry:
            # Entry exists, increment mutualFollowers by 1
            existing_entry.mutualFollowers += 1
        else:
            existing_entry = CompanyWeights.query.filter(
            (CompanyWeights.relationTwo == user_followed_company.companyID) &
            (CompanyWeights.relationOne == target.companyID)
            ).first()
            if existing_entry:
                existing_entry.mutualFollowers += 1
        




@event.listens_for(CompanyData, 'after_insert')
def afterCompanyInsert(mapper, connection, target):
    print(f"Inserting FollowedCompanies: companyID={target.id}")
    # Retrieve all existing companies
    all_companies = CompanyData.query.filter(CompanyData.id < target.id).all()

    # Iterate through all existing companies and add entries to CompanyWeights
    for existing_company in all_companies:
        new_entry = CompanyWeights(
            relationOne=target.id,
            relationTwo=existing_company.id,
            mutualFollowers=0  # This new company has just been added, so there will be no mutual followers
        )
        db.session.add(new_entry)

@event.listens_for(AffectedCompanies, 'after_insert')
def afterAffectedCompanyInsert(mapper, connection, target):
    print(f"Inserting AffectedCompanies: companyID={target.companyID}, articleID={target.articleID}")
    # Retrieve all existing users
    getPerception = text("""
        SELECT userID
        FROM FollowedCompanies
        WHERE FollowedCompanies.companyID=:companyID
    """)
    getPerceptionQry = getPerception.bindparams(companyID = target.companyID)
    results = db.session.execute(getPerceptionQry)
    all_users = results.fetchall()

    # Iterate through all existing companies and add entries to CompanyWeights
    for existing_user in all_users:
        new_entry = Notifications(
            userID=existing_user.id,
            articleID=target.articleID,
            viewed=False  # This new company has just been added, so there will be no mutual followers
        )
        db.session.add(new_entry)
        db.session.commit()

@event.listens_for(Notifications, 'after_insert')
def afterNotificationInsert(mapper, connection, target):
    print(f"Inserting Notification: userID={target.userID}, articleID={target.articleID}, viewed={target.viewed}")

def addNewArticle(dateTime, link, title, source, summary, companyID, effect, justification):
    if companyID is None:
        print("No affected company for article: " + title)
        return
    new_article = Articles(dateTime, link, title, source, summary)
    db.session.add(new_article)
    new_affected_company = AffectedCompanies(companyID, new_article.id, effect, justification)
    db.session.add(new_affected_company)
    db.session.commit()

def getRecommendedCompanies(userID):
    # gets all the companies that a user follows
    #SELECT companyID FROM FollowedCompanies WHERE userID = userID;
    # SELECT relationOne, relationTwo FROM CompanyWeights ORDER BY mutualFollowers DESC
    # gets all companies that the user follows
    recommended = []
    qrytext = text("SELECT companyID FROM FollowedCompanies WHERE userID=:userID;")
    qry = qrytext.bindparams(userID = userID)
    resultset = db.session.execute(qry)
    values = resultset.fetchall()

    qrytwo = text("SELECT relationOne, relationTwo FROM CompanyWeights ORDER BY mutualFollowers DESC")
    resultsetTwo = db.session.execute(qrytwo)
    valuesTwo = resultsetTwo.fetchall()

    count = 0
    for i in range (0,len(valuesTwo)):
        testing = valuesTwo[i]
        if (testing[0] in values and testing[1] not in values):
            count += 1
            recommended.append(testing[0])
        elif (testing[0] not in values and testing[1] in values):
            count += 1
            recommended.append(testing[1])
        if count == 3:
            return recommended
    return recommended


    # gets all companies that the user follows
    recommended = []
    qrytext = text("SELECT companyID FROM FollowedCompanies WHERE userID=:userID;")
    qry = qrytext.bindparams(userID = userID)
    resultset = db.session.execute(qry)
    values = resultset.fetchall()

    qrytwo = text("SELECT relationOne, relationTwo FROM CompanyWeights ORDER BY mutualFollowers DESC")
    resultsetTwo = db.session.execute(qrytwo)
    valuesTwo = resultsetTwo.fetchall()

    count = 0
    for i in range (0,len(valuesTwo)):
        testing = valuesTwo[i]
        if (testing[0] in values and testing[1] not in values):
            count += 1
            recommended.append(testing[0])
        elif (testing[0] not in values and testing[1] in values):
            count += 1
            recommended.append(testing[1])
        if count == 3:
            return recommended
    return recommended

# put some data into the tables
def dbinit():
    companyList = [
        CompanyData(0, 'Apple Inc.', 'AAPL', \
            '''Apple Inc. is an American multinational technology company that designs, 
            develops, and sells consumer electronics, computer software, and online 
            services. It is widely known for its iPhone smartphones, Mac computers, 
            iPad tablets, and Apple Watch smartwatches.'''
        ),
        CompanyData(1, 'Amazon.com Inc.', 'AMZN', \
            '''Amazon.com Inc. is an American multinational technology company that 
            focuses on e-commerce, cloud computing, digital streaming, and artificial 
            intelligence. It is the largest online marketplace and has expanded into 
            various industries, including logistics, healthcare, and entertainment.'''
        ),
        CompanyData(2, 'Alphabet Inc.', 'GOOGL', \
            '''Alphabet Inc. is an American multinational conglomerate that was created 
            through a corporate restructuring of Google in 2015. It is primarily 
            involved in technology and internet-related businesses, including online 
            advertising, search engines, cloud computing, and hardware.'''
        ),
        CompanyData(3, 'Microsoft Corporation', 'MSFT', \
            '''Microsoft Corporation is an American multinational technology company 
            that develops, manufactures, licenses, supports, and sells computer 
            software, consumer electronics, personal computers, and related services. 
            It is known for its Windows operating system and Office productivity suite.'''
        ),
        CompanyData(4, 'Tesla, Inc.', 'TSLA', \
            '''Tesla, Inc. is an American electric vehicle and clean energy company that 
            designs, manufactures, and sells electric cars, battery energy storage 
            systems, and solar panels. It is led by CEO Elon Musk and is known for 
            its innovative approach to transportation and energy.'''
        ),
        CompanyData(5, 'JPMorgan Chase & Co.', 'JPM', \
            '''JPMorgan Chase & Co. is an American multinational investment bank and 
            financial services company. It is the largest bank in the United States 
            by assets and is involved in investment banking, commercial banking, 
            asset management, and other financial services.'''
        ),
        CompanyData(6, 'Walmart Inc.', 'WMT', \
            '''Walmart Inc. is an American multinational retail corporation that operates 
            a chain of hypermarkets, discount department stores, and grocery stores. 
            It is the world's largest company by revenue and is known for its low 
            prices and wide range of products.'''
        ),
        CompanyData(7, 'The Coca-Cola Company', 'KO', \
            '''The Coca-Cola Company is an American multinational beverage corporation 
            that manufactures, markets, and sells nonalcoholic beverages, primarily 
            carbonated soft drinks and other beverages. It is one of the world's most 
            valuable brands and is known for its Coca-Cola soda.'''
        ),
        CompanyData(8, 'Pfizer Inc.', 'PFE', \
            '''Pfizer Inc. is an American multinational pharmaceutical corporation that 
            develops and produces medicines and vaccines for a wide range of medical 
            conditions. It is one of the largest pharmaceutical companies in the world 
            and is involved in research and development in various therapeutic areas.'''
        ),
        CompanyData(9, 'Netflix, Inc.', 'NFLX', \
            '''Netflix, Inc. is an American subscription-based streaming service that 
            offers a wide variety of movies, TV shows, documentaries, and original 
            content across a range of genres and languages. It is one of the leading 
            streaming platforms globally and has revolutionized the way people consume 
            entertainment.'''
        )
    ]
    
    # predictionsList = [
    #     Prediction(date_predicted=datetime.now(timezone.utc)+ timedelta(days=1), open=150, high=155, low=149, close=154, volume=100000),
    #     Prediction(date_predicted=datetime.datetime.utcnow(), open=3100, high=3200, low=3050, close=3150, volume=300000),
    #     Prediction(date_predicted=datetime.datetime.utcnow(), open=2700, high=2750, low=2690, close=2720, volume=150000),
    #     Prediction(date_predicted=datetime.datetime.utcnow(), open=290, high=300, low=285, close=295, volume=200000),
    #     Prediction(date_predicted=datetime.datetime.utcnow(), open=600, high=620, low=590, close=610, volume=120000),
    #     Prediction(date_predicted=datetime.datetime.utcnow(), open=130, high=135, low=128, close=132, volume=110000),
    #     Prediction(date_predicted=datetime.datetime.utcnow(), open=140, high=142, low=138, close=141, volume=70000),
    #     Prediction(date_predicted=datetime.datetime.utcnow(), open=50, high=52, low=49, close=51, volume=80000),
    #     Prediction(date_predicted=datetime.datetime.utcnow(), open=40, high=42, low=39, close=41, volume=90000),
    #     Prediction(date_predicted=datetime.datetime.utcnow(), open=500, high=510, low=495, close=505, volume=100000)
    # ]

    # rules for users: username must be an email, password must be between 5 and 20 chars
    userList = [
        UserData("user1@email.com","testpass"),
        UserData("user2@email.com","testpass"),
        UserData("user3@email.com","testpass"),
        UserData("user4@email.com","testpass"),
        UserData("user5@email.com","testpass"),
        UserData("user6@email.com","testpass"),
        UserData("user7@email.com","testpass"),
        UserData("user8@email.com","testpass")
    ]

    # 10 companies with IDs 0-9
    # 8 users with IDs 1-8
    followedCompanies = [
        FollowedCompanies(0, 1),  # Apple Inc. is followed by User 1
        FollowedCompanies(1, 1),  # Amazon.com Inc. is followed by User 1
        FollowedCompanies(2, 1),  # Alphabet Inc. is followed by User 1
        FollowedCompanies(3, 1),  # Microsoft Corporation is followed by User 1
        FollowedCompanies(4, 1),  # Tesla, Inc. is followed by User 1
        FollowedCompanies(5, 1),  # JPMorgan Chase & Co. is followed by User 1
        FollowedCompanies(6, 7),  # Walmart Inc. is followed by User 7
        FollowedCompanies(7, 8),  # The Coca-Cola Company is followed by User 8
        FollowedCompanies(8, 2),  # Pfizer Inc. is followed by User 2
        FollowedCompanies(9, 2),  # Netflix, Inc. is followed by User 2
        FollowedCompanies(5, 2),  # JPMorgan Chase & Co. is followed by User 2
        FollowedCompanies(7, 2),  # The Coca-Cola Company is followed by User 2
        FollowedCompanies(3, 3),  # Microsoft Corporation is followed by User 3
        FollowedCompanies(8, 4),  # Pfizer Inc. is followed by User 4
        FollowedCompanies(2, 5),  # Alphabet Inc. is followed by User 5
        FollowedCompanies(0, 6),  # Apple Inc. is followed by User 6
        FollowedCompanies(4, 6),  # Tesla, Inc. is followed by User 6
        FollowedCompanies(9, 7),  # Netflix, Inc. is followed by User 7
        FollowedCompanies(1, 8),  # Amazon.com Inc. is followed by User 8
        FollowedCompanies(6, 9),  # Walmart Inc. is followed by User 9
    ]


    db.session.add_all(userList)
    for i in range(0,len(companyList)):
        db.session.add(companyList[i])
    timeframes = ['intraday', 'daily', 'weekly', 'monthly']
    for company in companyList:
        for timeframe in timeframes:
            predictions = fetch_stock_prediction(company.id, timeframe)
            for prediction in predictions:
                new_prediction = Prediction(
                    companyID=company.id,
                    date_predicted=datetime.now(timezone.utc),
                    open=prediction[0],
                    high=prediction[1],
                    low=prediction[2],
                    close=prediction[3],
                    volume=prediction[4],
                    timeframe=timeframe
                )
                db.session.add(new_prediction)
    for company in companyList:
        for timeframe in timeframes:
            api_key = '8WATTBIUUCY9LFYZ'
            historic_data_df = fetch_historic_data(company.symbol, api_key, timeframe)
            for index, row in historic_data_df.iterrows():
                historic_data_entry = HistoricData(
                    companyID=company.id,
                    date=index.to_pydatetime(),
                    open=row['Open'],
                    high=row['High'],
                    low=row['Low'],
                    close=row['Close'],
                    volume=int(row['Volume']),
                    timeframe=timeframe
                )
                db.session.add(historic_data_entry)

    notifications_data = [
        {
            "userID": 1,
            "articleID": 0,
            "viewed": False
        },
        {
            "userID": 1,
            "articleID": 1,
            "viewed": False
        },
        {
            "userID": 1,
            "articleID": 2,
            "viewed": False
        }
    ]

    notificationsList = []

    for i in range(len(notifications_data)):
        notification = notifications_data[i]

        notificationsList.append(
            Notifications(
                notification["userID"],
                notification["articleID"],
                notification["viewed"]
            )
        )
    articles_data = process_articles(pageSize=30)  # Fetch articles data
    for article in articles_data:
        new_article = Articles(
            dateTime=datetime.strptime(article['date'], '%Y-%m-%dT%H:%M:%SZ'),
            link=article['link'],
            title=article['title'],
            source=article['source'],
            summary=article['summary'],
            company_id=article['company_id']
        )
        db.session.add(new_article)
    db.session.add_all(followedCompanies)
    db.session.add_all(notificationsList)
    # db.session.add_all(predictionsList)
    db.session.commit()
