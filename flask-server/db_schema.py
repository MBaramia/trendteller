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
    exchange = db.Column(db.Double)
    currPerception = db.Column(db.Integer) # stores the current perception of the company
    def __init__(self,id,name,description,symbol,exchange, currPerception): 
        self.id = id 
        self.name = name
        self.description = description
        self.symbol = symbol
        self.exchange = exchange
        self.currPerception = currPerception

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



# put some data into the tables
def dbinit():
    companyList = [
        CompanyData(0,'Tesla','Tesla Description', 'TSLA', 193.43, 0),
        CompanyData(1,'Alphabet Inc Class C','Alphabet Inc Class C description','GOOG',145.38, 1),
        CompanyData(2,'Microsoft Corp','Microsoft Corp Description', 'MSFT',410.48, 2),
        CompanyData(3,'Apple Inc','Apple Inc Description', 'AAPL',182.52, 1),
        CompanyData(4, 'J Sainsbury plc', 'J Sainsbury plc Description', 'SBRY', 252.70, 0)
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

    articleList = [Articles(datetime.datetime.now(),"https://www.bbc.co.uk/", "Story 1", "BBC", "Summary1", 1), 
                   Articles(datetime.datetime.now(),"https://www.bbc.co.uk/", "Story 2", "BBC", "Summary2", -1), 
                   Articles(datetime.datetime.now(),"https://www.bbc.co.uk/", "Story 3", "BBC", "Summary3", 0)]
    affectedList = [AffectedCompanies(1, 1, -1, "Analysis1", "Justification1"), 
                AffectedCompanies(2, 2, 1, "Analysis2", "Justification2"), 
                AffectedCompanies(3, 3, 0, "Analysis3", "Justification3")]

    db.session.add_all(userList)
    for i in range(0,len(companyList)):
        db.session.add(companyList[i])
    db.session.add_all(articleList)
    db.session.add_all(affectedList)

    db.session.commit()