import json
import os
from functools import wraps
from urllib.request import urlopen

from jose import jwt
from jose.utils import base64url_decode
from flask import request, jsonify

# Simple Auth0 JWT validation helper using JWKS

AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN')
AUTH0_AUDIENCE = os.getenv('AUTH0_AUDIENCE')

def get_jwks():
    if not AUTH0_DOMAIN:
        raise RuntimeError('AUTH0_DOMAIN not set')
    jwks_url = f'https://{AUTH0_DOMAIN}/.well-known/jwks.json'
    with urlopen(jwks_url) as response:
        return json.load(response)

def decode_and_verify_jwt(token: str):
    if not AUTH0_DOMAIN or not AUTH0_AUDIENCE:
        raise RuntimeError('Auth0 config missing (AUTH0_DOMAIN/AUDIENCE)')

    jwks = get_jwks()
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    for key in jwks.get('keys', []):
        if key.get('kid') == unverified_header.get('kid'):
            rsa_key = {
                'kty': key.get('kty'),
                'kid': key.get('kid'),
                'use': key.get('use'),
                'n': key.get('n'),
                'e': key.get('e')
            }
    if not rsa_key:
        raise Exception('Unable to find appropriate key')

    payload = jwt.decode(
        token,
        rsa_key,
        algorithms=['RS256'],
        audience=AUTH0_AUDIENCE,
        issuer=f'https://{AUTH0_DOMAIN}/'
    )

    return payload

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.headers.get('Authorization', None)
        if not auth:
            return jsonify({'error': 'Authorization header is expected'}), 401

        parts = auth.split()
        if parts[0].lower() != 'bearer':
            return jsonify({'error': 'Authorization header must start with Bearer'}), 401
        elif len(parts) == 1:
            return jsonify({'error': 'Token not found'}), 401
        elif len(parts) > 2:
            return jsonify({'error': 'Authorization header must be Bearer token'}), 401

        token = parts[1]
        try:
            payload = decode_and_verify_jwt(token)
        except Exception as e:
            return jsonify({'error': 'Invalid token', 'details': str(e)}), 401

        # attach payload to request context if needed
        request.auth_payload = payload
        return f(*args, **kwargs)

    return decorated
