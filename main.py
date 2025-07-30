import discord
from discord.ext import commands
import os
import logging
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Replace with your actual Discord user ID
OWNER_ID = 706535536650616833

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} - {bot.user.id}')

@bot.event
async def on_member_join(member):
    try:
        # Notify the owner via DM only (do not DM the new member)
        owner = await bot.fetch_user(OWNER_ID)
        await owner.send(f'📥 New member joined: {member.name} (ID: {member.id}) in server: {member.guild.name}')
    except Exception as e:
        print(f"Failed to notify owner about new member: {e}")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if "shit" in message.content.lower():
        await message.delete()
        await message.channel.send("Please refrain from using inappropriate language.")
    
    await bot.process_commands(message)

@bot.command()
async def hello(ctx):
    await ctx.send("Hello!")

    try:
        owner = await bot.fetch_user(OWNER_ID)
        await owner.send(f'📩 User {ctx.author} just used the !hello command in #{ctx.channel}')
    except Exception as e:
        print(f"Failed to send DM to owner: {e}")

bot.run(TOKEN, log_handler=handler, log_level=logging.DEBUG)
