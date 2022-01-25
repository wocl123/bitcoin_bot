from setuptools import Command
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import coin_def
import logging

logging.basicConfig(format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

my_token = "5118411582:AAFKcryheD3jhUoNjsQSC_gLRUpk-x15wso"
############################ 봇 기초 함수 #########################################
def start(update, context):
    text = f"=====================================\n"
    text += f"🎈  비트코인 챗봇에 오신것을 환영합니다  🎈\n"
    text += f"해당 챗봇은 사용자의 명령어에 따라 정보를 제공합니다.\n"
    text += f"자세한 설명은 /help 를 입력해주세요."
    context.bot.send_message(chat_id = update.effective_chat.id, text=text)

def help(update, context):
    text = f"🎈 해당 챗봇은 아래와 같은 기능을 제공합니다. 🎈\n"
    text += f"1️⃣ 업비트 가격정보(원화/BTC/USDT) /upbit\n"
    text += f"2️⃣ 빗썸 가격정보(원화/BTC) /bithumb\n"
    text += f"3️⃣ 코인원 가격정보(Main/Growth) /coinone\n"
    text += f"4️⃣ 코인뉴스 정보(실시간 알림 on/off)\n"
    text += f"❗실시간 알림은 /news_on 을, 필요없다면 /news_off \n"
    text += f"5️⃣ 업비트 코인동향(매도/매수 체결순위) - /upbit_trends\n"
    text += f"6️⃣ 업비트 디지털 자산뉴스(진행중)\n"
    text += f"그 외의 수정/건의사항은 wocl123@gmail.com으로 연락바랍니다."
    context.bot.send_message(chat_id = update.effective_chat.id, text=text)
############################ 비트코인 명령어 함수(업비트 가격) #########################################
def upbit(update, context):
    text = f"업비트 가격정보는 원화마켓, BTC마켓, USDT 마켓을 제공합니다.\n"
    text = f"현재가격, 전일가격, 김치프리미엄 등등 정보를 제공합니다."
    text += f"명령어는 /upbit_마켓 코인명 입니다.\n"
    text += f"ex) /upbit_krw 코인명, /upbit_btc 코인명, /upbit_usdt 코인명\n"
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
    text = f"업비트 입출금현황, 주간상승률, 일 매수/매도 체결순위를 제공합니다.\n"
    text += f"[명령어]\n"
    text += f"1️⃣ 입출금현황 : /deposit\n"
    text += f"2️⃣ 주간 상승률 : /weekly_up\n"
    text += f"3️⃣ 일 매수 체결순위(krw/btc) /days_buy\n"
    text += f"4️⃣ 일 매도 체결순위(krw/btc) /days_sell\n"
    text += f"현재 입출금 현황은 수정중에 있습니다."
    context.bot.send_message(chat_id = update.effective_chat.id, text=text)

def weekly_up(update, context):
    week = coin_def.Upbit_Trand()
    week = week.trand_list(6)
    context.bot.send_message(chat_id = update.effective_chat.id, text=week)

def days_buy(update, context):
    day = coin_def.Upbit_Trand()
    days = day.trand_list(2)
    days += day.trand_list(4)
    context.bot.send_message(chat_id = update.effective_chat.id, text=days)

def days_sell(update, context):
    day = coin_def.Upbit_Trand()
    days = day.trand_list(3)
    days += day.trand_list(5)
    context.bot.send_message(chat_id = update.effective_chat.id, text=days)
############################ 비트코인 명령어 함수(빗썸) #########################################
def bithumb(update, context):
    text = f"빗썸 가격정보는 원화마켓, BTC마켓을 제공합니다.\n"
    text = f"현재가격, 전일가격, 김치프리미엄 등등 정보를 제공합니다."
    text += f"명령어는 /bithumb_마켓 코인명 입니다.\n"
    text += f"ex) /bithumb_krw 코인명, /bithumb_btc 코인명\n"
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
    text = f"코인원 가격정보는 Main, Growth 마켓을 제공합니다.\n"
    text = f"현재가격, 전일가격, 김치프리미엄 등등 정보를 제공합니다."
    text += f"명령어는 /coinone 코인명 입니다.\n"
    text += f"ex) /coin 코인명\n"
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
    dp.add_handler(CommandHandler('bithumb', bithumb))
    dp.add_handler(CommandHandler('bithumb_krw', bithumb_krw))
    dp.add_handler(CommandHandler('bithumb_btc', bithumb_btc))
    dp.add_handler(CommandHandler('coinone', coinone))
    dp.add_handler(CommandHandler('coin', coin))
    dp.add_handler(MessageHandler(Filters.command, unknown))
    dp.add_error_handler(error)
    updater.idle()
    updater.stop()

if __name__ == '__main__':
    main()
    