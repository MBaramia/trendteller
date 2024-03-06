from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, Column, DateTime, Integer, MetaData, Table
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy import event 
import json
from sqlalchemy import text
import datetime
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
    description = db.Column(db.String(10000))
    symbol = db.Column(db.String(4))
    # exchange = db.Column(db.Double)
    # currPerception = db.Column(db.Integer) # stores the current perception of the company
    def __init__(self,id,name,description,symbol): 
        self.id = id 
        self.name = name
        self.description = description
        self.symbol = symbol
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
    effect = db.Column(db.Integer)
    def __init__(self,dateTime,link,title,source,summary, effect): 
        self.dateTime = dateTime
        self.link = link
        self.title = title
        self.source = source
        self.summary = summary
        self.effect = effect

# this is a table of companies that a user tracks
class FollowedCompanies(db.Model):
    __tablename__ = 'FollowedCompanies'

    companyID = Column(Integer, db.ForeignKey('CompanyData.id'), primary_key=True)
    userID = Column(Integer, db.ForeignKey('UserData.id'), primary_key=True)

    def __init__(self,companyID,userID):
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
    analysis = Column(db.String(500))
    justification = Column(db.String(100))
    def __init__(self,companyID,articleID,effect,analysis,justification):
        self.companyID = companyID
        self.articleID = articleID
        self.effect = effect
        self.analysis = analysis
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
    def __init__(self, companyID, close, volume, open, high, low):
        self.companyID = companyID
        self.close = close
        self.volume = volume
        self.open = open
        self.high = high
        self.low = low

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

    # rules for users: username must be an email, password must be between 5 and 20 chars
    userList = [
        UserData("user1@email.com","testpass"),
        UserData("user2@email.com","testpass"),
        UserData("user3@email.com","testpass"),
        UserData("user4@email.com","testpass"),
        UserData("user5@email.com","testpass"),
        UserData("user6@email.com","testpass"),
        UserData("user7@email.com","testpass"),
        UserData("uesr8@email.com","testpass")
    ]

    followedCompanies = [
        FollowedCompanies(0, 0),  # User 0 follows Apple Inc.
        FollowedCompanies(0, 1),  # User 0 follows Amazon.com Inc.
        FollowedCompanies(0, 2),  # User 0 follows Alphabet Inc.
        FollowedCompanies(0, 3),  # User 0 follows Microsoft Corporation
        FollowedCompanies(0, 4),  # User 0 follows Tesla, Inc.
        FollowedCompanies(0, 5),  # User 0 follows JPMorgan Chase & Co.
        FollowedCompanies(6, 6),  # User 6 follows Walmart Inc.
        FollowedCompanies(7, 7),  # User 7 follows The Coca-Cola Company
        FollowedCompanies(8, 8),  # User 8 follows Pfizer Inc.
        FollowedCompanies(9, 9),  # User 9 follows Netflix, Inc.
        FollowedCompanies(0, 5),  # User 0 follows JPMorgan Chase & Co.
        FollowedCompanies(1, 7),  # User 1 follows The Coca-Cola Company
        FollowedCompanies(2, 3),  # User 2 follows Microsoft Corporation
        FollowedCompanies(3, 8),  # User 3 follows Pfizer Inc.
        FollowedCompanies(4, 2),  # User 4 follows Alphabet Inc.
        FollowedCompanies(5, 0),  # User 5 follows Apple Inc.
        FollowedCompanies(6, 4),  # User 6 follows Tesla, Inc.
        FollowedCompanies(7, 9),  # User 7 follows Netflix, Inc.
        FollowedCompanies(8, 1),  # User 8 follows Amazon.com Inc.
        FollowedCompanies(9, 6),  # User 9 follows Walmart Inc.
    ]

    articleList = [Articles(datetime.datetime.now(),"https://www.bbc.co.uk/", "Story 1", "BBC", "Summary1", 1), 
                   Articles(datetime.datetime.now(),"https://www.bbc.co.uk/", "Story 2", "BBC", "Summary2", -1), 
                   Articles(datetime.datetime.now(),"https://www.bbc.co.uk/", "Story 3", "BBC", "Summary3", 0)
    ]
    
    affectedList = [AffectedCompanies(1, 1, -1, "Analysis1", "Justification1"), 
                AffectedCompanies(2, 2, 1, "Analysis2", "Justification2"), 
                AffectedCompanies(3, 3, 0, "Analysis3", "Justification3")
    ]

    db.session.add_all(userList)
    for i in range(0,len(companyList)):
        db.session.add(companyList[i])
    db.session.add_all(articleList)
    db.session.add_all(affectedList)

    db.session.commit()
