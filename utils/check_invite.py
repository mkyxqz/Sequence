import re

def findcodes(content):
  return re.findall(r'(?:https?:\/\/)?discord(?:app)?\.(?:com\/invite|gg)\/([a-zA-Z0-9]+)\/?', content)

async def check(client, message, code):
  async with client.session.get(f'https://discordapp.com/api/v9/invites/{code}') as res:
    if res.status == 200:
      json = await res.json()
      if int(json['guild']['id']) != int(message.guild.id):
        return False
      return True
    return True

async def resolve(client, message):
  codes = findcodes(message.content)
  if not codes:
    return
  for code in codes:
    if not (await check(client, message, code)):
     await message.delete()
     break
    