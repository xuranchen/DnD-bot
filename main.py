import discord
from webscraper import get_price
import re
import auth_token

def title_except(s, exceptions):
    word_list = re.split(' ', s)       # re.split behaves as expected
    final = [word_list[0].capitalize()]
    for word in word_list[1:]:
        final.append(word if word in exceptions else word.capitalize())
    return " ".join(final)

exceptions =  ['a', 'an', 'of', 'the', 'is']

client = discord.Client()

@client.event
async def on_ready():
    print("The bot is ready!")
    await client.change_presence(game=discord.Game(name="Making a    bot"))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content[0] == "\\":
        price = get_price(message.content[1:])
        await client.send_message(message.channel, price)

client.run(auth_token.Token)