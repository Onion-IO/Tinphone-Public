from multiprocessing import context
import discord
import asyncio

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author != client.user:  #ensures bot does not react to it's own messages
        if message.content.startswith('&'):
            if message.channel.type == discord.ChannelType.private:
                await message.channel.send('Which server would you like to find?')


                def pred(msg):
                    return message.author.id == msg.author.id   #makes sure message comes from right person
                try: 
                    msg = await client.wait_for("message", check=pred, timeout=20) #waits for message
                except asyncio.TimeoutError:   #catches timeout error
                    pass 
                else:
                    print(msg.content)
                    user = msg.author 
                    print("found mutual:", discord.utils.get(user.mutual_guilds, name = msg.content)) #checks mutual guilds for guild of name msg.content
                    await message.channel.send('Which channel would you like to speak in?')
                    return

    else:
        return

client.run('')