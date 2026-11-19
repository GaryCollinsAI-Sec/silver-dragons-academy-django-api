
import logging

from rest_framework import status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response

from .parsers import StrictJSONParser
from .serializers import ChatRequestSerializer
from .services import answer


logger = logging.getLogger(__name__)


@api_view(["GET"])
def health(request):
    return Response({"status": "ok"})


@api_view(["POST"])
@parser_classes([StrictJSONParser])
def chat(request):
    serializer = ChatRequestSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(
            {"error": "invalid_request"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    message = serializer.validated_data["message"]

    try:
        reply = answer(message)
    except Exception:
        logger.exception("Silvia chatbot processing failed.")
        return Response(
            {"error": "internal_server_error"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return Response({
        "assistant": "Silvia",
        "reply": reply,
    })
