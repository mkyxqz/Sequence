import discord, arrow, asyncio, random, json, typing, re, spotify, textwrap
from discord.ext import commands
from utils.misc import cmd
from utils.pages import Pages
from datetime import datetime
from discord import Webhook, AsyncWebhookAdapter
from gtts import gTTS


class Misc(commands.Cog):
  def __init__(self, client):
    self.client = client
    self.cooldown_map = commands.CooldownMapping.from_cooldown(3, 15, commands.BucketType.member)

  @commands.command(description='Gives the bots support server')
  async def support(self, ctx):
    await ctx.send(f"Support Server: https://discord.gg/TvHBQjbM3t")

  @commands.command(cls=cmd, description='Give\'s my invite.')
  async def invite(self, ctx):
    embed = discord.Embed(color=self.client.color)
    embed.description=f"[Click here to invite sequence](https://discord.com/api/oauth2/authorize?client_id={self.client.user.id}&permissions=8&scope=applications.commands%20bot)"
    await ctx.send(embed=embed)

  @commands.command(description='Upvote me on top.gg.')
  async def vote(self, ctx):
    await ctx.send(f"https://top.gg/bot/839676121804832788")

  @commands.command(description="Shows the bots latency.", cls=cmd, example='ping')
  async def ping(self, ctx):
    response = datetime.now() - ctx.message.created_at
    before = datetime.now()
    message = await ctx.send('resolving...')
    after = datetime.now()
    await message.edit(content=None, embed=discord.Embed(color=self.client.color,description=f'Command response: {round((response).total_seconds()*1000)}ms\nMessage ping: {round((after-before).total_seconds()*1000)}ms\nWebsocket latency: {round(self.client.latency * 1000)}ms'))

  @commands.command(description="Shows peoples pfp.", cls=cmd, example='avatar [@user]', aliases=['av'])
  async def avatar(self, ctx, member:discord.Member=None):
    member = member or ctx.author
    await ctx.send(embed=discord.Embed(color=self.client.color).set_author(name=f'{member.display_name}\'s avatar:').set_image(url=str(member.avatar_url)))
  
  @commands.command(description="Give the bot something to say.", cls=cmd, example='say hi')
  async def say(self, ctx,*, msg = None):
      if not msg:
        return await ctx.message.reply(f"Please enter a message that you want me to say.")
      await ctx.send(msg)

  @commands.command(description='Sends a suggestion to the devs.', cls=cmd, example='suggest autoresponses.')
  async def suggest(self, ctx, *, suggestion):
      suggestion = suggestion + f"\n-{str(ctx.author)} in {str(ctx.guild)}"
      await Webhook.from_url('https://discord.com/api/webhooks/841555575450894357/fzpaPVVI4bLY4NTuScx5YoI0fbuFHKtPJIqi1XucvyZpKLIg0RJItL-P5F3QUDmZulqB', adapter=AsyncWebhookAdapter(self.client.session)).send(content=suggestion)
      await ctx.send('Suggestion sent <a:checkmark:857155755923734559>')

  @commands.command(description="Sets your afk.", cls=cmd, example='afk eating')
  async def afk(self, ctx, *, message=None):
    message = message or "AFK"
    if str(ctx.author.id) in self.client.afks.find_one({"_id": ctx.guild.id}):
      self.client.afks.update(self.client.afks.find_one({"_id": ctx.guild.id}), {"$unset": {str(ctx.author.id):self.client.afks.find_one({"_id": ctx.guild.id})[str(ctx.author.id)]}})
      await ctx.send('You are no longer afk.')
      return

    self.client.afks.update_one(self.client.afks.find_one({"_id": ctx.guild.id}),{"$set": {str(ctx.author.id): {"message": message, "time": str(arrow.utcnow())}}})
    await ctx.send(f'<a:checkmark:857155755923734559> Set your AFK: {message} ')

  @commands.Cog.listener()
  async def on_message(self, message):
    if not message.guild or not message.content:
      return
    if message.author.bot:
      return
    if "afk" in message.content.lower():
      return
    asyncio.create_task(self.afk_check(message))

  async def afk_check(self, message):
    if str(message.author.id) in self.client.afks.find_one({"_id": message.guild.id}):
      self.client.afks.update(self.client.afks.find_one({"_id": message.guild.id}), {"$unset": {str(message.author.id):self.client.afks.find_one({"_id": message.guild.id})[str(message.author.id)]}})
      await message.channel.send(f'Welcome back {message.author.mention}!')
    if message.mentions:
      for user in message.mentions:
        if str(user.id) in self.client.afks.find_one({"_id": message.guild.id}):
          if self.cooldown_map.get_bucket(message).update_rate_limit():
            return
          data = self.client.afks.find_one({"_id": message.guild.id})[str(user.id)]
          await message.channel.send(f"{user.display_name} is AFK: {data['message']} - {arrow.get(data['time']).humanize()}")

  @commands.command(description='Shows a member\'s playing spotify track.', cls=cmd, example='suggest autoresponses.')
  async def spotify(self, ctx, member: discord.Member=None):
    member = member or ctx.author
    if not member.activities:
      return await ctx.send(f'{member} is not listening to anything.')
    if not isinstance(ctx.author.activity, discord.Spotify):
      return await ctx.send(f'{member} is not listening to anything.')
    await ctx.send(f"**{member} is listening to {ctx.author.activity.title} by {ctx.author.activity.artist}**")

  def tts(self, text):
      tts = gTTS(text=text, lang="en")
      tts.save("tts.mp3")

  @commands.command(description="Text to speech command.", cls=cmd, example='tts hello world', aliases=['tts'])
  async def texttospeech(self, ctx, channel:typing.Optional[discord.VoiceChannel]=None, *, message=None):
      destination = channel
      if not destination:
          destination = ctx.author.voice
          if not destination:
              return await ctx.send('You are not in VC.')
          else:
              destination = ctx.author.voice.channel
      if not message:
          await ctx.send(f'What should I say?') 
          return    
      message = str(message)
      for member in ctx.message.mentions:
          message = message.replace(member.mention, f'@{member.name}')
      emotes = re.compile(r"<a?:([\w]+):[0-9]+>")
      text = emotes.sub(r"\1", message)
      text = text.replace('.', 'dot')
      voice = ctx.guild.voice_client
      if voice:
          if voice.channel != destination:
              if not ctx.voice_client.is_playing():
                  await ctx.voice_client.move_to(ctx.author.voice.channel)
              else:
                  return await ctx.send('I am already in another voice channel.')
      if voice is None or voice.channel is None:
          if not destination.permissions_for(ctx.guild.me).view_channel:
              await ctx.send('I cannot view your vc.')
              return
          if not destination.permissions_for(ctx.guild.me).connect:
              await ctx.send('I do not have permission to join your vc.')
              return
          if not destination.permissions_for(ctx.guild.me).speak:
              await ctx.send('I do not have permission to speak in your vc.')
              return
          await destination.connect()
      vc = ctx.voice_client
      if not vc:
          await ctx.send(f'I am not in a voice channel.')    
          return
      try:
          await ctx.message.add_reaction("🔊")
      except:
          pass
      await self.client.loop.run_in_executor(None, self.tts, text)
      try:
          vc.play(discord.FFmpegPCMAudio('tts.mp3'))
          vc.source = discord.PCMVolumeTransformer(vc.source)
          vc.source.volume = 1
      except Exception as e:
          await ctx.send(f"{e}")

  @commands.command(description="Do a poll", cls=cmd, example='poll am i cute?')
  async def poll(self, ctx, *, pollInfo):
      emb = (discord.Embed(description=pollInfo, color=self.client.color))
      emb.set_author(name=f"Poll by {ctx.message.author}", icon_url="https://cdn.discordapp.com/emojis/860926553256755210.gif")
      try:
          await ctx.message.delete()
      except discord.Forbidden:
          pass
      try:
          pollMessage = await ctx.send(embed=emb)
          await pollMessage.add_reaction("a:check:841468504233345034")
          await pollMessage.add_reaction("a:invalid:862843405486391317")
      except Exception as e:
          await ctx.send(f"Oops, I couldn't react to the poll. Check that I have permission to add reactions! ```py\n{e}```")

  @commands.command(description="Gives info on the bot", cls=cmd, example='info', aliases=['about'])
  async def info(self, ctx):
      embed = discord.Embed(title="Bot Satistics", description=f"Developers: mky#2900 & manny#1234\n[Sequence's Invite](https://discord.com/api/oauth2/authorize?client_id={self.client.user.id}&permissions=8&scope=applications.commands%20bot) [Support Server](https://discord.gg/6BdzNJRWc3)", color=self.client.color)
   
      embed.add_field(name="**Stats**", value=f"Guilds: {len(ctx.bot.guilds)}\nUsers: {len(ctx.bot.users)}\n")
      embed.add_field(name="**Client**", value=f"Database: MongoDB\nLibrary: Discord.py\nLanguage: Python 3.8")
      embed.add_field(name="**Info**", value=f"Created: 5/5/21\nUptime: {(datetime.now()-self.client.start_time)}\nWebsocket latency: {round(self.client.latency * 1000)}ms")
      await ctx.send(embed=embed)

def setup(client):
  client.add_cog(Misc(client))