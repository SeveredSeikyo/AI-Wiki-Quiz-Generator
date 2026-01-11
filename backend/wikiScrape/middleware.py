import jwt
from django.contrib.auth.models import User
from django.conf import settings
from django.http import JsonResponse
import environ

env = environ.Env()
environ.Env.read_env()


class JWTAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        token = request.COOKIES.get('access_token')
        if token:
            try:
                payload = jwt.decode(token, env("JWT_SECRET_TOKEN"), algorithms=["HS256"])
                user_id = payload.get('user_id')
                if user_id:
                    try:
                        user = User.objects.get(email=user_id)
                        request.user = user
                    except User.DoesNotExist:
                        pass
            except jwt.ExpiredSignatureError:
                pass
            except jwt.InvalidTokenError:
                pass

        response = self.get_response(request)
        return response