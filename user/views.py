import time
from datetime import datetime, timedelta

from django.shortcuts import render

# Create your views here.
import jwt
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from .models import User
from .serializers import RegisterSerializer


def decode_jwt_token(token):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


class RegisterAPIView(GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if User.objects.filter(email=email).exists():
            return Response(data={
                "msg": "email already existed"
            })

        user = User.objects.create(email=email, password=password)

        return Response(data={
            "id": user.id,
            "email": user.email
        })


class LoginView(GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        print(request.data)
        try:
            user = User.objects.get(email=email, password=password)
        except User.DoesNotExist:
            return Response(data={
                "msg": "invalid credentials"
            })

        payload = {
            'user_id': user.id,  # 用户id
            'exp': datetime.utcnow() + timedelta(days=3)  # 令牌的失效时间
        }
        # access_token = 加密(payload[用户id, 过期时间])
        # payload = 解密(access_token)

        access_token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

        payload = {  # refresh_token 携带的信息
            'user_id': user.id,
            'exp': datetime.utcnow() + timedelta(days=10)
        }

        refresh_token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        return Response(data={
            "access_token": access_token,
            "refresh_token": refresh_token
        })


class MeView(GenericAPIView):
    def get(self, request):
        # 后端从headers的AUTHORIZATION中获取用户的access_token
        access_token = request.META.get('HTTP_AUTHORIZATION')

        parts = access_token.split(" ")
        if len(parts) != 2 or parts[0] != "Bearer":
            return Response(data={
                "msg": "please provide a valid access_token"
            })
        else:
            try:
                payload = decode_jwt_token(access_token.split(" ")[1])
            except Exception:
                return Response(data={
                    "msg": "please provide a valid access_token"
                })

            if payload["exp"] < time.time():
                return Response(data={
                    "msg": "access token expired"
                })

            user = User.objects.get(id=payload["user_id"])

            return Response(data={
                "email": user.email,
                "id": user.id
            })
