import discord
from discord.ext import commands

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

# =========================
# BOTÃO DE ABRIR TICKET
# =========================
class TicketView(discord.ui.View):
    @discord.ui.button(label="🎟️ Abrir Ticket", style=discord.ButtonStyle.green)
    async def abrir_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild = interaction.guild
        user = interaction.user

        # Permissões
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            user: discord.PermissionOverwrite(read_messages=True)
        }

        # Criar canal
        channel = await guild.create_text_channel(f"ticket-{user.name}", overwrites=overwrites)

        # Mensagem dentro do ticket
        await channel.send(
            f"Olá {user.mention}! 👋\n\n"
            "**Envie as informações abaixo:**\n"
            "• Tipo de arte\n"
            "• Tema/estilo\n"
            "• Texto\n"
            "• Referência (opcional)\n\n"
            "Quando terminar, clique no botão abaixo para fechar."
        , view=FecharView())

        await interaction.response.send_message("✅ Ticket criado!", ephemeral=True)

# =========================
# BOTÃO DE FECHAR TICKET
# =========================
class FecharView(discord.ui.View):
    @discord.ui.button(label="🔒 Fechar Ticket", style=discord.ButtonStyle.red)
    async def fechar_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Encerrando ticket... 🧹", ephemeral=True)
        await interaction.channel.delete()

# =========================
# COMANDO PRA ENVIAR PAINEL
# =========================
@bot.command()
async def painel(ctx):
    embed = discord.Embed(
        title="🎨 Atendimento Azure Striker",
        description="Clique no botão abaixo para abrir um ticket e solicitar seu design.",
        color=discord.Color.blue()
    )
    await ctx.send(embed=embed, view=TicketView())

# =========================
# INICIAR BOT
# =========================
@bot.event
async def on_ready():
    print(f"Logado como {bot.user}")

import os
bot.run(os.getenv("TOKEN"))