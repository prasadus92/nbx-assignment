CREATE_USER_REQUEST_SCHEMA = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "email": {"type": "string"}
    },
    "required": ["name", "email"],
    "additionalProperties": False
}

CREATE_USER_RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "id": {"type": "string"},
        "name": {"type": "string"},
        "email": {"type": "string"}
    }
}

UPDATE_USER_REQUEST_SCHEMA = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "email": {"type": "string"}
    },
    "additionalProperties": False
}

UPDATE_USER_RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "id": {"type": "string"},
        "name": {"type": "string"},
        "email": {"type": "string"}
    }
}
