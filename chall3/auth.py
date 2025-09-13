import jwt
import random
from datetime import datetime, timedelta, timezone
import uuid
from flask import Flask, request, redirect, url_for, make_response
from functools import wraps

SECRET_KEY = '6535ccea-7a73-4ab7-baa5-4954d16be029'

def generate_token(username, role):
	payload = {
		'exp': datetime.now(timezone.utc) + timedelta(hours=1),
		'iat': datetime.now(timezone.utc),
		'sub': username,
		'role': role
	}

	return jwt.encode(
		payload,
		SECRET_KEY,
		algorithm='HS256'
	)

def verify_token(token):
	try:
		payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
		return payload
	except jwt.ExpiredSignatureError:
		return None
	except jwt.InvalidTokenError:
		return None

def login_required(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		token = request.cookies.get('jwt_token')
		print(f">>>>> TOKEN: {token}")
		if not token:
			return redirect(url_for("index"))

		try:
			jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
		except jwt.ExpiredSignatureError:
			return "Token expired. Please login again."
		except jwt.InvalidTokenError:
			print(f">>>>> TOKEN: Invalid token")
			return redirect(url_for('index'))

		return f(*args, **kwargs)

	return decorated_function