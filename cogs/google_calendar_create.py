from discord.ext import commands
import discord
import datetime
import re
import asyncio
from utils.google_calendar import create_event as event
from utils import config as cfg
from utils.discord_api import events_create
import logging
from dateutil.parser import parse
import json
import base64

date_pattern = re.compile(
    "^data:[0-3]?[0-9].[0-3]?[0-9].(?:[0-9]{2})?[0-9]{2}$")
hour_pattern = re.compile("^hora:([0-1]?[0-9]|2[0-3]):[0-5][0-9]$")


class Calendar(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief="Criar um evento no google calendar")
    async def criar_agenda(self, ctx, data=None, hora=None):
        """
        usage: >criar_agenda

        """

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
            title="Qual assunto do evento? | Ex: Terraform: Trabalhar na issue #9 do iac-module-compute",
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
                dt_obj.minute,
                00,
                0,
                tzinfo=cfg.TZ,
            )
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
            embed = discord.Embed(title="Evento criado!!",
                                  colour=discord.Colour(0x7ED321))
            embed.add_field(name="Evento: ",   value=f"```{res['summary']}```", inline=False,
                            )
            embed.add_field(
                name="Data:",
                value=f"{data.strftime('%d/%m/%Y - %H:%M')} - Hora de Brasilia",
                inline=False,
            )
            embed.add_field(
                name="Local:", value=f"{res['location']} ", inline=False
            )

            event_description = f"""
            {msg.content}\n Google Calendário - Mentoria IAC
            {res['htmlLink']}
            """
            with open('cover.png', 'rb') as image_file:
                image_file_data = image_file.read()
                base64_encoded_data = base64.b64encode(image_file_data)
                encoded_image = base64_encoded_data.decode('utf-8')

            image_cover = f"data:image/png;base64,{encoded_image}"
            res_discord_event = events_create.create_event(
                msg.content, event_description, date.isoformat(), image_cover)
            if res_discord_event.status_code == 200:
                print("Evento criado com sucesso!")
                discord_event = json.loads(res_discord_event.text)
                discord_guild = cfg.config[0]['discord']["guild"]
                await ctx.send(f"https://discord.com/events/{discord_guild}/{discord_event['id']}")

            await ctx.message.delete()

        except events_create.requests.exceptions.RequestException as e:
            embed = discord.Embed(
                title="Erro ao criar o Evento no discord", color=0xffc800)
            await ctx.send(embed=embed)
            logging.error(e)

        except asyncio.TimeoutError:
            embed = discord.Embed(
                title="Agendamento cancelado por falta de reposta.", color=0xffc800)
            await ctx.send(embed=embed)
        except Exception as e:
            embed = discord.Embed(
                title=f"Erro ao criar o evento:  {msg.content}.", color=0xff0000)
            await ctx.send(embed=embed)
            logging.error(e)
            await sent.delete()


def setup(bot):
    bot.add_cog(Calendar(bot))
