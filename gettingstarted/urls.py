from django.urls import path

import hello.views

urlpatterns = [
    path("", hello.views.index, name="index"),
]
