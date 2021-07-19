import discord, math, asyncio, contextlib

class Pages():
  def __init__(self, ctx, pages, **kwargs):
    self.ctx = ctx
    self.pages = [str(p) for p in pages]
    self.title = kwargs.get('title') or None
    self.author = kwargs.get('author') or None
    self.author_icon = kwargs.get('author_icon') or None
    self.footer = kwargs.get('footer') or None
    self.footer_icon = kwargs.get('footer_icon') or None
    self.image = kwargs.get('image') or None
    self.thumbnail = kwargs.get('thumbnail') or None
    self.color = kwargs.get('color') or None
    self.per_page = kwargs.get('per_page') or None
    self.max_pages =  math.ceil(len(pages)/self.per_page)
    self.current_page = 1 
    self.active = True

  def generate_page(self):
    current = self.pages[(self.current_page - 1)*self.per_page:self.current_page*self.per_page]
    embed = discord.Embed(description=' '.join(current), color=self.color)
    if self.title:
      embed.title = self.title
    footer_kwargs = {} 
    if self.max_pages > 1:
      embed.set_footer(text=f'{self.current_page}/{self.max_pages}')
    if self.footer:
        footer_kwargs['text'] = self.footer
        if self.max_pages > 1:
          footer_kwargs['text'] = self.footer + f' | {self.current_page}/{self.max_pages}'
    if self.footer_icon:
        footer_kwargs['icon_url'] = self.footer_icon
    if len(footer_kwargs) > 0:
        embed.set_footer(**footer_kwargs)

    author_kwargs = {}
    if self.author:
        author_kwargs['name'] = self.author
    if self.author_icon:
        author_kwargs['icon_url'] = self.author_icon
    if len(author_kwargs) > 0:
        embed.set_author(**author_kwargs)

    if self.image:
      embed.set_image(url=self.image)
    if self.thumbnail:
      embed.set_thumbnail(url=self.thumbnail)
    return embed

  async def start(self):
    m = await self.ctx.send(embed=self.generate_page())
    if self.max_pages <= 1:
      return
    await m.add_reaction('⬅️')
    await m.add_reaction('⏹️')
    await m.add_reaction('➡️')
    def check(r, u):
        return u == self.ctx.author and r.emoji in ['⬅️', '⏹️','➡️'] and r.message == m
    with contextlib.suppress(discord.NotFound):
      while self.active:
        done, pending = await asyncio.wait([self.ctx.bot.wait_for('reaction_add', check=check), self.ctx.bot.wait_for('reaction_remove', check=check)], return_when=asyncio.FIRST_COMPLETED, timeout=60)
        reaction = None

        try:
          m.author
        except:
          break

        try:
          reaction, user = done.pop().result()
        except:
          await m.clear_reactions()
          break

        for future in done:
          if future.exception():
            await m.clear_reactions()
            break

        for future in pending:
          future.cancel()

        if not reaction:
          await m.clear_reactions()
          break
        
        if str(reaction.emoji) == '⬅️':
          if self.current_page <= 1:
            self.current_page = self.max_pages  
          else:
            self.current_page -= 1
        elif str(reaction.emoji) == '➡️':
          if self.current_page == self.max_pages:
            self.current_page = 1
          else:
            self.current_page += 1
        else:
          await m.clear_reactions()
          break
        await m.edit(embed=self.generate_page())