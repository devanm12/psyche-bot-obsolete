import discord
from discord.ext import commands, tasks
from datetime import datetime
from discord import Member
from aiohttp import ClientSession
from itertools import cycle
from pymongo import MongoClient

status = cycle(['for errors', 'people', 'Master', 'new YouTube videos','for .'])
mongo_url="" #MONGO TOKEN GOES HERE
cluster= MongoClient(mongo_url)
db=cluster["discord"]

class EVENTS(commands.Cog):

    def __init__(self, client):
        self.client= client
    '''
    @commands.Cog.listener()
    async def on_message(self, ctx):
        if not ctx.author.bot:
            if ctx.content.count(":")>1:
                event_invoked=False
                message=ctx.content
                result=""
                while message.count(":") > 1:
                    first = message.find(":")
                    second = message.find(":",first+1)
                    result+=message[:message.find(":")]
                    emoji_name = message[first+1:second]
                    found_emoji=False
                    for emoji in ctx.guild.emojis:
                        if emoji_name==emoji.name:
                            found_emoji=True
                            result+="<a:"+emoji.name+":"+str(emoji.id)+">"
                            event_invoked=True
                            break
                    if not found_emoji:
                        result+=":"+emoji_name
                        message=message[second:]
                    else:
                        message=message[second+1:]
                result+=message
                #await ctx.channel.send(result)
                WEBHOOK_URL=''
                has_hook=False
                webhooks=await ctx.channel.webhooks()
                for web in webhooks:
                    if web.name == 'Psyche':
                        WEBHOOK_URL=web.url
                        has_hook=True
                if not has_hook:
                    hook= await ctx.channel.create_webhook(name="Psyche")
                    WEBHOOK_URL=hook.url
                async with ClientSession() as session:
                    webhook = discord.Webhook.from_url(WEBHOOK_URL, adapter=discord.AsyncWebhookAdapter(session))
                    await webhook.send(content=result, username=ctx.author.display_name, avatar_url=ctx.author.avatar_url)
                    await ctx.delete()
    '''

    @commands.Cog.listener()
    async def on_ready(self):
        self.client.launch_time = datetime.utcnow()
        await self.client.change_presence(status=discord.Status.dnd)
        self.change_status.start()
        print('Psyche#1252\nStatus: Online')

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if not before.author.bot:
            collection=db["editsnipe"] #name means user id for testing
            if not collection.find_one({"id":after.channel.id}):
                collection.delete_one({"_id":after.channel.id})
            post={"_id":before.channel.id, "name": before.author.id, "oldcontents": before.content, "newcontents": after.content, "time": after.edited_at}
            collection.insert_one(post)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if (not message.author.bot) and (not message.attachments) and (message.content!=''):
            collection1=db["deletesnipe"] #name means user id for testing
            if not collection1.find_one({"id":message.channel.id}):
                collection1.delete_one({"_id":message.channel.id})
            post1={"_id":message.channel.id, "name": message.author.id, "contents": message.content, "time": datetime.utcnow()}
            collection1.insert_one(post1)
            collection2=db["deletesnipelist"]
            if collection2.find_one({"_id":message.channel.id}):
                collection2.update_one({"_id":message.channel.id},{"$pop":{"name":-1}})
                collection2.update_one({"_id":message.channel.id},{"$pop":{"contents":-1}})
                collection2.update_one({"_id":message.channel.id},{"$pop":{"time":-1}})
                if not collection2.find_one({"_id":message.channel.id}).get("index") == 0:
                    collection2.update_one({"_id":message.channel.id},{"$inc":{"index":-1}})
                collection2.update_one({"_id":message.channel.id},{"$push":{"name":message.author.id}})
                collection2.update_one({"_id":message.channel.id},{"$push":{"contents":message.content}})
                collection2.update_one({"_id":message.channel.id},{"$push":{"time":datetime.utcnow()}})
            else: #if it doesnt exist
                post2={"_id":message.channel.id, "name": [0,0,0,0,message.author.id], "contents": ["","","","",message.content], "time": [0,0,0,0,datetime.utcnow()],"index": 4}
                collection2.insert_one(post2)

    @tasks.loop(seconds=10)
    async def change_status(self):
        await self.client.change_presence(status=discord.Status.dnd,activity=discord.Activity(type=discord.ActivityType.watching, name=next(status)))

def setup(client):
    client.add_cog(EVENTS(client))
