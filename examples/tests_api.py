from kapi.responses import *
from .long_text import text


async def home():
	# return WebResponse("i am kapi", cache=True)
	return Response(text, cache=True, content_type='text')


async def user(uid):
	return Response({'data': uid}, content_type='json')


async def no_content():
	return Response()


async def error_tester():
	for i in range('x'):
		print(i)
	return Response({'free': [f]}, content_type='', cache='Shower')