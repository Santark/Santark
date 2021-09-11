from databaseAccessors import *
from flask import abort
import json
import time

def getArgs(request, *args):
	""" Handle the Get request params"""
	out = []
	for val in args:
		try:
		    res = request.args.get(val)
		    out.append(res)
		except Exception as e:
			print(e)
			abort(404)
	return out

def getPostArgs(request, *args):
	""" Handle the Post request body"""
	out = []
	for val in args:
		try:
		    res = request.json[val]
		    out.append(res)
		except Exception as e:
			print(e)
			abort(404)
	return out

def getPutArgs(request, *args):
	""" Handle the Put request body"""
	out = []
	for val in args:
		try:
		    res = request.json[val]
		    out.append(res)
		except Exception as e:
			print(e)
			abort(404)
	return out