from selenium import webdriver
import mysql.connector
from linebot.models import *
from linebot import LineBotApi
from config import *
import time
import random
import string
#使用quote進行中文轉碼
from urllib.parse import quote
from web_crawler import *


def youtube_vedio_parser(keyword):
    connection = mysql.connector.connect(host='localhost',
                                         port='3306',
                                         user='root',
                                         password='',
                                         database='1228',)

    cursor = connection.cursor()
    try:

        #建立url跟目錄
        url = 'https://ecshweb.pchome.com.tw/search/v3.3/?q=AMD&scope=all&sortParm=sale&sortOrder=dc&cateId=DRAI'
        #開啟Chrome瀏覽器
        #driver = webdriver.Chrome(options=chromeOption)
        driver = webdriver.Chrome()
        #調整瀏覽器視窗大小
        driver.set_window_size(1024, 960)
        #======================依關鍵字在pchome網站上搜尋===========================
        #進入指定網址
        driver.get(url)
        #定義一個物件，以name標籤找到youtube的關鍵字搜尋欄位
        """search_vedio = driver.find_element_by_id('keyword')
        #將關鍵字文字送入搜尋欄位
        search_vedio.send_keys(keyword)"""
        time.sleep(1)

        #按下輸入搜尋按鈕
    #    search_vedio.send_keys(Keys.RETURN)
        """search_button = driver.find_element_by_id('doSearch')
        search_button.click()"""
        #等待網頁讀取

        time.sleep(2)
        driver.refresh()  # 刷新網頁

        #滾動視窗捲軸，使瀏覽器獲取影片縮圖資訊
        for i in range(130):
            y_position = i*200
            driver.execute_script(f'window.scrollTo(0, {y_position});')
            time.sleep(0.1)
        #======================從網頁獲取前十個商品連結===========================
        #建立影片url列表
        pc_url_list = []
        pc_urls = driver.find_elements_by_css_selector('.prod_img')
        #將每個商品連結放入連結list
        #print(len(pc_urls))
        for url in pc_urls:
            if len(pc_url_list) < 100:
                    pc_url_list.append(url.get_attribute('href'))

        #======================從網頁獲取前十個圖片連結===========================
        #建立圖片列表
        pc_images = []
        pc_images_urls = driver.find_elements_by_css_selector('.prod_img img')

        #將每個圖片放入圖片list
        for image in pc_images_urls:
            if str(type(image.get_attribute('src'))) != "<class 'NoneType'>":
                if len(pc_images) < 100:
                    pc_images.append(image.get_attribute('src'))

       
        #======================從網頁獲取前十個商品標題===========================
        #建立標題列表
        pc_title_list = []
        pc_title_infos = driver.find_elements_by_css_selector('.prod_img img')
        for infos in pc_title_infos:
            if len(pc_title_list) < 100:
                pc_title_list.append(infos.get_attribute('title'))
            #print(infos.get_attribute('title'))
        #===================從網頁獲取前十個發布者商品資訊========================
        #建立頻道資訊列表(圖片)
        pc_channel_infos_image_urls = []
        pc_channel_infos_image_list = driver.find_elements_by_css_selector(
            '.prod_img img')
        for infos in pc_channel_infos_image_list:
            pc_channel_infos_image_urls.append(infos.get_attribute('src'))
            #print(infos.get_attribute('src'))
        #======================從網頁獲取前十個商品資訊===========================
        Commodity_list = []
        Commodity_web = driver.find_elements_by_css_selector(".nick")
        #將價錢放置陣列
        print(len(Commodity_list))
        for price in Commodity_web:
            if len(Commodity_list) < 100:
                Commodity_list.append(price.text)
        #======================從網頁獲取前十個價錢===========================
        price_list = []
        price_web = driver.find_elements_by_css_selector(".price .value")
        #將價錢放置陣列
        print(len(price_list))
        for price in price_web:
            if len(price_list)<100:
                price_list.append(price.text)
        """print("價錢", price_list)
        print("商品資訊", Commodity_list)
        print("圖片連結", pc_images)
        print("商品連結", pc_url_list)"""
        print("商品連結長度", len(pc_url_list))
        print("圖片連結長度", len(pc_images))
        print("商品資訊長度", len(Commodity_list))
        print("價錢長度", len(price_list))
        print("標題長度", len(pc_title_list))


        for i in range(101):
            try:
                sql = 'INSERT INTO `1228test`.`func3api_cpu` (`id`,`name`, `price`, `Commodity`, `url_list`, `pc_images`,`vendor`) VALUES (%s,%s, %s, %s, %s, %s, %s);'
                cursor.execute(
                    sql, (i+100, pc_title_list[i], price_list[i], Commodity_list[i], pc_url_list[i], pc_images[i],"AMD"))
                connection.commit()
            except:
                connection.rollback()
        driver.close()
        #=====================================================================
        message = []
        cursor.close()
        connection.close()

        #回傳搜尋結果的FlexMessage
        message.append(image_carousel('搜尋結果', pc_images, pc_url_list,
                                      pc_title_list, pc_channel_infos_image_urls, Commodity_list))
        return message
    except:
        #print("錯誤")
        """line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text='發生錯誤！'))"""




def image_carousel(alt_text, image_url_list, pc_url_list, title_list, pc_channel_infos_image_urls, Commodity_list):
    contents = dict()
    contents['type'] = 'carousel'
    contents['contents'] = []
    i = 0
    if i < 1:
        bubble = {
            "type": "bubble",
            "size": "giga",
            "body": {
                "type": "box",
                "layout": "vertical",
                "spacing": "md",
                "action": {
                    "type": "uri",
                    "uri": "https://linecorp.com"
                },
                "contents": [
                    {
                        "type": "text",
                        "text": "搜尋結果",
                        "size": "xl",
                        "weight": "bold"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "spacing": "none",
                        "contents": [
                            {
                                "type": "image",
                                "url": pc_images_dict['1'],
                                "aspectRatio": "2:1",
                                "aspectMode": "cover",
                                "gravity": "top",
                                "size": "full",
                                "margin": "none"
                            },
                            {
                                "type": "box",
                                "layout": "baseline",
                                "contents": [
                                    {
                                        "type": "icon",
                                        "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/restaurant_regular_32.png"
                                    },
                                    {
                                        "type": "text",
                                        "text": atitle_from_list['1'],
                                        "weight": "bold",
                                        "margin": "sm",
                                        "flex": 0,
                                        "size": "sm",
                                        "offsetStart": "none",
                                        "offsetEnd": "xxl"
                                    }
                                ],
                                "margin": "lg"
                            },
                            {
                                "type": "separator",
                                "margin": "none",
                                "color": "#000000"
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": gCommodity['1'],
                                        "margin": "none",
                                        "offsetTop": "none",
                                        "size": "xxs",
                                        "wrap": True
                                    },
                                    {
                                        "type": "text",
                                        "text": "價格"+gprice['1'],
                                        "contents": [],
                                        "align": "end",
                                        "weight": "bold",
                                        "color": "#ff4d4d",
                                        "size": "xxl"
                                    },
                                    {
                                        "type": "button",
                                        "action": {
                                            "type": "uri",
                                            "label": "前往購買",
                                            "uri": dict_from_list["1"]
                                        },
                                        "style": "secondary"
                                    }
                                ],
                                "margin": "sm"
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "spacing": "none",
                                "contents": [
                                    {
                                        "type": "separator",
                                        "color": "#000000"
                                    },
                                    {
                                        "type": "image",
                                        "url": pc_images_dict['2'],
                                        "aspectRatio": "2:1",
                                        "aspectMode": "cover",
                                        "gravity": "top",
                                        "size": "full",
                                        "margin": "xl"
                                    },
                                    {
                                        "type": "box",
                                        "layout": "baseline",
                                        "contents": [
                                            {
                                                "type": "icon",
                                                "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/restaurant_regular_32.png"
                                            },
                                            {
                                                "type": "text",
                                                "text": atitle_from_list['2'],
                                                "weight": "bold",
                                                "margin": "sm",
                                                "flex": 0,
                                                "size": "sm",
                                                "offsetStart": "none",
                                                "offsetEnd": "xxl"
                                            }
                                        ],
                                        "margin": "lg"
                                    },
                                    {
                                        "type": "separator",
                                        "margin": "none",
                                        "color": "#000000"
                                    },
                                    {
                                        "type": "box",
                                        "layout": "vertical",
                                        "contents": [
                                            {
                                                "type": "text",
                                                "text": gCommodity['2'],
                                                "margin": "none",
                                                "offsetTop": "none",
                                                "size": "xxs",
                                                "wrap": True
                                            },
                                            {
                                                "type": "text",
                                                "text": "價格"+gprice['2'],
                                                "contents": [],
                                                "align": "end",
                                                "weight": "bold",
                                                "color": "#ff4d4d",
                                                "size": "xxl"
                                            },
                                            {
                                                "type": "button",
                                                "action": {
                                                    "type": "uri",
                                                    "label": "前往購買",
                                                    "uri": dict_from_list["2"]
                                                },
                                                "style": "secondary"
                                            }
                                        ],
                                        "margin": "sm"
                                    },
                                    {
                                        "type": "box",
                                        "layout": "vertical",
                                        "spacing": "none",
                                        "contents": [
                                            {
                                                "type": "separator",
                                                "color": "#000000"
                                            },
                                            {
                                                "type": "image",
                                                "url": pc_images_dict['3'],
                                                "aspectRatio": "2:1",
                                                "aspectMode": "cover",
                                                "gravity": "top",
                                                "size": "full",
                                                "margin": "xl"
                                            },
                                            {
                                                "type": "box",
                                                "layout": "baseline",
                                                "contents": [
                                                    {
                                                        "type": "icon",
                                                        "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/restaurant_regular_32.png"
                                                    },
                                                    {
                                                        "type": "text",
                                                        "text": atitle_from_list['3'],
                                                        "weight": "bold",
                                                        "margin": "sm",
                                                        "flex": 0,
                                                        "size": "sm",
                                                        "offsetStart": "none",
                                                        "offsetEnd": "xxl"
                                                    }
                                                ],
                                                "margin": "lg"
                                            },
                                            {
                                                "type": "separator",
                                                "margin": "none",
                                                "color": "#000000"
                                            },
                                            {
                                                "type": "box",
                                                "layout": "vertical",
                                                "contents": [
                                                    {
                                                        "type": "text",
                                                        "text": gCommodity['3'],
                                                        "margin": "none",
                                                        "offsetTop": "none",
                                                        "size": "xxs",
                                                        "wrap": True
                                                    },
                                                    {
                                                        "type": "text",
                                                        "text": "價格"+gprice['3'],
                                                        "contents": [],
                                                        "align": "end",
                                                        "weight": "bold",
                                                        "color": "#ff4d4d",
                                                        "size": "xxl"
                                                    },
                                                    {
                                                        "type": "button",
                                                        "action": {
                                                            "type": "uri",
                                                            "label": "前往購買",
                                                            "uri": dict_from_list["3"]
                                                        },
                                                        "style": "secondary"
                                                    }
                                                ],
                                                "margin": "sm"
                                            }
                                        ],
                                        "margin": "xl"
                                    },
                                    {
                                        "type": "box",
                                        "layout": "vertical",
                                        "spacing": "none",
                                        "contents": [
                                            {
                                                "type": "separator",
                                                "color": "#000000"
                                            },
                                            {
                                                "type": "image",
                                                "url": pc_images_dict['4'],
                                                "aspectRatio": "2:1",
                                                "aspectMode": "cover",
                                                "gravity": "top",
                                                "size": "full",
                                                "margin": "xl"
                                            },
                                            {
                                                "type": "box",
                                                "layout": "baseline",
                                                "contents": [
                                                    {
                                                        "type": "icon",
                                                        "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/restaurant_regular_32.png"
                                                    },
                                                    {
                                                        "type": "text",
                                                        "text": atitle_from_list['4'],
                                                        "weight": "bold",
                                                        "margin": "sm",
                                                        "flex": 0,
                                                        "size": "sm",
                                                        "offsetStart": "none",
                                                        "offsetEnd": "xxl"
                                                    }
                                                ],
                                                "margin": "lg"
                                            },
                                            {
                                                "type": "separator",
                                                "margin": "none",
                                                "color": "#000000"
                                            },
                                            {
                                                "type": "box",
                                                "layout": "vertical",
                                                "contents": [
                                                    {
                                                        "type": "text",
                                                        "text": gCommodity['4'],
                                                        "margin": "none",
                                                        "offsetTop": "none",
                                                        "size": "xxs",
                                                        "wrap": True
                                                    },
                                                    {
                                                        "type": "text",
                                                        "text": "價格"+gprice['4'],
                                                        "contents": [],
                                                        "align": "end",
                                                        "weight": "bold",
                                                        "color": "#ff4d4d",
                                                        "size": "xxl"
                                                    },
                                                    {
                                                        "type": "button",
                                                        "action": {
                                                            "type": "uri",
                                                            "label": "前往購買",
                                                            "uri": dict_from_list["4"]
                                                        },
                                                        "style": "secondary"
                                                    }
                                                ],
                                                "margin": "sm"
                                            }
                                        ],
                                        "margin": "xl"
                                    },
                                    {
                                        "type": "box",
                                        "layout": "vertical",
                                        "spacing": "none",
                                        "contents": [
                                            {
                                                "type": "separator",
                                                "color": "#000000"
                                            },
                                            {
                                                "type": "image",
                                                "url": pc_images_dict['5'],
                                                "aspectRatio": "2:1",
                                                "aspectMode": "cover",
                                                "gravity": "top",
                                                "size": "full",
                                                "margin": "xl"
                                            },
                                            {
                                                "type": "box",
                                                "layout": "baseline",
                                                "contents": [
                                                    {
                                                        "type": "icon",
                                                        "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/restaurant_regular_32.png"
                                                    },
                                                    {
                                                        "type": "text",
                                                        "text": atitle_from_list['5'],
                                                        "weight": "bold",
                                                        "margin": "sm",
                                                        "flex": 0,
                                                        "size": "sm",
                                                        "offsetStart": "none",
                                                        "offsetEnd": "xxl"
                                                    }
                                                ],
                                                "margin": "lg"
                                            },
                                            {
                                                "type": "separator",
                                                "margin": "none",
                                                "color": "#000000"
                                            },
                                            {
                                                "type": "box",
                                                "layout": "vertical",
                                                "contents": [
                                                    {
                                                        "type": "text",
                                                        "text": gCommodity['5'],
                                                        "margin": "none",
                                                        "offsetTop": "none",
                                                        "size": "xxs",
                                                        "wrap": True
                                                    },
                                                    {
                                                        "type": "text",
                                                        "text": "價格"+gprice['5'],
                                                        "contents": [],
                                                        "align": "end",
                                                        "weight": "bold",
                                                        "color": "#ff4d4d",
                                                        "size": "xxl"
                                                    },
                                                    {
                                                        "type": "button",
                                                        "action": {
                                                            "type": "uri",
                                                            "label": "前往購買",
                                                            "uri": dict_from_list["5"]
                                                        },
                                                        "style": "secondary"
                                                    }
                                                ],
                                                "margin": "sm"
                                            }
                                        ],
                                        "margin": "xl"
                                    }
                                ],
                                "margin": "xl"
                            }
                        ],
                        "margin": "xl"
                    }
                ]
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "button",
                        "style": "primary",
                        "color": "#905c44",
                        "action": {
                            "type": "uri",
                            "label": "前往網頁版",
                            "uri": "https://linecorp.com"
                        }
                    }
                ]
            }
        }
        contents['contents'].append(bubble)
        i += 1
    message = FlexSendMessage(alt_text=alt_text, contents=contents)
    return message

#可於本機中直接執行python web_crawler.py進行單元測試，但必須先將CHANNEL_ACCESS_TOKEN、USERID都在config.py設定好
if __name__ == '__main__':
    from linebot import LineBotApi, WebhookHandler
    from linebot.exceptions import InvalidSignatureError
    from linebot.models import *
    message = youtube_vedio_parser('SSD')
    line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
    line_bot_api.push_message(USERID, message)
