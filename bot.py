from discord.ext import commands
from utils import config as cfg
import os


bot = commands.Bot(command_prefix=cfg.config[0]['discord']['prefix'],
                   description='Bot para agendamento de estudos da Comunidade Mentoria IAC',
                   reconnect=True)

@bot.event
async def on_ready():
    print("Username: {0}\nID: {0.id}".format(bot.user))

    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            bot.load_extension(f'cogs.{filename[:-3]}')


async def on_command_error(self, ctx, error):
    if isinstance(error, (commands.CommandNotFound, commands.BadArgument, commands.MissingRequiredArgument)):
        return await ctx.send(error)
    else:
        return

bot.run(cfg.config[0]['discord']["token"])
