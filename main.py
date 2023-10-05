from app import App


routes = (('home', 123), ('home/<user>', 456), ('home/<user>/profile', 789))
app = App(None, routes)
