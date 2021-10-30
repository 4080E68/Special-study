from bs4 import BeautifulSoup
from abc import ABC, abstractmethod
import requests


# 美食抽象類別
class Food(ABC):

    def __init__(self, area):
        self.area = area  # 地區

    @abstractmethod
    def scrape(self):
        pass


# 愛食記爬蟲
class IFoodie(Food):

    def scrape(self):
        response = requests.get(
            "https://ifoodie.tw/explore/" + self.area +
            "/list?sortby=popular&opening=true")

        soup = BeautifulSoup(response.content, "html.parser")

        # 爬取前五筆餐廳卡片資料
        cards = soup.find_all(
            'div', {'class': 'jsx-1776651079 restaurant-info'}, limit=5)

        content = ""
        for card in cards:

            title = card.find(  # 餐廳名稱
                "a", {"class": "jsx-1776651079 title-text"}).getText()

            stars = card.find(  # 餐廳評價
                "div", {"class": "jsx-1207467136 text"}).getText()

            address = card.find(  # 餐廳地址
                "div", {"class": "jsx-1776651079 address-row"}).getText()

            #將取得的餐廳名稱、評價及地址連結一起，並且指派給content變數
            content += f"{title} \n{stars}顆星 \n{address} \n\n"

        return content
