from discord import TextChannel, Role
from discord.ext.commands import Cog, Bot, Context, command
from discord.ext.tasks import loop

from cogs.bot_status import listener
from cogs.util.ainit_ctx_mgr import AinitManager
from cogs.util.assign_variables import assign_role
from cogs.util.placeholder import Placeholder
from core.global_enum import ConfigurationNameEnum
from core.logger import get_discord_child_logger
from core.predicates import has_role_plus, bot_chat

first_init = True
news = Placeholder()
nsfw = Placeholder()
verified: set[Role] = set()
bot_channels: set[TextChannel] = set()
logger = get_discord_child_logger("roles")


class Roles(Cog):
    """
    Some small role commands.
    """

    def __init__(self, bot: Bot):
        self.bot = bot
        self.need_init = True
        if not first_init:
            self.ainit.start()

    @listener()
    async def on_ready(self):
        global first_init
        if first_init:
            first_init = False
            self.ainit.start()

    @loop()
    async def ainit(self):
        """
        Loads the configuration for the module.
        """
        global news, nsfw, verified, bot_channels
        # noinspection PyTypeChecker
        async with AinitManager(bot=self.bot,
                                loop=self.ainit,
                                need_init=self.need_init,
                                bot_channels=bot_channels,
                                verified=verified) as need_init:
            if need_init:
                news.item = await assign_role(self.bot, ConfigurationNameEnum.NEWSLETTER)
                nsfw.item = await assign_role(self.bot, ConfigurationNameEnum.NSFW)
        logger.info(f"The cog is online.")

    def cog_unload(self):
        logger.warning("Cog has been unloaded.")

    # Not Safe For Work

    @command(name="nsfw-add",
             help="Add nsfw role")
    @has_role_plus(verified)
    @bot_chat(bot_channels)
    async def nsfw_add(self, ctx: Context):
        global nsfw
        await ctx.author.add_roles(nsfw.item, reason="request by user")
        await ctx.reply(content=f"{ctx.author.mention} added you to the {nsfw.item.name} role")

    @command(name="nsfw-rem",
             help="Remove nsfw role")
    @bot_chat(bot_channels)
    async def nsfw_rem(self, ctx: Context):
        global nsfw
        await ctx.author.remove_roles(nsfw.item, reason="request by user")
        await ctx.reply(content=f"{ctx.author.mention} removed you from the {nsfw.item.name} role")

    # News

    @command(name="news-add",
             help="Add news role")
    @has_role_plus(verified)
    @bot_chat(bot_channels)
    async def news_add(self, ctx: Context):
        global news
        await ctx.author.add_roles(news.item, reason="request by user")
        await ctx.reply(content=f"{ctx.author.mention} added you to the {news.item.name} role")

    @command(name="news-rem",
             help="Remove news role")
    @bot_chat(bot_channels)
    async def news_rem(self, ctx: Context):
        global news
        await ctx.author.remove_roles(news.item, reason="request by user")
        await ctx.reply(content=f"{ctx.author.mention} removed you from the {news.item.name} role")


async def setup(bot: Bot):
    await bot.add_cog(Roles(bot))
