from discord.ext import commands
from utils import config as cfg
import os
import asyncpg

bot = commands.Bot(command_prefix=cfg.config[0]['discord']['prefix'],
                   description='Bot para agendamento de estudos da Comunidade Mentoria IAC',
                   reconnect=True)


async def create_database_pool():
    bot.pg_con = await asyncpg.create_pool(user=cfg.config[0]['postgres']['user'], password=cfg.config[0]['postgres']['password'], database=cfg.config[0]['postgres']['database'], host=cfg.config[0]['postgres']['host'], port=5432)
    await bot.pg_con.execute("CREATE TABLE IF NOT EXISTS Events (id  SERIAL PRIMARY KEY, message_id bigint, calendar_id text, date_time timestamp with time zone, event_name text , event_link text);")
    await bot.pg_con.execute("CREATE TABLE IF NOT EXISTS Notifications (id SERIAL PRIMARY KEY, user_id bigint, message_id bigint, calendar_id text, event_link text );")



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

bot.loop.run_until_complete(create_database_pool())
bot.run(cfg.config[0]['discord']["token"])
