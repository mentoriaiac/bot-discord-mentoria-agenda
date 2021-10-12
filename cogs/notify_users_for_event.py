from discord.ext import tasks, commands
from utils import config as cfg
from utils.google_calendar import list_events
from datetime import date
from dateutil.parser import parse
import discord, datetime
from dateutil import tz


async def notify(channel):

    eventos = list_events.getEvents()
    data = date.today().strftime("%d %b %Y")

    if not eventos:
        embed = discord.Embed(
            title="📚 Agenda de Estudos :loudspeaker: ", description=data
        )
        embed.add_field(
            name=f"**:cold_sweat: Sem Agenda**",
            value=f"Use ```>criar_agenda```  e agende um estudo, bora aprender!! ",
            inline=False,
        )
        embed.set_footer(
            text="Se você está afim de aprender algo, agende um momento de estudo, para que os demais possam saber do seu interesse."
        )
        await channel.send(embed=embed)
    else:
        embed = discord.Embed(
            title="📚 Agenda de Estudos :loudspeaker: ", description=data
        )
        for event in eventos:
            data = parse(event["start"]["dateTime"])
            embed.add_field(
                name=f"**:white_check_mark: {event['summary']}**",
                value=f" Local:  {event['location']} Horário: {data.time()} ",
                inline=False,
            )
            embed.add_field(
                name=f"Descrição:", value=f"```{event['description']}``` ", inline=False
            )
            embed.set_footer(
                text="Agenda: ✅ - Ativa - 🟥 - Cancelada(provavelmente já passou do horário)"
            )
        await channel.send(embed=embed)


class Calendar(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.calendar_cron.start()

    def cog_unload(self):
        self.calendar_cron.cancel()

    @tasks.loop(minutes=1)
    async def calendar_cron(self):
        events = await self.bot.pg_con.fetch(
            "SELECT date_time FROM events WHERE notified = false"
        )
        for event in events:
            dt = datetime.datetime.strptime(
                str(event["date_time"]), "%Y-%m-%d %H:%M:%S%z"
            )
            dt_now = datetime.datetime.now(tz=cfg.TZ).strftime("%Y-%m-%d %H:%M:%S%z")
            dt_now = datetime.datetime.strptime(str(dt_now), "%Y-%m-%d %H:%M:%S%z")
            event_date = datetime.datetime(
                dt.year, dt.month, dt.day, dt.hour, 0, 00, 0, tzinfo=cfg.TZ
            )
            if event_date < dt_now:
                pass
        #         channel = self.bot.get_channel(cfg.notify_channel)
        #         await notify(channel)
        #         await self.bot.pg_con.execute("UPDATE events SET notified = true WHERE date_time = $1", event['date_time'])
        #         self.bot.pg_con.commit()
        # data = events[0]
        # user_notify = await self.bot.pg_con.fetch("SELECT * FROM notifications WHERE user_id = $1 AND message_id = $2 AND calendar_id = $3",  payload.user_id, payload.message_id, str(calendar_id[0]))
def setup(bot):
    bot.add_cog(Calendar(bot))
