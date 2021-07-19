import discord
from discord.ext import commands
from utils.misc import cmd

class Prefix(commands.Cog):
  def __init__(self, client):
    self.client = client

  @commands.guild_only()
  @commands.group(description='Shows the current prefix.')
  async def prefix(self, ctx):
    prefix = self.client.prefixes.find_one({"_id": ctx.guild.id})['prefix']
    embed = discord.Embed(color=self.client.color,description=f"`Prefix:` **{prefix}**")
    await ctx.send(embed=embed)

  @commands.guild_only()
  @commands.has_guild_permissions(manage_guild=True)
  @commands.command(description='Changes the current server prefix.', aliases=['sp', 'changeprefix'], cls=cmd, premissions='MANAGE_GUILD', example="setprefix $")
  async def setprefix(self, ctx, prefix):
    self.client.prefixes.update_one(self.client.prefixes.find_one({"_id": ctx.guild.id}), {"$set": {"prefix": prefix}})
    await ctx.send(f'Prefix set to {prefix} <a:checkmark:857155755923734559>')

  @commands.guild_only()
  @commands.has_guild_permissions(manage_guild=True)
  @commands.command(description='Reset prefix back to ;.', aliases=['resetprefix'], cls=cmd, premissions='MANAGE_GUILD', example="unsetprefix")
  async def unsetprefix(self, ctx):
    self.client.prefixes.update_one
    (self.client.prefixs.find_one({"_id": ctx.guild.id}), {"$set": {"prefix": ';'}})
    await ctx.send(f'Prefix has been reset back to ; <a:checkmark:857155755923734559>')
    
def setup(client):
  client.add_cog(Prefix(client))