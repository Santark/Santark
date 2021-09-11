import json

def isInt(val):
	try:
		val = int(val)
		return True
	except:
		return False

def isFloat(val):
	try:
		val = float(val)
		return True
	except:
		return False

def isString(val):
	try:
		val = str(val)
		return True
	except:
		return False

def castToDict(val):
    try:
        return json.loads(val)
    except:
        return None