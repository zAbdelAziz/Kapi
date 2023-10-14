import os
from . import __BASEDIR__
from .responses import WebResponse


async def route_404(url):
	body = f"<html><body><p>404 - {url} Not found</p></body></html>"
	return WebResponse(body)


async def route_static(url):
	path = os.path.join(__BASEDIR__, 'static', url)
	return WebResponse(path=path)


async def route_favicon():
	path = os.path.join(__BASEDIR__, 'favicon.ico')
	return WebResponse(path=path)
