from kapi.app import App

from examples.tests_routes import routes

if __name__ == "__main__":
    # routes = {("/home", {"test": 123}), ("/user/<username>", {"user_handler": 456})}
    # routes = {"/": {"main": 12}, "/home": {"test": 123}, "/user/<username>": {"user_handler": 456}}

    app = App(routes=routes)

    host = "127.0.0.1"
    port = 80

    app.run(host=host, port=port)

