import json
from django.http import JsonResponse
from django.views import View
from .tasks import send_message
from celery import current_app
from celery.result import AsyncResult
from django.views.decorators.csrf import csrf_exempt

from jsonschema import validate
from jsonschema.exceptions import ValidationError
from .schemas import POST_SCHEMA, GET_PUT_SCHEMA


class SendMessages(View):
    json_data = []
    errors = []

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(SendMessages, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        # logging.info("get")
        self.validate_json(request, GET_PUT_SCHEMA)
        if self.errors:
            return JsonResponse({'error': self.errors}, status=400)
        statuses = []
        for messenger in self.json_data:
            for message_id in self.json_data[messenger]["users_id"]:
                status = AsyncResult(str(message_id)).state
                statuses.append(status)
        return JsonResponse(status=200, data={'message_status': '%s' % statuses})

    def post(self, request):
        self.validate_json(request, POST_SCHEMA)
        if self.errors:
            return JsonResponse({'error': self.errors}, status=400)
        messages_id = []
        for messenger in self.json_data:
            for message in self.json_data[messenger]:
                task_id = send_message.apply_async((message["user_id"], message["message"]), eta=message["date_time"] if "date_time" in message else None)
                messages_id.append(str(task_id))
        return JsonResponse(status=200, data={'Messages added to send queue with id': '%s' % messages_id})

    def put(self, request):
        # logging.info("put")
        self.validate_json(request, GET_PUT_SCHEMA)
        if self.errors:
            return JsonResponse({'error': self.errors}, status=400)
        for messenger in self.json_data:
            for message_id in self.json_data[messenger]["users_id"]:
                current_app.control.revoke(message_id)
        return JsonResponse(status=200, data={'Message canceled': 'True'})

    def validate_json(self, request, schema):
        self.errors = []
        try:
            self.json_data = json.loads(request.body)
            validate(self.json_data, schema)
        except json.JSONDecodeError:
            self.errors.append('Invalid JSON')
        except ValidationError as exc:
            self.errors.append(exc.message)


