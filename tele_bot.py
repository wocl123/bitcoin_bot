from setuptools import Command
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import coin_def
from apscheduler.schedulers.blocking import BlockingScheduler
import logging

logging.basicConfig(format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

sched = BlockingScheduler()
old_titles = []
old_contents = []
my_token = "토큰"
bot = telegram.Bot(token = my_token)
############################ 봇 기초 함수 #########################################
def start(update, context):
    text = f"===============================\n"
    text += f"🎈  비트코인 챗봇에 오신것을 환영합니다  🎈\n"
    text += f"해당 챗봇은 사용자의 명령어에 따라 정보를 제공합니다.\n"
    text += f"자세한 설명은 /help 를 입력해주세요."
    context.bot.send_message(chat_id = update.effective_chat.id, text=text)

def help(update, context):
    text = f"🎈 해당 챗봇은 아래와 같은 기능을 제공합니다. 🎈\n"
    text += f"1️⃣ 업비트 가격정보(원화/BTC/USDT) /upbit\n"
    text += f"2️⃣ 빗썸 가격정보(원화/BTC) /bithumb\n"
    text += f"3️⃣ 코인원 가격정보(Main/Growth) /coinone\n"
    text += f"4️⃣ 업비트 코인동향(매도/매수 체결순위) /upbit_trends\n"
    text += f"5️⃣ 업비트 디지털 자산뉴스 /upbit_news\n"
    text += f"6️⃣ 환율정보 /exrate\n"
    text += f"그 외의 수정/건의사항은 wocl123@gmail.com으로 연락바랍니다."
    context.bot.send_message(chat_id = update.effective_chat.id, text=text)
############################ 비트코인 명령어 함수(업비트 가격) #########################################
def upbit(update, context):
    text = f"🗨[업비트 가격정보] 설명서 입니다.\n"
    text += f"⭕원화마켓, BTC마켓, USDT마켓의 코인정보를 제공합니다.\n"
    text += f"⭕현재가격, 전일가격, 김치프리미엄 등등 정보를 제공합니다."
    text += f"⭕명령어는 /upbit_마켓 코인명 입니다.\n"
    text += f"‼[명령어 사용법]‼\n"
    text += f"원화 마켓 : /upbit_krw 코인명\nBTC 마켓 : /upbit_btc 코인명\nUSDT 마켓 : /upbit_usdt 코인명\n"
    context.bot.send_message(chat_id = update.effective_chat.id, text=text)

def upbit_krw(update, context):
    user_text = update.message.text
    name = user_text[10:].strip()
    if name:
        try:
            info = coin_def.Upbit.krw_coin_price(name)
            context.bot.send_message(chat_id = update.effective_chat.id, text=info)
        except:
            context.bot.send_message(chat_id = update.effective_chat.id, text="[ERROR!] 코인명을 제대로 입력해주세요!")
    else:
        context.bot.send_message(chat_id = update.effective_chat.id, text="[ERROR!] 코인명을 입력해주세요")
def upbit_btc(update, context):
    user_text = update.message.text
    name = user_text[10:].strip()
    if name:
        try:
            info = coin_def.Upbit.btc_coin_price(name)
            context.bot.send_message(chat_id = update.effective_chat.id, text=info)
        except:
            context.bot.send_message(chat_id = update.effective_chat.id, text="[ERROR!] 코인명을 제대로 입력해주세요!")
    else:
        context.bot.send_message(chat_id = update.effective_chat.id, text="[ERROR!] 코인명을 입력해주세요")

def upbit_usdt(update, context):
    user_text = update.message.text
    name = user_text[11:].strip()
    if name:
        try:
            info = coin_def.Upbit.usdt_coin_price(name)
            context.bot.send_message(chat_id = update.effective_chat.id, text=info)
        except:
            context.bot.send_message(chat_id = update.effective_chat.id, text="[ERROR!] 코인명을 제대로 입력해주세요!")
    else:
        context.bot.send_message(chat_id = update.effective_chat.id, text="[ERROR!] 코인명을 입력해주세요!")
############################ 비트코인 명령어 함수(업비트 코인동향) #########################################
def upbit_trends(update, context):
    text = f"🗨[업비트 코인동향] 설명서입니다.\n"
    text += f"업비트 입출금현황, 주간상승률, 일 매수/매도 체결순위를 제공합니다.\n"
    text += f"‼[명령어 사용법]‼\n"
    text += f"1️⃣ 입출금현황 : /deposit\n"
    text += f"2️⃣ 주간 상승률 : /weekly_up\n"
    text += f"3️⃣ 일 매수 체결순위(krw/btc) /days_buy\n"
    text += f"4️⃣ 일 매도 체결순위(krw/btc) /days_sell\n"
    context.bot.send_message(chat_id = update.effective_chat.id, text=text)

def weekly_up(update, context):
    week = coin_def.Upbit_Trand()
    week = week.trand_list(5)
    context.bot.send_message(chat_id = update.effective_chat.id, text=week)

def days_buy(update, context):
    day = coin_def.Upbit_Trand()
    days = day.trand_list(1)
    days += day.trand_list(3)
    context.bot.send_message(chat_id = update.effective_chat.id, text=days)

def days_sell(update, context):
    day = coin_def.Upbit_Trand()
    days = day.trand_list(2)
    days += day.trand_list(4)
    context.bot.send_message(chat_id = update.effective_chat.id, text=days)
############################ 비트코인 명령어 함수(업비트 입출금현황) #########################################
def deposit(update, context):
    user_text = update.message.text
    coin = user_text[8:].strip().upper()
    if coin:
        a = coin_def.Upbit_Trand()
        context.bot.send_message(chat_id = update.effective_chat.id, text=a.upbit_deposit(coin))
    else:
        text = f"[입출금 현황] 메뉴입니다.\n"
        text += f"업비트에서 제공하는 입출금 현황을 검색하실 수 있습니다.\n"
        text += f"❓블록상태 정보❓\n"
        text += f"⭕normal : 정상\n⭕delayed : 지연\n⭕inactive : 비활성\n⭕??? : 대기중\n"
        text += f"‼[명령어 사용법]‼\n"
        text += f"사용자 입력 : /deposit 코인심볼\n ex) /deposit btc\n"
        context.bot.send_message(chat_id = update.effective_chat.id, text = text)
############################ 비트코인 명령어 함수(업비트 코인동향뉴스) #########################################
def upbit_news(update, context):
    text = f"🗨[업비트 자산뉴스] 설명서입니다.\n"
    text += f"최대 10개의 최신 뉴스리스트를 제공합니다.\n"
    text += f"‼[명령어 사용법]‼\n"
    text += f"1️⃣일반 뉴스 : /general 갯수(최대10)\n"
    text += f"2️⃣규제/정책 뉴스 : /policy 갯수(최대10)\n"
    text += f"3️⃣산업/테크 뉴스 : /tech 갯수(최대10)\n"
    text += f"4️⃣칼럼/인터뷰 뉴스 : /column 갯수(최대10)\n"
    text += f"ex) /general 5"
    context.bot.send_message(chat_id = update.effective_chat.id, text=text)
def general(update, context):
    user_text = update.message.text
    count = user_text[8:]
    try:
        co_def = coin_def.Upbit_News()
        result = co_def.get_news(1, int(count))
        context.bot.send_message(chat_id = update.effective_chat.id, text=result)
    except:
        context.bot.send_message(chat_id = update.effective_chat.id, text="[ERROR!]갯수를 정확하게 입력해주세요(범위 : 1~10)")
def policy(update, context):
    user_text = update.message.text
    count = user_text[7:]
    try:
        co_def = coin_def.Upbit_News()
        result = co_def.get_news(2, int(count))
        context.bot.send_message(chat_id = update.effective_chat.id, text=result)
    except:
        context.bot.send_message(chat_id = update.effective_chat.id, text="[ERROR!]갯수를 정확하게 입력해주세요(범위 : 1~10)")
def tech(update, context):
    user_text = update.message.text
    count = user_text[6:]
    try:
        co_def = coin_def.Upbit_News()
        result = co_def.get_news(3, int(count))
        context.bot.send_message(chat_id = update.effective_chat.id, text=result)
    except:
        context.bot.send_message(chat_id = update.effective_chat.id, text="[ERROR!]갯수를 정확하게 입력해주세요(범위 : 1~10)")
def column(update, context):
    user_text = update.message.text
    count = user_text[7:]
    try:
        co_def = coin_def.Upbit_News()
        result = co_def.get_news(3, int(count))
        context.bot.send_message(chat_id = update.effective_chat.id, text=result)
    except:
        context.bot.send_message(chat_id = update.effective_chat.id, text="[ERROR!]갯수를 정확하게 입력해주세요(범위 : 1~10)")
############################ 비트코인 명령어 함수(빗썸) #########################################
def bithumb(update, context):
    text = f"🗨[빗썸 가격정보] 설명서 입니다.\n"
    text += f"⭕원화마켓, BTC마켓의 코인정보를 제공합니다.\n"
    text += f"⭕현재가격, 전일가격, 김치프리미엄 등등 정보를 제공합니다."
    text += f"⭕명령어는 /bithumb_마켓 코인명 입니다.\n"
    text += f"‼[명령어 사용법]‼\n"
    text += f"원화 마켓 : /bithumb_krw 코인명\nBTC 마켓 : /bithumb_btc 코인명\n"
    context.bot.send_message(chat_id = update.effective_chat.id, text=text)

def bithumb_krw(update, context):
    user_text = update.message.text
    name = user_text[12:].strip()
    if name:
        try:
            info = coin_def.Bithumb.get_krw_coin_price(name)
            context.bot.send_message(chat_id = update.effective_chat.id, text=info)
        except:
            context.bot.send_message(chat_id = update.effective_chat.id, text="[ERROR!] 코인명을 제대로 입력해주세요!")
    else:
        context.bot.send_message(chat_id = update.effective_chat.id, text="[ERROR!] 코인명을 입력해주세요!")

def bithumb_btc(update, context):
    user_text = update.message.text
    name = user_text[12:].strip()
    if name:
        try:
            info = coin_def.Bithumb.get_btc_coin_price(name)
            context.bot.send_message(chat_id = update.effective_chat.id, text=info)
        except:
            context.bot.send_message(chat_id = update.effective_chat.id, text="[ERROR!] 코인명을 제대로 입력해주세요!")
    else:
        context.bot.send_message(chat_id = update.effective_chat.id, text="[ERROR!] 코인명을 입력해주세요!")
############################ 비트코인 명령어 함수(코인원) #########################################
def coinone(update, context):
    text = f"🗨[코인원 가격정보] 설명서 입니다.\n"
    text += f"⭕Main마켓, Growth마켓의 코인정보를 제공합니다.\n"
    text += f"⭕현재가격, 전일가격, 김치프리미엄 등등 정보를 제공합니다."
    text += f"⭕명령어는 /coinone 코인명 입니다.\n"
    text += f"‼[명령어 사용법]‼\n"
    text += f"마켓 통합검색 : /coin 코인명\n"
    context.bot.send_message(chat_id = update.effective_chat.id, text=text)    

def coin(update, context):
    user_text = update.message.text
    name = user_text[6:].strip()
    if name:
        try:
            info = coin_def.Coinone.get_coin_price(name)
            context.bot.send_message(chat_id = update.effective_chat.id, text=info)
        except:
            context.bot.send_message(chat_id = update.effective_chat.id, text="[ERROR!] 코인명을 제대로 입력해주세요!")
    else: 
        context.bot.send_message(chat_id = update.effective_chat.id, text="[ERROR!] 코인명을 입력해주세요!")
############################ 환율정보 #########################################
def exrate(update, context):
    text = f"🗨[환율 정보] 설명서입니다.\n"
    text += f"⭕환율은 달러, 엔, 유로, 위안의 정보를 제공합니다.\n"
    text += f"⭕해당 수치는 네이버 증권에서 받아옵니다.\n"
    text += f"‼[명령어 사용법]‼\n"
    text += f"달러 환율 : /exrate_usd\n엔화 환율 : /exrate_jpy\n유로 환율 : /exrate_eur\n위안화 환율 : /exrate_cny\n"
    context.bot.send_message(chat_id = update.effective_chat.id, text=text)
def exrate_usd(update, context):
    usd = coin_def.Rate_Krw.dollar_rate()
    hour = coin_def.real_time(0)
    min = coin_def.real_time(1)
    sec = coin_def.real_time(2)
    text = f"🗨[달러 환율] 정보입니다.\n"
    text += f"⭕검색 결과 : {usd}원\n"
    text += f"⭕검색 시간 : {hour}시 {min}분 {sec}초"
    context.bot.send_message(chat_id = update.effective_chat.id, text=text)
def exrate_jpy(update, context):
    jpy = coin_def.Rate_Krw.jpy_rate()
    hour = coin_def.real_time(0)
    min = coin_def.real_time(1)
    sec = coin_def.real_time(2)
    text = f"🗨[엔화 환율] 정보입니다.\n"
    text += f"⭕검색 결과 : {jpy}원\n"
    text += f"⭕검색 시간 : {hour}시 {min}분 {sec}초"
    context.bot.send_message(chat_id = update.effective_chat.id, text=text)    
def exrate_eur(update, context):
    eur = coin_def.Rate_Krw.eur_rate()
    hour = coin_def.real_time(0)
    min = coin_def.real_time(1)
    sec = coin_def.real_time(2)
    text = f"🗨[유로 환율] 정보입니다.\n"
    text += f"⭕검색 결과 : {eur}원\n"
    text += f"⭕검색 시간 : {hour}시 {min}분 {sec}초"
    context.bot.send_message(chat_id = update.effective_chat.id, text=text)
def exrate_cny(update, context):
    cny = coin_def.Rate_Krw.cny_rate()
    hour = coin_def.real_time(0)
    min = coin_def.real_time(1)
    sec = coin_def.real_time(2)
    text = f"🗨[위안화 환율] 정보입니다.\n"
    text += f"⭕검색 결과 : {cny}원\n"
    text += f"⭕검색 시간 : {hour}시 {min}분 {sec}초"
    context.bot.send_message(chat_id = update.effective_chat.id, text=text)
############################ 오류 발생 시 호출되는 함수 #########################################
def error(update, context):
    print(f'Update {update} caused error {context.error}')

def unknown(update, context):
    context.bot.send_message(chat_id = update.effective_chat.id, text="죄송하지만 그 명령어를 이해할 수 없습니다.")

def main():
    updater = Updater(my_token)
    dp = updater.dispatcher
    print("Bot start")

    updater.start_polling()
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('help', help))
    dp.add_handler(CommandHandler('upbit', upbit))
    dp.add_handler(CommandHandler('upbit_krw', upbit_krw))
    dp.add_handler(CommandHandler('upbit_btc', upbit_btc))
    dp.add_handler(CommandHandler('upbit_usdt', upbit_usdt))
    dp.add_handler(CommandHandler('upbit_trends', upbit_trends))
    dp.add_handler(CommandHandler('weekly_up', weekly_up))
    dp.add_handler(CommandHandler('days_buy', days_buy))
    dp.add_handler(CommandHandler('days_sell', days_sell))
    dp.add_handler(CommandHandler('upbit_news', upbit_news))
    dp.add_handler(CommandHandler('general', general))
    dp.add_handler(CommandHandler('policy', policy))
    dp.add_handler(CommandHandler('tech', tech))
    dp.add_handler(CommandHandler('column', column))
    dp.add_handler(CommandHandler('bithumb', bithumb))
    dp.add_handler(CommandHandler('bithumb_krw', bithumb_krw))
    dp.add_handler(CommandHandler('bithumb_btc', bithumb_btc))
    dp.add_handler(CommandHandler('coinone', coinone))
    dp.add_handler(CommandHandler('coin', coin))
    dp.add_handler(CommandHandler('exrate', exrate))
    dp.add_handler(CommandHandler('exrate_usd', exrate_usd))
    dp.add_handler(CommandHandler('exrate_jpy', exrate_jpy))
    dp.add_handler(CommandHandler('exrate_eur', exrate_eur))
    dp.add_handler(CommandHandler('exrate_cny', exrate_cny))
    dp.add_handler(CommandHandler('deposit', deposit))
    dp.add_handler(MessageHandler(Filters.command, unknown))
    dp.add_error_handler(error)
    updater.idle()
    updater.stop()
    

if __name__ == '__main__':
    main()
    