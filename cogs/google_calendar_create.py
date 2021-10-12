from typing import Pattern
from discord.ext import commands
import discord
import datetime, re, asyncio
from utils.google_calendar import create_event as event
from utils import config as cfg
from datetime import date
import logging
from dateutil.parser import parse


date_pattern = re.compile("^data:[0-3]?[0-9].[0-3]?[0-9].(?:[0-9]{2})?[0-9]{2}$")
hour_pattern = re.compile("^hora:([0-1]?[0-9]|2[0-3]):[0-5][0-9]$")



class Calendar(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief="Criar um evento no google calendar")
    async def criar_agenda(self, ctx, data=None, hora=None):
        """
        usage: >criar_agenda

        """
        event_name = ""
        event_response_timout = cfg.config[0]['discord']["timeout_response"]
        if not data:
            embed = discord.Embed(
                title="Crie um momento de estudo aqui",
                colour=discord.Colour(0xACB4CE),
                description="Crie um momento de estudo, a agenda será enviada no canal de agenda no dia do evento!!",
            )
            embed.add_field(
                name="Copie o comando abaixo e modifique os dados nescessarios",
                value="```>criar_agenda  data:dd/mm/yyyy hora:HH:mm ```",
                inline=False,
            )
            await ctx.send(embed=embed, delete_after=60)
            return
            

        embed = discord.Embed(
            title="Qual assunto do evento?",
            description="Responda em até 2 minutos!!",
        )
        sent = await ctx.send(embed=embed, delete_after=event_response_timout)
        try:
            msg = await self.bot.wait_for(
                "message",
                timeout=event_response_timout,
                check=lambda message: message.author == ctx.author
                and message.channel == ctx.channel,
            )
            await sent.delete()
            await msg.delete()

            dt_str = data[-10:] + " " + hora[-5:]
            dt_obj = datetime.datetime.strptime(dt_str, "%d/%m/%Y %H:%M")
            date = datetime.datetime(
                dt_obj.year,
                dt_obj.month,
                dt_obj.day,
                dt_obj.hour,
                0,
                00,
                0,
                tzinfo=cfg.TZ,
            )
            event_name = msg.content
            if not date_pattern.match(data) or not hour_pattern.match(hora):
                await ctx.reply("Ajuste a data ou a hora!")
                return
            res = event.createEvent(
                msg.content,
                date,
                "🎙️ CANAL DE VOZ",
                msg.content,
            )
            data = parse(res["start"]["dateTime"])
            embed = discord.Embed( title="Evento criado!!", colour=discord.Colour(0x7ED321) )
            embed.add_field( name="Evento: ",   value=f"```{res['summary']}```", inline=False,
            )
            embed.add_field(
                name="Data:",
                value=f"{data.strftime('%d/%m/%Y - %H:%M')} - Hora de Brasilia",
                inline=False,
            )
            embed.add_field(
                name="Local:", value=f"{res['location']} ", inline=False
            )
            message_sent = await ctx.send(embed=embed)
            dt = datetime.datetime.strptime(
                str(res["start"]["dateTime"]), "%Y-%m-%dT%H:%M:%S%z"
            )
            await self.bot.pg_con.execute(
                "INSERT INTO events (message_id, calendar_id, date_time, event_name, event_link ) VALUES ($1, $2, $3, $4, $5)",
                message_sent.id,
                res["id"],
                dt,
                res["summary"],
                res["htmlLink"],
            )
            await ctx.message.delete()
                
        except asyncio.TimeoutError:
            embed=discord.Embed(title=f"Agendamento cancelado por falta de reposta.", color=0xffc800)
            await ctx.send(embed=embed)               
        except Exception as e:
            embed=discord.Embed(title=f"Erro ao criar o evento:  {event_name}.", color=0xff0000)
            await ctx.send(embed=embed)
            await logging.error(e)
            await sent.delete()



def setup(bot):
    bot.add_cog(Calendar(bot))
