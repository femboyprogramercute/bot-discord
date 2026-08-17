import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Configuración de roles con tus nombres exactos
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
        await ctx.send(f"⚠️ El rol `{NOMBRE_ROL_ACCESO}` no existe en el servidor.")

@darrol.error
async def darrol_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("❌ No tienes el rol de GATITO JOVEN para usar este comando.")

# PEGA TU TOKEN AQUÍ
bot.run(os.getenv("DISCORD_TOKEN"))
