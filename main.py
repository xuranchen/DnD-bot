import discord
import re
import auth_token

client = discord.Client()

@client.event
async def on_ready():
    print("The bot is ready!")
    #await client.change_presence(game=discord.Game(name="Making a bot"))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content[0] == "\\roll":
        if 'd' in message.content.lower():
            
        await message.channel.send('received')

client.run(auth_token.Token)
