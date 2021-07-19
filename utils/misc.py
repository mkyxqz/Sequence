import discord, re, json
from num2words import num2words
from discord.ext import commands

def add_point(user):
  with open('logodb.json', 'r') as file:
    data = json.loads(file.read())
  if str(user.id) not in data:
    data[str(user.id)] = 0
  data[str(user.id)] += 1
  with open('logodb.json', 'w+') as file:
    file.write(json.dumps(data, indent=4))
  return data[str(user.id)]

logos = {
  "Adidas": "0",
  "ADT": "1",
  "Airbnb": "2",
  "Amazon": "3",
  "AMD": "4",
  "Anker": "5",
  "Apple": "6",
  "Asos": "7",
  "Atari": "8",
  "Balenciaga": "9",
  "Bandai Namco": "10",
  "Band M Bargains": "11",
  "Bank Of America": "12",
  "Barclays": "13",
  "Bing": "14",
  "Bitcoin": "15",
  "BMW": "16",
  "Booking": "17",
  "BP": "18",
  "Capcom": "19",
  "Champion": "20",
  "Cisco": "21",
  "Citroen": "22",
  "CNBC": "23",
  "Coke": "24",
  "Costa": "25",
  "Crunchyroll": "26",
  "Dodge": "27",
  "Dolby": "28",
  "Dominos": "29",
  "DreamWorks": "30",
  "Ducati": "31",
  "Ebay": "32",
  "Eizo": "33",
  "Ericsson": "34",
  "Facebook": "35",
  "Fjallraven": "36",
  "Ford": "37",
  "Github": "38",
  "Givenchy": "39",
  "Google": "40",
  "Goyard": "41",
  "Gucci": "42",
  "Honda": "43",
  "Huawei": "44",
  "IBM": "45",
  "Infiniti": "46",
  "Intel": "47",
  "Jaguar": "48",
  "John Deere": "49",
  "Kappa": "50",
  "KFC": "51",
  "Koenigsegg": "52",
  "Lamborghini": "53",
  "Lexus": "54",
  "LG": "55",
  "Liteon": "56",
  "Louis Vuitton": "57",
  "Maersk": "58",
  "Mazda": "59",
  "McDonalds": "60",
  "Mercedes Benz": "61",
  "Microsoft": "62",
  "Mitsubishi": "63",
  "Monster": "64",
  "Monster Cable": "65",
  "MTV": "66",
  "Nandos": "67",
  "Napster": "68",
  "Nestle": "69",
  "Netflix": "70",
  "Nike": "71",
  "Nintendo": "72",
  "Novation": "73",
  "Nvidia": "74",
  "Papa Johns": "75",
  "Patagonia": "76",
  "Peugeot": "77",
  "Philips": "78",
  "Pioneer": "79",
  "PizzaHut": "80",
  "Playboy": "81",
  "Playstation": "82",
  "Porsche": "83",
  "Rayban": "84",
  "Razer": "85",
  "RedBull": "86",
  "RioTinto": "87",
  "Rossignol": "88",
  "Samsung": "89",
  "Sanyo": "90",
  "SAP": "91",
  "Shell": "92",
  "Skull candy": "93",
  "Skype": "94",
  "Snapchat": "95",
  "Sonos": "96",
  "Sony": "97",
  "Soundcloud": "98",
  "Spotify": "99",
  "Starbucks": "100",
  "Steam": "101",
  "Subway": "102",
  "Superdry": "103",
  "Supreme": "104",
  "Tannoy": "105",
  "Tesla": "106",
  "The Hundreds": "107",
  "Timberland": "108",
  "Toyota": "109",
  "Twitch": "110",
  "Twitter": "111",
  "Uber": "112",
  "Ubisoft": "113",
  "Vine": "114",
  "Visa": "115",
  "Volkswagen": "116",
  "Wikipedia": "117",
  "Xbox": "118",
  "Yamaha": "119",
  "YSL": "120"
}

class cmd(commands.Command):
    def __init__(self, *args, **kwargs):
        self.example = kwargs.get('example') or None
        self.permissions = kwargs.get('permissions') or None
        super().__init__(*args, **kwargs)

def clean_prefix(client, prefix):
  return re.sub(f'<@!?{client.user.id}>', '@'+ client.user.name, prefix)

async def send_command_help(ctx, missing_permissions, usage):   
  embed = discord.Embed(color=0xFF0000, title=ctx.command.qualified_name, description=ctx.command.description)
  if ctx.command.aliases:
    embed.add_field(name="Aliases", value=" | ".join(ctx.command.aliases), inline=True)
  if ctx.command.clean_params:
    embed.add_field(name="Parameters", value=" | ".join(list(ctx.command.clean_params)), inline=True)
  embed.add_field(name="Permissions", value=missing_permissions, inline=True)
  embed.add_field(name="Usage", value=usage, inline=True)
  await ctx.send(embed=embed)

def variables(member):
  return {
    "{member}": member.mention,
    "{member_tag}": str(member),
    "{member_name}": member.name,
    "{member_avatar}": str(member.avatar_url),
    "{member_discrim}": member.discriminator,
    "{member_nick}": member.display_name,
    "{member_joindate}": member.joined_at.strftime("%m/%d/%Y, %H:%M:%S"),
    "{member_createdate}": member.created_at.strftime("%m/%d/%Y, %H:%M:%S"),
    "{server_name}": member.guild.name, 
    "{server_membercount}": str(member.guild.member_count),
    "{server_membercount_ordinal}": str(num2words(member.guild.member_count, to="ordinal_num")),
    "{server_membercount_nobots}": str(len([m for m in member.guild.members if not m.bot])),
    "{server_membercount_nobots_ordinal}": str(num2words(len([m for m in member.guild.members if not m.bot]), to="ordinal_num")),
    "{server_botcount}": str(len([m for m in member.guild.members if m.bot])),
    "{server_botcount_ordinal}": str(num2words(len([m for m in member.guild.members if not m.bot]), to="ordinal_num")),
    "{server_icon}": str(member.guild.icon_url),
    "{server_owner}": str(member.guild.owner),
    "{server_createdate}": member.guild.created_at.strftime("%m/%d/%Y, %H:%M:%S"),
    "{server_boostlevel}": str(member.guild.premium_tier),
    "{server_boostcount}": str(member.guild.premium_subscription_count)
  }

def to_var(text, member):
  for var, initial in variables(member).items():
    text = text.replace(var, initial)
  return text

async def send_welcome_message_test(ctx):
  data = ctx.bot.welcome.find_one({"_id": ctx.guild.id})
  embed = discord.Embed(color=data['color'])
  if data['title'].lower() != 'none':
    embed.title = to_var(data['title'], ctx.author)
  if data['description'].lower() != 'none':
    embed.description = to_var(data['description'], ctx.author)
  author = {}
  if data['author_name'].lower() != 'none':
      author['name'] = to_var(data['author_name'], ctx.author)
  if data['author_icon'].lower() != 'none':
      author['icon_url'] = to_var(data['author_icon'], ctx.author)
  if len(author) > 0:
      try:
          embed.set_author(**author)
      except:
          pass
  footer = {}
  if data['footer_text'].lower() != 'none':
      footer['text'] = to_var(data['footer_text'], ctx.author)
  if data['footer_icon'].lower() != 'none':
      footer['icon_url'] = to_var(data['footer_icon'], ctx.author)
  if len(footer) > 0:
      try:
          embed.set_footer(**footer)
      except:
          pass
  if data['image'].lower() != 'none':
    embed.set_image(url=to_var(data['image'], ctx.author))
  if data['thumbnail'].lower() != 'none':
    embed.set_thumbnail(url=to_var(data['thumbnail'], ctx.author))
  if data['timestamp']:
    embed.timestamp = ctx.message.created_at
  message = to_var(data['message'], ctx.author)
  if message.lower() == 'none':
    message = ''
  if not data['enabled']:
   return await ctx.send(f'Welcome message is not enabled, use {ctx.prefix}toggle') 
  if not ctx.bot.get_channel(data['channel']):
    return await ctx.send(f'No channel has been set, use {ctx.prefix}channel')
  try:
    if data['title'].lower() == data['description'].lower() == data['author_name'].lower() == data['footer_text'].lower() == data['image'].lower() == data['thumbnail'].lower() == 'none' and not data['timestamp']:
      if message == '':
        return await ctx.bot.get_channel(data['channel']).send('No message to send.')
      return await ctx.bot.get_channel(data['channel']).send(message)
    await ctx.bot.get_channel(data['channel']).send(content= message,embed=embed)
  except Exception as error:
    await ctx.bot.get_channel(data['channel']).send(f'`An error occured:` {error}')

async def send_welcome_message(client, member):
  data = client.welcome.find_one({"_id": member.guild.id})
  embed = discord.Embed(color=data['color'])
  if data['title'].lower() != 'none':
    embed.title = to_var(data['title'], member)
  if data['description'].lower() != 'none':
    embed.description = to_var(data['description'], member)
  author = {}
  if data['author_name'].lower() != 'none':
      author['name'] = to_var(data['author_name'], member)
  if data['author_icon'].lower() != 'none':
      author['icon_url'] = to_var(data['author_icon'], member)
  if len(author) > 0:
      try:
          embed.set_author(**author)
      except:
          pass
  footer = {}
  if data['footer_text'].lower() != 'none':
      footer['text'] = to_var(data['footer_text'], member)
  if data['footer_icon'].lower() != 'none':
      footer['icon_url'] = to_var(data['footer_icon'], member)
  if len(footer) > 0:
      try:
          embed.set_footer(**footer)
      except:
          pass
  if data['image'].lower() != 'none':
    embed.set_image(url=to_var(data['image'], member))
  if data['thumbnail'].lower() != 'none':
    embed.set_thumbnail(url=to_var(data['thumbnail'], member))
  if data['timestamp']:
    embed.timestamp = member.joined_at
  message = to_var(data['message'], member)
  if message.lower() == 'none':
    message = ''
  if not data['enabled']:
   return
  if not client.get_channel(data['channel']):
    return 
  try:
    if data['title'].lower() == data['description'].lower() == data['author_name'].lower() == data['footer_text'].lower() == data['image'].lower() == data['thumbnail'].lower() == 'none' and not data['timestamp']:
      return await client.get_channel(data['channel']).send(message)
    await client.get_channel(data['channel']).send(content= message,embed=embed)
  except Exception as error:
    await client.get_channel(data['channel']).send(f'`An error occured:` {error}')