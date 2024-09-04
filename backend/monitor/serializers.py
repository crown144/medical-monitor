from .models import MedicalService
from rest_framework import serializers

class MedicalServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalService
        fields =('local_service_name', 'project_content')