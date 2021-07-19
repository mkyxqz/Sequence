from utils.fm import get_user, set_user, get_recent_track_data, get_scrobbles, get_artist_real_name, get_recent_10, get_user_info, get_top_artists
import discord, datetime
from discord.ext import commands
from utils.misc import cmd
reactions = ["🔥","🗑️"]

class FM(commands.Cog):
  def __init__(self, client):
    self.client = client

  @commands.command(description="Shows a users recently scrobbled track.", cls=cmd, example='fm dremo')
  async def fm(self, ctx, member:discord.Member=None):
    member = member or ctx.author
    data = get_user(self.client, member.id)
    if not data:
      return await ctx.send(f'{member} has not set a Last.fm username.')
    username = data
    total_scrobbles, artist, track, album, song_link, image, date = await get_recent_track_data(self.client, username)
    if not artist:
        return await ctx.send("No track data was found.")
    scrobbles = await get_scrobbles(self.client, username, artist, track)
    artist, artist_link = await get_artist_real_name(self.client, artist)
    
    date_obj = discord.Embed.Empty 
    
    em = discord.Embed(timestamp=date_obj, color= ctx.bot.color)
    if date != "true":
        date_obj = datetime.datetime.fromtimestamp(int(date))
        em.set_author(name=f'Last played | {username}', icon_url=member.avatar_url)
    else:
        em.set_author(name=f'Now playing | {username}', icon_url=member.avatar_url)
    em.set_thumbnail(url=image)
    em.add_field(name='Artist', value=f'[{artist}]({artist_link})', inline=False)
    em.add_field(name='Track', value=f'[{track}]({song_link})', inline=False)
    em.set_footer(text=f'Scrobbles for {track}: {scrobbles} | Total Scrobbles: {total_scrobbles}')
    m = await ctx.send(embed=em)
    try:
        for emoji in reactions:
            await m.add_reaction(emoji)
    except:
        pass

  @commands.command(description="Sets Last.fm username.", cls=cmd, example='fmset dremofloyd')
  async def fmset(self, ctx, username):
    status = await set_user(self.client, ctx.author.id, username)
    if not status:
      return await ctx.send(f'{username} is not a valid Last.fm username.')
    await ctx.send(embed=discord.Embed(color=self.client.color,description=f"Last.fm set to [{username}]({status})"))

  @commands.command(description='Displays recent scrobbles.', cls=cmd, example='recents @Manny')
  async def fmrecents(self, ctx, member : discord.Member =None):
    member = member or ctx.author
    username = get_user(self.client, member.id)
    if not username:
      return await ctx.send(f'{member} has not set a Last.fm username.')
    async with ctx.channel.typing():
      registered, username, url, image, scrobbles = await get_user_info(self.client, username)
      data = await get_recent_10(self.client, username)
      top_artists_names = [f'{number}: [{name["name"]}]({name["url"]}) by {name["artist"]["#text"]}' for number, name in enumerate(data, 1)]
      top_artists_string = "\n".join(top_artists_names)
      embed = discord.Embed(description = f"{top_artists_string}",color = self.client.color)
      embed.set_footer(text=f'Total scrobbles: {scrobbles}')
      embed.set_thumbnail(url=image)
      embed.set_author(name=f"Recent scrobbles for {username}", icon_url=member.avatar_url)
      await ctx.send(embed=embed)

  @commands.command(description='Shows a member\'s top artists.', aliases=['fmta'], cls=cmd, example='fmtopartists @dremo')
  @commands.bot_has_permissions(embed_links=True, attach_files=True)
  async def fmtopartists(self, ctx, member:discord.Member=None):
    member = member or ctx.author
    username = get_user(self.client, member.id)
    if not username:
      return await ctx.send(f'{member} has not set a Last.fm username.')
    async with ctx.channel.typing():
      data = await get_top_artists(self.client, username)
      top_artists_names = [f'{number}: [{name["name"]}]({name["url"]}) ({name["playcount"]} plays)' for number, name in enumerate(data[:10], 1)]
      top_artists_string = "\n".join(top_artists_names)
      embed = discord.Embed(description = f"{top_artists_string}", color = ctx.bot.color)
      artist_str = f'{len([name for name in data])} different artists in this time period'
      if int(len([name for name in data])) == 1:
          artist_str = '1 artist in this time period'
      if int(len([name for name in data])) == 1000:
          artist_str = '1000+ artists in this time period'
      embed.set_author(name=f"Top 10 artists overall for {username}", icon_url=member.avatar_url)
      embed.set_footer(text=str(artist_str))
    await ctx.send(embed=embed)    

  @commands.command(description='FM account setup instructions.') 
  async def fmsetup(self, ctx):
    embed = discord.Embed(color = ctx.bot.color, description=f'**first**\ncreate an account [here](https://www.last.fm/join)\n**then**\nconnect your spotify [here](https://www.last.fm/settings/application)\n**lastly**\nset your account using\n{ctx.prefix}fmset [Last.fm username]')
    await ctx.send(embed=embed)



def setup(client):
  client.add_cog(FM(client))