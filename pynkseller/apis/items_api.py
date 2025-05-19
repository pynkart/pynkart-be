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


# Pynkart imports --
from pynkseller.pagination import (
    LimitOffsetPagination, get_paginated_response
)
from pynkseller.models import (
    Items
)
from pynkseller.services import (
    item_create
)
from pynkauth.models import User


# Item Models APIs --
class ItemsListApi(APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 10
        
    class OutputSerializer(serializers.ModelSerializer):
        class Meta():
            model = Items
            fields = "__all__"
        
    def get(self, request) -> Response:
        item_list = Items.objects.filter().all()
        
        paginated_response = get_paginated_response(
            pagination_class=self.Pagination,
            serializer_class=self.OutputSerializer,
            queryset=item_list,
            request=request,
            view=self
        )
        
        return paginated_response


class UserItemsListApi(APIView):
    def get(self, request: Request, username) -> Response:
        user = User.objects.get(username=username)
        if not user:
            return Response(status=status.HTTP_404_NOT_FOUND)
            
        item_list = Items.objects.filter(UserID=user).all()
        
        paginated_response = get_paginated_response(
            pagination_class=ItemsListApi.Pagination,
            serializer_class=ItemsListApi.OutputSerializer,
            queryset=item_list,
            request=request,
            view=self
        )
        
        return paginated_response


class ItemsGetApi(APIView):
    class OutputSerializer(serializers.ModelSerializer):
        class Meta():
            model = Items
            fields = ["ItemCode", "ItemName"]
            
    def get(self, request: Request, item_code):
        try:
            # item_code = request.data.get("item_code")
            item =  get_object_or_404(Items, ItemCode=item_code)
            
            if item is None:
                return Response(status=status.HTTP_204_NO_CONTENT)
            
            data = self.OutputSerializer(item).data
            return Response(data=data, status=status.HTTP_200_OK)
        
        except Http404:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        
class ItemsCreateApi(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    
    class InputSerializer(serializers.Serializer):
        name = serializers.CharField()
        description = serializers.CharField()
        image_url = serializers.CharField(required=False)
    
    def post(self, request: Request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        item = item_create(**serializer.validated_data, user=request.user)
        data = ItemsGetApi.OutputSerializer(item).data
        
        return Response(data=data,status=status.HTTP_201_CREATED)
        

# class ItemsDelistAPI(APIView):
#     authentication_classes = [SessionAuthentication, BasicAuthentication]
#     permission_classes = [IsAuthenticated]
    
#     class InputSerializer(serializers.Serializer):
#         item_code = serializers.IntegerField()
    
#     def post(self, request: Request):
#         serializers = self.InputSerializer(data=request.data)
#         serializers.is_valid(raise_exception=True)
        
#         item = item_delist(**serializers.validated_data, user=request.user)
#         if item:
#             return Response(status=status.HTTP_202_ACCEPTED)
#         else:
#             return Response(status=status.HTTP_400_BAD_REQUEST)
        
        
# class ItemsUpdateAPI(APIView):
#     authentication_classes = [SessionAuthentication, BasicAuthentication]
#     permission_classes = [IsAuthenticated]
    
#     class InputSerializer(serializers.Serializer):
#         item_code = serializers.IntegerField()
#         name = serializers.CharField()
#         description = serializers.CharField()
    
#     def post(self, request: Request):
#         serializers = self.InputSerializer(data=request.data)
#         serializers.is_valid(raise_exception=True)
        
#         item = item_update(**serializers.validated_data, user=request.user)
#         data = ItemsGetApi.OutputSerializer(item).data
#         return Response(data=data, status=status.HTTP_202_ACCEPTED)
