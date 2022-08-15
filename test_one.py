import telegram

# подключение к боту
bot = telegram.Bot(token='5504212810:AAETMdBz7GHwrLXYmlt4lE03omb_080YifY')
chat_id = bot.getUpdates()[-1]['message']['chat']['id']

bot.sendMessage(text='Hi', chat_id=chat_id)

#%%
