from functools import wraps
from time import time

import jwt
import requests
from flask import current_app, g, jsonify, request
from jwt import PyJWKClient


_jwks_client = None
_jwks_loaded_at = 0


def get_jwks_client():
    global _jwks_client, _jwks_loaded_at

    jwks_url = current_app.config["KEYCLOAK_JWKS_URL"]
    if _jwks_client is None or time() - _jwks_loaded_at > 300:
        _jwks_client = PyJWKClient(jwks_url)
        _jwks_loaded_at = time()
    return _jwks_client


def decode_token(token):
    signing_key = get_jwks_client().get_signing_key_from_jwt(token)
    payload = jwt.decode(
        token,
        signing_key.key,
        algorithms=["RS256"],
        issuer=current_app.config["KEYCLOAK_ISSUER"],
        options={"verify_aud": False},
    )

    expected_client = current_app.config["KEYCLOAK_CLIENT_ID"]
    if payload.get("azp") != expected_client:
        raise jwt.InvalidTokenError("Token was not issued for this client")

    return payload


def require_auth(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return jsonify({"error": "Missing bearer token"}), 401

        token = auth_header.removeprefix("Bearer ").strip()
        try:
            g.current_user = decode_token(token)
        except (jwt.PyJWTError, requests.RequestException) as error:
            return jsonify({"error": "Invalid or expired token", "detail": str(error)}), 401

        return view(*args, **kwargs)

    return wrapped
