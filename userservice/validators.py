from aiohttp import web
from email_validator import validate_email, EmailNotValidError


def validate_email(email):
    try:
        v = validate_email(email)
        email = v["email"]
        return email
    except EmailNotValidError as e:
        raise web.HTTPBadRequest(text=str(e))
