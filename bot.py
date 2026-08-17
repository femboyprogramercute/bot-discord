import os
import threading
import discord
from discord.ext import commands
from flask import Flask

# Servidor Flask para engañar a Render
app = Flask("")


@app.route("/")
def home():
  return "Bot activo"


def run():
  app.run(host="0.0.0.0", port=8080)


threading.Thread(target=run).start()

# Configuración del bot
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Configuración de roles
NOMBRE_ROL_MODERADOR = "GATITO JOVEN"
NOMBRE_ROL_ACCESO = "MICHISITO"


@bot.event
async def on_ready():
  print(f"✅ Bot conectado con éxito como {bot.user}")


@bot.command()
@commands.has_role(NOMBRE_ROL_MODERADOR)
async def darrol(ctx, miembro: discord.Member):
  rol = discord.utils.get(ctx.guild.roles, name=NOMBRE_ROL_ACCESO)
  if rol:
    await miembro.add_roles(rol)
    await ctx.send(f"✅ Se le otorgó el rol **{rol.name}** a {miembro.mention}.")
  else:
    await ctx.send(
        f"⚠️ El rol `{NOMBRE_ROL_ACCESO}` no existe en el servidor."
    )


@darrol.error
async def darrol_error(ctx, error):
  if isinstance(error, commands.MissingRole):
    await ctx.send(
        "❌ No tienes el rol de GATITO JOVEN para usar este comando."
    )


bot.run(os.getenv("DISCORD_TOKEN"))
