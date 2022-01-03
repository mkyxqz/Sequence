import pymongo, aiohttp
from discord.ext import commands
from datetime import datetime

async def create_session(loop):
  return aiohttp.ClientSession(loop=loop)

class sequence(commands.Bot):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.color = 0xFF0000
    self.start_time = datetime.now()
    self.mongoclient = pymongo.MongoClient(
        'MONGODB SERVER HERE'
    )
    self.database = self.mongoclient['bot_db']
    self.welcome = self.database['welcome_message']
    self.ars = self.database['autoresposes']
    self.session = self.loop.run_until_complete(create_session(self.loop))
      
    async def close(self):
      await self.session.close()
      await super().close()
