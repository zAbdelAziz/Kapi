
async def home():
	# print('Testing Home View')
	return "<html><body><h1>Home View</h1></body></html>"


async def user(uid):
	# print(f'Testing User view for {uid}')
	return {"data": uid}
	# return f"<html><body><h1>User {uid}</h1></body></html>"
