# encoding=utf-8
from django.db import models


# Create your models here.
class MedicalService(models.Model):
    local_service_code = models.CharField(
        max_length=255, blank=True, null=False, db_column='地方医疗服务项目代码', primary_key=True
    )
    local_service_name = models.CharField(
        max_length=255, blank=True, null=True, db_column='地方医疗服务项目名称'
    )
    project_content = models.CharField(
        max_length=255, blank=True, null=True, db_column='项目内涵'
    )
    except_content = models.CharField(
        max_length=255, blank=True, null=True, db_column='除外内容'
    )
    pricing_unit = models.CharField(
        max_length=255, blank=True, null=True, db_column='计价单位'
    )
    project_description = models.CharField(
        max_length=255, blank=True, null=True, db_column='项目说明'
    )

    class Meta:
        managed = False
        db_table = 'medical_service'
