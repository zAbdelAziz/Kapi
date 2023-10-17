import os
from . import __BASEDIR__
from .responses import Response


async def route_404(url):
	body = f"404 - '{url}' Not found"
	return Response(data=body, status=404, cache=True, content_type='text')


async def route_500(error):
	body = (f"Something went wrong here\n\n{error}")
	return Response(data=body, status=500, cache=True, content_type='text')


async def route_static(url):
	path = os.path.join(__BASEDIR__, 'static', url)
	return Response(path=path, cache=True)


async def route_favicon():
	path = os.path.join(__BASEDIR__, 'favicon.ico')
	return Response(path=path, cache=True)
