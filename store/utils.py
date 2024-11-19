from rest_framework.response import Response

def response_formatter(message, data=None, status=200):
    return Response({
        'message': message,
        'data': data if data is not None else {}
    }, status=status)
