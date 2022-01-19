# from ast import Index
import re
# from numpy.lib.shape_base import column_stack
# import ccxt
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import json
import time
import datetime
import urllib.request as req

# 환율 (네이버 증권)
class Rate_Krw:
    def dollar_rate():
        url = "https://finance.naver.com/marketindex/"
        result = requests.get(url)
        bs_obj = BeautifulSoup(result.text, "html.parser")

        d_price = bs_obj.findAll("span", {"class": "value"})
        d_price = float(d_price[0].string.replace(",", ""))
        # 1$ = price
        return d_price

    def jpy_rate():
        url = "https://finance.naver.com/marketindex/"
        result = requests.get(url)
        bs_obj = BeautifulSoup(result.text, "html.parser")

        j_price = bs_obj.findAll("span", {"class": "value"})
        j_price = float(j_price[1].string.replace(",", ""))

        return j_price

    def eur_rate():
        url = "https://finance.naver.com/marketindex/"
        result = requests.get(url)
        bs_obj = BeautifulSoup(result.text, "html.parser")

        e_price = bs_obj.findAll("span", {"class": "value"})
        e_price = float(e_price[2].string.replace(",", ""))

        return e_price

    def cny_rate():
        url = "https://finance.naver.com/marketindex/"
        result = requests.get(url)
        bs_obj = BeautifulSoup(result.text, "html.parser")

        c_price = bs_obj.findAll("span", {"class": "value"})
        c_price = float(c_price[3].string.replace(",", ""))

        return c_price

# 업비트 가격
class Upbit:
    # 코인 정보(이름)이 담겨있는 곳 크롤링하는 함수  
    def get_coin_code():
        url = "https://api.upbit.com/v1/market/all"
        result = req.urlopen(url)
        json_obj = json.load(result)

        return json_obj
    # KRW 로 명시되어 있는 코인의 정보
    def krw_upbit_name():
        KRW_coin_name = {}
        json_obj = Upbit.get_coin_code()
        for i in json_obj:
            if i['market'][:3] == "KRW":
                KRW_coin_name[i['korean_name']] = i['market']    
        return KRW_coin_name
    # BTC 로 명시되어 있는 코인의 정보
    def btc_upbit_name():
        BTC_coin_name = {}
        json_obj = Upbit.get_coin_code()

        for i in json_obj:
            if i['market'][:3] == "BTC":
                BTC_coin_name[i['korean_name']] = i['market']
        return BTC_coin_name
    # USDT 로 명시되어 있는 코인의 정보
    def usdt_upbit_name():
        USDT_coin_name = {}
        json_obj = Upbit.get_coin_code()

        for i in json_obj:
            if i['market'][:4] == "USDT":
                USDT_coin_name[i['korean_name']] = i['market']
        return USDT_coin_name
    # 원화시장 검색
    def krw_coin_price(coin_name):
        coin_info = Upbit.krw_upbit_name()
        url = "https://api.upbit.com/v1/ticker?markets="
        for key, value in coin_info.items():
            if coin_name == key:
                krw_url = url + value
                result = req.urlopen(krw_url)
                json_obj = json.load(result)
                break      
        co_list = []
        try:
            co_list.append("검색하신 "+ coin_name+ " 코인의 결과입니다. (" + str(real_time(0)) + "시 " + str(real_time(1)) + "분 " + str(real_time(2)) + "초)")
            co_list.append("\n코인명 : " + json_obj[0]['market'])
            co_list.append("\n현재가격 : " + str(json_obj[0]['trade_price']) + " (" + str(round(json_obj[0]['signed_change_rate']*100, 2)) + "%)")
            co_list.append("\n당일시가 : " + str(json_obj[0]['opening_price']))
            co_list.append("\n당일고가 : " + str(json_obj[0]['high_price']))
            co_list.append("\n당일저가 : " + str(json_obj[0]['low_price']))
            co_list.append("\n24시간 거래량 : " + str(round(json_obj[0]['acc_trade_volume_24h'], 3)) + str(json_obj[0]['market'][4:]))
            co_list.append("\n24시간 거래대금 : " + str(round(json_obj[0]['acc_trade_price_24h'])) + "KRW")
            return " ".join(co_list)
        except IndexError:
            return "없는 코인입니다."
    # BTC 시장 검색
    def btc_coin_price(coin_name):
        coin_info = Upbit.btc_upbit_name()
        url = "https://api.upbit.com/v1/ticker?markets="
        for key, value in coin_info.items():
            if coin_name == key:
                btc_url = url + value
                result = req.urlopen(btc_url)
                json_obj = json.load(result)
                break
        co_list = []
        try:    
            co_list.append("검색하신 "+ coin_name+ " 코인의 결과입니다. (" + str(real_time(0)) + "시 " + str(real_time(1)) + "분 " + str(real_time(2)) + "초)")
            co_list.append("\n코인명 : " + json_obj[0]['market'])
            co_list.append("\n현재가격 : " + str(format(json_obj[0]['trade_price'], ".8f")) + "(" + str(round(json_obj[0]['signed_change_rate']*100, 2))+ "%)")
            co_list.append("\n당일시가 : " + str(format(json_obj[0]['opening_price'], ".8f")))
            co_list.append("\n당일고가 : " + str(format(json_obj[0]['high_price'], ".8f")))
            co_list.append("\n당일저가 : " + str(format(json_obj[0]['low_price'], ".8f")))
            co_list.append("\n24시간 거래량 : " + str(round(json_obj[0]['acc_trade_volume_24h'], 3)) + json_obj[0]['market'][4:])
            co_list.append("\n24시간 거래대금 : " + str(round(json_obj[0]['acc_trade_price_24h'])) + "BTC")
            return " ".join(co_list)
        except IndexError:
            return "없는 코인입니다."
    # USDT 시장 검색
    def usdt_coin_price(coin_name):
        coin_info = Upbit.usdt_upbit_name()
        url = "https://api.upbit.com/v1/ticker?markets="
        for key, value in coin_info.items():
            if coin_name == key:
                usdt_url = url + value
                result = req.urlopen(usdt_url)
                json_obj = json.load(result)
                break
        co_list = []
        try:
            co_list.append("검색하신 "+ coin_name+ " 코인의 결과입니다. (" + str(real_time(0)) + "시 " + str(real_time(1)) + "분 " + str(real_time(2)) + "초)")
            co_list.append("\n코인명 : " + json_obj[0]['market'])
            co_list.append("\n현재가격 : " + str(json_obj[0]['trade_price']) + "(" + str(round(json_obj[0]['signed_change_rate']*100, 2)) + "%)")
            co_list.append("\n당일시가 : " + str(json_obj[0]['opening_price']))
            co_list.append("\n당일시가 : " + str(json_obj[0]['opening_price']))
            co_list.append("\n당일고가 : " + str(json_obj[0]['high_price']))
            co_list.append("\n당일저가 : " + str(json_obj[0]['low_price']))
            co_list.append("\n24시간 거래량 : " + str(round(json_obj[0]['acc_trade_volume_24h'], 3)) + json_obj[0]['market'][5:])
            co_list.append("\n24시간 거래대금 : " + str(round(json_obj[0]['acc_trade_price_24h'])) + "USDT")
            return " ".join(co_list)
        except IndexError:
            return "없는 코인입니다."

    def Notice(index):
        url = "https://api-manager.upbit.com/api/v1/notices?page=1&per_page=20&thread_name=general"
        result = req.urlopen(url)
        json_obj = json.load(result)

        data = json_obj["data"]["list"]
        today = str(datetime.datetime.now())[:10]
        title_list = []
        title_link = []
        total_list = []
        notice_url = "https://upbit.com/service_center/notice?id="
        count= 1
        count2 = 1
        # 최근 공지사항 10개
        if index == 1:
            for i in range(0, 10):
                title_list.append('{}.'.format(count2) + data[i]["title"])
                title_link.append(notice_url + str(data[i]["id"]) + "\n\n")
                count2 += 1
            for i, j in zip(title_list, title_link):
                total_list.append(i + j)
            return " ".join(total_list)
        else:
        # 오늘 날짜로 올라온 공지사항이 있는지 체크
            for i in range(0, 10):
                update_at = data[i]["created_at"][:10]
                if update_at == today:
                    title_list.append('{}.'.format(count) + data[i]["title"] + "\n")
                    title_link.append(notice_url + str(data[i]["id"]) + "\n\n")
                    count += 1
            for i, j in zip(title_list, title_link):
                total_list.append(i + j)
            return " ".join(total_list)
    def deposit_possible():
        url = "https://ccx.upbit.com/api/v1/status/wallet"
        result = req.urlopen(url)
        js_obj = json.load(result)
        coin_name = []
        wallet_state = []
        block_state = []
        block_height = []
        message = []

        for i in js_obj:
            coin_name.append("코인명 : " + i["currency"])
            if i["wallet_state"] == "working":
                wallet_state.append("입출금현황 : 입출금 가능")
            elif i["wallet_state"] == "withdraw_only":
                wallet_state.append("입출금현황 : 출금만 가능")
            elif i["wallet_state"] == "paused":
                wallet_state.append("입출금현황 : 일시중단")
            elif i["wallet_state"] == "unsupported":
                wallet_state.append("입출금현황 : 준비중")
            else:
                wallet_state.append("입출금현황 : 중단")
            block_state.append("블록상태 : " + i["block_state"])
            block_height.append("블록높이 : " + str(i["block_height"]))
            message.append("비고 : " + str(i["message"]))
        
        final_result = []
        for i in zip(coin_name, wallet_state, block_state, block_height, message):
            print(i)    
        
        

class Bithumb:          
    def get_krw_coin_price(coin_name):
        with open('bithumb_krw.json', 'r', encoding="utf8") as f:
            contents = f.read()
            json_data = json.loads(contents)

        for key, value in json_data.items():
            if coin_name == key:
                search_code = value
                break
        try:
            url = "https://api.bithumb.com/public/ticker/{}_KRW".format(search_code)
            result = req.urlopen(url)
            resultString = result.read().decode('utf-8')
            result = json.loads(resultString)
                #opening_price, closing_price, min_price, max_price
                #units_traded_24H(거래량LTC), acc_trade_value_24H(거래금액KRW)
                #prev_closing_price(전일종가), fluctate_24H(최근 24시간 변동가)
                #fluctate_rate_24H(최근 24시간 변동률)
            data = result["data"]

            url2 = "https://api.bithumb.com/public/orderbook/{}_KRW".format(search_code)
            result2 = req.urlopen(url2)
            resultString2 = result2.read().decode('utf-8')
            result2 = json.loads(resultString2)
            now_price = result2["data"]["bids"][0]["price"] #현재가
            c_code = result2["data"]['order_currency'] #코인코드

            co_list = []
            co_list.append("검색하신 " + coin_name + " 코인의 결과입니다. (" + str(real_time(0)) + "시 " + str(real_time(1)) +"분 " + str(real_time(2))+ "초)")
            co_list.append("\n현재가격 : " + now_price + " ("+data["fluctate_rate_24H"]+"%)")
            co_list.append("\n전일종가 : " + data["prev_closing_price"])
            co_list.append("\n당일시가 : " + data["opening_price"])
            co_list.append("\n당일고가 : " + data["max_price"])
            co_list.append("\n당일저가 : " + data["min_price"])
            co_list.append("\n24시간 거래량 : " + str(format(float(data["units_traded_24H"]), ".3f")) + c_code)
            co_list.append("\n24시간 거래금액 : " + data["acc_trade_value_24H"] + "KRW")
            return " ".join(co_list)
        except IndexError:
            return "없는 코인입니다."
        

    def get_btc_coin_price(coin_name):
        with open('bithumb_btc.json', 'r', encoding="utf8") as f:
            contents = f.read()
            json_data = json.loads(contents)

        for key, value in json_data.items():
            if coin_name == key:
                search_code = value
                break
        try:
            url = "https://api.bithumb.com/public/ticker/{}_BTC".format(search_code)
            result = req.urlopen(url)
            resultString = result.read().decode('utf-8')
            result = json.loads(resultString)
                #opening_price, closing_price, min_price, max_price
                #units_traded_24H(거래량LTC), acc_trade_value_24H(거래금액KRW)
                #prev_closing_price(전일종가), fluctate_24H(최근 24시간 변동가)
                #fluctate_rate_24H(최근 24시간 변동률)
            data = result["data"]

            url2 = "https://api.bithumb.com/public/orderbook/{}_BTC".format(search_code)
            result2 = req.urlopen(url2)
            resultString2 = result2.read().decode('utf-8')
            result2 = json.loads(resultString2)
            now_price = result2["data"]["bids"][0]["price"] #현재가
            c_code = result2["data"]['order_currency'] #코인코드

            co_list = []
            co_list.append("검색하신 " + coin_name + " 코인의 결과입니다. (" + str(real_time(0)) + "시 " + str(real_time(1)) +"분 " + str(real_time(2))+ "초)")
            co_list.append("\n현재가격 : " + now_price + " ("+data["fluctate_rate_24H"]+"%)")
            co_list.append("\n전일종가 : " + data["prev_closing_price"])
            co_list.append("\n당일시가 : " + data["opening_price"])
            co_list.append("\n당일고가 : " + data["max_price"])
            co_list.append("\n당일저가 : " + data["min_price"])
            co_list.append("\n24시간 거래량 : " + str(format(float(data["units_traded_24H"]), ".3f")) + c_code)
            co_list.append("\n24시간 거래금액 : " + data["acc_trade_value_24H"] + "KRW")
            return " ".join(co_list)
        except IndexError:
            return "없는 코인입니다."

class Coinone:
    def get_coin_price(coin_name):
        with open('coinone.json', 'r', encoding="utf8") as f:
            contents = f.read()
            json_data = json.loads(contents)

        for key, value in json_data.items():
            if coin_name == key:
                search_code = value
                break
        try:
            url = "https://api.coinone.co.kr/ticker?currency={}".format(search_code)
            result = req.urlopen(url)
            resultString = result.read().decode('utf-8')
            result = json.loads(resultString)

            co_list = []
            co_list.append("검색하신 " + coin_name + " 코인의 결과입니다. (" + str(real_time(0)) + "시 " + str(real_time(1)) +"분 " + str(real_time(2))+ "초)")
            co_list.append("\n현재가격 : " + result["last"])
            co_list.append("\n당일고가 : " + result["high"])
            co_list.append("\n당일저가 : " + result["low"])
            co_list.append("\n24시간 거래량 : " + result["volume"] + search_code)
            co_list.append("\n24H~48H 중 최고가 : " + result["yesterday_high"])
            co_list.append("\n24H~48H 중 최저가 : " + result["yesterday_low"])
            co_list.append("\n24H~48H 동안 최초가격 : " + result["yesterday_first"])
            co_list.append("\n24H 이전 요청 시 가격 : " + result["yesterday_last"])
            co_list.append("\n24H~48H 동안 완료된 주문의 코인수량 : " + result["yesterday_volume"] + search_code)
            return " ".join(co_list)
        except IndexError:
            return "없는 코인입니다."


class Coinness:
    def crawl():
        url = "https://api.coinness.live/v1/news"
        result = req.urlopen(url)
        json_obj = json.load(result)

        data_id = [] # id값을 받아올 리스트
        data_title = [] # 뉴스기사 제목을 받을 리스트
        data_content = [] # 뉴스 내용을 받을 리스트
        for i in range(0, len(json_obj)):
            data_id.append((str(json_obj[i]["id"]))) #id값을 가져옴
            data_title.append(json_obj[i]["title"]) #title 가져옴
            data_content.append(json_obj[i]["content"]) #content 가져옴

        result = []
        for i in range(0, len(json_obj)):
            result.append(data_id[i] + data_title[i] + data_content[i] + "\n\n")
        
        return " ".join(result)
        
    def get_new_links():
        url = "https://api.coinness.live/v1/news"
        result = req.urlopen(url)
        json_obj = json.load(result)
    
        result = []
        for i in range(0, len(json_obj)):
            result.append({
                "id" : str(json_obj[i]["id"]),
                "title" : json_obj[i]["title"],
                "content" : json_obj[i]["content"]
            })
        
        with open("./coin_news.json", "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=3)
        
        with open("coin_news.json", 'r', encoding="utf8") as f:
            contents = f.read()
            json_data = json.loads(contents)

        print(json_data)


def real_time(index):
    now = time.localtime()
    now_list = [now.tm_hour, now.tm_min, now.tm_sec]
    return now_list[index]

