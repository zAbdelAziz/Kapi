from kapi.responses import *


async def home():
	return Response("<html><body><h1>Home View</h1></body></html>")


async def user(uid):
	return JSON({'data': uid})


async def no_content():
	return JSON()
