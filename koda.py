import discord
import asyncio

TOKEN = 'YOUR_DISCORD_BOT_TOKEN'  # <-- tvoj bot token
USER_ID = 123456789012345678      # <-- tvoj Discord ID

intents = discord.Intents.default()
intents.messages = True
intents.members = True
client = discord.Client(intents=intents)

async def poslji_dm():
    await client.wait_until_ready()
    user = await client.fetch_user(USER_ID)
    
    # Simulacija temperature – zamenjaj z dejanskim branjem iz senzorja
    temperatura = preberi_temperaturo()
    vsebina = f"🌡️ Trenutna temperatura: `{temperatura:.2f} °C`"
    
    await user.send(vsebina)
    await client.close()

def preberi_temperaturo():
    # Primer iz internega senzorja RPi
    with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
        temp_raw = int(f.read().strip())
        return temp_raw / 1000.0

@client.event
async def on_ready():
    print(f'Bot prijavljen kot {client.user}')
    await poslji_dm()

client.run(TOKEN)

