from django.contrib import admin
from django.urls import path
from applications.views import apply, status

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", apply, name="apply"),
    path("status/<uuid:token>/", status, name="status"),
]
