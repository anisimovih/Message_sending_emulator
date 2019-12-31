import json

POST_SCHEMA = {
    '$schema': 'http://json-schema.org/schema',
    'type': 'object',
    'additionalProperties': False,
    'properties': {
        'Telegram': {
            'type': 'array',
            "uniqueItems": True,
            'items': {
                "type": "object",
                "properties": {
                    'user_id': {'type': 'number'},
                    'message': {'type': 'string'},
                    'date_time': {'type': 'string'},
                },
                'required': ['user_id', 'message'],
            },
        },
        'WhatsApp': {
            'type': 'array',
            "uniqueItems": True,
            'items': {
                "type": "object",
                "properties": {
                    'user_id': {'type': 'number'},
                    'message': {'type': 'string'},
                    'date_time': {'type': 'string'},
                },
                'required': ['user_id', 'message'],
            },
        },
        'Viber': {
            'type': 'array',
            "uniqueItems": True,
            'items': {
                "type": "object",
                "properties": {
                    'user_id': {'type': 'number'},
                    'message': {'type': 'string'},
                    'date_time': {'type': 'string'},
                },
                'required': ['user_id', 'message'],
            },
        },
    },
    "anyOf": [
        {
            'required': ['Telegram'],
        },
        {
            'required': ['WhatsApp'],
        },
        {
            'required': ['Viber'],
        },
    ],
}

GET_PUT_SCHEMA = {
    '$schema': 'http://json-schema.org/schema',
    'type': 'object',
    'additionalProperties': False,
    'properties':
        {
            'Telegram':
                {
                    'type': 'object',
                    'properties':
                        {
                            'users_id':
                                {
                                    "type": "array",
                                    "items":
                                        {'type': 'number', },
                                    "minItems": 1,
                                },
                        },
                    'required': ['users_id'],
                },
            'WhatsApp':
                {
                    'type': 'object',
                    'properties':
                        {
                            'users_id':
                                {
                                    "type": "array",
                                    "items":
                                        {'type': 'number', },
                                    "minItems": 1,
                                },
                        },
                    'required': ['users_id'],
                },
            'Viber':
                {
                    'type': 'object',
                    'properties':
                        {
                            'users_id':
                                {
                                    "type": "array",
                                    "items":
                                        {'type': 'number', },
                                    "minItems": 1,
                                },
                        },
                    'required': ['users_id'],
                },
        },
    'anyOf': [
        {
            'required': ['Telegram'],
        },
        {
            'required': ['WhatsApp'],
        },
        {
            'required': ['Viber'],
        },
    ],
}

PUT_SCHEMA = {
    "$schema": "http://json-schema.org/schema",
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "messages_id": {
            "type": "array",
            "items": {
                "type": "string"
            },
            "minItems": 1
        }
    }
}
