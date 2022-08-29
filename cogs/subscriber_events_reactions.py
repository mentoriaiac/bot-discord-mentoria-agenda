from discord.ext import commands
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


            embed = discord.Embed(
                title="📚 Lembrete de estudo :loudspeaker: ",
                description=f"**Obrigado, fique à vontade para participar do evento**: ```{message.content}```",
            )
            embed.add_field(
                name="Descrição:",
                value="Nosso evento vai ocorrer no canal de voz do discord da MentoriaIac",
                inline=False,
            )
            await user.send(embed=embed)


def setup(bot):
    bot.add_cog(Calendar(bot))
