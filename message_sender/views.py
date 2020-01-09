import json
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from celery import current_app
from jsonschema import validate
from jsonschema.exceptions import ValidationError
from .schemas import POST_SCHEMA, GET_PUT_SCHEMA
from .tasks import send_message
from .models import MessagesTable


class SendMessages(View):
    json_data = []
    errors = []

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(SendMessages, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        self.validate_json(request, GET_PUT_SCHEMA)
        if self.errors:
            return JsonResponse({'error': self.errors}, status=400)
        results_list = []
        scheduled_tasks_list, reserved_tasks_list = self.tasks_args_list()
        for messenger in self.json_data:
            for message in self.json_data[messenger]:
                if [message["sender_id"], message["recipient_id"], message["message"]] in scheduled_tasks_list:
                    results_list.append('PENDING')
                elif [message["sender_id"], message["recipient_id"], message["message"]] in reserved_tasks_list:
                    results_list.append('SENDING')
                elif MessagesTable.objects.check_existence_by_text(message["sender_id"], message["recipient_id"], message["message"]):
                    results_list.append('SENT')
                else:
                    results_list.append('NOT FOUND')
        return JsonResponse(status=200, data={"results": results_list})

    def post(self, request):
        self.validate_json(request, POST_SCHEMA)
        if self.errors:
            return JsonResponse({'error': self.errors}, status=400)
        results_list = []
        scheduled_tasks_list, reserved_tasks_list = self.tasks_args_list()
        for messenger in self.json_data:
            for message in self.json_data[messenger]:
                if [message["sender_id"], message["recipient_id"], message["message"]] in scheduled_tasks_list:
                    results_list.append('PENDING')
                elif [message["sender_id"], message["recipient_id"], message["message"]] in reserved_tasks_list:
                    results_list.append('SENDING')
                elif MessagesTable.objects.check_existence_by_text(messenger, message["sender_id"], message["recipient_id"], message["message"]):
                    results_list.append('ALREADY SENT')
                else:
                    results_list.append('ADDED')
                    send_message.apply_async((messenger, message["sender_id"], message["recipient_id"], message["message"]),
                                             eta=message["date_time"] if "date_time" in message else None)
        return JsonResponse(status=200, data={"results": results_list})

    def put(self, request):
        self.validate_json(request, GET_PUT_SCHEMA)
        if self.errors:
            return JsonResponse({'error': self.errors}, status=400)
        results_list = []
        scheduled_tasks_args_and_id = self.scheduled_tasks_args_and_id()
        for messenger in self.json_data:
            for message in self.json_data[messenger]:
                for row in scheduled_tasks_args_and_id:
                    if [message["sender_id"], message["recipient_id"], message["message"]] == row[0]:
                        current_app.control.revoke(row[1])
                        results_list.append('CANCELED')
                        break
                else:
                    results_list.append('NOT FOUND')
        return JsonResponse(status=200, data={"results": results_list})

    def validate_json(self, request, schema):
        self.errors = []
        try:
            self.json_data = json.loads(request.body)
            validate(self.json_data, schema)
        except json.JSONDecodeError:
            self.errors.append('Invalid JSON')
        except ValidationError as exc:
            self.errors.append(exc.message)

    def scheduled_tasks_args_and_id(self):
        i = current_app.control.inspect()

        scheduled_tasks_map = i.scheduled()
        scheduled_tasks_list = []
        for part in scheduled_tasks_map[list(scheduled_tasks_map)[0]]:
            scheduled_tasks_list.append((part['request']['args'], part['request']['id']))
        return scheduled_tasks_list

    def tasks_args_list(self):
        i = current_app.control.inspect()

        scheduled_tasks_map = i.scheduled()
        scheduled_tasks_list = []
        for part in scheduled_tasks_map[list(scheduled_tasks_map)[0]]:
            scheduled_tasks_list.append(part['request']['args'])

        reserved_tasks_map = i.reserved()
        reserved_tasks_list = []
        for part in reserved_tasks_map[list(reserved_tasks_map)[0]]:
            reserved_tasks_list.append(part['request']['args'])
        return scheduled_tasks_list, reserved_tasks_list
