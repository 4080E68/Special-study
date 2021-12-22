from django.db import models


class Location(models.Model):  # 設計LINE Bot所需要使用的資料表(Table)欄位
    area = models.CharField(max_length=20)  # 地區
    name = models.CharField(max_length=100)  # 景點名稱
    address = models.CharField(max_length=500)  # 地址


class display(models.Model):  # 設計LINE Bot所需要使用的資料表(Table)欄位
    name = models.CharField(max_length=100)  # 名稱
    price = models.IntegerField(max_length=500)  # 價格
    commodity = models.CharField(max_length=3000)  # 詳細資訊
    url_list = models.CharField(max_length=3000)  # 商品連結
    pc_images = models.CharField(max_length=3000) #圖片網址
# Create your models here.


