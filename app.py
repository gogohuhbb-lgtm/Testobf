import discord
from discord import app_commands
from discord.ext import commands
import io
import random
import string

# ---------- Pure data obfuscator (6 reversals, only numbers and strings) ----------
def obfuscate_python(source: str) -> str:
    data = list(source.encode('utf-8'))
    for _ in range(6):
        data.reverse()
        new_data = []
        for b in data:
            new_data.append(b)
            if random.random() < 0.3:
                noise = ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(3, 6)))
                new_data.append(noise)
        data = new_data
    for _ in range(3):
        data.insert(0, ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(3, 6))))
        data.append(''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(3, 6))))
    
    data_str = ', '.join(repr(x) for x in data)
    py_code = f'''_=({data_str}); exec(bytes([x for x in _ if type(x)==int][::-1][::-1][::-1][::-1][::-1][::-1]).decode())'''
    return '# made by darien\n' + py_code

def obfuscate_lua(source: str) -> str:
    data = list(source.encode('utf-8'))
    for _ in range(6):
        data.reverse()
        new_data = []
        for b in data:
            new_data.append(b)
            if random.random() < 0.3:
                noise = ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(3, 6)))
                new_data.append(noise)
        data = new_data
    for _ in range(3):
        data.insert(0, ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(3, 6))))
        data.append(''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(3, 6))))
    
    data_str = ', '.join(repr(x) for x in data)
    lua_code = f'''local _={{{data_str}}}; local n={{}}; for _,v in ipairs(_) do if type(v)=="number" then n[#n+1]=v end end; local function r(t) local o={{}}; for i=#t,1,-1 do o[#o+1]=t[i] end; return o end; n=r(n); n=r(n); n=r(n); n=r(n); n=r(n); n=r(n); local s=""; for _,b in ipairs(n) do s=s..string.char(b) end; loadstring(s)()'''
    return '-- made by darien\n' + lua_code

# ---------- Discord Bot ----------
intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    try:
        synced = await bot.tree.sync()
        print(f'Synced {len(synced)} commands')
    except Exception as e:
        print(e)

@bot.tree.command(name="obf", description="Obfuscate Python/Lua with 6 reversals, pure data look")
@app_commands.describe(attachment="Upload a .py or .lua file")
async def obf(interaction: discord.Interaction, attachment: discord.Attachment):
    await interaction.response.defer()
    if not attachment.filename.endswith(('.py', '.lua')):
        await interaction.followup.send('❌ Please attach a .py or .lua file.')
        return
    try:
        content = await attachment.read()
        source = content.decode('utf-8')
    except Exception as e:
        await interaction.followup.send(f'⚠️ Error: {e}')
        return

    if attachment.filename.endswith('.py'):
        obfuscated = obfuscate_python(source)
        out_name = attachment.filename.rsplit('.',1)[0] + '.obf.py'
    else:
        obfuscated = obfuscate_lua(source)
        out_name = attachment.filename.rsplit('.',1)[0] + '.obf.lua'

    file_obj = discord.File(io.BytesIO(obfuscated.encode('utf-8')), filename=out_name)
    await interaction.followup.send('**made by darien**', file=file_obj)
