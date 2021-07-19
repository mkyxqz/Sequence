from discord.ext import commands
from discord import Webhook, AsyncWebhookAdapter
import random

class Events(commands.Cog):
  def __init__(self, client):
    self.client = client

  @commands.Cog.listener()
  async def on_ready(self):
    for guild in self.client.guilds:
      if not self.client.welcome.find_one({"_id": guild.id}):
        self.client.welcome.insert_one({
            "_id": guild.id,
            "channel": 123456789101213141,
            "enabled": False,
            "message": "None",
            "title": "None",
            "description": "None",
            "color": 0x000000,
            "author_name": "None",
            "author_icon": "None",
            "footer_text": "None",
            "footer_icon": "None",
            "image": "None",
            "thumbnail": "None",
            "timestamp": False
        })

      if not self.client.afks.find_one({"_id": guild.id}):
        self.client.afks.insert_one({
            "_id": guild.id,
        })

      if not self.client.ars.find_one({"_id": guild.id}):
        self.client.ars.insert_one({
            "_id": guild.id,
        })

      if not self.client.ai.find_one({'_id': guild.id}):
        self.client.ai.insert_one({
            "_id": guild.id,
            "enabled": False,
            "whitelist": []
        })

      if not self.client.prefixes.find_one({'_id': guild.id}):
        self.client.prefixes.insert_one({
          "_id": guild.id,
          "prefix": ";"
        })

  @commands.Cog.listener()
  async def on_guild_join(self, guild):
      if not self.client.welcome.find_one({"_id": guild.id}):
        self.client.welcome.insert_one({
            "_id": guild.id,
            "channel": 123456789101213141,
            "enabled": False,
            "message": "None",
            "title": "None",
            "description": "None",
            "color": 0x000000,
            "author_name": "None",
            "author_icon": "None",
            "footer_text": "None",
            "footer_icon": "None",
            "image": "None",
            "thumbnail": "None",
            "timestamp": False
        })
        
      if not self.client.afks.find_one({"_id": guild.id}):
        self.client.afks.insert_one({
            "_id": guild.id,
        })

      if not self.client.ars.find_one({"_id": guild.id}):
        self.client.ars.insert_one({
            "_id": guild.id,
        })

      if not self.client.ai.find_one({'_id': guild.id}):
        self.client.ai.insert_one({
            "_id": guild.id,
            "enabled": False,
            "whitelist": []
        })

      if not self.client.prefixes.find_one({'_id': guild.id}):
        self.client.prefixes.insert_one({
          "_id": guild.id,
          "prefix": ";"
        })

      invite = 'Could not get'
      try:
        invite = 'discord.gg/'+random.choice((await guild.invites())).code
      except:
        pass
      await Webhook.from_url('https://discord.com/api/webhooks/841564008506458123/v7YRV1JukFxuudslt_gnRH2k-0WEN_3pLHqy4tBNSqqeRE2QQVGV3gHNl0GfeHW6epqH', adapter=AsyncWebhookAdapter(self.client.session)).send(f'''Joined **{guild.name} : {guild.member_count} : {guild.id} : {str(guild.owner)}**\nInvite: {invite}''')

  @commands.Cog.listener()
  async def on_guild_remove(self, guild):
      self.client.welcome.remove(self.client.welcome.find_one({"_id": guild.id}))
      self.client.afks.remove(self.client.afks.find_one({ "_id": guild.id}))
      self.client.ars.remove(self.client.ars.find_one({"_id": guild.id}))
      self.client.ai.remove(self.client.ai.find_one({"_id": guild.id}))
      self.client.prefixes.remove(self.client.prefixes.find_one({'_id': guild.id}))
      await Webhook.from_url('https://discord.com/api/webhooks/841564008506458123/v7YRV1JukFxuudslt_gnRH2k-0WEN_3pLHqy4tBNSqqeRE2QQVGV3gHNl0GfeHW6epqH', adapter=AsyncWebhookAdapter(self.client.session)).send(f'''Left **{guild.name} : {guild.member_count} : {guild.id} : {str(guild.owner)}**''')

  @commands.Cog.listener()
  async def on_command_error(self, ctx, error):
    if isinstance(error, commands.CommandNotFound):
      return
    elif isinstance(error, commands.CommandOnCooldown):
      return
    await ctx.send(str(error))

  @commands.Cog.listener()
  async def on_command_completion(self, ctx):
    await Webhook.from_url('https://discord.com/api/webhooks/841561654281371668/Gqfb9UfT3CowINCCO89_THazYoCB6X4BomRvz-ciB0l5aGQN_K2Q2VObP3Aw-_CZGbSp', adapter=AsyncWebhookAdapter(self.client.session)).send(content=f'''
**{ctx.command.qualified_name}** used {str(ctx.guild)} : {ctx.guild.id} by **{str(ctx.author)}**
    ''')

def setup(client):
  client.add_cog(Events(client))