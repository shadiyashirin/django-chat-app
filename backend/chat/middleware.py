from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from django.contrib.auth import get_user_model
from channels.middleware import BaseMiddleware
from asgiref.sync import sync_to_async
from urllib.parse import parse_qs

User = get_user_model()


@sync_to_async
def get_user(user_id):
    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        return None


class JWTAuthMiddleware(BaseMiddleware):

    async def __call__(self, scope, receive, send):
        query_string = scope["query_string"].decode()
        query_params = parse_qs(query_string)

        token = query_params.get("token")

        if token:
            token = token[0]
            try:
                validated_token = UntypedToken(token)
                user_id = validated_token["user_id"]
                user = await get_user(user_id)
                scope["user"] = user
            except (InvalidToken, TokenError):
                scope["user"] = None
        else:
            scope["user"] = None

        return await super().__call__(scope, receive, send)
