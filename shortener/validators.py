from datetime import datetime

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_datetime(value):
    if value <= datetime.now():
        raise ValidationError(
            _('%(value)s is less than current date'),
            params={'value': value},
        )
