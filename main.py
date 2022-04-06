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

        if message.content == '&Thelp':
            embed=discord.Embed(title="Help", color=0x87c0ac)
            embed.set_author(name="TinPhone")
            embed.add_field(name="-----------", value="-----------", inline=False)
            embed.add_field(name="&Tmsg (DMs only)", value="Begins prompting for anonymous message sending", inline=False)
            embed.add_field(name="&Tadd", value="Provides link to add this bot to your server", inline=False)
            embed.add_field(name="&Thelp", value="Brings up this window", inline=False)
            await message.channel.send(embed=embed)
            return

        if message.content == '&Tadd': #THIS WILL INVITE THE ORIGINAL TINPHONE BOT. If you would like to invite YOUR bot, a link can be found within the discord applications page.
            await message.channel.send('Use this link to add me to your server: https://discord.com/api/oauth2/authorize?client_id=960824698160185364&permissions=274878131200&scope=bot')
            return


        if message.content.startswith('&Tmsg'):
            if message.channel.type == discord.ChannelType.private:
                await message.channel.send('Which server would you like to find?')


                def pred(srv):
                    return message.author.id == srv.author.id   #makes sure message comes from right person
                try: 
                    srv = await client.wait_for("message", check=pred, timeout=20) #waits for message
                except asyncio.TimeoutError:   #catches timeout error
                    pass 
                else:
                    print("looking for: ", srv.content)
                    user = srv.author 
                    print("found mutual:", discord.utils.get(user.mutual_guilds, name = srv.content)) #checks mutual guilds for guild of name msg.content
                    mutualserver = discord.utils.get(user.mutual_guilds, name = srv.content)  #logs mutual guild as 'mutualserver'
                    if mutualserver == None:
                            await message.channel.send("Sorry, I couldn't find that! Please use '&Tmsg' again") #If utils.get returns nothing, returns
                            return
                    await message.channel.send('Which channel would you like to speak in?')
                    


                    def pred(chn):
                        return message.author.id == chn.author.id
                    try: 
                        chn = await client.wait_for("message", check=pred, timeout=20) 
                    except asyncio.TimeoutError:   
                        pass 
                    else:
                        print("looking for: ", chn.content) #Logs reply
                        ServChn = discord.utils.get(mutualserver.text_channels, name=chn.content)  #Finds 'chn.content' in 'mutualserver' and logs as 'ServChn'
                        if ServChn == None:
                            await message.channel.send("Sorry, I couldn't find that! Please use '&Tmsg' again") #If utils.get returns nothing, returns
                            return
                        print("found: ", ServChn)
                        await message.channel.send('What is your message?')



                        def pred(msg):
                            return message.author.id == msg.author.id
                        try: 
                            msg = await client.wait_for("message", check=pred, timeout=20) 
                        except asyncio.TimeoutError:   
                            pass 
                        else:
                            print(msg.content)
                            await ServChn.send(msg.content)
                            await message.channel.send('Message sent!')
                            return


                    return
            else:
                await message.channel.send('Woops! That command has to be used in DMs only.')
    
    else:
        return
#Place your token here:
client.run('')