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
    setting_create_or_set, format_create, validate_gkey_task
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
        
        if (not validate_gkey_task(**serializer.validated_data)):
            return Response(data="Key is invalid", status=status.HTTP_406_NOT_ACCEPTABLE)
        
        setting = setting_create_or_set(**serializer.validated_data, user=request.user)
        return Response(data="Setting success.",status=status.HTTP_201_CREATED)


class CreateEmailFormatAPI(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    
    class InputSerializer(serializers.Serializer):
        title = serializers.CharField()
        body = serializers.CharField()
        
    def post(self, request:Request):
        serializers = self.InputSerializer(data=request.data)
        serializers.is_valid(raise_exception=True)
        
        format = format_create(**serializers.validated_data, user=request.user)
        return Response(data="Create success",status=status.HTTP_201_CREATED)
        