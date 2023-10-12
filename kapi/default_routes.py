import os
from . import __BASEDIR__
from .responses import Static


async def handle_404(url):
	return f"<html><body><p>404 - {url} Not found</p></body></html>"


async def route_static(url):
	path = os.path.join(__BASEDIR__, 'static', url)
	return Static(path)


async def route_favicon():
	path = os.path.join(__BASEDIR__, 'favicon.ico')
	return Static(path)
