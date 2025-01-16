from django.urls import path
from . import views


urlpatterns = [
    path("notes/", views.NoteListCreate.as_view(), name="note-list"), 
    path("notes/delete/<int:pk>/", views.NoteDelete.as_view(), name="delete-note"),
    path("blocklist/", views.BlocklistView.as_view(), name="blocklist"),
    path("iplist/", views.IPListView.as_view(), name="ip-list"),
    path("domainlist/", views.DomainListView.as_view(), name="domain-list"),
]

