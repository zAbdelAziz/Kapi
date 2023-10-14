from kapi.responses import *


async def home():
	return WebResponse("I am kapi", cache=True)


async def user(uid):
	return WebResponse({'data': uid}, content_type='json')


async def no_content():
	return WebResponse()
