from .tests_api import *


routes = {
	("/", home, 'get'),
	("/home", home, 'get'),
	("/user/<uid>", user, 'get'),
	("/user/<uid>/x", no_content, 'get')
}
