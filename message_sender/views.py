import json
import hashlib
import redis
import base64
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from celery import current_app
from celery.result import AsyncResult
from jsonschema import validate
from jsonschema.exceptions import ValidationError
from .schemas import POST_SCHEMA, GET_PUT_SCHEMA, PUT_SCHEMA
from .tasks import send_message
from Message_sending_emulator.settings import CELERY_DB_NUMBER

R = redis.Redis(db=int(CELERY_DB_NUMBER))


class SendMessages(View):
    json_data = []
    errors = []

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(SendMessages, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        self.validate_json(request, PUT_SCHEMA)
        if self.errors:
            return JsonResponse({'error': self.errors}, status=400)
        statuses = {}
        for message_id in self.json_data["messages_id"]:
            status = AsyncResult(str(message_id)).state
            statuses[message_id] = status
        return JsonResponse(status=200, data=statuses)

    def post(self, request):
        self.validate_json(request, POST_SCHEMA)
        if self.errors:
            return JsonResponse({'error': self.errors}, status=400)
        results = {}
        for messenger in self.json_data:
            for message in self.json_data[messenger]:
                task_id = messenger[0] + str(message["user_id"]) + message["message"]
                task_id_hash = hashlib.md5(task_id.encode()).hexdigest()
                if R.exists("celery-task-meta-" + task_id_hash) == 1:
                    results[task_id_hash] = str('FAILED')
                else:
                    send_message.apply_async((message["user_id"], message["message"]),
                                             eta=message["date_time"] if "date_time" in message else None,
                                             task_id=task_id_hash)
                    results[task_id_hash] = str('SUCCESS')
        return JsonResponse(status=200, data=results)

    def put(self, request):
        self.validate_json(request, PUT_SCHEMA)
        if self.errors:
            return JsonResponse({'error': self.errors}, status=400)
        #tasks = self.get_celery_queue_items()
        # tasks = current_app.control.inspect()
        tasks = []
        results = {}
        info = getattr(current_app.control.inspect(), 'scheduled')()
        for part in info[list(info)[0]]:
            tasks.append(part['request']['id'])
        for message_id in self.json_data["messages_id"]:
            if message_id in tasks:
                results[message_id] = 'SUCCESS'
            else:
                results[message_id] = 'PENDING'
            current_app.control.revoke(message_id)
        return JsonResponse(status=200, data=results)

    def validate_json(self, request, schema):
        self.errors = []
        try:
            self.json_data = json.loads(request.body)
            validate(self.json_data, schema)
        except json.JSONDecodeError:
            self.errors.append('Invalid JSON')
        except ValidationError as exc:
            self.errors.append(exc.message)

    def get_celery_queue_items(self):
        with current_app.pool.acquire(block=True) as conn:
            tasks = conn.default_channel.client.lrange("celery", 0, -1)

        decoded_tasks = []

        for task in tasks:
            j = json.loads(task)
            body = json.loads(base64.b64decode(j['body']))
            decoded_tasks.append(body)

        return decoded_tasks
