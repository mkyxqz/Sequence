import discord
from discord.ext import commands
from utils.misc import send_welcome_message, send_command_help, send_welcome_message_test, to_var, cmd

class Welcome(commands.Cog):
  def __init__(self, client): 
    self.client = client

  @commands.command(description='Tests the welcome message.', cls=cmd, example='test', permissions='MANAGE_GUILD')
  @commands.has_guild_permissions(manage_guild=True)
  async def test(self, ctx):
    await send_welcome_message_test(ctx)

  @commands.command(description="Sets the message.", cls=cmd, example='message {member}, welcome to {server_name}!', permissions='MANAGE_GUILD')
  @commands.has_guild_permissions(manage_guild=True)
  async def message(self, ctx, *, message:str=None):
    if not message:
      return await send_command_help(ctx, 'manage_guild', "```Usage: message <text>\nExample: message welcome to the server!```")
    if len(message) > 2000:
        return await ctx.send('The message cannot be longer than 2000 characters.')
    self.client.welcome.update_one(self.client.welcome.find_one({"_id": ctx.guild.id}), {"$set": {"message": message}})
    await send_welcome_message_test(ctx)

  @commands.command(description="Sets the description.", cls=cmd, example='description {member_tag}\'s created: {member_createdate}', permissions='MANAGE_GUILD')
  @commands.has_guild_permissions(manage_guild=True)
  async def description(self, ctx, *, description:str=None):
    if not description:
      return await send_command_help(ctx, 'manage_guild', "```Usage: description <text>\nExample: description welcome to the server!```")
    if len(description) > 2000:
        return await ctx.send('The description cannot be longer than 2000 characters.')
    self.client.welcome.update_one(self.client.welcome.find_one({"_id": ctx.guild.id}), {"$set": {"description": description}})
    await send_welcome_message_test(ctx)

  @commands.command(description="Sets the thumbnail.", cls=cmd, example='thumbnail https://imgbb.com/219dwio', permissions='MANAGE_GUILD')
  @commands.has_guild_permissions(manage_guild=True)
  async def thumbnail(self, ctx, *, thumbnail:str=None):
    if not thumbnail:
      return await send_command_help(ctx, 'manage_guild', "```Usage: thumbnail <url>\nExample: thumbnail https://realimagelink.com```")
    self.client.welcome.update_one(self.client.welcome.find_one({"_id": ctx.guild.id}), {"$set": {"thumbnail": thumbnail}})
    await send_welcome_message_test(ctx)

  @commands.command(description="Sets the image.", cls=cmd, example='image https://imgbb.com/9dwyio', permissions='MANAGE_GUILD')
  @commands.has_guild_permissions(manage_guild=True)
  async def image(self, ctx, *, image:str=None):
    if not image:
      return await send_command_help(ctx, 'manage_guild', "```Usage: image <url>\nExample: image https://realimagelink.com```")
    self.client.welcome.update_one(self.client.welcome.find_one({"_id": ctx.guild.id}), {"$set": {"image": image}})
    await send_welcome_message_test(ctx)

  @commands.command(description="Sets the title.", cls=cmd, example='Welcome to {server_name}!', permissions='MANAGE_GUILD')
  @commands.has_guild_permissions(manage_guild=True)
  async def title(self, ctx, *, title:str=None):
    if not title:
      return await send_command_help(ctx, 'manage_guild', "```Usage: title <text>\nExample: title welcome to the server!```")
    if len(title) > 2000:
        return await ctx.send('The title cannot be longer than 2000 characters.')
    self.client.welcome.update_one(self.client.welcome.find_one({"_id": ctx.guild.id}), {"$set": {"title": title}})
    await send_welcome_message_test(ctx)

  @commands.command(description="Sets the author icon.", cls=cmd, example='authoricon https://imgbb.com/9dwyio', permissions='MANAGE_GUILD')
  @commands.has_guild_permissions(manage_guild=True)
  async def authoricon(self, ctx, *, authoricon:str=None):
    if not authoricon:
      return await send_command_help(ctx, 'manage_guild', "```Usage: authoricon <url>\nExample: authoricon https://realimagelink.com```")
    self.client.welcome.update_one(self.client.welcome.find_one({"_id": ctx.guild.id}), {"$set": {"author_icon": authoricon}})
    await send_welcome_message_test(ctx)

  @commands.command(description="Sets the author name.", cls=cmd, example='author We are on top', permissions='MANAGE_GUILD')
  @commands.has_guild_permissions(manage_guild=True)
  async def author(self, ctx, *, author:str=None):
    if not author:
      return await send_command_help(ctx, 'manage_guild', "```Usage: author <name>\nExample: author Welcome to the server!```")
    self.client.welcome.update_one(self.client.welcome.find_one({"_id": ctx.guild.id}), {"$set": {"author_name": author}})
    await send_welcome_message_test(ctx)

  @commands.command(description="Sets the footer text.", cls=cmd, example='footer Enjoy your stay!', permissions='MANAGE_GUILD')
  @commands.has_guild_permissions(manage_guild=True)
  async def footer(self, ctx, *, footer:str=None):
    if not footer:
      return await send_command_help(ctx, 'manage_guild', "```Usage: footer <text>\nExample: footer Welcome to the server!```")
    self.client.welcome.update_one(self.client.welcome.find_one({"_id": ctx.guild.id}), {"$set": {"footer_text": footer}})
    await send_welcome_message_test(ctx)

  @commands.command(description="Sets the footer text.", cls=cmd, example='footericon https://imgbb.com/9dwyio', permissions='MANAGE_GUILD')
  @commands.has_guild_permissions(manage_guild=True)
  async def footericon(self, ctx, *, footericon:str=None):
    if not footericon:
      return await send_command_help(ctx, 'manage_guild', "```Usage: footericon <url>\nExample: footericon https://realimagelink.com```")
    self.client.welcome.update_one(self.client.welcome.find_one({"_id": ctx.guild.id}), {"$set": {"footer_icon": footericon}})
    await send_welcome_message_test(ctx)

  @commands.command(description="Sets the channel where the welcome messages are sent.", cls=cmd, example='channel #joins', permissions='MANAGE_GUILD')
  @commands.has_guild_permissions(manage_guild=True)
  async def channel(self, ctx, channel: discord.TextChannel=None):
   if not channel:
      return await send_command_help(ctx, 'manage_guild', "```Usage: channel <channel>\nExample: channel #joins```")
   
   self.client.welcome.update_one(self.client.welcome.find_one({"_id": ctx.guild.id}), {"$set": {"channel": channel.id}})
   await send_welcome_message_test(ctx)
  
  @commands.command(description="Changes the embed color.", cls=cmd, example='color FF0000', permissions='MANAGE_GUILD')
  @commands.has_guild_permissions(manage_guild=True)
  async def color(self, ctx, color:str=None):
    if not color:
      return await send_command_help(ctx, 'manage_guild', "```Usage: color <hexcode>\nExample: color 0xFF00000```")

    if not color.startswith('0x'):
      color = '0x'+color
    try:
      discord.Embed(color=int(color,16))
    except:
      return await ctx.send('Invalid hex code provided.')

    self.client.welcome.update_one(self.client.welcome.find_one({"_id": ctx.guild.id}), {"$set": {"color": int(color,16)}})
    await send_welcome_message_test(ctx)

  @commands.command(description='Enables and disables the timestamp.', cls=cmd, example='timestamp', permissions='MANAGE_GUILD')
  @commands.has_guild_permissions(manage_guild=True)
  async def timestamp(self, ctx):
    if self.client.welcome.find_one({"_id": ctx.guild.id})['timestamp']:
      new_toggle = False
    else:
      new_toggle = True
    self.client.welcome.update_one(self.client.welcome.find_one({"_id": ctx.guild.id}), {"$set": {"timestamp": new_toggle}})
    await send_welcome_message_test(ctx)

  @commands.command(description='Enables and disables the welcome message.', cls=cmd, example='toggle', permissions='MANAGE_GUILD')
  @commands.has_guild_permissions(manage_guild=True)
  async def toggle(self, ctx):
    if self.client.welcome.find_one({"_id": ctx.guild.id})['enabled']:
      new_toggle = False
    else:
      new_toggle = True
    self.client.welcome.update_one(self.client.welcome.find_one({"_id": ctx.guild.id}), {"$set": {"enabled": new_toggle}})
    embed = discord.Embed(color=self.client.color, description=f"{ctx.author.mention} toggled the welcome {str(new_toggle).replace('True', 'on').replace('False', 'off')}")
    await ctx.send(embed=embed)

  @commands.command(description='Lists all available variable.', cls=cmd, example='variables', permissions='MANAGE_GUILD')
  async def variables(self, ctx):
    var = '''
**Member related variables**
`{member}`
Mentions the member
`{member_tag}`
Shows the member's name and tag, Ex: manny#1234 
`{member_name}`
Shows the member's name, Ex: mky
`{member_avatar}`
Gives the member's avatar url
`{member_discrim}`
Gives the member's discrim, Ex: #1234
`{member_nick}`
Gives the member's nickname
`{member_joindate}`
Gives the member's join date, Ex: 5/5/2021, 11:47:25
`{member_createdate}`
Gives the member's account creation date, Ex: 5/5/2021, 11:47:25
**Server related variables**
`{server_name}`
Gives the server's name
`{server_membercount}`
Gives the server's member count, Ex: 1231
`{server_membercount_ordinal}`
Gives the server's member count in ordinal, Ex: 1025th
`{server_membercount_nobots}`
Gives the server's member count with no bots
`{server_membercount_nobots_ordinal}`
Gives the server's member count with no bots in ordinal 
`{server_botcount}`
Gives the server's bot count
`{server_botcount_ordinal}`
Gives the server's bot count in ordinal
`{server_icon}`
Gives the server's icon url
`{server_owner}`
Gives the server's owner name and tag, Ex: mky#2900
`{server_createdate}`
Gives the server's creation date, Ex: 5/5/2021, 11:47:25
`{server_boostlevel}`
Gives the server's current boost tier (1-3)
`{server_boostcount}`
Gives the server's boost count
    '''
    await ctx.send(embed=discord.Embed(description=var, color=self.client.color))

  @commands.command(description='Test variables.', cls=cmd, example='variable {member} | {server_name} | {server_owner} | {member_avatar}', permissions='MANAGE_GUILD')
  @commands.has_guild_permissions(manage_guild=True)
  async def variable(self, ctx, *, message=None):
    if not message:
      return await ctx.send('No text was given.')
    message = to_var(message, ctx.author)
    await ctx.send(message)

  @commands.Cog.listener()
  async def on_member_join(self, member):
    await send_welcome_message(self.client, member)

def setup(client):
  client.add_cog(Welcome(client))