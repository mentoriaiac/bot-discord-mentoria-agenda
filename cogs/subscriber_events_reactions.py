from discord.ext import tasks, commands
from utils import config as cfg
from utils.google_calendar import list_events
from datetime import date, datetime
from dateutil.parser import parse
import discord


class Calendar(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        channel = await self.bot.fetch_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        user = await self.bot.fetch_user(payload.user_id)
        emoji = payload.emoji
        if str(emoji) == "✅":
            calendar = await self.bot.pg_con.fetch(
                "SELECT event_name, calendar_id, event_link FROM events WHERE message_id = $1",
                message.id,
            )
            calendar = calendar[0]
            if calendar:
                user_notify = await self.bot.pg_con.fetch(
                    "SELECT * FROM notifications WHERE user_id = $1 AND message_id = $2 AND calendar_id = $3",
                    payload.user_id,
                    payload.message_id,
                    str(calendar[1]),
                )
                if not user_notify:
                    await self.bot.pg_con.execute(
                        "INSERT INTO notifications (user_id, message_id, calendar_id, event_link ) VALUES ($1, $2, $3, $4)",
                        payload.user_id,
                        payload.message_id,
                        str(calendar[1]),
                        str(calendar[2]),
                    )
                    embed = discord.Embed(
                        title="📚 Lembrete de estudo :loudspeaker: ",
                        description=f"Você escolheu ser aviso de um evento. {calendar[0]}",
                    )
                    embed.add_field(
                        name=f"Descrição:",
                        value=f"Você será avisado do evento da comunidade Mentoria IAC",
                        inline=False,
                    )
                    await user.send(embed=embed)
            else:
                await user.send(user)


def setup(bot):
    bot.add_cog(Calendar(bot))
