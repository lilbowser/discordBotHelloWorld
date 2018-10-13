import discord
import asyncio
import yaml


with open('secrets.yaml') as secret_info:
    discord_secrets = yaml.load(secret_info)['discord']

client = discord.Client()
owner = None


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    global owner
    owner = await client.get_user_info(discord_secrets['owner_userid'])


@client.event
async def on_message(message):
    if message.content.startswith('!test'):
        counter = 0
        tmp = await client.send_message(message.channel, 'Calculating messages...')
        async for log in client.logs_from(message.channel, limit=100):
            if log.author == message.author:
                counter += 1

        await client.edit_message(tmp, 'You have {} messages.'.format(counter))
    elif message.content.startswith('!sleep'):
        await asyncio.sleep(5)
        await client.send_message(message.channel, 'Done sleeping')
    else:
        if message.author != client.user and message.channel.name == 'mike_time' and message.author != owner and message.author.bot is False:
            ###MENTION MODE###
            tmp = await client.send_message(message.channel, "<@!{}>".format(discord_secrets['owner_userid']))
            await asyncio.sleep(0.5)
            await client.delete_message(tmp)
            # ###DM MODE###
            # #
            # # tmp = await client.send_message(message.channel, "<@!{}>".format(discord_secrets['owner_userid']))
            #
            # tmp = await client.send_message(owner,
            #                                 '{message_content}\n https://discordapp.com/channels/{server_id}/{channel_id}/{message_id}'.format(
            #                                     message_content=message.content, server_id=message.server.id, channel_id=message.channel.id, message_id=message.id))
            # print("Name: {}, id: {}".format(message.author, message.author.id))
            # # await tmp.
            # # await asyncio.sleep(3)
            # # await client.delete_message(tmp)


client.run(discord_secrets['discord_token'])