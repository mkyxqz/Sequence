from discord.ext import commands
from utils.misc import clean_prefix, cmd
from utils.pages import Pages

class Autoresponses(commands.Cog):
  def __init__(self, client):
    self.client = client
    self.cooldown_map = commands.CooldownMapping.from_cooldown(3, 15, commands.BucketType.member)

  @commands.Cog.listener()
  async def on_message(self, message):
    if message.author.bot:
      return
    if not message.guild:
      return
    ars = self.client.ars.find_one({"_id": message.guild.id})
    del ars["_id"]
    if not ars:
      return
    if message.content in ars:
      await message.channel.send(ars[message.content])

   # if message.content in ars:
     # await message.channel.send(ars[message.content])

  @commands.group(name='autoresponse', description='Lists the auto response commands.',aliases=['ar'], invoke_without_command=True)
  async def arcommand(self, ctx):
    await ctx.send(f'{clean_prefix(self.client, ctx.prefix)}autoresponse add | remove | list')

  @arcommand.command(name='add', aliases=['create'], description='Creates a new auto response.', cls=cmd, example='autoresponse add welc welcome to hood!', permissions='MANAGE_GUILD')
  @commands.has_guild_permissions(manage_guild=True)
  async def addsubcommand(self, ctx, trigger, *, response):
    if trigger in self.client.ars.find_one({"_id": ctx.guild.id}):
      return await ctx.send('That auto response already exists.')
    try:
      self.client.ars.update_one(self.client.ars.find_one({"_id": ctx.guild.id}), {"$set": {trigger: response}})
    except:
      return await ctx.send('Trigger contains forbidden characters.')
    await ctx.send(f'Auto response created for the word "{trigger}" <a:checkmark:857155755923734559>')

  @arcommand.command(name='remove', aliases=['delete'], description='Deletes an existing auto response.', cls=cmd, example='autoresponse delete welc', permissions='MANAGE_GUILD')
  @commands.has_guild_permissions(manage_guild=True)
  async def removesubcommand(self, ctx, trigger):
    if trigger not in self.client.ars.find_one({"_id": ctx.guild.id}):
      return await ctx.send('That auto response does not exist.')
    self.client.ars.update_one(self.client.ars.find_one({"_id": ctx.guild.id}), {"$unset": {trigger: self.client.ars.find_one({"_id": ctx.guild.id})[trigger]}})
    await ctx.send(f'Deleted the auto response for "{trigger}" <a:checkmark:857155755923734559>')

  @arcommand.command(name='list', description='Lists all existing auto responses.', cls=cmd, example='autoresponse list')
  async def listsubcommand(self, ctx):
    ars = self.client.ars.find_one({"_id": ctx.guild.id})
    del ars["_id"]
    if not ars:
      return await ctx.send('No auto responses exist')
    ars = [f'\n**{word}**: `{self.client.ars.find_one({"_id": ctx.guild.id})[word][:500]}`' for word in ars]
    await Pages(ctx, ars, per_page=5, embed=False, author=f"Auto responses: {len(ars)}", color=self.client.color).start()


def setup(client):
  client.add_cog(Autoresponses(client))