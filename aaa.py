import telegram

import asyncio
 
 
my_token = "6539259446:AAEr3Ck-9o92x4GQHiZIGQM-RSwSq9RmKsI"
chat_id = 5467498555
bot = telegram.Bot(token=my_token)
 
 
async def send_message(text):
    await bot.sendMessage(chat_id=chat_id, text=text)
 
 
asyncio.run(send_message('python-telegram-bot sendmessage test'))