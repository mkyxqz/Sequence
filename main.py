import discord, os, asyncio
from discord.ext import commands
from utils.sequence import sequence
from utils.check_invite import resolve

async def get_prefix(client, message):
  if not message.guild:
    return
  try:
    data = client.prefixes.find_one({"_id": message.guild.id}) 
    return commands.when_mentioned_or(data['prefix'])(client, message)
  except:
    return commands.when_mentioned_or(';')(client, message)

client = sequence(command_prefix=get_prefix,    
  intents=discord.Intents.all(),
  help_command=None,
  activity=discord.Game(name=';help'),
  case_insensitive=True,
  allowed_mentions=discord.AllowedMentions(everyone=False, roles=False))

_cd = commands.CooldownMapping.from_cooldown(6, 17, commands.BucketType.member)
@client.check
async def cooldown_check(ctx):
    bucket = _cd.get_bucket(ctx.message)
    retry_after = bucket.update_rate_limit()
    if retry_after:
      raise commands.CommandOnCooldown(bucket, retry_after)
    return True

for file in os.listdir('cogs'):
	if file.endswith('.py'):
		try:
			client.load_extension(f'cogs.{file[:-3]}')
		except Exception as error:
			print(str(error))

client.run('bot token here')
