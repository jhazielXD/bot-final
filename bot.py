import discord
from dotenv import load_dotenv 
from discord.ext import commands
import asyncio
import random
import webserver
import os
import requests
import deepl

load_dotenv()


DISCORD_TOKEN=os.getenv ("DISCORD_TOKEN")




intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command()
async def hello(ctx):
    await ctx.send(f'Hola, soy un bot {bot.user}!')

@bot.command()
async def heh(ctx, count_heh = 5):
    await ctx.send("he" * count_heh)

@bot.command()
async def ppt(ctx):
    opciones=["piedra", "papel" , "tijera"]
    gana={"piedra":"tijera" , "papel":"piedra" , "tijera":"papel"}

    victorias=0
    derrotas=0
    empates=0

    await ctx.send ("piedra , papel o tijera , escribe tu jugada o escribe salir")


    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    while True:
        try:
           msg=await bot.wait_for ("message" , check=check , timeout=120)
        except asyncio . TimeoutError:
            await ctx.send ("Pasaron 2 minutos y no has jugado , fin del juego")
            break
        jugada=msg.content.lower()
        if jugada=="salir":
            break
        bot_jugada=random.choice(opciones)
        if jugada ==bot_jugada:
            resultado="Empate"
            empates +=1
        elif gana [jugada]==bot_jugada:
            resultado="Ganaste"
            victorias+=1

        else:
            resultado="Perdiste"
            derrotas +=1

        await ctx.send (f"el bot ha elegido: {bot_jugada}")
        await ctx.send (f"el resultado es: {resultado}")

        await ctx.send (f"los marcadores son:")
        await ctx.send (f"victorias: {victorias}")
        await ctx.send (f"empates: {empates}")
        await ctx.send (f"derrotas: {derrotas}")


@bot.command()
async def suma (ctx , num1:int , num2:int):
   resultado=num1 + num2
   await ctx.send(f"la suma de {num1} con {num2} es : {resultado}")



@bot.command()
async def resta (ctx , num1:int , num2:int):
   resultado=num1 - num2
   await ctx.send(f"la resta de {num1} con {num2} es : {resultado}")




@bot.command()
async def multiplicación (ctx , num1:int , num2:int):
   resultado=num1 * num2
   await ctx.send(f"la multiplicación de {num1} con {num2} es : {resultado}")



@bot.command()

async def división (ctx , num1:int , num2:int):
    if num2==0:
          await ctx.send(f"No es posible dividir por 0")
   
    resultado=num1 / num2
    await ctx.send(f"la división de {num1} con {num2} es : {resultado}")





@bot.command()
async def imagenes (ctx):
    img=random.choice(os.listdir ("imagenes"))
    with open (f"imagenes/{img}" , "rb") as f:
        picture=discord.File (f)
    await ctx.send (file=picture)




@bot.command ()
async def adivinar (ctx):

    puntaje=0
    errores=0
    intentos=0

    await ctx.send ("Bienvenido al juego de números aleatorios , tienes 3 intentos")

    numeros=random.randint (1,50)
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel 
    mensaje = await bot.wait_for("message", check=check, timeout=30)
    pregunta=int(mensaje.content)

    if pregunta == numeros:
        await ctx.send ("Adivinaste el número")
        puntaje +=1
        intentos +=1


    else:
        await ctx.send (f"El número es incorrecto el número es {numeros}")
        errores +1
        intentos -=1


    if intentos==3:
        await ctx.send(" Se acabaron tus intentos")


@bot.command()
async def dato (ctx):
   url = "https://uselessfacts.jsph.pl/random.json"
   response=requests.get(url)


   if response.status_code ==200:
      print (response.json())
      client = deepl.DeepLClient("35870bce-545f-4ac7-9aca-258b24149803:fx")
      result = client.translate_text(response.json () ["text"], target_lang="ES")
      await ctx.send (result.text)

      return await ctx.send (response.json () ["text"])
      
   else:
      return await ctx.send ("No te dimos permiso")







webserver.keep_alive()
bot.run(DISCORD_TOKEN)
