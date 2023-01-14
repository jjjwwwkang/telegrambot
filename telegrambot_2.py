import telegram
import asyncio
import newscrawiling as nc

old_links = []
contents = nc.extract_links(old_links)


async def main() :
    # 텔레그램 봇 토큰
    my_token = '5909311694:AAEhJcEhFnL7Rw0XLdC-Lb1vnjqDD6angm4'
    chat_id = 93432349
    # 텔레그램 봇 생성
    bot = telegram.Bot(token=my_token)
    await bot.sendMessage(chat_id, text=contents)

asyncio.run(main())





