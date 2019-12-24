import discord
import re
import auth_token
import random

ERROR_MESSAGE = "roll commands should be in the form of #D# + #"
client = discord.Client()

@client.event
async def on_ready():
    print("The bot is ready!")
    #await client.change_presence(game=discord.Game(name="Making a bot"))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content[:5] == "\\roll":
        msg = message.content[5:]
        if msg.lower().count('d') == 1:
            mult, dice = msg.split('d')
            mod = 0
            try:
                mult = int(mult.strip())

                dice = dice.strip()
                if dice.count('+') == 1:
                    dice, mod = dice.split("+")
                    dice, mod = int(dice), int(mod)
                elif dice.count('+') == 0:
                    dice = int(dice)
                else:
                    print("more than one +")
                    await message.channel.send(ERROR_MESSAGE)
                    return
                if dice == 0 or mult == 0:
                    await message.channel.send(f"no dice to roll...\n{mod}")
                    return
                diceRolls = ""
                sum = mod
                for x in range(mult):
                    diceRoll = random.randint(1, dice)
                    sum += diceRoll
                    diceRolls = diceRolls + str(diceRoll) + ", "
                endMod = f" + {mod}" if mod != 0 else ""
                await message.channel.send(f"rolling {msg.strip()}... \n{sum} ({diceRolls[:-2]}{endMod})")
                return
            except Exception as e:
                print(f"error parsing: {e}")
                await message.channel.send(ERROR_MESSAGE)
                return
        else:
            print("must have exactly 1 D")
            await message.channel.send(ERROR_MESSAGE)
            return

client.run(auth_token.Token)

def test(message):
    return

#test("\\roll 50d10000 + 1")
