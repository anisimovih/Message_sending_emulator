import json
from django.http import JsonResponse
from django.views import View
from .tasks import send_message
from celery import current_app
from celery.result import AsyncResult
from django.views.decorators.csrf import csrf_exempt


class SendMessages(View):
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(SendMessages, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        # logging.info("get")
        (json_data, errors) = self.parse_json(request)
        if errors:
            # logging.error(errors)
            return JsonResponse(status=400, data={"errors": errors})
        if "message_id" in json_data:
            statuses = []
            for message_id in json_data["message_id"]:
                status = AsyncResult(message_id).state
                statuses.append(status)
            return JsonResponse(status=200, data={'message_status': '%s' % statuses})
        else:
            return JsonResponse(status=400, data={'error': 'Missing message_id parameter'})

    def post(self, request):
        (json_data, errors) = self.parse_json(request)
        if errors:
            # logging.error(errors)
            return JsonResponse(status=400, data={"errors": errors})
        messages_id = []
        for messenger in json_data:
            for message in json_data[messenger]:
                task_id = send_message.apply_async((message["user_id"], message["message"]), eta=message["date_time"] if "date_time" in message else None)
                messages_id.append(str(task_id))
        return JsonResponse(status=200, data={'Messages added to send queue with id': '%s' % messages_id})

    def put(self, request):
        # logging.info("put")
        (json_data, errors) = self.parse_json(request)
        if errors:
            # logging.error(errors)
            return JsonResponse(status=400, data={"errors": errors})
        if "message_id" in json_data:
            for message_id in json_data["message_id"]:
                current_app.control.revoke(message_id)
            return JsonResponse(status=200, data={'Message canceled': 'True'})
        else:
            return JsonResponse(status=400, data={'error': 'Missing message_id parameter'})

    @staticmethod
    def parse_json(request):
        errors = []
        json_data = json.loads(request.body)
        if json_data is None:
            errors.append(
                "No JSON sent. Did you forget to set Content-Type header" +
                " to application/json?")
            return None, errors
        return json_data, errors

