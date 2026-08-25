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


# --- FUNCIÓN PARA VALIDAR MODERADORES (No importa el nombre del rol) ---
def es_moderador():
    async def predicate(ctx):
        # El dueño del servidor siempre tiene acceso
        if ctx.author == ctx.guild.owner:
            return True
        
        # Revisa si su rol tiene permisos de gestionar mensajes o roles
        if ctx.author.guild_permissions.manage_messages or ctx.author.guild_permissions.manage_roles:
            return True
            
        raise commands.MissingPermissions(["manage_messages"])
    return commands.check(predicate)


# -----------------------------------------------
# COMANDO PARA DAR ROLES
# -----------------------------------------------
@bot.command()
@es_moderador()
async def darrol(ctx, miembro: discord.Member, *, rol: discord.Role):
    """Uso: !darrol @usuario Nombre Del Rol"""
    try:
        await miembro.add_roles(rol)
        await ctx.send(f"✅ Se le otorgó el rol **{rol.name}** a {miembro.mention}.")
    except discord.Forbidden:
        await ctx.send("❌ No tengo permisos suficientes para asignar este rol (asegúrate de que mi rol esté por encima de este en la lista).")
    except Exception as e:
        await ctx.send(f"⚠️ Ocurrió un error: {e}")


# -----------------------------------------------
# COMANDO PARA QUITAR ROLES
# -----------------------------------------------
@bot.command()
@es_moderador()
async def quitarrol(ctx, miembro: discord.Member, *, rol: discord.Role):
    """Uso: !quitarrol @usuario Nombre Del Rol"""
    try:
        await miembro.remove_roles(rol)
        await ctx.send(f"✅ Se le removió el rol **{rol.name}** a {miembro.mention}.")
    except discord.Forbidden:
        await ctx.send("❌ No tengo permisos suficientes para quitar este rol (asegúrate de que mi rol esté por encima de este en la lista).")
    except Exception as e:
        await ctx.send(f"⚠️ Ocurrió un error: {e}")


# -----------------------------------------------
# COMANDO PARA EXPULSAR (KICK)
# -----------------------------------------------
@bot.command()
@es_moderador()
async def expulsar(ctx, miembro: discord.Member, *, razon: str = "No se especificó una razón"):
    """Uso: !expulsar @usuario [razón]"""
    try:
        await miembro.kick(reason=razon)
        await ctx.send(f"✅ Se ha expulsado a {miembro.mention} del servidor. Razón: {razon}")
    except discord.Forbidden:
        await ctx.send("❌ No tengo permisos suficientes para expulsar a este usuario (mi rol debe estar más arriba).")
    except Exception as e:
        await ctx.send(f"⚠️ Ocurrió un error: {e}")


# -----------------------------------------------
# COMANDO PARA EXPULSAR MASIVAMENTE A UN ROL
# -----------------------------------------------
@bot.command()
@es_moderador()
async def expulsarrol(ctx, *, rol: discord.Role):
    """Uso: !expulsarrol Nombre Del Rol"""
    
    if not ctx.guild.me.guild_permissions.kick_members:
        await ctx.send("❌ No tengo el permiso de **Expulsar miembros** habilitado en el servidor.")
        return

    if ctx.guild.me.top_role <= rol:
        await ctx.send("❌ Mi rol debe estar **por encima** del rol que intentas expulsar en la lista de roles del servidor.")
        return

    contador = 0
    fallidos = 0
    
    await ctx.send(f"⏳ Iniciando expulsión masiva de todos los usuarios con el rol **{rol.name}**... Esto puede tomar un momento.")

    for miembro in rol.members:
        if miembro == ctx.guild.owner or miembro == ctx.guild.me:
            continue
            
        try:
            await miembro.kick(reason=f"Expulsión masiva ordenada por {ctx.author}")
            contador += 1
        except Exception:
            fallidos += 1

    await ctx.send(f"✅ Proceso finalizado. Se expulsó correctamente a **{contador}** usuarios con el rol **{rol.name}**." + (f" (Fallidos: {fallidos})" if fallidos > 0 else ""))


# -----------------------------------------------
# COMANDO PARA BANEAR PERMANENTEMENTE
# -----------------------------------------------
@bot.command()
@es_moderador()
async def ban(ctx, miembro: discord.Member, *, razon: str = "No se especificó una razón"):
    """Uso: !ban @usuario [razón]"""
    try:
        await miembro.ban(reason=razon)
        await ctx.send(f"✅ Se ha baneado permanentemente a {miembro.mention}. Razón: {razon}")
    except discord.Forbidden:
        await ctx.send("❌ No tengo permisos suficientes para banear a este usuario (mi rol debe estar más arriba).")
    except Exception as e:
        await ctx.send(f"⚠️ Ocurrió un error: {e}")


# -----------------------------------------------
# MANEJO DE ERRORES
# -----------------------------------------------
@darrol.error
@quitarrol.error
@expulsar.error
@expulsarrol.error  # <-- Añadido aquí correctamente
@ban.error
async def comandos_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("❌ No tienes los permisos necesarios para usar este comando.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("⚠️ Faltan datos obligatorios. Revisa cómo usar el comando.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("⚠️ No pude encontrar al usuario o rol especificado.")


# Iniciar el bot
bot.run(os.getenv("DISCORD_TOKEN"))
