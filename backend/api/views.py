from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics, viewsets, permissions, status
from .serializers import UserSerializer, NoteSerializer, BlocklistItemSerializer, IPListSerializer, DomainListSerializer
from .models import Note, BlocklistItem, IPList, DomainList
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView  # Add this line
from rest_framework.parsers import JSONParser
import os
import ipaddress
import re


class NoteListCreate(generics.ListCreateAPIView):
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Note.objects.filter(author=user)
    
    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(author=self.request.user)
        else:
            print(serializer.errors)

class NoteDelete(generics.DestroyAPIView):
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated] #AllowAny

    def get_queryset(self):
        user = self.request.user
        return Note.objects.filter(author=user)


# Create your views here.
class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class BlocklistView(generics.ListCreateAPIView):
    queryset = BlocklistItem.objects.all()
    serializer_class = BlocklistItemSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(added_by=self.request.user if self.request.user.is_authenticated else None)


class IPListView(generics.ListCreateAPIView):
    queryset = IPList.objects.all()
    serializer_class = IPListSerializer
    permission_classes = [AllowAny]


class DomainListView(generics.ListCreateAPIView):
    queryset = DomainList.objects.all()
    serializer_class = DomainListSerializer
    permission_classes = [AllowAny]