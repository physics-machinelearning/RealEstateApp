import os
import sys
import requests
from bs4 import BeautifulSoup
import time
import urllib

import django
from django.conf import settings
from dotenv import load_dotenv

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.settings')
django.setup()

from realestate.models import Rentproperty, AddressCoordinate

load_dotenv()

POSTGRES_USER = os.environ['POSTGRES_USER']
POSTGRES_PASSWORD = os.environ['POSTGRES_PASSWORD']
POSTGRES_HOST = os.environ['POSTGRES_HOST']
POSTGRES_DB = os.environ['POSTGRES_DB']
URL = 'http://www.geocoding.jp/api/'

SUUMO_URL_DICT = {
    '中央区': 'https://suumo.jp/chintai/tokyo/sc_chuo/',
    '千代田区': 'https://suumo.jp/chintai/tokyo/sc_chiyoda/',
    '文京区': 'https://suumo.jp/chintai/tokyo/sc_bunkyo/',
    '港区': 'https://suumo.jp/chintai/tokyo/sc_minato/',
    '新宿区': 'https://suumo.jp/chintai/tokyo/sc_shinjuku/',
    '品川区': 'https://suumo.jp/chintai/tokyo/sc_shinagawa/',
    '目黒区': 'https://suumo.jp/chintai/tokyo/sc_meguro/',
    '大田区': 'https://suumo.jp/chintai/tokyo/sc_ota/',
    '世田谷区': 'https://suumo.jp/chintai/tokyo/sc_setagaya/',
    '渋谷区': 'https://suumo.jp/chintai/tokyo/sc_shibuya/',
    '中野区': 'https://suumo.jp/chintai/tokyo/sc_nakano/',
    '杉並区': 'https://suumo.jp/chintai/tokyo/sc_suginami/',
    '練馬区': 'https://suumo.jp/chintai/tokyo/sc_nerima/',
    '板橋区': 'https://suumo.jp/chintai/tokyo/sc_itabashi/',
    '豊島区': 'https://suumo.jp/chintai/tokyo/sc_toshima/',
    '北区': 'https://suumo.jp/chintai/tokyo/sc_kita/',
    '台東区': 'https://suumo.jp/chintai/tokyo/sc_taito/',
    '墨田区': 'https://suumo.jp/chintai/tokyo/sc_sumida/',
    '江東区': 'https://suumo.jp/chintai/tokyo/sc_koto/',
    '荒川区': 'https://suumo.jp/chintai/tokyo/sc_arakawa/',
    '足立区': 'https://suumo.jp/chintai/tokyo/sc_adachi/',
    '葛飾区': 'https://suumo.jp/chintai/tokyo/sc_katsushika/',
    '江戸川区': 'https://suumo.jp/chintai/tokyo/sc_edogawa/',
}


class SuumoParser:
    def __init__(self, url):
        self.url = url
        self.pages_num = self.get_pages()
        self.urls = self.get_urls()

    def get_pages(self):
        result = requests.get(self.url)
        content = result.content
        soup = BeautifulSoup(content)
        body = soup.find("body")
        pages = body.find_all("div", {'class':'pagination pagination_set-nav'})
        pages_text = str(pages)
        pages_split = pages_text.split('</a></li>\n</ol>')
        pages_num = pages_split[0][-3:].replace('>','')
        pages_num = int(pages_num)
        return pages_num

    def get_summary(self, url):
        results = requests.get(url)
        content = results.content

        soup = BeautifulSoup(content)
        summary = soup.find("div", {"id":"js-bukkenList"})
        return summary

    def get_urls(self):
        urls = []
        urls.append(self.url)

        for i in range(self.pages_num-1):
            pg = str(i+2)
            url = self.url + '&pn=' + pg
            urls.append(url)
        return urls

    def insert_db(self, url):
        summary = self.get_summary(url)
        cassetteitems = summary.find_all("div",{'class':'cassetteitem'})

        for cassetteitem in cassetteitems:
            try:
                title = self._get_title(cassetteitem)
                address = self._get_address(cassetteitem)
                latitude, longititude = self._get_coordinate(address)
                age = self._get_age(cassetteitem)
                close_station = self._get_close_station(cassetteitem)
                tables = cassetteitem.find_all('table')
                for table in tables:
                    # date = datetime.now
                    rent = self._get_rent(table)
                    kanrihi = self._get_administration(table)
                    sikikin = self._get_sikikin(table)
                    reikin = self._get_reikin(table)
                    area = self._get_area(table)
                    floor = self._get_floor(table)
                    floor_plan = self._get_floor_plan(table)
                    detail_url = self._get_detail_url(table)
                    url_all = urllib.parse.urljoin(url, detail_url)
                    bath_toilet, auto_lock = self._get_details(url_all)
                    print(url_all)

                    rp = Rentproperty(
                        # date=date,
                        rent=rent,
                        kanrihi=kanrihi,
                        sikikin=sikikin,
                        reikin=reikin,
                        subtitle=title,
                        location=address,
                        latitude=latitude,
                        longititude=longititude,
                        close_station=close_station,
                        floor_plan=floor_plan,
                        area=area,
                        age=age,
                        floor=floor,
                        bath_toilet=bath_toilet,
                        auto_lock=auto_lock,
                        url=url_all
                    )
                    if len(Rentproperty.objects.filter(url=url_all).all()) == 0:
                        rp.save()
                    else:
                        print('This property is already registered')
            except Exception as e:
                print(e)

    def _get_title(self, cassetteitem):
        #マンション名取得
        try:
            subtitle = cassetteitem.find_all("div",{
                'class':'cassetteitem_content-title'})
            subtitle = str(subtitle)
            subtitle = subtitle.replace('[<div class="cassetteitem_content-title">', '')
            subtitle = subtitle.replace('</div>]', '')
        except Exception as err:
            print('_get_title: ', err)
        return subtitle

    def _get_address(self, cassetteitem):
        #住所取得
        try:
            subaddress = cassetteitem.find_all("li",{'class':'cassetteitem_detail-col1'})
            subaddress = str(subaddress)
            subaddress = subaddress.replace('[<li class="cassetteitem_detail-col1">', '')
            subaddress = subaddress.replace('</li>]', '')
            return subaddress
        except Exception as err:
            print('_get_address: ', err)

    def _get_age(self, cassetteitem):
        try:
            col3 = cassetteitem.find("li",{'class':'cassetteitem_detail-col3'})
            col = col3.find('div')
            age = col.find(text=True)
            age = age[1:-1]
        except Exception as err:
            print('_get_age: ', err)
        try:
            age = float(age)
        except Exception as e:
            age = None
        return age
    
    def _get_rent(self, table):
        try:
            rent = table.find("span", {"class":"cassetteitem_price cassetteitem_price--rent"})
            rent = rent.text
            if '万円' in rent:
                rent = str(rent)[:-2]
                rent = float(rent)
            else:
                rent = None
            return rent
        except Exception as err:
            print('_get_rent :', err)

    def _get_administration(self, table):
        try:
            rent = table.find("span", {"class":"cassetteitem_price cassetteitem_price--administration"})
            rent = rent.text
            if '円' in rent:
                rent = str(rent)[:-1]
                rent = float(rent)
                rent /= 10000
            else:
                rent = 0
            return rent
        except Exception as err:
            print('_get_administration: ', err)
    
    def _get_sikikin(self, table):
        try:
            rent = table.find("span", {"class":"cassetteitem_price cassetteitem_price--deposit"})
            rent = rent.text
            if '万円' in rent:
                rent = str(rent)[:-2]
            else:
                rent = 0
            return rent
        except Exception as err:
            print('_get_sikikin: ', err)
    
    def _get_reikin(self, table):
        try:
            rent = table.find("span", {"class":"cassetteitem_price cassetteitem_price--gratuity"})
            rent = rent.text
            if '万円' in rent:
                rent = str(rent)[:-2]
                rent = float(rent)
            else:
                rent = 0
            return rent
        except Exception as err:
            print('_get_reikin: ', err)

    def _get_area(self, table):
        try:
            area = table.find("span", {"class":"cassetteitem_menseki"})
            area = area.text
            if 'm2' in area:
                area = area[:-2]
                area = float(area)
            else:
                area = None
            return area
        except Exception as err:
            print('_get_area: ', err)
    
    def _get_close_station(self, cassetteitem):
        try:
            station_list = cassetteitem.find_all("div", {"class":"cassetteitem_detail-text"})
            station_list_min = []
            for station in station_list:
                station = station.text
                if '歩' in station and '分' in station:
                    start = station.find(' 歩')
                    end = -1
                    station_min = station[start+2:end]
                    station_min = int(station_min)
                    station_list_min.append(station_min)
            
            if len(station_list_min):
                return min(station_list_min)
            else:
                return None
        except Exception as err:
            print('_get_close_sation: ', err)

    def _get_floor_plan(self, table):
        try:
            floor_plan = table.find("span", {"class":"cassetteitem_madori"})
            floor_plan = floor_plan.text
            return floor_plan
        except Exception as err:
            print('_get_floor_plan: ', err)

    def _get_floor(self, table):
        try:
            contents = table.find_all("td")
            floor = contents[2].text
            floor = floor[:-1]
            floor = int(floor)
            return floor
        except Exception as err:
            print('_get_floor :', err)

    def _get_detail_url(self, table):
        try:
            url = table.find("td", {"class":"ui-text--midium ui-text--bold"}).find("a").get("href")
            return url
        except Exception as err:
            print('_get_detail_url: ', err)

    def _get_details(self, detail_url):
        """detail url1を受け取り、「部屋の特徴・設備」の中身を返す"""
        try:
            results = requests.get(detail_url)
            content = results.content

            soup = BeautifulSoup(content, features="html.parser")
            summary = soup.find("div", {"class":"section l-space_small"}).find("li").text
            
            if summary == "":
                return None, None
            else:
                bath_toilet = 'バストイレ別' in summary
                auto_lock = 'オートロック' in summary
                return bath_toilet, auto_lock
        except Exception as err:
            print('_get_details :', err)

    def _get_coordinate(self, address):
        try:
            if len(AddressCoordinate.objects.filter(address=address)):
                instance = AddressCoordinate.objects.get(address=address)
                return instance.latitude, instance.longititude
            else:
                latitude, longititude = _coordinate(address)
                ac = AddressCoordinate(address=address,
                                        latitude=latitude,
                                        longititude=longititude)
                ac.save()
                return latitude, longititude
        except Exception as err:
            print('_get_coordinate: ', err)


def _coordinate(address):
    """
    addressに住所を指定すると緯度経度を返す。

    >>> coordinate('東京都文京区本郷7-3-1')
    ['35.712056', '139.762775']
    """
    payload = {'q': address}
    html = requests.get(URL, params=payload)
    soup = BeautifulSoup(html.content, "html.parser")
    if soup.find('error'):
        raise ValueError(f"Invalid address submitted. {address}")
    latitude = soup.find('lat').string
    longitude = soup.find('lng').string
    time.sleep(1)
    return latitude, longitude


if __name__ == '__main__':
    for city_url in SUUMO_URL_DICT.values():
        try:
            sp = SuumoParser(city_url)
            urls = sp.get_urls()
            for url in urls[:2]:
                sp.insert_db(url)
        except Exception as err:
            print(err)