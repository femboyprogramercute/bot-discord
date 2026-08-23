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


# -----------------------------------------------
# COMANDO PARA DAR ROLES
# -----------------------------------------------
@bot.command()
@commands.has_permissions(administrator=True)
async def darrol(ctx, miembro: discord.Member, *, rol: discord.Role):
    """Uso: !darrol @usuario Nombre Del Rol"""
    try:
        await miembro.add_roles(rol)
        await ctx.send(f"✅ Se le otorgó el rol **{rol.name}** a {miembro.mention}.")
    except discord.Forbidden:
        await ctx.send(
            "❌ No tengo permisos suficientes para asignar este rol (asegúrate de"
            " que mi rol esté por encima de este en la lista)."
        )
    except Exception as e:
        await ctx.send(f"⚠️ Ocurrió un error: {e}")

@darrol.error
async def darrol_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ No tienes permisos de administrador para usar este comando.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("⚠️ Faltan datos. Uso correcto: `!darrol @usuario NombreDelRol`")
    elif isinstance(error, commands.BadArgument):
        await ctx.send(
            "⚠️ No pude encontrar ese rol. Asegúrate de escribirlo bien o mencionar"
            " el rol."
        )


# -----------------------------------------------
# COMANDO PARA QUITAR ROLES
# -----------------------------------------------
@bot.command()
@commands.has_permissions(administrator=True)
async def quitarrol(ctx, miembro: discord.Member, *, rol: discord.Role):
    """Uso: !quitarrol @usuario Nombre Del Rol"""
    try:
        await miembro.remove_roles(rol)
        await ctx.send(f"✅ Se le removió el rol **{rol.name}** a {miembro.mention}.")
    except discord.Forbidden:
        await ctx.send(
            "❌ No tengo permisos suficientes para quitar este rol (asegúrate de"
            " que mi rol esté por encima de este en la lista)."
        )
    except Exception as e:
        await ctx.send(f"⚠️ Ocurrió un error: {e}")

@quitarrol.error
async def quitarrol_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ No tienes permisos de administrador para usar este comando.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("⚠️ Faltan datos. Uso correcto: `!quitarrol @usuario NombreDelRol`")
    elif isinstance(error, commands.BadArgument):
        await ctx.send(
            "⚠️ No pude encontrar ese rol. Asegúrate de escribirlo bien o mencionar"
            " el rol."
        )


# -----------------------------------------------
# COMANDO PARA EXPULSAR (KICK)
# -----------------------------------------------
@bot.command()
@commands.has_permissions(administrator=True)
async def expulsar(ctx, miembro: discord.Member, *, razon: str = "No se especificó una razón"):
    """Uso: !expulsar @usuario [razón]"""
    try:
        await miembro.kick(reason=razon)
        await ctx.send(f"✅ Se ha expulsado a {miembro.mention} del servidor. Razón: {razon}")
    except discord.Forbidden:
        await ctx.send("❌ No tengo permisos suficientes para expulsar a este usuario (mi rol debe estar más arriba).")
    except Exception as e:
        await ctx.send(f"⚠️ Ocurrió un error: {e}")

@expulsar.error
async def expulsar_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ No tienes permisos de administrador para usar este comando.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("⚠️ Faltan datos. Uso correcto: `!expulsar @usuario [razón]`")


# -----------------------------------------------
# COMANDO PARA BANEAR PERMANENTEMENTE
# -----------------------------------------------
@bot.command()
@commands.has_permissions(administrator=True)
async def ban(ctx, miembro: discord.Member, *, razon: str = "No se especificó una razón"):
    """Uso: !ban @usuario [razón]"""
    try:
        await miembro.ban(reason=razon)
        await ctx.send(f"✅ Se ha baneado permanentemente a {miembro.mention}. Razón: {razon}")
    except discord.Forbidden:
        await ctx.send("❌ No tengo permisos suficientes para banear a este usuario (mi rol debe estar más arriba).")
    except Exception as e:
        await ctx.send(f"⚠️ Ocurrió un error: {e}")

@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ No tienes permisos de administrador para usar este comando.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("⚠️ Faltan datos. Uso correcto: `!ban @usuario [razón]`")


# Iniciar el bot
bot.run(os.getenv("DISCORD_TOKEN"))
