import os
from . import __BASEDIR__
from .responses import Static, Response


async def route_404(url):
	body = f"<html><body><p>404 - {url} Not found</p></body></html>"
	return Response(body)


async def route_static(url):
	path = os.path.join(__BASEDIR__, 'static', url)
	return Static(path)


async def route_favicon():
	path = os.path.join(__BASEDIR__, 'favicon.ico')
	return Static(path)
