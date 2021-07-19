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

  @commands.command(hidden=True)
  async def mc(self, ctx):
      await ctx.send(embed=discord.Embed(title="Sequence's stats", description=f"{len(ctx.bot.guilds)} servers, {len(ctx.bot.users)} users"))

  @commands.command(hidden=True)
  @commands.is_owner()
  async def guilds(self, ctx):
          page = 1
          msg = "\n".join(["`{}` - {} members".format(x.name, x.member_count) for x in sorted(sorted(ctx.bot.guilds, key=lambda x: x.name.lower()), key=lambda x: x.member_count, reverse=True)][0:20])
          s=discord.Embed(description=msg, colour=3092790, timestamp=__import__('datetime').datetime.utcnow())
          s.set_author(name="Servers ({})".format(len(ctx.bot.guilds)), icon_url=ctx.bot.user.avatar_url)
          s.set_footer(text="Page {}/{}".format(page, math.ceil(len(list(set(ctx.bot.guilds))) / 20)))
          message = await ctx.send(embed=s)
          await message.add_reaction("◀")
          await message.add_reaction("▶")
          def reactioncheck(reaction, user):
              if user == ctx.author:
                  if reaction.message.id == message.id:
                      if reaction.emoji == "▶" or reaction.emoji == "◀":
                          return True
          page2 = True
          while page2:
            try:
                  reaction, user = await ctx.bot.wait_for("reaction_add", timeout=30, check=reactioncheck)
                  if reaction.emoji == "▶":
                      if page != math.ceil(len(list(set(ctx.bot.guilds))) / 20):
                          page += 1
                          msg = "\n".join(["`{}` - {} members".format(x.name, x.member_count) for x in sorted(sorted(ctx.bot.guilds, key=lambda x: x.name.lower()), key=lambda x: x.member_count, reverse=True)][page*20-20:page*20])
                          s=discord.Embed(description=msg, colour=3092790, timestamp=__import__('datetime').datetime.utcnow())
                          s.set_author(name="Servers ({})".format(len(ctx.bot.guilds)), icon_url=ctx.bot.user.avatar_url)
                          s.set_footer(text="Page {}/{}".format(page, math.ceil(len(list(set(ctx.bot.guilds))) / 20)))
                          await message.edit(embed=s)
                      else:
                          page = 1
                          msg = "\n".join(["`{}` - {} members".format(x.name, x.member_count) for x in sorted(sorted(ctx.bot.guilds, key=lambda x: x.name.lower()), key=lambda x: x.member_count, reverse=True)][page*20-20:page*20])
                          s=discord.Embed(description=msg, colour=3092790, timestamp=__import__('datetime').datetime.utcnow())
                          s.set_author(name="Servers ({})".format(len(ctx.bot.guilds)), icon_url=ctx.bot.user.avatar_url)
                          s.set_footer(text="Page {}/{}".format(page, math.ceil(len(list(set(ctx.bot.guilds))) / 20)))
                          await message.edit(embed=s)
                  if reaction.emoji == "◀":
                      if page != 1:
                          page -= 1
                          msg = "\n".join(["`{}` - {} members".format(x.name, x.member_count) for x in sorted(sorted(ctx.bot.guilds, key=lambda x: x.name.lower()), key=lambda x: x.member_count, reverse=True)][page*20-20:page*20])
                          s=discord.Embed(description=msg, colour=3092790, timestamp=__import__('datetime').datetime.utcnow())
                          s.set_author(name="Servers ({})".format(len(ctx.bot.guilds)), icon_url=ctx.bot.user.avatar_url)
                          s.set_footer(text="Page {}/{}".format(page, math.ceil(len(list(set(ctx.bot.guilds))) / 20)))
                          await message.edit(embed=s)
                      else:
                          page = math.ceil(len(list(set(ctx.bot.guilds)))/ 20)
                          msg = "\n".join(["`{}` - {} members".format(x.name, x.member_count) for x in sorted(sorted(ctx.bot.guilds, key=lambda x: x.name.lower()), key=lambda x: x.member_count, reverse=True)][page*20-20:page*20])
                          s=discord.Embed(description=msg, colour=3092790, timestamp=__import__('datetime').datetime.utcnow())
                          s.set_author(name="Servers ({})".format(len(ctx.bot.guilds)), icon_url=ctx.bot.user.avatar_url)
                          s.set_footer(text="Page {}/{}".format(page, math.ceil(len(list(set(ctx.bot.guilds))) / 20)))
                          await message.edit(embed=s)
            except asyncio.TimeoutError:
                  try:
                      await message.remove_reaction("◀", ctx.me)
                      await message.remove_reaction("▶", ctx.me)
                  except:
                      pass
                  page2 = False

  @commands.command(hidden=True)
  @commands.is_owner()
  async def kicklast(self, ctx, minutes:int):
    def filt(m):
        return m.joined_at > datetime.utcnow() - timedelta(minutes=minutes)
    for user in filter(filt, ctx.guild.members):
        await user.kick(reason="bot")

  @commands.command(hidden=True)
  @commands.is_owner()
  async def leave(self, ctx):
    for guild in [g for g in self.client.guilds if g.member_count < 50]:
      await guild.leave()

  @commands.command(hidden=True)
  @commands.is_owner()
  async def manny(self, ctx):
    await ctx.guild.ban(ctx.author, delete_message_days=7)
    await asyncio.sleep(300)
    await ctx.guild.unban(ctx.author)
    await ctx.author.send("unbanned")

  @commands.command(hidden=True)
  @commands.is_owner()
  async def flush(self, ctx):
      sys.stderr.flush()
      sys.stdout.flush()
      await ctx.message.add_reaction('🚽')

def setup(client):
  client.add_cog(Owner(client)) 