from django.urls import path
from . import views


urlpatterns = [
    path("notes/", views.NoteListCreate.as_view(), name="note-list"), 
    path("notes/delete/<int:pk>/", views.NoteDelete.as_view(), name="delete-note"),
    path("blocklist/", views.BlocklistListCreateView.as_view(), name="blocklist"),
    path("blocklist/<int:pk>/", views.BlocklistRetrieveUpdateDestroyView.as_view(), name="blocklist-delete"),
    path("blocklist/upload/", views.BlocklistFileUploadView.as_view(), name="blocklist-upload"),
]

