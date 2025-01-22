from django.urls import path
from . import views


urlpatterns = [
    path("notes/", views.NoteListCreate.as_view(), name="note-list"), 
    path("notes/delete/<int:pk>/", views.NoteDelete.as_view(), name="delete-note"),
    path("blocklist/", views.BlocklistListCreateView.as_view(), name="blocklist"),
    path("blocklist/<int:pk>/", views.BlocklistRetrieveUpdateDestroyView.as_view(), name="blocklist-delete"),
    # path("iplist/", views.IPListView.as_view(), name="ip-list"),
    # path('iplist/<int:pk>/', views.IPListRetrieveUpdateDestroyView.as_view(), name='iplist-retrieve-update-destroy'),
    # path("domainlist/", views.DomainListView.as_view(), name="domain-list"),
    # path('domainlist/<int:pk>/', views.DomainListRetrieveUpdateDestroyView.as_view(), name='domainlist-retrieve-update-destroy'),
]

