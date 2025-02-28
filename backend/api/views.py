from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics, viewsets, permissions, status
from .serializers import UserSerializer, NoteSerializer, BlocklistItemSerializer
from .models import BlocklistItem
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
import os
import ipaddress
import re



# Create your views here.
class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class BlocklistListCreateView(generics.ListCreateAPIView):
    queryset = BlocklistItem.objects.all()
    serializer_class = BlocklistItemSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(added_by=self.request.user if self.request.user.is_authenticated else None)

class BlocklistRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BlocklistItem.objects.all()
    serializer_class = BlocklistItemSerializer
    permission_classes = [AllowAny]

class BlocklistFileUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        file = request.FILES['file']
        notes = request.data.get('notes', '')
        delete_date = request.data.get('delete_date', None)
        existing_entries = []
        new_entries = []

        for line in file:
            entry = line.strip().decode('utf-8')
            if BlocklistItem.objects.filter(entry=entry).exists():
                existing_entries.append(entry)
            else:
                BlocklistItem.objects.create(
                    entry=entry,
                    notes=notes,
                    delete_date=delete_date,
                    added_by=request.user if request.user.is_authenticated else None
                )
                new_entries.append(entry)

        return Response({
            'existing_entries': existing_entries,
            'new_entries': new_entries
        }, status=status.HTTP_200_OK)