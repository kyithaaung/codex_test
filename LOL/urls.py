from django.contrib import admin
from django.http import HttpRequest, JsonResponse
from django.shortcuts import redirect
from django.urls import include, path


def health(_: HttpRequest) -> JsonResponse:
    return JsonResponse({"app": "LOL", "status": "ok"})


def index(request: HttpRequest):
    port = request.get_port()
    if port in {"90080", "9000", "19080"}:
        return redirect("customer-login")
    return redirect("internal-login")


urlpatterns = [
    path("", index),
    path("admin/", admin.site.urls),
    path("health/", health),
    path("", include("accounts.urls")),
]
