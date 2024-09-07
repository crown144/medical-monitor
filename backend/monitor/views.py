from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import MedicalService
from .serializers import MedicalServiceSerializer
# Create your views here.

class testView(APIView):
    def get(self, request):
        return Response("Hello World")
    def post(self, request):
        data = request.data.get("data")
        return Response(data)

class queryView(APIView):
    def post(self, request):
        data = request.data.get("收费明细")
        return Response(data)
    def get(self, request):
        # 查询数据库model
        listTest = MedicalService.objects.filter(local_service_name="椎间盘造影")
        # 序列化
        serializer = MedicalServiceSerializer(listTest, many=True)
        # 返回json数据
        return Response(serializer.data)