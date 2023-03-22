import pyodbc
import os
import twitchio
from twitchio.ext import commands


driver = '{ODBC Driver 18 for SQL Server}' # Or the relevent driver
server = 'Servername,1434'  # 1434 being the port
database = 'DBname'
username = 'username'
password = 'password'
conn = pyodbc.connect(f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password};TrustServerCertificate=yes')


# This next part is pulling from an ENV file, you can also put the above SQL info in the env file.
bot = commands.Bot(
    irc_token=os.environ['TMI_TOKEN']
    client_id=os.environ['CLIENT_ID']
    nick=os.environ['BOT_NICK']
    prefix=os.environ['BOT_PREFIX']
    initial_channels=[os.environ['CHANNEL']]
)
@bot.event
async def event_ready():
    print(f'Logged in as {bot.nick}')

@bot.command(name='add')
@twitchio.twitchapi.mod_only
async def add_username(ctx, username: str):
    cursor = conn.cursor()
    sql = "INSERT INTO users (username) VALUES (?)"
    val = (username,)
    cursor.execute(sql, val)
    conn.commit()
    await ctx.send(f"{username} has been added to the database.")

@bot.command(name='update')
@twitchio.twitchapi.mod_only
async def ban_users(ctx):
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM users")
    rows = cursor.fetchall()
    for row in rows:
        username = row[0]
        await ctx.channel.ban(username)
        await ctx.send(f"{username} has been banned.")

bot.run()
