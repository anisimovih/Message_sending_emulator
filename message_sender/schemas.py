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
                "additionalProperties": False,
                "properties": {
                    'sender_id': {'type': 'number'},
                    'recipient_id': {'type': 'number'},
                    'message': {'type': 'string'},
                    'date_time': {'type': 'string'},
                },
                'required': ['sender_id', 'recipient_id', 'message'],
            },
        },
        'WhatsApp': {
            'type': 'array',
            "uniqueItems": True,
            'items': {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    'sender_id': {'type': 'number'},
                    'recipient_id': {'type': 'number'},
                    'message': {'type': 'string'},
                    'date_time': {'type': 'string'},
                },
                'required': ['sender_id', 'recipient_id', 'message'],
            },
        },
        'Viber': {
            'type': 'array',
            "uniqueItems": True,
            'items': {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    'sender_id': {'type': 'number'},
                    'recipient_id': {'type': 'number'},
                    'message': {'type': 'string'},
                    'date_time': {'type': 'string'},
                },
                'required': ['sender_id', 'recipient_id', 'message'],
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
    'properties': {
        'Telegram': {
            'type': 'array',
            "uniqueItems": True,
            'items': {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    'sender_id': {'type': 'number'},
                    'recipient_id': {'type': 'number'},
                    'message': {'type': 'string'},
                },
                'required': ['sender_id', 'recipient_id', 'message'],
            },
        },
        'WhatsApp': {
            'type': 'array',
            "uniqueItems": True,
            'items': {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    'sender_id': {'type': 'number'},
                    'recipient_id': {'type': 'number'},
                    'message': {'type': 'string'},
                },
                'required': ['sender_id', 'recipient_id', 'message'],
            },
        },
        'Viber': {
            'type': 'array',
            "uniqueItems": True,
            'items': {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    'sender_id': {'type': 'number'},
                    'recipient_id': {'type': 'number'},
                    'message': {'type': 'string'},
                },
                'required': ['sender_id', 'recipient_id', 'message'],
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
