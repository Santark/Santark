from databaseAccessors import *
from flask import abort
import json
import time

def fetchUserDetails(userId):
	""" """
	user = getUser(userId)
	if user != None:
		return (user.toString(), 200)
	abort(404)

def fetchUserActivity(userId):
	""" """
	user = getUser(userId)
	if user != None:
		activity = user.getUserActivity()
		data = getMultiActivity(activity)
		out = []
		for val in data:
			out.append(val.toString())
		return (json.dumps(out), 200)
	abort(404)

def fetchActivityById(activityID):
	""" """
	activity = getActivity(activityID)
	if activity != None:
		return (activity.toString(), 200)
	abort(404)

def fetchGroupDetails(grpId):
	""" """
	group = getGroup(grpId)
	if group != None:
		return (group.toString(), 200)
	abort(404)

