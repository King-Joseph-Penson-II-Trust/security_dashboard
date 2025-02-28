from django.urls import path
from . import views


urlpatterns = [
    path("blocklist/", views.BlocklistListCreateView.as_view(), name="blocklist"),
    path("blocklist/<int:pk>/", views.BlocklistRetrieveUpdateDestroyView.as_view(), name="blocklist-delete"),
    path("blocklist/upload/", views.BlocklistFileUploadView.as_view(), name="blocklist-upload"),
]

