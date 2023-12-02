import discord
from discord import Member
from discord.ext import commands
from datetime import datetime
from itertools import cycle
import time

responses = cycle(['Aah! Let me be alone!','OMG I\'m a bot, I can\'t do anything ;-;','Please, please stop.','*What?*','Uhh!Please, lemme alone...'])

class BOT(commands.Cog):

    def __init__(self, client):
        self.client= client

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'Ping: {round(self.client.latency*1000)}ms')

    @commands.command(aliases=["advancedping"])
    async def aPing(self,ctx):
        start=time.perf_counter()
        message = await ctx.send("Pinging...")
        end=time.perf_counter()
        taken=round((end-start)*1000,3)
        await message.edit(content=f"Bot latency: {taken} ms\nWebsocket Latency: {round(self.client.latency*1000,3)}ms")

    @commands.command()
    async def listservers(self, ctx):
        isAdmin=False
        for admin in self.client.admins:
            if ctx.message.author.id==admin:
                isAdmin=True
                ans='Heyyo Master (◕ω◕✿)```'
                for guild in self.client.guilds:
                    ans+=('\nID: '+str(guild.id)+' || Name: '+str(guild))
                ans+='```'
                await ctx.send(ans)
        if not isAdmin:
            await ctx.send('``I answer to my Masters only.`` UwU')

    @commands.command()
    async def bye(self, ctx,id: int):
        isAdmin=False
        for admin in self.client.admins:
            if ctx.message.author.id==admin:
                isAdmin=True
                for guild in self.client.guilds:
                    if guild.id==id:
                        to_leave = self.client.get_guild(id)
                        await to_leave.leave()
        if not isAdmin:
            await ctx.send('``I answer to my Masters only.`` UwU')

    @commands.command()
    async def invite(self, ctx):
        embed = discord.Embed(title='Hello senpai!',color =self.client.colour1)
        embed.add_field(name='Invite Link',value='Here: [click me](https://discord.com/api/oauth2/authorize?client_id=776380258810200084&permissions=738585600&scope=bot)')
        await ctx.send(embed=embed)

    @commands.command()
    async def uptime(self, ctx):
        delta_uptime = datetime.utcnow() - self.client.launch_time
        hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        await ctx.send(f"{days}d {hours}h {minutes}m")

    @commands.command(aliases=["test"])
    async def hello(self, ctx):
        await ctx.send(next(responses))

    @commands.command(aliases=["abt"])
    async def about(self, ctx):
        await ctx.send("``Psyche`` by Ballard & Porky")

    @commands.command()
    async def say(self, ctx, *, contents):
        message=ctx.message
        await message.delete()
        await ctx.send(contents)

    @commands.command()
    async def help(self, ctx, var=None):
        print("yeah")
        if var=="search":
            embed = discord.Embed(title="Search~", color=self.client.colour1)
            embed.add_field(name="means, dict, dictionary", value="Search the dictionary\n",inline=False)
            embed.add_field(name="urban, ud", value="Search the Urban Dictionary®\n",inline=False)
            embed.add_field(name="image, img", value="A simple image lookup (Bing®)\n",inline=False)
            embed.add_field(name="wikipedia, wiki", value="A simple Wikipedia® lookup\n",inline=False)
            embed.add_field(name="youtube, yt, utube", value="Youtube® search\n",inline=False)
            #embed.add_field(name="reddit, redd", value="Search various subreddits\n",inline=False)
        elif var=="misc":
            embed = discord.Embed(title="Misc~", color=self.client.colour1)
            embed.add_field(name="pokedex, pokemon, dex", value="A simple Pokedex\n",inline=False)
            embed.add_field(name="anime", value="A simple anime lookup\n", inline=False)
        elif var=="utility":
            embed = discord.Embed(title="Utility~", color=self.client.colour1)
            embed.add_field(name="ping", value="Bot ping \n",inline=False)
            embed.add_field(name="whois, userinfo", value="Info on a member\n",inline=False)
            embed.add_field(name="weather, forecast", value="Check the weather\n",inline=False)
            embed.add_field(name="uptime", value="Bot uptime\n",inline=False)
            embed.add_field(name="avatar, av, pfp, dp", value="Display a user's avatar\n",inline=False)
            embed.add_field(name="clear", value="Purge messages (admin)\n",inline=False)
        else:
            embed = discord.Embed(title="Help~", color=self.client.colour1)
            embed.add_field(name="help search", value="Search commands\n",inline=False)
            embed.add_field(name="help utility", value="Utility commands \n",inline=False)
            embed.add_field(name="help misc", value="Miscellaneous commands \n",inline=False)
            embed.add_field(name="help", value="Show this help dialogue \n",inline=False)
            embed.add_field(name="about, abt", value="Info about the bot\n",inline=False)
            embed.set_image(url='https://data.whicdn.com/images/232708748/original.gif')
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(BOT(client))
