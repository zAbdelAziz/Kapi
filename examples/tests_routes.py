from .tests_api import *


routes = {
	"/": home,
	"/home": home,
	"/user/<uid>": user
}
