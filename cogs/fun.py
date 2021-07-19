import discord, requests, asyncio, random, pyfiglet, json, typing, spotify, unicodedata, functools, io, os
from discord.ext import commands
from discord.ext.commands import clean_content
from utils.misc import cmd, logos, add_point
from datetime import datetime

class Fun(commands.Cog):
  def __init__(self, client):
    self.client = client
    self.cooldown_map = commands.CooldownMapping.from_cooldown(3, 15, commands.BucketType.member)

  @commands.command(description='Guess that logo game.')
  @commands.cooldown(1, 7, commands.BucketType.channel)
  async def logo(self, ctx): 
    '''Guess the given logo.'''
    logo = random.choice([logo for logo in logos])
    e = discord.Embed(color=self.client.color)
    f = discord.File(f'utils/logos/Logos/{logos[logo]}.png', filename=f'{logos[logo]}.png')
    e.set_image(url=f'attachment://{logos[logo]}.png')
    e.set_author(name='Guess the logo.')
    await ctx.send(embed=e, file=f)
    tries = []
    failed = True
    def check(m):
      return m.channel == ctx.channel and not m.author.bot
    while True:
        try:
          mes = await self.client.wait_for('message', check=check, timeout=20)
          if len(tries) != 5:
            if str(mes.content.lower()) == logo.lower():
              await mes.add_reaction('✅')
              failed = False
              winner = mes.author
              break 
            else:
              await mes.add_reaction('🚫')
              tries.append(1)
          else:
            if str(mes.content.lower()) == logo.lower():
              await mes.add_reaction('✅')
              failed = False
              winner = mes.author
              break 
            else:
              await mes.add_reaction('🚫')
              await ctx.send(f'The correct answer was {logo.lower()}.')
              failed = True
              break
        except asyncio.TimeoutError:
          await ctx.send(f'The correct answer was {logo.lower()}.')
          failed = True
          break
    if not failed:
      points = add_point(winner)
      e = discord.Embed(color=self.client.color)
      f = discord.File(f'utils/logos/Answers/{logos[logo]}.png', filename=f'{logos[logo]}.png')
      e.set_image(url=f'attachment://{logos[logo]}.png')
      e.set_author(name=f'{winner.name} was correct.', icon_url=str(winner.avatar_url))
      e.set_footer(text=f'{winner.name}\'s correct guesses: {points}')
      await ctx.send(embed=e, file=f)  

  @commands.command(description='Users with the most points for logo game.')
  async def logolb(self, ctx):
    with open('logodb.json') as file:
      data = json.loads(file.read())
    lb = '\n'.join(f'<@{ID}> : {data[ID]}' for ID in dict(sorted(list(data.items())[:15], key=lambda item: item[1], reverse=True)))
    await ctx.send(f'**__Top Users__**\n{lb}', allowed_mentions=discord.AllowedMentions.none())

  @commands.command(description="Gives advice", cls=cmd, example='advice',)
  async def advice(self, ctx):
      url = "https://api.adviceslip.com/advice"
      response = requests.get(url)
      advice = response.json()
      real_advice = advice['slip']['advice']
      await ctx.message.reply(real_advice)   

  @commands.command(description="Puts tect into ascii", cls=cmd, example='ascii hi',)
  async def ascii(self, ctx, text = None):
      if text == None:
          await ctx.message.reply(f"Please enter some text.")
      else:
          if len(pyfiglet.figlet_format(text)) > 2000:
              await ctx.message.reply(f"Text too long. Please enter short text.")
          else:
              await ctx.message.reply(f"```{pyfiglet.figlet_format(text)}```")

  @commands.command(description="Turns ur text crazy", cls=cmd, example='crazy sequence')
  async def crazy(self, ctx, *, text=None):

      if text == None:
          await ctx.message.reply("Please enter some text!")
      else:

          filter = ['@here', '@everyone', '<@&', '<@!']

          for word in filter:
              if text.count(word) > 0:
                  await ctx.message.reply(f"Im not pinging anyone bozo!")
                  return

          res = ""
          for c in text:
              chance = random.randint(0,1)
              if chance:
                  res += c.upper()
              else:
                  res += c.lower()
          await ctx.message.reply(res)



  @commands.command(description="Puts spaces in ur text", cls=cmd, example='space aaa\n;space hi | i\n;space hi | b', aliases=["spaces"])
  async def space(self, ctx, *, args=None):
      if args == None:
          await ctx.send("Invalid args. Try doing `;help space` if you need help!")
          return

      if args.count(" | ") == 0:
          m = "n"
      else:
          m = args[-1]

      s = ""
      if m == "b":
          s += "**"
      elif m == "i":
          s += "_"

      msg = "".join(args.split(" | ")[0])
      args = args.split(" | ")[:-1]
      for c in msg:
          s += c + " "
      if m == "b":
          s += "**"
      elif m == "i":
          s += "_"

      await ctx.message.reply(s)

  @commands.command(description="Shows how gay you are", cls=cmd, example='gayscanner @user', aliases=['gay', 'scan', 'gayrate'])
  async def gayscanner(self, ctx,* ,user: clean_content=None):
        if not user:
            user = ctx.author.name
        gayness = random.randint(0,100)
        if gayness <= 33:
            gayStatus = random.choice(["No homo", 
                                       "Wearing socks", 
                                       '"Only sometimes"', 
                                       "Straight-ish", 
                                       "No homo bro", 
                                       "Girl-kisser", 
                                       "Hella straight"])
            gayColor = self.client.color
        elif 33 < gayness < 66:
            gayStatus = random.choice(["Possible homo", 
                                       "My gay-sensor is picking something up", 
                                       "I can't tell if the socks are on or off", 
                                       "Gay-ish", 
                                       "Looking a bit homo", 
                                       "lol half  g a y", 
                                       "safely in between for now"])
            gayColor = self.client.color
        else:
            gayStatus = random.choice(["LOL YOU GAY XDDD FUNNY", 
                                       "HOMO ALERT", 
                                       "MY GAY-SENSOR IS OFF THE CHARTS", 
                                       "STINKY GAY", 
                                       "BIG GEAY", 
                                       "THE SOCKS ARE OFF", 
                                       "HELLA GAY"])
            gayColor = self.client.color
        emb = discord.Embed(description=f"Gayness for **{user}**", color=gayColor)
        emb.add_field(name="Gayness:", value=f"{gayness}% gay")
        emb.add_field(name="Comment:", value=f"{gayStatus} :kiss_mm:")
        emb.set_author(name="Gay Scanner", icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/a/a4/ICA_flag.svg/2000px-ICA_flag.svg.png")
        await ctx.send(embed=emb)

  @commands.command(description="Ships you and the person", cls=cmd, example='ship @user @user')
  async def ship(self, ctx, name1 : clean_content, name2 : clean_content):
      shipnumber = random.randint(0,100)
      if 0 <= shipnumber <= 10:
          status = "Really low! {}".format(random.choice(["Friendzone ;(", 
                                                          'Just "friends"', 
                                                          '"Friends"', 
                                                          "Little to no love ;(", 
                                                          "There's barely any love ;("]))
      elif 10 < shipnumber <= 20:
          status = "Low! {}".format(random.choice(["Still in the friendzone", 
                                                    "Still in that friendzone ;(", 
                                                    "There's not a lot of love there... ;("]))
      elif 20 < shipnumber <= 30:
          status = "Poor! {}".format(random.choice(["But there's a small sense of romance from one person!", 
                                                    "But there's a small bit of love somewhere", 
                                                    "I sense a small bit of love!", 
                                                    "But someone has a bit of love for someone..."]))
      elif 30 < shipnumber <= 40:
          status = "Fair! {}".format(random.choice(["There's a bit of love there!", 
                                                    "There is a bit of love there...", 
                                                    "A small bit of love is in the air..."]))
      elif 40 < shipnumber <= 60:
        status = "Moderate! {}".format(random.choice(["But it's very one-sided OwO", 
                                                      "It appears one sided!", 
                                                      "There's some potential!", 
                                                      "I sense a bit of potential!", 
                                                      "There's a bit of romance going on here!", 
                                                      "I feel like there's some romance progressing!", 
                                                      "The love is getting there..."]))
      elif 60 < shipnumber <= 70:
        status = "Good! {}".format(random.choice(["I feel the romance progressing!", 
                                                  "There's some love in the air!", 
                                                  "I'm starting to feel some love!"]))
      elif 70 < shipnumber <= 80:
        status = "Great! {}".format(random.choice(["There is definitely love somewhere!", 
                                                    "I can see the love is there! Somewhere...", 
                                                    "I definitely can see that love is in the air"]))
      elif 80 < shipnumber <= 90:
          status = "Over average! {}".format(random.choice(["Love is in the air!", 
                                                            "I can definitely feel the love", 
                                                            "I feel the love! There's a sign of a match!", 
                                                            "There's a sign of a match!", 
                                                            "I sense a match!", 
                                                            "A few things can be imporved to make this a match made in heaven!"]))
      elif 90 < shipnumber <= 100:
          status = "True love! {}".format(random.choice(["It's a match!", 
                                                          "There's a match made in heaven!", 
                                                          "It's definitely a match!", 
                                                          "Love is truely in the air!", 
                                                          "Love is most definitely in the air!"]))

      if shipnumber <= 33:
          shipColor = self.client.color
      elif 33 < shipnumber < 66:
          shipColor = self.client.color
      else:
          shipColor = self.client.color

      emb = (discord.Embed(color=shipColor, \
                            title="Love test for:", \
                            description="**{0}** and **{1}** {2}".format(name1, name2, random.choice([
                                                                                                      ":sparkling_heart:", 
                                                                                                      ":heart_decoration:", 
                                                                                                      ":heart_exclamation:", 
                                                                                                      ":heartbeat:", 
                                                                                                      ":heartpulse:", 
                                                                                                      ":hearts:", 
                                                                                                      ":blue_heart:", 
                                                                                                      ":green_heart:", 
                                                                                                      ":purple_heart:", 
                                                                                                      ":revolving_hearts:", 
                                                                                                      ":yellow_heart:", 
                                                                                                      ":two_hearts:"]))))
      emb.add_field(name="Results:", value=f"{shipnumber}%", inline=True)
      emb.add_field(name="Status:", value=(status), inline=False)
      emb.set_author(name="Shipping", icon_url="https://media.discordapp.net/attachments/860254259526238248/862227211192369152/kis.jpeg?width=528&height=517")
      await ctx.send(embed=emb)

  @commands.command(description="shows ur pp size", cls=cmd, example='pp')
  async def pp(self, ctx, user: discord.Member = None):
      if user is None:
          user = ctx.author
      size = random.randint(1, 15)
      dong = ""
      for _i in range(0, size):
          dong += "="
      em = discord.Embed(title=f"**{user}'s pp**", description=f"8{dong}D", color=self.client.color)
      em.set_footer(text=f'Thats a nice pp')
      await ctx.send(embed=em)

  @commands.command(description="sends a roast", cls=cmd)
  async def roast(self, ctx):
      response = requests.get(url="https://evilinsult.com/generate_insult.php?lang=en&type=json")
      roast = json.loads(response.text)
      await ctx.reply(roast['insult'])

  @commands.command(description="enlarges a emote", cls=cmd, example='enlarge <a:check:841468504233345034>', pass_context=True, aliases=['bigemote'])
  async def enlarge(self, ctx, emoji):
      try:
          if emoji[0] == '<':
              name = emoji.split(':')[1]
              emoji_name = emoji.split(':')[2][:-1]
              anim = emoji.split(':')[0]
              if anim == '<a':
                  url = f'https://cdn.discordapp.com/emojis/{emoji_name}.gif'
              else:
                  url = f'https://cdn.discordapp.com/emojis/{emoji_name}.png'
              try:
                  await ctx.send(url)
              except Exception as e:
                  print(e)
                  async with self.session.get(url) as resp:
                      if resp.status != 200:
                          await ctx.send('```Emote not found.```')
                          return
                      img = await resp.read()

                  kwargs = {'parent_width': 1024, 'parent_height': 1024}
                  convert = False
                  task = functools.partial(Fun.generate, img, convert, **kwargs)
                  task = self.bot.loop.run_in_executor(None, task)
                  try:
                      img = await asyncio.wait_for(task, timeout=15)
                  except asyncio.TimeoutError:
                      await ctx.send("```Timed Out. Try again in a few seconds")
                      return
                  await ctx.send(file=discord.File(img, filename=name + '.png'))
            
      except Exception as e:
          await ctx.send(f"```Couldn't send emote.\n{e}```")

  @staticmethod
  def generate(img, convert, **kwargs):
      img = io.BytesIO(img)
      return img

def setup(client):
  client.add_cog(Fun(client))
