from databaseAccessors import *
from flask import abort
import json
import time



def addActivityToGroup(jsonData, groupId):
	"""
    Adds the transaction to the Group
	"""
	group = getGroup(groupId)
	if group == None:
		pass
	data = json.loads(group.userIDData)
	finalData = {}
	for key, value in data.items():
		if key not in jsonData:
			finalData[key] = value + jsonData[key]
		
	for key, value in jsonData.items():
		if key in data:
			finalData[key] = value + data[key]
		else:
			finalData[key] = value
	group.userIDData = json.dumps(finalData)

def createGroupOrAdd(grpId, grpName, friendList):
	"""

	"""
	group = getGroup(grpId)
	if group == None:
		group = createGroup(grpName, grpId)
	data = json.loads(group.userIDData)
	for val in friendList:
		if val not in data:
			data[val] = 0
	commitToDb()
	return (json.dumps({"success": True}), 200)