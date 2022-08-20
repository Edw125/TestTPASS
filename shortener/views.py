from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect

from .models import URL


def root(request, url_hash):
    url = get_object_or_404(URL, url_hash=url_hash)
    url.clicked()
    if url.created_at < url.expiration_time:
        return redirect(url.full_url)
    else:
        return HttpResponse("500 Bad request", status=500)
