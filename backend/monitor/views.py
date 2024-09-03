from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
# Create your views here.

class testView(APIView):
    def get(self, request):
        return Response("Hello World")
    def post(self, request):
        data = request.data.get("data")
        return Response(data)