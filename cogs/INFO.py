import discord
from discord import Member
from discord.ext import commands
from datetime import datetime
import requests
import pytz

class INFO(commands.Cog):

    def __init__(self, client):
        self.client= client

    @commands.command(aliases=["whois"])
    async def userinfo(self, ctx, member: discord.Member = None):
        if not member:  # if member is not mentioned
            member = ctx.message.author  # set member as the author
        #roles = [role for role in member.roles]
        embed = discord.Embed(color=self.client.colour1, timestamp=ctx.message.created_at, title=f"User Info - {member}")
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text=f"Requested by {ctx.author}")
        embed.add_field(name="ID:", value=member.id)
        embed.add_field(name="Display Name:", value=member.display_name)
        embed.add_field(name="Created Account On:", value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
        embed.add_field(name="Joined Server On:", value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
        embed.add_field(name="Highest Role:", value=member.top_role.mention)
        await ctx.send(embed=embed)

    @commands.command(aliases=['av', 'pfp','dp'])
    async def avatar(self, ctx, member: Member = None):
        if not member:
            member = ctx.author
        embed = discord.Embed(title=member.display_name, description='Here you go, Oni-chan! UwU', color=self.client.colour1)
        embed.set_image(url=member.avatar_url)
        embed.set_footer(icon_url=ctx.author.avatar_url, text=f'Requeested by {ctx.author.name}')
        await ctx.send(embed=embed)

    @commands.command(aliases=["forecast"])
    async def weather(self, ctx, *, var):
            url =f"https://api.weatherapi.com/v1/current.json?key=f5f7f59c74cf4187891153339202111&q={var}"
            response = requests.request("GET", url)
            data=response.json()
            embed = discord.Embed(title="Weather "+str(data['location']['name']).capitalize(), color =self.client.colour1)
            embed.add_field(name="Condition:", value=data['current']['condition']['text'])
            embed.add_field(name="Temp:", value=data['current']['temp_c'])
            embed.add_field(name="Time:", value=data['location']['localtime'])
            await ctx.send(embed=embed)

    @commands.command()
    async def time(self, ctx, var):
            utc_now = pytz.utc.localize(datetime.utcnow())
            pst = utc_now.astimezone(pytz.timezone(f"{var}"))
            embed = discord.Embed(title=pst.strftime('%I:%M %p, %a, %#d %B %Y'), color =self.client.colour1)
            await ctx.send(embed=embed)

def setup(client):
    client.add_cog(INFO(client))
