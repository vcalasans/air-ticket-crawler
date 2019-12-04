from django.urls import path

import views.views

urlpatterns = [
    path("", views.views.index, name="index"),
]
