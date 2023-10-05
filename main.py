from app import App
import cProfile
import timeit, time

routes = (('home', 123), ('home/<user>', 456), ('home/<user>/profile', 789))
app = App(None, routes)

# print(app.router.root.children['h'].children['o'].children['m'].children['e'].ptype)

# print(app.router._search('home/<int>').callback)
print(app.router.resolve('home/1'))
print(app.router.resolve('/home/xyz/profile'))


time_taken = timeit.timeit(lambda: app.router.resolve("/home/xyz/profile"), number=5000000)
print(time_taken)
del app