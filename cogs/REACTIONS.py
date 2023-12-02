import discord
from discord import Member
from discord.ext import commands
from random import choice
import requests
import json

tenor_key="" #TENOR KEY GOES HERE
tenor_limit=50

class REACTIONS(commands.Cog):

    def __init__(self, client):
        self.client= client

    @commands.command()
    async def hug(self, ctx, member: Member = None):
        search_term = "anime hug"
        r = requests.get("https://g.tenor.com/v1/search?q=%s&key=%s&limit=%s" % (search_term, tenor_key, tenor_limit))
        gifs=[]
        if r.status_code == 200:
            top10gifs = json.loads(r.content)
            for i in range(len(top10gifs['results'])):
                url = top10gifs['results'][i]['media'][0]['gif']['url'] #This is the url from json
                gifs.append(url)
        else:
            top10gifs = None
        embed = discord.Embed(title=f"{ctx.message.author.display_name} hugs {member.display_name}", color=self.client.colour1)
        embed.set_image(url=choice(gifs))
        await ctx.send(embed=embed)

    @commands.command()
    async def spank(self, ctx, member: Member = None):
        search_term = "anime spank"
        r = requests.get("https://g.tenor.com/v1/search?q=%s&key=%s&limit=%s" % (search_term, tenor_key, tenor_limit))
        gifs=[]
        if r.status_code == 200:
            top10gifs = json.loads(r.content)
            for i in range(len(top10gifs['results'])):
                url = top10gifs['results'][i]['media'][0]['gif']['url'] #This is the url from json
                gifs.append(url)
        else:
            top10gifs = None
        embed = discord.Embed(title=f"{ctx.message.author.display_name} spanks {member.display_name}", color=self.client.colour1)
        embed.set_image(url=choice(gifs))
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(REACTIONS(client))
