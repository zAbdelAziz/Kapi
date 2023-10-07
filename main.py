from kapi.app import App

from examples.tests_routes import routes


if __name__ == "__main__":
    host = "127.0.0.1"
    port = 80

    app = App(host=host, port=port, routes=routes)
    app.run()

