from kapi.responses import *


async def home():
	return Response("I am kapi", cache=True)


async def user(uid):
	return JSON({'data': uid})


async def no_content():
	return JSON()
