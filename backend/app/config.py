import os


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg://admissions:admissions@localhost:5432/admissions",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")
    KEYCLOAK_ISSUER = os.getenv("KEYCLOAK_ISSUER", "http://localhost:8080/realms/outpatient")
    KEYCLOAK_JWKS_URL = os.getenv(
        "KEYCLOAK_JWKS_URL",
        "http://localhost:8080/realms/outpatient/protocol/openid-connect/certs",
    )
    KEYCLOAK_CLIENT_ID = os.getenv("KEYCLOAK_CLIENT_ID", "admissions-frontend")
