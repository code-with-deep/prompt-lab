from functools import wraps
from flask import current_app, request, jsonify, g
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from models.database import User


def _serializer():
    return URLSafeTimedSerializer(current_app.config['SECRET_KEY'])


def create_auth_token(user_id: int) -> str:
    return _serializer().dumps({'user_id': user_id}, salt='auth-token')


def decode_auth_token(token: str, max_age_seconds: int):
    return _serializer().loads(token, salt='auth-token', max_age=max_age_seconds)


def token_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Authorization token required'}), 401

        token = auth_header.split(' ', 1)[1].strip()
        if not token:
            return jsonify({'error': 'Authorization token required'}), 401

        max_age = current_app.config.get('AUTH_TOKEN_MAX_AGE_SECONDS', 86400)

        try:
            payload = decode_auth_token(token, max_age_seconds=max_age)
            user = User.query.get(payload.get('user_id'))
            if not user:
                return jsonify({'error': 'Invalid token'}), 401

            g.current_user = user
            return fn(*args, **kwargs)
        except SignatureExpired:
            return jsonify({'error': 'Session expired. Please log in again.'}), 401
        except BadSignature:
            return jsonify({'error': 'Invalid token'}), 401

    return wrapper
