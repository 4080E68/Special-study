from django.db import models


class Location(models.Model):  # 設計LINE Bot所需要使用的資料表(Table)欄位
    area = models.CharField(max_length=20)  # 地區
    name = models.CharField(max_length=100)  # 景點名稱
    address = models.CharField(max_length=500)  # 地址
# Create your models here.
