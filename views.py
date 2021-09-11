from flask import request, abort
from validation import *
from action import *
from handler.expenseHandler import *
from handler.argsHandler import *
from app import app


"""
Consider a bill payment of 400 Rs on 4 ppl(a,b,c,d)
a pays 350 Rs and b pays 50 Rs. In this case the 
request body would look something like
{
	"expense": 400,
	"payerData": {"1":250, "2": -50, "3":-100, "4": -100}
}
+ve means money lended 
-ve means money is owned
"""
@app.route('/handleExpense', methods=['POST'])
def handleAddExpense():
    expense, payerData = getPostArgs(request, "expense", "payerData")
    groupId = None
    try:
    	groupId = request.json["groupId"]
    except:
    	groupId = None
    #handling 400 scenarios
    if not isFloat(expense):
        abort(400)
    return addNewExpense(expense, payerData, groupId)


@app.route('/handleExpense', methods=['PUT'])
def handleUpdateExpense():
	activityId, expense, payerData = getPutArgs(request, "activityId", "expense", "payerData")
	return editActivity(activityId, expense, payerData)


@app.route('/handleExpense', methods=['DELETE'])
def handleDeleteExpense():
    activityId = getArgs(request, "activityId")[0]
    # handling 400 scenarios
    if not isInt(activityId):
        abort(400)
    return deleteExpense(activityId)


@app.route('/fetchUserDetails', methods=['GET'])
def getUserDetails():
    userId = getArgs(request, "userId")[0]
    #handling 400 scenarios
    if not isInt(userId):
        abort(400)
    return fetchUserDetails(userId)


@app.route('/fetchUserActivity', methods=['GET'])
def getUserActivity():
	userId = getArgs(request, "userId")[0]
    # handling 400 scenarios
	if not isInt(userId): 
	    abort(400)
	return fetchUserActivity(userId)


@app.route('/fetchActivityDetails', methods=['GET'])
def getActivityDetails():
	activityId = getArgs(request, "activityId")[0]
    # handling 400 scenarios
	if not isInt(activityId): 
	    abort(400)
	return fetchActivityById(activityId)

@app.route('/setNormalize', methods=['POST'])
def setNormalize():
	userId, expense = getPostArgs(request, "userId", "expense")
	return 'hello'

# POST request to create a group. And add friends to it
@app.route('/inviteToGroup', methods=['POST'])
def add():
	grpId, grpName, friendList = getPostArgs(request, "grpId", "grpName", "friendList")
	return createGroupOrAdd(grpId, grpName, friendList)

@app.route('/fetchGroupDetails', methods=['GET'])
def getGroupDetails():
	grpId = getArgs(request, "grpId")[0]
	if not isString(grpId): 
	    abort(400)
	return fetchGroupDetails(grpId)

