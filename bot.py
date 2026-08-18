import os
import threading
import discord
from discord.ext import commands
from flask import Flask

# Servidor Flask para mantener activo en Render
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

@bot.event
async def on_ready():
    print(f"✅ Bot conectado con éxito como {bot.user}")

@bot.command()
@commands.has_permissions(administrator=True) # O puedes mantener un sistema de roles de moderación por servidor
async def darrol(ctx, miembro: discord.Member, *, rol: discord.Role):
    """
    Uso: !darrol @usuario Nombre Del Rol
    Funciona en cualquier servidor y con cualquier nombre de rol.
    """
    try:
        await miembro.add_roles(rol)
        await ctx.send(f"✅ Se le otorgó el rol **{rol.name}** a {miembro.mention}.")
    except discord.Forbidden:
        await ctx.send("❌ No tengo permisos suficientes para asignar este rol (asegúrate de que mi rol esté por encima de este en la lista).")
    except Exception as e:
        await ctx.send(f"⚠️ Ocurrió un error: {e}")

@darrol.error
async def darrol_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ No tienes permisos de administrador para usar este comando.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("⚠️ Faltan datos. Uso correcto: `!darrol @usuario NombreDelRol`")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("⚠️ No pude encontrar ese rol. Asegúrate de escribirlo bien o mencionar el rol.")

bot.run(os.getenv("DISCORD_TOKEN"))
