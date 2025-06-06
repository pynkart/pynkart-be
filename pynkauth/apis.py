# DRF imports
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import serializers, status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

# Django imports
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.shortcuts import get_object_or_404
from django.middleware.csrf import get_token
from django.http import Http404

# Python imports
import smtplib

# Users APIs
class CreateUserAPI(APIView):
    class InputSerializer(serializers.Serializer):
        username = serializers.CharField()
        password = serializers.CharField()
        first_name = serializers.CharField()
        last_name = serializers.CharField()
        email = serializers.EmailField()
        
        
    def post(self, request: Request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = User.objects.create_user(**serializer.validated_data)
        login(request, user)
        return Response(data={"Created user"}, status=status.HTTP_201_CREATED) # TODO not fully implemented yet
    

class GetUserDetailsAPI(APIView):
    class OutputSerializer(serializers.ModelSerializer):
        class Meta():
            model = User
            fields = ["username", "id"]
            
    def get(self, request: Request, username):
        try:
            user =  get_object_or_404(User, username=username)
            
            if user is None:
                return Response(status=status.HTTP_204_NO_CONTENT)
            
            data = self.OutputSerializer(user).data
            return Response(data=data, status=status.HTTP_200_OK)
        
        except Http404:
            return Response(status=status.HTTP_404_NOT_FOUND)


class AuthenticatedAPI(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request: Request):
        return Response(data={"detail" : "You are authenticated."}, status=status.HTTP_200_OK)


class GetCsrfAPI(APIView):
    def get(self, request: Request):
        token = get_token(request)
        response = Response(data={"Info":"Success - CSRF Sent"})
        response["X-CSRFToken"] = token
        return response


class LoginUserAPI(APIView):
    class InputSerializer(serializers.Serializer):
        username = serializers.CharField()
        password = serializers.CharField()
        
    def post(self, request: Request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        username = request.data.get('username')
        password = request.data.get('password')
        
        user = User.objects.filter(username=username).first()
        if user is None or not user.check_password(password):
            return Response({"detail": "Invalid username or password"}, status=status.HTTP_401_UNAUTHORIZED)
        
        login(request, user)
        data = GetUserDetailsAPI.OutputSerializer(user).data
        
        return Response(
            {"logged-in-user" : data}, status=status.HTTP_200_OK
        )
        

class LogoutUserAPI(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request: Request):
        logout(request)
        return Response(data={"detail" : "Successfully logged out"}, status=status.HTTP_200_OK)
