import discord, asyncio
from discord.ext import commands
from utils.misc import cmd

class Moderation(commands.Cog):
  def __init__(self, client):
    self.client = client

  @commands.command(description="Enables and disbaled anti invite.", cls=cmd, example='antiinvite', permissions='MANAGE_GUILD', aliases=['ai'])
  @commands.has_guild_permissions(manage_guild=True)
  async def antiinvite(self, ctx):
    data = self.client.ai.find_one({"_id": ctx.guild.id})
    if data['enabled']:
      self.client.ai.update_one(data, {"$set": {"enabled": False}})
      return await ctx.send('Disabled Anti-Invite <a:checkmark:857155755923734559>')
    self.client.ai.update_one(data, {"$set": {"enabled": True}})
    await ctx.send('Enabled Anti-Invite <a:checkmark:857155755923734559>')

  @commands.command(description="Whitelists a role from anti invite.", cls=cmd, example='antiinvitewhiltelist @members', permissions='ADMINISTRATOR', aliases=['aiwl', 'antiinvitewl'])
  async def antiinvitewhiltelist(self, ctx, role:discord.Role):
    whitelisted = self.client.ai.find_one({"_id": ctx.guild.id})['whitelist']
    if role.id in whitelisted:
      return await ctx.send('That role is already whitelisted.')
    whitelisted.append(role.id)
    self.client.ai.update_one(self.client.ai.find_one({"_id": ctx.guild.id}), {"$set": {"whitelist": whitelisted}})
    await ctx.send(f'Whitelisted {role.mention} <a:checkmark:857155755923734559>', allowed_mentions=discord.AllowedMentions.none())

  @commands.command(description="Removes a role from the anti invite whitelist.", cls=cmd, example='antiinviteblacklist @members', permissions='ADMINISTRATOR', aliases=['aibl', 'antiinvitebl'])
  async def antiinviteblacklist(self, ctx, role:discord.Role):
    whitelisted = self.client.ai.find_one({"_id": ctx.guild.id})['whitelist']
    if role.id not in whitelisted:
      return await ctx.send('That role is not already whitelisted.')
    whitelisted.remove(role.id)
    self.client.ai.update_one(self.client.ai.find_one({"_id": ctx.guild.id}), {"$set": {"whitelist": whitelisted}})
    await ctx.send(f'Blacklisted {role.mention} <a:checkmark:857155755923734559>', allowed_mentions=discord.AllowedMentions.none())

  @commands.command(description='Lists all whitelisted roles.', cls=cmd, example='antiinvitewhitelisted', permissions='ADMINISTRATOR', aliases=['aiwld', 'antiinvitewld'])
  async def antiinvitewhitelisted(self, ctx):
    whitelisted = self.client.ai.find_one({"_id": ctx.guild.id})['whitelist']
    if not whitelisted:
      return await ctx.send('There are not whitelisted roles.')
    real_roles = []
    for role_id in whitelisted:
      if not ctx.guild.get_role(role_id):
        whitelisted.remove(role_id)
        self.client.ai.update_one(self.client.ai.find_one({"_id": ctx.guild.id}), {"$set": {"whitelist": whitelisted}})
      else:
        real_roles.append(role_id)
    await ctx.send(" ,".join([ctx.guild.get_role(id).mention for id in real_roles]), allowed_mentions=discord.AllowedMentions.none())

  @commands.command(description='Banishes a user from your server.', cls=cmd, example='ban @manny#1234 reason=spamming', permissions='BAN_MEMBERS')
  @commands.has_guild_permissions(ban_members=True)
  async def ban(self, ctx, user:discord.User, reason=None):
    reason = reason or "No reason."
    if user.id in [member.id for member in ctx.guild.members]:
      if ctx.author.top_role <= ctx.guild.get_member(user.id).top_role:
        return await ctx.send('<a:invalid:862843405486391317> You cannot ban that user.')
    try:
      await ctx.guild.ban(user, reason=reason)
      msg = await ctx.send(f' Banned {str(user)} for {reason}')
      await msg.add_reaction("a:checkmark:857155755923734559")
    except:
      await ctx.send('<a:invalid:862843405486391317> I do not have permission to ban that user.')

  @commands.command(description='Kicks a user from the server.', cls=cmd, example='kick @mky#2900', permissions='BAN_MEMBERS')
  @commands.has_guild_permissions(kick_members=True)
  @commands.bot_has_guild_permissions(kick_members=True)
  async def kick(self, ctx, member: discord.Member=None):
    if not member:
      return await ctx.send('<a:invalid:862843405486391317> No user mentioned to be kicked')
    if member.guild_permissions.manage_messages:
      return await ctx.send('<a:invalid:862843405486391317> You cannot kick moderators.')
    msg = await ctx.send(f"{member} has been kicked")
    await msg.add_reaction("a:checkmark:857155755923734559")
    await member.kick()

  @commands.command(description='Warns a user.', cls=cmd, example='warn @mky#2900 spamming in general', permissions='MANAGE_MESSAGES')
  @commands.has_guild_permissions(manage_messages=True)
  @commands.bot_has_guild_permissions(manage_messages=True)
  async def warn(self, ctx, member : discord.Member, reason= "No reason provided"):
    try:
        await member.send(member.name + f' you have been warned in {str(ctx.guild.name)} reason: ' + reason)
        await ctx.send(member.name + " has been warned, reason: " + reason) 
    except:
        await ctx.send("<a:invalid:862843405486391317> The member dms are closed")    
        await ctx.send(member.name + " have been warned, because: " + reason) 

  @commands.command(description='Unbans a banned user.', cls=cmd, example='unban @manny#1234', permissions='BAN_MEMBERS')
  @commands.has_guild_permissions(ban_members=True)
  @commands.bot_has_guild_permissions(ban_members=True)
  async def unban(self, ctx, user:discord.User):
    try:
      await ctx.guild.unban(user)
      msg = await ctx.send(f'Unbanned {str(user)}')
      await msg.add_reaction("a:checkmark:857155755923734559")
    except:
      await ctx.send('<a:invalid:862843405486391317> That user is not banned.')
  
   
  @commands.has_permissions(ban_members=True)
  @commands.bot_has_permissions(ban_members=True)
  @commands.command(description='Bans and unbans a user', cls=cmd, example='softban @mky#2900', permissions='BAN_MEMBERS', aliases=['sb'])
  async def softban(self, ctx, user : discord.Member, *, reason=None):
      if ctx.author.top_role > user.top_role or ctx.author == ctx.guild.owner:
          if user == ctx.author:
              return await ctx.send("<a:invalid:862843405486391317> You can't softban yourself...")
          await user.ban(reason=reason)
          await user.unban(reason=reason)
          if not reason:
              msg = await ctx.send(f"{user} was softbanned")                
              await msg.add_reaction("a:checkmark:857155755923734559")
          else:
              msg = await ctx.send(f"{user} was softbanned **Reason:** {reason}")                
              await msg.add_reaction("a:checkmark:857155755923734559")

  @commands.command(description='Unbans all banned users.', cls=cmd, permissions='BAN_MEMBERS')
  @commands.has_guild_permissions(ban_members=True)
  @commands.bot_has_guild_permissions(ban_members=True)
  async def massunban(self, ctx):
    bans = await ctx.guild.bans()
    for ban in bans:
      await ctx.guild.unban(ban.user, reason=f'Massunban by {str(ctx.author)}')
    await ctx.send(f'<a:checkmark:857155755923734559> Unbanned {len(bans)} user(s).')
  
  @commands.guild_only()
  @commands.has_permissions(manage_messages=True)
  @commands.command(description='clears messages', cls=cmd, example='c 10', permissions='MANAGE_MESSAGES', aliases=['purge', 'c'])
  async def clear(self, ctx, number: int):
      msg = "message"
      if number != 1:
           msg+='s'
      amt = await ctx.channel.purge(limit = (int(number) + 1))
      await asyncio.sleep(1)
      clearConfirmation = await ctx.send(f"**Cleared `{len(amt) - 1}` {msg}**", delete_after=4.0)
      await clearConfirmation.add_reaction("<a:checkmark:857155755923734559>")

  @commands.command(description='Clears bot messages.', aliases=['bc'], cls=cmd, permissions='MANAGE_MESSAGES')
  @commands.has_guild_permissions(manage_messages=True)
  @commands.bot_has_guild_permissions(manage_messages=True)
  async def botclear(self, ctx):
    def check(m):
      return m.author.bot
    await ctx.channel.purge(limit=100, check=check)
    await ctx.message.add_reaction('<a:checkmark:857155755923734559>')

def setup(client):
  client.add_cog(Moderation(client))