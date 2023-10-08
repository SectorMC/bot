import discord
from discord import AppInfo, Guild, VoiceChannel, option
from discord.ext import bridge
from discord.ext.commands import Bot
from discord.commands.context import ApplicationContext
from discord.commands import Option
from mcstatus import JavaServer
from webserver import keep_alive
import os  # default module
import random

# response = os.system("ping -c 1 " + hostname)
intents = discord.Intents.all()

bot = discord.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
  print(f"{bot.user} is ready and online!")
  await bot.change_presence(activity=discord.Game(name="Пингани меня!"),
                            status=discord.Status.idle)


@bot.event
async def on_message(message):
  randommessage = [
      'Зачем ты это сделал? Ладно, вот',
      'Привет, привет! Как дела? Посмотри на',
      'Вау, меня кто-то пинганул? Круто, вот', 'Спасибо за напоминание о смазке конечностей. Вот'
  ]
  if message.author == bot.user:
    return
  else:
    if bot.user in message.mentions:
      await message.channel.send(
          f"{random.choice(randommessage)} список моих команд (будет обновляться):\n • **/статус** - отправляет статус Minecraft-сервера FoxCraft\n • **/инфо** - отправляет сведения о боте\n • **...**"
      )


@bot.slash_command(name="status",
                   description="Посмотреть статус Minecraft-сервера Сектор.")
# @bot.bridge_command()
async def status(ctx):
  try:
    server = JavaServer.lookup(os.environ['IP_ADDRESS'])
    status = server.status()
  except ConnectionRefusedError:
    embed = discord.Embed(
        title="Сервер Сектор выключен или к нему не удалось подключиться!",
        description=
        "Если вы хотите узнать доп. информацию, то заходите на [**Discord-сервер**](https://dsc.gg/foxcraft-mc)!",
        color=discord.Colour.red(
        )  # Pycord provides a class with default colors you can choose from
    )
    embed.set_author(name="Команда Сектора",
                     icon_url="https://ibb.co/GR6sq2g")
  else:
    embed = discord.Embed(
        title="Сервер Сектор включен!",
        description=
        "Если вы хотите узнать доп. информацию, то заходите на [**Discord-сервер**](https://dsc.gg/foxcraft-mc)!",
        color=discord.Colour.green())
    embed.set_author(name="Команда Сектора",
                     icon_url="https://ibb.co/GR6sq2g")
    embed.add_field(name="Задержка (ping):", value=f"{int(status.latency)} мс")
    embed.add_field(name="Онлайн-игроки:",
                    value=f"{status.players.online} игрок(а/ов)")

  await ctx.respond(embed=embed)


@bot.slash_command(name="info", description="Посмотреть информацию обо мне!")
# @bot.bridge_command()
async def info(ctx):
  embed = discord.Embed(
      title="SectorBot",
      description=
      "Я личный ~~раб~~ бот для Discord-сервера Сектор! Мне поручили реализовывать те функции, которые не умеют делать другие боты.\n\nОбязательно загляните на [**наш Discord-сервер**](https://dsc.gg/foxcraft-mc), там должно быть весело! Удачной игры на нашем сервере!",
      color=discord.Colour.blurple())
  embed.set_author(name="Команда Сектора", icon_url="https://ibb.co/GR6sq2g")
  embed.add_field(name="Версия:", value="0.0.3", inline=True)
  embed.add_field(name="Разработчик:", value="lotigara", inline=True)
  embed.add_field(name="Лицензия:", value="GNU GPL v3.0", inline=True)
  embed.add_field(name="Исходный код:",
                  value="[Вот](https://github.com/lotigara/sector/)",
                  inline=False)
  embed.set_footer(
      text="Ставьте GNU/Linux или *BSD.")  # footers can have icons too
  await ctx.respond(embed=embed)


keep_alive()
bot.run(os.getenv('DISCORD_TOKEN'))  # run the bot with the token