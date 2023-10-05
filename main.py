from app import App
import timeit
import asyncio

# routes = (('home', 123), ('home/<user>', 456), ('home/<user>/profile', 789))
# app = App(routes=routes)


if __name__ == "__main__":
    routes = {("/home", "home_handler"), ("/user/<username>", "user_handler")}
    app = App(routes=routes)

    host = "127.0.0.1"
    port = 8080

    asyncio.run(app.run(host, port))

