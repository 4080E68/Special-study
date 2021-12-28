from django.db import models


class display(models.Model):  # 設計LINE Bot所需要使用的資料表(Table)欄位
    vendor = models.CharField(max_length=100, default="")  # 名稱
    name = models.CharField(max_length=100, default="")  # 名稱
    price = models.IntegerField(max_length=500, default="")  # 價格
    commodity = models.CharField(max_length=3000, default="")  # 詳細資訊
    url_list = models.CharField(max_length=3000, default="")  # 商品連結
    pc_images = models.CharField(max_length=3000, default="")  # 圖片網址


class cpu(models.Model):  # 設計LINE Bot所需要使用的資料表(Table)欄位
    vendor = models.CharField(max_length=100, default="")  # 名稱
    name = models.CharField(max_length=100, default="")  # 名稱
    price = models.IntegerField(max_length=500, default="")  # 價格
    commodity = models.CharField(max_length=3000, default="")
    url_list = models.CharField(max_length=3000, default="")  # 商品連結
    pc_images = models.CharField(max_length=3000, default="")  # 圖片網址


class ssd(models.Model):  # 設計LINE Bot所需要使用的資料表(Table)欄位
    vendor = models.CharField(max_length=100, default="")  # 名稱
    name = models.CharField(max_length=100, default="")  # 名稱
    price = models.IntegerField(max_length=500, default="")  # 價格
    commodity = models.CharField(max_length=3000, default="")
    url_list = models.CharField(max_length=3000, default="")  # 商品連結
    pc_images = models.CharField(max_length=3000, default="")  # 圖片網址
# Create your models here.


