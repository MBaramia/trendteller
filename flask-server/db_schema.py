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
    __tablename__='Articles'
    id = db.Column(db.Integer, primary_key=True)
    dateTime = db.Column(DateTime(timezone=True),default=func.now(), nullable=False)
    link = db.Column(db.String(255))
    title = db.Column(db.String(100))
    source = db.Column(db.String(100))
    summary =  db.Column(db.String(500))

    def __init__(self,dateTime,link,title,source,summary, id=None): 
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
    def __init__(self, companyID, date_predicted, close, volume, open, high, low):
        self.companyID = companyID
        self.date_predicted = date_predicted
        self.close = close
        self.volume = volume
        self.open = open
        self.high = high
        self.low = low
        
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
    def __init__(self, companyID, date, open, high, low, close, volume):
        self.companyID = companyID
        self.date = date
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.volume = volume
  
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

def fetch_historic_data_from_alpha_vantage(symbol, api_key):
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&outputsize=compact&apikey={api_key}"
    response = requests.get(url)
    data = response.json()
    time_series_key = 'Time Series (Daily)'
    if time_series_key not in data:
        return []
    historical_data = []
    for date_str, daily_data in data[time_series_key].items():
        date = datetime.datetime.strptime(date_str, '%Y-%m-%d')
        historical_data.append({
            'date': date,
            'open': float(daily_data['1. open']),
            'high': float(daily_data['2. high']),
            'low': float(daily_data['3. low']),
            'close': float(daily_data['4. close']),
            'volume': int(daily_data['5. volume'])
        })
    return historical_data
def insert_historic_data():
    api_key = "8WATTBIUUCY9LFYZ"  
    symbols = ['AAPL', 'AMZN', 'GOOGL', 'MSFT', 'TSLA', 'JPM', 'WMT', 'KO', 'PFE', 'NFLX']
    for index, symbol in enumerate(symbols):
        historic_data = fetch_historic_data_from_alpha_vantage(symbol, api_key)
        for data in historic_data:
            new_record = HistoricData(
                companyID=index,  
                date=data['date'],
                open=data['open'],
                high=data['high'],
                low=data['low'],
                close=data['close'],
                volume=data['volume']
            )
            db.session.add(new_record)
    db.session.commit()

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

    # Expanded list of dummy articles for each company, with three articles each
    articles_data = [
        # Articles for Apple
        {
            "link": "https://www.bloomberg.com/news/articles/2022-09-07/apple-unveils-iphone-14-lineup",
            "title": "Apple Unveils iPhone 14 Lineup",
            "source": "Bloomberg",
            "summary": "Apple's latest iPhone 14 lineup introduces groundbreaking features and improvements.",
            "analysis": "Positive",
            "effect": 2,
            "companyID": 0
        },
        {
            "link": "https://www.cnbc.com/2022/09/07/apple-september-2022-event-live-updates.html",
            "title": "Apple's September Event Highlights",
            "source": "CNBC",
            "summary": "Apple reveals new products and updates at its annual September event.",
            "analysis": "Neutral",
            "effect": 1,
            "companyID": 0
        },
        {
            "link": "https://www.macrumors.com/2022/09/07/apple-fall-2022-event-what-to-expect/",
            "title": "Expectations from Apple's Fall Event",
            "source": "MacRumors",
            "summary": "Speculations on what Apple might unveil at its highly anticipated fall event.",
            "analysis": "Positive",
            "effect": 2,
            "companyID": 0
        },
        # Articles for Amazon
        {
            "link": "https://www.reuters.com/business/retail-consumer/amazon-sets-up-first-ever-physical-store-outside-us-2022-09-05/",
            "title": "Amazon Opens Its First Physical Store Abroad",
            "source": "Reuters",
            "summary": "Amazon expands its retail presence with its first-ever physical store outside the United States.",
            "analysis": "Positive",
            "effect": 2,
            "companyID": 1
        },
        {
            "link": "https://www.cnet.com/tech/services-and-software/amazons-new-alexa-features-aim-to-protect-your-home/",
            "title": "Amazon Enhances Alexa for Home Safety",
            "source": "CNET",
            "summary": "New features in Amazon's Alexa are designed to offer users enhanced home security and peace of mind.",
            "analysis": "Positive",
            "effect": 2,
            "companyID": 1
        },
        {
            "link": "https://techcrunch.com/2022/09/06/amazon-aws-to-invest-12-billion-in-india-by-2030/",
            "title": "Amazon's Major Investment in India with AWS",
            "source": "TechCrunch",
            "summary": "Amazon announces a significant $12 billion investment in India to expand its AWS services.",
            "analysis": "Positive",
            "effect": 2,
            "companyID": 1
        },
        # Articles for Alphabet (Google)
        {
            "link": "https://www.theverge.com/2022/9/6/23339804/google-search-updates-ai-features-mum-algorithm",
            "title": "Google Unveils AI-Powered Search Updates",
            "source": "The Verge",
            "summary": "Google introduces new AI-powered features in its search engine, promising a revolutionary user experience.",
            "analysis": "Positive",
            "effect": 2,
            "companyID": 2
        },
        {
            "link": "https://www.bloomberg.com/news/articles/2022-09-08/google-s-cloud-gaming-service-stadia-is-shutting-down",
            "title": "Google Announces Shutdown of Stadia Service",
            "source": "Bloomberg",
            "summary": "Google's cloud gaming service Stadia is set to shut down, marking an end to the tech giant's gaming experiment.",
            "analysis": "Negative",
            "effect": 0,
            "companyID": 2
        },
        {
            "link": "https://www.cnbc.com/2022/09/07/google-antitrust-case-focuses-on-search-defaults.html",
            "title": "Google Faces Antitrust Case Over Search Defaults",
            "source": "CNBC",
            "summary": "Google is in the spotlight as antitrust regulators focus on its search default agreements with device manufacturers.",
            "analysis": "Negative",
            "effect": 0,
            "companyID": 2
        },
        # Articles for Microsoft
        {
            "link": "https://www.engadget.com/microsoft-365-copilot-ai-productivity-143545869.html",
            "title": "Microsoft Introduces AI Copilot for 365 Suite",
            "source": "Engadget",
            "summary": "Microsoft unveils an AI-powered copilot feature for its Microsoft 365 suite, aiming to enhance productivity.",
            "analysis": "Positive",
            "effect": 2,
            "companyID": 3
        },
        {
            "link": "https://www.techradar.com/news/microsoft-edge-is-getting-a-huge-upgrade-to-challenge-chrome",
            "title": "Microsoft Edge to Receive Significant Upgrades",
            "source": "TechRadar",
            "summary": "Microsoft plans a series of significant updates for its Edge browser to better compete with Chrome.",
            "analysis": "Positive",
            "effect": 2,
            "companyID": 3
        },
        {
            "link": "https://www.zdnet.com/article/microsoft-confirms-layoffs-across-multiple-divisions/",
            "title": "Microsoft Confirms Layoffs Across Divisions",
            "source": "ZDNet",
            "summary": "Microsoft announces layoffs affecting various divisions within the company, as part of its restructuring plan.",
            "analysis": "Negative",
            "effect": 0,
            "companyID": 3
        },
        # Articles for Tesla
        {
            "link": "https://www.bloomberg.com/news/articles/2022-09-09/tesla-faces-fresh-challenge-from-mercedes-ev-push",
            "title": "Tesla Faces New Competition from Mercedes",
            "source": "Bloomberg",
            "summary": "Mercedes steps up its EV game, presenting a new challenge to Tesla's dominance in the electric vehicle market.",
            "analysis": "Neutral",
            "effect": 1,
            "companyID": 4
        },
        {
            "link": "https://www.reuters.com/business/autos-transportation/tesla-recalls-nearly-12-million-vehicles-due-software-glitch-2022-09-05/",
            "title": "Tesla Recalls Vehicles Over Software Glitch",
            "source": "Reuters",
            "summary": "Tesla is recalling nearly 1.2 million vehicles to fix a software issue that may impact the car's safety features.",
            "analysis": "Negative",
            "effect": 0,
            "companyID": 4
        },
        {
            "link": "https://www.cnbc.com/2022/09/08/tesla-to-unveil-updated-self-driving-beta-software.html",
            "title": "Tesla to Unveil New Self-Driving Software",
            "source": "CNBC",
            "summary": "Tesla is set to release an updated version of its self-driving beta software, promising enhanced autonomous driving capabilities.",
            "analysis": "Positive",
            "effect": 2,
            "companyID": 4
        },
        # Articles for JPMorgan
        {
            "link": "https://www.ft.com/content/285d6884-aedb-4310-bf15-2de65a0b55b7",
            "title": "JPMorgan Acquires Fintech Startup",
            "source": "Financial Times",
            "summary": "JPMorgan Chase & Co. has acquired a leading fintech startup, signaling a stronger move into the financial technology space.",
            "analysis": "Positive",
            "effect": 2,
            "companyID": 5
        },
        {
            "link": "https://www.wsj.com/articles/jpmorgan-to-hire-thousands-for-its-new-uk-bank-11631021489",
            "title": "JPMorgan to Hire Thousands in the UK",
            "source": "The Wall Street Journal",
            "summary": "JPMorgan announces plans to hire thousands of new employees for its expanding UK digital bank.",
            "analysis": "Positive",
            "effect": 2,
            "companyID": 5
        },
        {
            "link": "https://www.bloomberg.com/news/articles/2022-09-08/jpmorgan-faces-probe-over-client-money-management",
            "title": "JPMorgan Under Probe for Client Money Management",
            "source": "Bloomberg",
            "summary": "Regulators are investigating JPMorgan over how it manages and safeguards client funds, amid broader scrutiny on bank practices.",
            "analysis": "Negative",
            "effect": 0,
            "companyID": 5
        },
        # Articles for Walmart
        {
            "link": "https://www.cnbc.com/2022/09/07/walmart-to-test-drone-delivery-in-six-states.html",
            "title": "Walmart Expands Drone Delivery Test to Six States",
            "source": "CNBC",
            "summary": "Walmart is set to expand its drone delivery pilot program to six more states, aiming for broader coverage and faster delivery times.",
            "analysis": "Positive",
            "effect": 2,
            "companyID": 6
        },
        {
            "link": "https://www.reuters.com/business/retail-consumer/walmart-raises-wages-store-workers-2022-09-08/",
            "title": "Walmart Raises Wages for Store Workers",
            "source": "Reuters",
            "summary": "Walmart announces wage increases for its store employees, part of its ongoing efforts to improve worker compensation and benefits.",
            "analysis": "Positive",
            "effect": 2,
            "companyID": 6
        },
        {
            "link": "https://www.bloomberg.com/news/articles/2022-09-09/walmart-faces-lawsuit-over-alleged-disability-discrimination",
            "title": "Walmart Faces Lawsuit Over Disability Discrimination Allegations",
            "source": "Bloomberg",
            "summary": "A new lawsuit accuses Walmart of discriminating against disabled employees, a claim that the company denies and vows to fight.",
            "analysis": "Negative",
            "effect": 0,
            "companyID": 6
        },
        # Articles for Coca-Cola
        {
            "link": "https://www.forbes.com/sites/forbesbusinesscouncil/2022/09/07/how-coca-cola-is-reshaping-its-brand-identity-for-the-modern-consumer/",
            "title": "Coca-Cola's Brand Reshaping Strategy",
            "source": "Forbes",
            "summary": "Coca-Cola is actively reshaping its brand identity to connect with modern consumers, focusing on sustainability and innovation.",
            "analysis": "Positive",
            "effect": 2,
            "companyID": 7
        },
        {
            "link": "https://www.cnn.com/2022/09/08/business/coca-cola-new-flavor/index.html",
            "title": "Coca-Cola Launches New Flavor",
            "source": "CNN",
            "summary": "Coca-Cola announces the launch of a new flavor, aiming to expand its product portfolio and cater to diverse consumer tastes.",
            "analysis": "Positive",
            "effect": 2,
            "companyID": 7
        },
        {
            "link": "https://www.businessinsider.com/coca-cola-lawsuit-challenge-to-sugar-tax-2022-09",
            "title": "Coca-Cola Challenges New Sugar Tax",
            "source": "Business Insider",
            "summary": "Coca-Cola is challenging a newly implemented sugar tax, arguing it unfairly targets soda manufacturers.",
            "analysis": "Negative",
            "effect": 0,
            "companyID": 7
        },
        # Articles for Pfizer
        {
            "link": "https://www.nytimes.com/2022/09/08/health/pfizer-covid-vaccine-booster.html",
            "title": "Pfizer's New COVID Booster Gets FDA Nod",
            "source": "The New York Times",
            "summary": "The FDA has authorized Pfizer's latest COVID-19 booster, designed to protect against new variants of the virus.",
            "analysis": "Positive",
            "effect": 2,
            "companyID": 8
        },
        {
            "link": "https://www.wsj.com/articles/pfizer-buys-biotech-firm-in-11-billion-deal-11631678407",
            "title": "Pfizer Acquires Biotech Firm in $11 Billion Deal",
            "source": "The Wall Street Journal",
            "summary": "Pfizer has completed an $11 billion acquisition of a biotech firm, bolstering its portfolio in cancer treatments.",
            "analysis": "Positive",
            "effect": 2,
            "companyID": 8
        },
        {
            "link": "https://www.reuters.com/business/healthcare-pharmaceuticals/pfizer-recalls-some-batches-its-antismoking-drug-over-impurity-2022-09-09/",
            "title": "Pfizer Recalls Antismoking Drug Over Impurity",
            "source": "Reuters",
            "summary": "Pfizer is recalling specific batches of its antismoking medication due to the presence of an impurity.",
            "analysis": "Negative",
            "effect": 0,
            "companyID": 8
        },
        # Articles for Netflix
        {
            "link": "https://variety.com/2022/tv/news/netflix-new-series-announcement-1235058329/",
            "title": "Netflix Announces Exciting New Series Lineup",
            "source": "Variety",
            "summary": "Netflix has unveiled its new series lineup, featuring diverse genres and star-studded casts, aimed at captivating audiences worldwide.",
            "analysis": "Positive",
            "effect": 2,
            "companyID": 9
        },
        {
            "link": "https://www.theverge.com/2022/9/9/23344334/netflix-video-game-expansion-cloud-gaming",
            "title": "Netflix Expands into Video Gaming",
            "source": "The Verge",
            "summary": "Netflix is making a major push into video gaming, planning to offer cloud gaming services to its subscribers.",
            "analysis": "Positive",
            "effect": 2,
            "companyID": 9
        },
        {
            "link": "https://www.cnbc.com/2022/09/08/netflix-shares-drop-on-weak-subscriber-growth-forecast.html",
            "title": "Netflix Faces Headwinds with Subscriber Growth",
            "source": "CNBC",
            "summary": "Netflix's latest earnings report shows weak subscriber growth, causing concerns among investors and analysts.",
            "analysis": "Negative",
            "effect": 0,
            "companyID": 9
        }
    ]

    articleList = []
    affectedList = []

    for i in range(len(articles_data)):
        article=articles_data[i]

        articleList.append(
            Articles(
                datetime.now(timezone.utc), 
                article["link"],
                article["title"],
                article["source"],
                article["summary"],
                id=i
            ) 
        )

        affectedList.append(
            AffectedCompanies(
                article["companyID"],
                i,
                article["effect"],
                article["analysis"]
            )
        )

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

    db.session.add_all(userList)
    for i in range(0,len(companyList)):
        db.session.add(companyList[i])
    db.session.add_all(articleList)
    db.session.add_all(affectedList)
    db.session.add_all(followedCompanies)
    db.session.add_all(notificationsList)
    # db.session.add_all(predictionsList)
    db.session.commit()
    insert_historic_data()
    fetch_stock_prediction()
