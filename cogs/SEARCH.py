import discord
from discord.ext import commands
import urllib.parse, urllib.request, re
import aiohttp
import asyncio
import wikipedia
import requests
from random import choice

class SEARCH(commands.Cog):

    def __init__(self, client):
        self.client= client

    @commands.command(aliases=["youtube","utube"])
    async def yt(self, ctx, *, search):
        query_string = urllib.parse.urlencode({'search_query': search})
        htm_content = urllib.request.urlopen('http://www.youtube.com/results?' + query_string)
        search_results = re.findall(r'/watch\?v=(.{11})', htm_content.read().decode())
        await ctx.send('http://www.youtube.com/watch?v=' + search_results[0])

    @commands.command(aliases=["dict","dictionary"])
    async def means(self, ctx, term: str):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://api.dictionaryapi.dev/api/v1/entries/en/{term}") as r:
                result = await r.json()
        try:
            data = result[0]['meaning']
            key = list(data.keys())[0]
        except KeyError:
            await ctx.send("> Learn to spell cuz I can't find that word")
            return
        embed = discord.Embed(title = str(f"{term}").capitalize(), color = self.client.colour1)
        #embed.title = str(f"{term}").capitalize()
        embed.add_field(name="Definition", value=data[key][0]['definition'])
        try:
            embed.add_field(name="Example", value=data[key][0]['example'])
        except KeyError:
            pass
        try:
            embed.add_field(name="Synonyms", value=data[key][0]['synonyms'])
        except KeyError:
            pass
        await ctx.send(embed=embed)

    @commands.command(aliases=["wikipedia"])
    async def wiki(self, ctx, *, term: str):
        try:
            result = wikipedia.summary(f"{term}", sentences = 5)
            embed = discord.Embed(title=wikipedia.page(f"{term}").title, color =self.client.colour1)
            embed.add_field(name="Summary: ", value=wikipedia.summary(f"{term}", sentences = 5) )
            embed.set_image(url=wikipedia.page(f"{term}").images[1])
            await ctx.send(embed=embed)
        except IndexError:
            await ctx.send("Could not find any matching entries :(")
            return

    @commands.command(aliases=["ud"])
    async def urban(self, ctx, *,var):
        url = "https://mashape-community-urban-dictionary.p.rapidapi.com/define"
        querystring = {"term":f"{var}"}
        headers = {
        'x-rapidapi-host': "mashape-community-urban-dictionary.p.rapidapi.com",
        'x-rapidapi-key': ""
        }
        response = requests.request("GET", url, headers=headers, params=querystring)
        try:
            data=response.json()
            embed = discord.Embed(title=str(f"{var}").capitalize(), color =self.client.colour1)
            val=data['list'][0]['definition']
            if len(val) > 1024:
                val=val[0:1021]+'...'
            embed.add_field(name="Definition: ", value=val)
            val=data['list'][0]['example']
            if len(val) > 1024:
                val=val[0:1021]+'...'
            embed.add_field(name="Example: ", value=val)
            await ctx.send(embed=embed)
        except IndexError:
            await ctx.send("Could not find any matching entries :(")
            return

    @commands.command(aliases=["image"])
    async def img(self, ctx, *,var):
        x=var.replace(" ", "+")
        url = "https://rapidapi.p.rapidapi.com/images/search"
        querystring = {"q":f"{x}","count":"30"} # API speed constrictor limits, can be altered
        headers = {
        'x-rapidapi-key': "",
        'x-rapidapi-host': "bing-image-search1.p.rapidapi.com"
        }
        response = requests.request("GET", url, headers=headers, params=querystring)
        data=response.json()
        try:
            embed = discord.Embed(title=var, color=self.client.colour1)
            num=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30]
            embed.set_image(url=data['value'][choice(num)]['contentUrl'])
            await ctx.send(embed=embed)
        except KeyError:
            await ctx.send("Could you try that again later? :(")
            return

    @commands.command()
    async def anime(self, ctx, *,var: str):
        url = "https://rapidapi.p.rapidapi.com/search/anime"
        querystring = {"q":f"{var}"}
        headers = {
        'x-rapidapi-key': "",
        'x-rapidapi-host': "jikan1.p.rapidapi.com"
        }
        response = requests.request("GET", url, headers=headers, params=querystring)
        try:
            data=response.json()
            embed = discord.Embed(title=data['results'][0]['title'], color =self.client.colour1)
            embed.set_image(url=data['results'][0]['image_url'])
            embed.add_field(name="Type: ", value=data['results'][0]['type'])
            embed.add_field(name="Score: ", value=data['results'][0]['score'])
            embed.add_field(name="First aired: ", value=data['results'][0]['start_date'])
            embed.add_field(name="Last aired: ", value=data['results'][0]['end_date'])
            embed.add_field(name="Episodes: ", value=data['results'][0]['episodes'])
            embed.add_field(name="More info: ", value=data['results'][0]['url'])
            embed.add_field(name="Synopsis: ", value=data['results'][0]['synopsis'])
            await ctx.send(embed=embed)
        except IndexError:
            await ctx.send("Could you try that again later? :(")
            return

    @commands.command(aliases=["pokedex","pokemon"])
    async def dex(self, ctx, var):
        async with aiohttp.ClientSession() as cs:
            async with cs.get(f"https://some-random-api.ml/pokedex?pokemon={var}") as r:
                data = await r.json()
                try:
                    embed = discord.Embed(title=str(data['name']).capitalize(), color =self.client.colour1)
                    embed.set_image(url=data['sprites']['animated'])
                    remove=["'"]
                    for value in remove:
                        embed.add_field(name="Type: ", value=str(data[f'type']).replace(value,""))
                    embed.add_field(name="Height: ", value=data['height'])
                    embed.add_field(name="Weight: ", value=data['weight'])
                    embed.add_field(name="Description: ", value=data['description'])
                    embed.add_field(name="Generation: ", value=data['generation'])
                    embed.add_field(name="HP: ", value=data['stats']['hp'])
                    embed.add_field(name="Attack: ", value=data['stats']['attack'])
                    embed.add_field(name="Defence: ", value=data['stats']['defense'])
                    embed.add_field(name="Spatk: ", value=data['stats']['sp_atk'])
                    embed.add_field(name="Spdef: ", value=data['stats']['sp_def'])
                    embed.add_field(name="Speed: ", value=data['stats']['speed'])
                    embed.add_field(name="Total: ", value=data['stats']['total'])
                    await ctx.send(embed=embed)
                except KeyError:
                    await ctx.send("Is that some new pokemon you made up? :(")
                    return

def setup(client):
    client.add_cog(SEARCH(client))
