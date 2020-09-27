__all__ = ['validate']

def validate(data):
	print(data)
	if data.get('username') == 'musician' and data.get('password') == 'wanggan':
		return True
	else:
		return False