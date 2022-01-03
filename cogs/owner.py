import discord, sys, math, asyncio, typing
from discord.ext import commands
from datetime import datetime, timedelta

class Owner(commands.Cog):
  def __init__(self, client):
    self.client = client

  @commands.command(hidden=True)
  @commands.is_owner()
  async def load(self, ctx, extension:str):
    try:
      self.client.load_extension(f'cogs.{extension}')
      await ctx.send('loaded '+extension)
    except Exception as error:
      await ctx.send(str(error))

  @commands.command(hidden=True)
  @commands.is_owner()
  async def unload(self, ctx, extension:str):
    if extension.lower() == 'owner':
      return await ctx.send('You cannot reload the owner extension')
    try:
      self.client.unload_extension(f'cogs.{extension}')
      await ctx.send('unloaded '+extension)
    except Exception as error:
      await ctx.send(str(error))

  @commands.command(hidden=True)
  @commands.is_owner()
  async def reload(self, ctx, extension:str):
    if extension.lower() == 'owner':
      return await ctx.send('You cannot reload the owner extension')
    try:
      self.client.unload_extension(f'cogs.{extension}')
      self.client.load_extension(f'cogs.{extension}')
      await ctx.send('reloaded '+extension)
    except Exception as error:
      await ctx.send(str(error))

def setup(client):
  client.add_cog(Owner(client)) 
