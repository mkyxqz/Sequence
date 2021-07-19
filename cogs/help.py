import discord
from discord.ext import commands
from utils.misc import cmd, clean_prefix

class Help(commands.Cog):
  def __init__(self, client):
    self.client = client

  def filter(self, command):
    return command.qualified_name

  def cog_filter(self, cog):
    return str(cog)

  @commands.command(description='Shows this message.', cls=cmd, example='help message', permissions='SEND_MESSAGES', hidden=True)
  async def help(self, ctx, command_cog:str = None):
    if not command_cog:
      string = ''
      for cog in sorted(self.client.cogs, key=self.cog_filter):
        cog = self.client.get_cog(cog)
        if not cog.get_commands():
          continue
        else:
          c = []
          for command in sorted(cog.walk_commands(), key=self.filter):
            if not command.hidden:
              c.append(command) 
          if not c:
            continue

          string += f"**{cog.qualified_name}** [{len(c)}]\n{clean_prefix(self.client, ctx.prefix)}help {cog.qualified_name}\n"
      embed = discord.Embed(color=self.client.color, description=string)
      embed.set_author(name=f'{self.client.user.name} Commands:', icon_url=self.client.user.avatar_url)
      embed.set_footer(text=f'{clean_prefix(self.client, ctx.prefix)}help [command]/[cog] for more information about a command or cog.')
      await ctx.send(embed=embed)
    else: 
      cog = self.client.get_cog(command_cog)
      if cog:
          string = ''
          for command in sorted(cog.walk_commands(), key=self.filter):
            string += f'{command.name} - {command.description}\n'
          embed = discord.Embed(title=f' '+str(cog.qualified_name), color=self.client.color, description=string)
          await ctx.send(embed=embed)
      else:
        command = self.client.get_command(command_cog)
        if not command:
          return await ctx.send('That command/cog was not found.')
        else:
          embed = discord.Embed(color=self.client.color,title=command.name, description=command.description)
          params = " | ".join([f'[{p}]' for p in command.clean_params])
          embed.add_field(name='Usage:', value=f'{clean_prefix(self.client, ctx.prefix)}{command.name} {params}', inline=False)
          if hasattr(command, 'example'):
            if command.example:
              embed.add_field(name='Example:', value=f'{clean_prefix(self.client, ctx.prefix)}{command.example}', inline=False)
          if hasattr(command, 'permissions'):
            if command.permissions:
              embed.add_field(name='Permission:', value=f'{command.permissions}', inline=False)
          if command.aliases:
            embed.add_field(name='Aliases:', value=' | '.join(command.aliases))
          await ctx.send(embed=embed)

def setup(client):
  client.add_cog(Help(client))