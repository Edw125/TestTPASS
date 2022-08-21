from datetime import datetime, timedelta, timezone
from hashlib import md5

from django.db import models
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

from graphql import GraphQLError

from shortener.validators import validate_datetime


def default_expiration_time():
    return datetime.now(tz=timezone.utc) + timedelta(days=10)


class URL(models.Model):
    full_url = models.URLField(unique=True)
    url_hash = models.URLField(unique=True)
    clicks = models.IntegerField(default=0)
    expiration_time = models.DateTimeField(default=default_expiration_time, validators=[validate_datetime])
    created_at = models.DateTimeField(auto_now_add=True)

    def clicked(self):
        self.clicks += 1
        self.save()

    def save(self, *args, **kwargs):
        if not self.id:
            self.url_hash = md5(self.full_url.encode()).hexdigest()[:10]

        validate = URLValidator()
        try:
            validate(self.full_url)
        except ValidationError as e:
            raise GraphQLError('invalid url')

        return super().save(*args, **kwargs)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return str(self.full_url)
