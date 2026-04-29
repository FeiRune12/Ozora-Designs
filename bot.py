import discord
from discord.ext import commands
import os

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

CANAL_TICKETS_ID = 1498073866457714899

# =========================
# MENU DE SERVIÇOS
# =========================
class ServicoSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Banner"),
            discord.SelectOption(label="Ícone"),
            discord.SelectOption(label="Flyer"),
            discord.SelectOption(label="Identidade Visual"),
            discord.SelectOption(label="Premium")
        ]
        super().__init__(placeholder="Escolha o serviço...", options=options)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            f"Você escolheu: **{self.values[0]}**\nEnvie os detalhes do pedido 👇",
            ephemeral=True
        )

class ServicoView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(ServicoSelect())

# =========================
# BOTÃO DE FECHAR
# =========================
class FecharView(discord.ui.View):
    @discord.ui.button(label="🔒 Fechar Ticket", style=discord.ButtonStyle.red)
    async def fechar_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Encerrando ticket... 🧹", ephemeral=True)
        await interaction.channel.delete()

# =========================
# BOTÃO DE ABRIR TICKET
# =========================
class TicketView(discord.ui.View):
    @discord.ui.button(label="🎟️ Abrir Ticket", style=discord.ButtonStyle.green)
    async def abrir_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild = interaction.guild
        user = interaction.user

        channel = guild.get_channel(CANAL_TICKETS_ID)

        thread = await channel.create_thread(
            name=f"ticket-{user.name}",
            type=discord.ChannelType.private_thread
        )

        await thread.add_user(user)

        await thread.send(
            f"Olá {user.mention}! 👋\n\nEscolha o serviço abaixo:",
            view=ServicoView()
        )

        await thread.send("Quando terminar, clique abaixo para fechar:", view=FecharView())

        await interaction.response.send_message("✅ Ticket criado!", ephemeral=True)

# =========================
# COMANDO PRA ENVIAR PAINEL
# =========================
@bot.command()
async def painel(ctx):
    embed = discord.Embed(
        title="🎨 Atendimento Azure Striker",
        description="Clique abaixo para abrir um ticket.",
        color=discord.Color.blue()
    )
    await ctx.send(embed=embed, view=TicketView())

# =========================
# INICIAR BOT
# =========================
@bot.event
async def on_ready():
    print(f"Logado como {bot.user}")

bot.run(os.getenv("TOKEN"))
