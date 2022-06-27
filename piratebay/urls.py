from django.contrib import admin
from django.urls import path
from piratebay import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.root, name="root"),
]
