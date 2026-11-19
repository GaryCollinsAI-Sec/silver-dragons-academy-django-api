
from django.core.exceptions import RequestDataTooBig
from django.http import JsonResponse


class RequestBodyLimitMiddleware:
    MAX_BODY_SIZE = 4096

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        content_length = request.META.get("CONTENT_LENGTH")

        if content_length:
            try:
                content_length = int(content_length)
            except (TypeError, ValueError):
                return JsonResponse(
                    {"error": "invalid_request"},
                    status=400,
                )

            if content_length < 0 or content_length > self.MAX_BODY_SIZE:
                return JsonResponse(
                    {"error": "invalid_request"},
                    status=400,
                )

        try:
            if len(request.body) > self.MAX_BODY_SIZE:
                return JsonResponse(
                    {"error": "invalid_request"},
                    status=400,
                )

            return self.get_response(request)

        except RequestDataTooBig:
            return JsonResponse(
                {"error": "invalid_request"},
                status=400,
            )
