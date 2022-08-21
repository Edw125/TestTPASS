from rest_framework import serializers

from shortener.models import URL


class UrlSerializer(serializers.ModelSerializer):
    class Meta:
        model = URL
        fields = "__all__"
