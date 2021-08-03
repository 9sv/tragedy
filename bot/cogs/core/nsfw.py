# -*- coding: utf-8 -*-

import json

import aiohttp
import discord
from discord.colour import Color
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType


class Nsfw(commands.Cog, description="Porn"):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(description="Porn", help="nsfw <type>")
	@commands.is_nsfw()
	@commands.cooldown(1, 3, type=BucketType.member)
	async def nsfw(self, ctx, *, type: str):
		with open("bot/assets/json/nsfw.json", "r") as urls:
			try:
				jObj = json.load(urls)
				query = jObj[type.replace(' ', '_')]
				async with aiohttp.ClientSession() as requests:
					async with requests.get("https://scathach.redsplit.org/v3{}".format(query)) as response:
						data = await response.json()
						_url = data["url"]
						embed = discord.Embed(title=type.title(), description="Take this weirdo",
						                      color=Color.green()).set_image(url=_url)
						await ctx.reply(embed=embed, mention_author=True)
			except Exception as exc:
				embed = discord.Embed(title="Error", description="{} is not a valid type.".format(exc),
				                      color=Color.red())
				await ctx.reply(embed=embed, mention_author=True)


def setup(bot):
	bot.add_cog(Nsfw(bot))
