from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import MedicalService
from .serializers import MedicalServiceSerializer
from .support.promptplus import MedicalServiceManager
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
        conn_details = {
        "host": "localhost",
        "port": 3306,
        "user": "root",
        "password": "1234567890Wyx",
        "database": "medical",
    }
        api_key = 'sk-JpP5E3J1fIIpqfuf82A362E05e724067995b51Df399e035d'
        try:
            manager = MedicalServiceManager(api_key, conn_details)
            service_names = manager.extract_service_names(data)
            print(service_names)
        except:
            service_names = []
        return Response(service_names)
    def get(self, request):
        # 查询数据库model
        listTest = MedicalService.objects.filter(local_service_name="椎间盘造影")
        # 序列化
        serializer = MedicalServiceSerializer(listTest, many=True)
        # 返回json数据
        return Response(serializer.data)