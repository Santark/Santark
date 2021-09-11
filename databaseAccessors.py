from models import User, Activity, UserGroup
from app import db 
import json

def getUser(userId):
    """
    To query the db and fetch the user details for a particular id
    """
    try:
        user = User.query.filter(User.id == userId).one()
        return user
    except:
        return None

def getMultiUserInfo(userIdList):
    """ To query the db and fetch the user details for large no of id"""
    try:
        userIdTuple = tuple(userIdList)
        return User.query.filter(User.id.in_(userIdTuple)).all()
    except:
        return []

def addUser(name, email):
    """ INsert Query for users table"""
    user = User(name, email)
    db.session.add(user)
    commitToDb()
    return user

def getActivity(activityId):
    """ To fetch the activity information"""
    try:
        activity = Activity.query.filter(Activity.activityId == activityId).one()
        return activity
    except:
        return None

def deleteActivity(activityId):
    """ Delete Query operation on Activity table"""
    try:
        activity = Activity.query.filter(Activity.activityId == activityId).delete()
        commitToDb()
    except Exception as e:
        print(e)
        raise Exception("Error occured")

def getMultiActivity(activityIdList):
    """ """
    try:
        activityIdTuple = tuple(activityIdList)
        return Activity.query.filter(Activity.activityId.in_(activityIdTuple)).all()
    except:
        return []

def addActivity(expense, data):
    """ """
    activity = Activity(expense, data)
    db.session.add(activity)
    commitToDb()
    return activity

def createGroup(grpName, grpId):
    """ """
    group = UserGroup(grpName, grpId, "{}")
    db.session.add(group)
    commitToDb()
    return group

def getGroup(groupId):
    """ """
    try:
        group = UserGroup.query.filter(UserGroup.groupId == groupId).one()
        return group
    except:
        return None

def commitToDb():
	""" """
	db.session.commit()