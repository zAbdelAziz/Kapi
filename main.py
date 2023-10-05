from app import App
import timeit

routes = (('home', 123), ('home/<user>', 456), ('home/<user>/profile', 789))
app = App(routes=routes)

time_taken = timeit.timeit(lambda: app.router.resolve("/home/xyz/profile"), number=5000000)
print(time_taken)