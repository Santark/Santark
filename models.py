from app import db 
import json

"""
CREATE TABLE user (
    id INTEGER NOT NULL, 
    name VARCHAR(64), 
    email VARCHAR(100), 
    amount FLOAT, 
    "isExpenseNormalized" BOOLEAN, 
    "friendsInfo" TEXT, 
    "activityIdList" TEXT, 
    PRIMARY KEY (id), 
    CHECK ("isExpenseNormalized" IN (0, 1))
);
"""
class User(db.Model):
    # unique id
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # user info like name, email
    name = db.Column(db.String(64))
    email = db.Column(db.String(100))
    # user wallet
    amount = db.Column(db.Float)
    isExpenseNormalized = db.Column(db.Boolean, default=False)

    friendsInfo = db.Column(db.Text())
    activityIdList = db.Column(db.Text())

    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.isExpenseNormalized = False
        self.amount = 0
        self.friendsInfo = "{}"
        self.activityIdList = "[]"

    def getUserDetails(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "amount": self.amount,
            "isExpenseNormalized": self.isExpenseNormalized,
            "friendsInfo": json.loads(self.friendsInfo)
        }

    def toString(self):
        return json.dumps(self.getUserDetails())

    def getUserActivity(self):
        return json.loads(self.activityIdList)

"""
CREATE TABLE activity (
    "activityId" INTEGER NOT NULL, 
    expense INTEGER, 
    data TEXT, 
    "groupId" VARCHAR(264), 
    PRIMARY KEY ("activityId")
);
"""
class Activity(db.Model):
    activityId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    expense = db.Column(db.Integer)
    data = db.Column(db.Text())
    groupId = db.Column(db.String(264))

    def __init__(self, expense, data, groupId=None):
        self.expense = expense
        self.data = data
        self.groupId = groupId

    def getActivityDetails(self):
        return {
            "expense": self.expense,
            "groupId": self.groupId,
            "data": json.loads(self.data)
        }

    def toString(self):
        return json.dumps(self.getActivityDetails())

"""
CREATE TABLE IF NOT EXISTS "group" (
    "groupName" VARCHAR(264), 
    "groupId" VARCHAR(264) NOT NULL, 
    "userIDData" TEXT, 
    PRIMARY KEY ("groupId")
);
"""
class UserGroup(db.Model):
    groupName = db.Column(db.String(264))
    groupId = db.Column(db.String(264), primary_key=True)
    userIDData = db.Column(db.Text())

    def __init__(self, groupName, groupId, userIDData):
        self.groupName = groupName
        self.groupId = groupId
        self.userIDData = userIDData

    def getGroupDetails(self):
        return {
            "groupName": self.groupName,
            "groupId": self.groupId,
            "userIDData": json.loads(self.userIDData)
        }

    def toString(self):
        return json.dumps(self.getGroupDetails())


def addDummyUsers():
    user = User("abhilash ranjan", "abhi@gmail.com")
    user1 = User("ashish", "ashish@gmail.com")
    user2 = User("testUser", "testUser@gmail.com")
    user3 = User("rohan", "rohan@gmail.com")
    user4 = User("demoUser", "demoUser@gmail.com")
    db.session.add(user)
    db.session.add(user1)
    db.session.add(user2)
    db.session.add(user3)
    db.session.add(user4)
    db.session.commit()

if __name__ == "__main__":
    print "Creating database tables..."
    db.create_all()
    addDummyUsers()
    print "Done!"
