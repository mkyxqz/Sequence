import discord
from discord.ext import commands
from utils.misc import cmd


class Snipe(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.client.sniped_messages = {}
        self.client.edit_sniped_messages = {}

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.bot:
            return
        self.client.sniped_messages[message.guild.id, message.channel.id] = (
            message.content, message.author, message.channel.name,
            message.created_at, message.attachments)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.author.bot:
            return
        self.client.edit_sniped_messages[before.guild.id, before.channel.id] = (
                                                before.content,
                                                after.content,
                                                before.author,
                                                before.channel.name
                                                )
                                              
    @commands.command(description='Snipes the recent deleted message.', cls=cmd, example='snipe')
    async def snipe(self, ctx):
      try:
        contents, author, channel_name, time, attachments = self.client.sniped_messages[
              ctx.guild.id, ctx.channel.id]
      except:
        return await ctx.send("Theres no messages to snipe!")
      files = ""
      for file in attachments:
          files += f"[{file.filename}]({file.proxy_url})" + "\n"
      embed = discord.Embed(
          description=contents, color=0xFF0000)
      embed.set_author(
          name=f"{author.name}#{author.discriminator}",
          icon_url=author.avatar_url)
      await ctx.send(embed=embed)

    @commands.command(description='Snipes the recent edited message.', cls=cmd, example='esnipe')
    async def esnipe(self, ctx):
      try:
          before_content, after_content, author, channel_name = self.client.edit_sniped_messages[ctx.guild.id, ctx.channel.id]
      except:
          return await ctx.send("Theres no messages to esnipe!")
      embed = discord.Embed(description = f"{before_content}", color=0xFF0000)
      embed.set_author(name=f"{author.name}#{author.discriminator}", icon_url=author.avatar_url)
      await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Snipe(client))