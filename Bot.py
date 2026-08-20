import discord
from discord import app_commands
from discord.ext import commands
import io
import random
import string
import os

# ---------- Obfuscator ----------
def obfuscate_python(source: str) -> str:
    # Convert source to list of integers (Unicode code points)
    numbers = [ord(ch) for ch in source]
    # Insert random noise (strings) between numbers
    scrambled = []
    for num in numbers:
        scrambled.append(num)
        # 30% chance to insert random noise after each number
        if random.random() < 0.3:
            # Generate a random string of letters and digits
            noise = ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(3, 6)))
            scrambled.append(noise)
    # Build the obfuscated Python script
    return f'''# Obfuscated Python script
_data = {scrambled}
_decoded = ''.join(chr(x) for x in _data if isinstance(x, int))
exec(_decoded)
'''

def obfuscate_lua(source: str) -> str:
    numbers = [ord(ch) for ch in source]
    scrambled = []
    for num in numbers:
        scrambled.append(num)
        if random.random() < 0.3:
            noise = ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(3, 6)))
            scrambled.append(f'"{noise}"')  # Lua strings must be quoted
    # Build Lua script with table and decoder
    return f'''-- Obfuscated Lua script
local data = {{{', '.join(str(x) for x in scrambled)}}}
local decoded = ""
for _, v in ipairs(data) do
    if type(v) == "number" then
        decoded = decoded .. string.char(v)
    end
end
loadstring(decoded)()
'''

# ---------- Discord Bot ----------
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

@bot.tree.command(name="obf", description="Obfuscate a Python or Lua script from an attachment")
@app_commands.describe(attachment="Upload a .py or .lua file")
async def obf(interaction: discord.Interaction, attachment: discord.Attachment):
    await interaction.response.defer()  # Prevent timeout

    # Check file extension
    if not attachment.filename.endswith(('.py', '.lua')):
        await interaction.followup.send("❌ Please attach a `.py` or `.lua` file.")
        return

    # Read file content
    try:
        content = await attachment.read()
        source = content.decode('utf-8')
    except Exception as e:
        await interaction.followup.send(f"⚠️ Failed to read file: {e}")
        return

    # Obfuscate
    if attachment.filename.endswith('.py'):
        obfuscated = obfuscate_python(source)
        out_name = attachment.filename.rsplit('.', 1)[0] + '.obf.py'
    else:  # .lua
        obfuscated = obfuscate_lua(source)
        out_name = attachment.filename.rsplit('.', 1)[0] + '.obf.lua'

    # Send as file
    file_obj = discord.File(io.BytesIO(obfuscated.encode('utf-8')), filename=out_name)
    await interaction.followup.send(f"✅ Obfuscated **{attachment.filename}**", file=file_obj)

# ---------- Run ----------
if __name__ == "__main__":
    TOKEN = "MTUzOTk4MjI2MTUzNjAzODkyMg.GPvwlQ.iYrqUtQcpXoUMPOzpJEv5hcbhJtMP4qcCSPEvg"   # <-- Paste your token between the quotes
    bot.run(TOKEN)
