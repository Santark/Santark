from databaseAccessors import *
from flask import abort
import json
import time
from handler.groupHandler import *

def distributeExpense(jsonPayerData):
	"""
	Receives a json string of format {"a":250, "b": -50, "c":-100, "d": -100}
	This function then converts it to below output

	a: { sum: 250, b: -50, c: -100, d: -100 }
	b: { sum: -50, a: 50}
	c: { sum: -100, a: 100}
	d: { sum: -100, a: 100}
	The above string helps in updating value in friends blob of user obj
	"""
	lis = []
	for key, val in jsonPayerData.items():
		lis.append({"id": key, "sum": val})
	lis = sorted(lis, key = lambda i: i['sum'], reverse=True)
	i = len(lis) - 1
	for val in lis:
		if val["sum"] == 0:
			continue
		while val["sum"] > 0:
			if lis[i]["sum"] + val["sum"] > 0:
				val[lis[i]["id"]] = lis[i]["sum"]
				lis[i][val["id"]] = lis[i]["sum"] * -1
				val["sum"] = lis[i]["sum"] + val["sum"] 
				lis[i]["sum"] = 0
				i = i - 1
			else:
				val[lis[i]["id"]] = val["sum"] * -1
				lis[i][val["id"]] = val["sum"] 
				lis[i]["sum"] = lis[i]["sum"] + val["sum"] 
				val["sum"] = 0
	data = {}
	for val in lis:
		id = val["id"]
		del val["id"]
		del val["sum"]
		data[id] = val
	return data


def validateActivity(jsonData):
    """ 
    Validates the payerLoad. The payload contains info about how much he owns/lent.
    Based on this, for the whole transaction, total money owned should be equal to 
    total money lent
    """
    negativeExpenseCount = 0
    positiveExpenseCount = 0
    for key, val in jsonData.items():
        if val < 0:
            negativeExpenseCount = negativeExpenseCount + val
        else:
            positiveExpenseCount = positiveExpenseCount + val
    print(negativeExpenseCount, positiveExpenseCount)
    if (negativeExpenseCount + positiveExpenseCount != 0):
        raise Exception("Wrong data passed")

def addNewExpense(expense, payerData, groupId):
    """ 
	Handles the case for the new activity. 
	Actions:
	 1. would update all the users wallet
	 2. would also update the wallet on the friends

	 Payload:
	 1. expense
	 2. payerData
	 3. groupId if this is a part of group expense.
    """
    activity = addActivity(expense, json.dumps(payerData))
    jsonData = payerData
    try:
       validateActivity(jsonData)
    except:
       abort(400)
    userList = jsonData.keys()
    # converting the payerData to a dictionary containg data of how much
    # they own to each other
    sharedExpense = distributeExpense(jsonData)
    print(sharedExpense)
    if groupId != None:
        addActivityToGroup(jsonData, groupId)
        activity.groupId = groupId
    # updating user one by one
    usersList = getMultiUserInfo(userList)
    for val in usersList:
        val.amount = val.amount + jsonData[str(val.id)]
        val.activityIdList = json.loads(val.activityIdList)
        val.activityIdList.append(str(activity.activityId))
        val.activityIdList = json.dumps(val.activityIdList)
        val.friendsInfo = json.loads(val.friendsInfo)
        for key, val1 in sharedExpense[str(val.id)].items():
            if key not in val.friendsInfo:
                val.friendsInfo[key] = val1
            else:
                val.friendsInfo[key] = val.friendsInfo[key] + val1
        val.friendsInfo = json.dumps(val.friendsInfo)
    commitToDb()
    return (json.dumps({"success": True, "activityId": str(activity.activityId)}), 200)
    

def deleteExpense(activityId):
	"""
    This API is called when the we want to delete the Activity.
    Payload:
    1. activityId
	"""
	activity = getActivity(activityId)
	print(activity)
	if not activity:
		abort(404)
	jsonData = json.loads(activity.data)
	# generating a reverse envirnoment of what is done on addNewExpense
	for key, val in jsonData.items():
		jsonData[key] = jsonData[key] * -1
	print(activity.groupId)
	if activity.groupId != None:
		addActivityToGroup(jsonData, activity.groupId)
	sharedExpense = distributeExpense(jsonData)
	print(sharedExpense)
	userList = jsonData.keys()
	usersList = getMultiUserInfo(userList)
	for val in usersList:
		val.amount = val.amount + jsonData[str(val.id)]
		val.activityIdList = json.loads(val.activityIdList)
		print(val.activityIdList, activityId)
		try: val.activityIdList.remove(str(activityId))
		except: print("Not able to delete")
		val.activityIdList = json.dumps(val.activityIdList)
		friendJson = json.loads(val.friendsInfo)
		for key, val1 in sharedExpense[str(val.id)].items():
			if key not in friendJson:
				friendJson[key] = val1
			else:
				friendJson[key] = friendJson[key] + val1
		val.friendsInfo = json.dumps(friendJson)
	deleteActivity(activityId)
	return (json.dumps({"success": True}), 200)

def editActivity(activityId, expense, data):
	"""
	This API is used update the activity.

	This operation would first delete the old data 
	And then insert the new data
	Payload:
	 1. activityId
	 2. expense
	 3. data
	"""
	activity = getActivity(activityId)
	groupId = activity.groupId
	deleteExpense(activityId)
	addNewExpense(expense, data, groupId)
	return (json.dumps({"success": True}), 200)