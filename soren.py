#!/usr/bin/env python3
import config
import discord
import asyncio
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="+", intents=intents)
role_owner = "Vanguard"
role_coowner = "Lord"
role_veteran = "Hero"
role_recruit = "Ranger"


@bot.group()
@commands.is_owner()
async def ct(ctx):
    if ctx.invoked_subcommand is None:
        return


@ct.command()
@commands.is_owner()
async def archive(ctx, num: str = None):
    to_archive = []
    if num.isnumeric():
        category = discord.utils.get(ctx.guild.categories, name=f"contested territory #{num}")
        to_archive.append(category)
    elif num == "all":
        for category in ctx.guild.categories:
            if "contested territory #" in category.name:
                to_archive.append(category)

    for category in to_archive:
        for channel in category.channels:
            await lock_channel(channel, ctx.guild.default_role)

    await ctx.message.add_reaction("👍")


@ct.command()
@commands.is_owner()
async def new(ctx, num=None):
    if num is None:
        await ctx.message.add_reaction("❌")

    category = await ctx.guild.create_category(f"contested territory #{num}")
    war_info = await category.create_text_channel("war-info")
    await lock_channel(war_info, ctx.guild.default_role)
    map = await category.create_text_channel("map")
    await lock_channel(map, ctx.guild.default_role)
    strategy = await category.create_text_channel("strategy")
    await lock_channel(strategy, ctx.guild.default_role)
    await category.create_text_channel("tile-strategy")
    await category.create_text_channel("general")

    await ctx.message.add_reaction("👍")


@ct.command()
@commands.is_owner()
async def delete(ctx, num):
    if num is None:
        await ctx.message.add_reaction("❌")

    category = discord.utils.get(ctx.guild.categories, name=f"contested territory #{num}")
    for channel in category.channels:
        await channel.delete()
    await category.delete()

    await ctx.message.add_reaction("👍")


async def lock_channel(channel, role):
    await channel.set_permissions(role, send_messages=False, add_reactions=False)


async def main():
    async with bot:
        await bot.start(config.TOKEN)


if __name__ == '__main__':
    asyncio.run(main())
