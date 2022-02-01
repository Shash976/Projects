from django.urls import path, re_path
from . import views


app_name="encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path('search', views.search, name="search"),
    path("create", views.new_page, name="create"),
    path("random", views.random_page, name="random"),
    re_path(r"^(?P<title>\w+)/edit$", views.edit_page, name="edit"),
    re_path(r"^(?P<title>\w+)$", views.entry, name="entry"),
]
