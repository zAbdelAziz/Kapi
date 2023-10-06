from app import App


if __name__ == "__main__":
    routes = {("/home", "home_handler"), ("/user/<username>", "user_handler")}
    app = App(routes=routes)

    host = "127.0.0.1"
    port = 8080

    app.run()

