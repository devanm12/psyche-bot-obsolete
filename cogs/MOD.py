import discord
from discord import Member
from discord.ext import commands
from pymongo import MongoClient
from datetime import datetime

mongo_url="" #MONGO TOKEN GOES HERE
cluster= MongoClient(mongo_url)
db=cluster["discord"]
snipelistlimit=5

class MOD(commands.Cog):

    def __init__(self, client):
        self.client= client

    @commands.command()
    async def snipe(self, ctx):
        collection=db["deletesnipe"]
        result=collection.find_one({"_id":ctx.channel.id})
        if not result:
            await ctx.send("No messages were deleted :D")
        else:
            auth= self.client.get_user(result.get("name"))
            embed = discord.Embed(title=auth.name+"#"+auth.discriminator, color=self.client.colour1, description=result.get("contents"), timestamp=result.get("time"))
            embed.set_thumbnail(url=auth.avatar_url)
            await ctx.send(embed=embed)

    @commands.command(aliases=['editsnipe'])
    async def esnipe(self, ctx):
        collection=db["editsnipe"]
        result=collection.find_one({"_id":ctx.channel.id})
        if not result:
            await ctx.send("No messages were edited :D")
        else:
            auth= self.client.get_user(result.get("name"))
            descript=""
            if len(result.get("oldcontents"))>1023 or len(result.get("newcontents"))>1023:
                descript="Long message, eh? Gotta show it in 2 parts then :("
            embed = discord.Embed(title=auth.name+"#"+auth.discriminator, color=self.client.colour1, description=descript, timestamp=result.get("time"))
            if len(result.get("oldcontents"))>1023:
                embed.add_field(name="Old Message (Part I)", value=result.get("oldcontents")[0:1023]+"-", inline=False)
                embed.add_field(name="Old Message (Part II)", value=result.get("oldcontents")[1023:], inline=False)
            else:
                embed.add_field(name="Old Message", value=result.get("oldcontents"), inline=False)
            if len(result.get("newcontents"))>1023:
                embed.add_field(name="New Message (Part I)", value=result.get("newcontents")[0:1023]+"-", inline=False)
                embed.add_field(name="New Message (Part II)", value=result.get("newcontents")[1023:], inline=False)
            else:
                embed.add_field(name="New Message", value=result.get("newcontents"), inline=False)
            embed.set_thumbnail(url=auth.avatar_url)
            await ctx.send(embed=embed)

    @commands.command()
    async def snipelist(self,ctx):
        collection=db["deletesnipelist"]
        result=collection.find_one({"_id":ctx.channel.id})
        if not result:
            await ctx.send("No messages were deleted :D")
        else:
            index=result.get("index")
            embed = discord.Embed(title="Snipe List", color=self.client.colour1)
            for i in range(snipelistlimit-1,index-1,-1):
                auth=result.get("name")
                auth=self.client.get_user(auth[i])
                time_then=result.get("time")
                delta_time = datetime.utcnow() - time_then[i]
                hours, remainder = divmod(int(delta_time.total_seconds()), 3600)
                minutes, seconds = divmod(remainder, 60)
                days, hours = divmod(hours, 24)
                time_now=""
                if minutes==0:
                    time_now = f" [{seconds}s ago]"
                elif hours==0:
                    time_now = f" [{minutes}m {seconds}s ago]"
                elif days==0:
                    time_now = f" [{hours}h {minutes}m {seconds}s ago]"
                else:
                    time_now = f" [{days}d {hours}h {minutes}m {seconds}s ago]"
                embed.add_field(name=auth.name+"#"+auth.discriminator+time_now, value=result.get("contents")[i][0:1023], inline=False)
            await ctx.send(embed=embed)

    @commands.command()
    async def clear(self, ctx, var: int):
        await ctx.channel.purge(limit=var+1)
        await ctx.send(content=f'Cleared {var} messages', delete_after=3.0)

def setup(client):
    client.add_cog(MOD(client))
