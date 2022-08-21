
from datetime import timezone, datetime

from django.core.serializers import json
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from rest_framework import status, permissions, authentication
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import URL
from .serializers import UrlSerializer


def root(request, url_hash):
    url = get_object_or_404(URL, url_hash=url_hash)
    url.clicked()
    if url.created_at < url.expiration_time:
        return redirect(url.full_url)
    else:
        return HttpResponse("500 Bad request", status=500)


class UrlView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        data = URL.objects.all()
        if data:
            return Response(
                data.values(),
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {'detail': 'Записей не существует'},
                status=status.HTTP_404_NOT_FOUND
            )

    def post(self, request, *args, **kwargs):
        url = self.request.data['full_url']
        date = self.request.data['expiration_time']
        if URL.objects.filter(full_url=url).exists():
            return Response(
                {'detail': 'Запись уже есть в базе данных'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if date <= str(datetime.now(tz=timezone.utc)):
            return Response(
                {'detail': 'Время действия короткой ссылки меньше текущего'},
                status=status.HTTP_400_BAD_REQUEST
            )

        new_url = URL.objects.create(
            full_url=url,
            expiration_time=date
        )
        return Response(
                {
                    'detail': 'Запись успешно добавлена',
                    'data': URL.objects.filter(full_url=new_url).values()[0]
                 },
                status=status.HTTP_201_CREATED
            )
