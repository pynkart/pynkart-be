# DRF imports --
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import serializers, status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

# Django imports --
from django.shortcuts import get_object_or_404
from django.http import Http404

from pynkseller.pagination import (
    LimitOffsetPagination, get_paginated_response
)

from pynkmail.services import (
    setting_create_or_set
)


class SetEmailSettingsAPI(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    
    class InputSerializer(serializers.Serializer):
        email = serializers.EmailField()
        key = serializers.CharField()
    
    def post(self, request:Request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        setting = setting_create_or_set(**serializer.validated_data, user=request.user)
        return Response(data="Setting success.",status=status.HTTP_201_CREATED)
        