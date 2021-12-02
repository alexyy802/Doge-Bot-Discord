from asyncio.tasks import sleep
from io import BytesIO
from operator import delitem
import random
from discord.utils import sleep_until
import nextcord
import urllib
from typing import Final, Text
import time
import json
import quart
import os
import discord
from PIL import Image
import animec
from discord import client
from discord.ext import commands, ipc
from discord_components import *
import datetime

os.chdir("D:\\Code\\Python\\Discord bot\\Test")

class myBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ipc = ipc.Server(self, secret_key='sus')

    async def on_ipc_read(self):
        print("IPC is ready!")
    async def on_ipc_error(self, endpoint, error):
        print(endpoint, "raised", error)
    async def on_ready(self):
        print("ready!")      





TOKEN = 'Put the bot token here'
PREFIX = '-'
INTENTS = discord.Intents().all()

client = myBot(command_prefix=PREFIX, intents=INTENTS)


@client.event
async def on_ready():
    print(f"{client.user.name} is Online.")
    print(f"and is Logged In as: {client.user.id}")

client.remove_command("help")

snipe_message_author = {}
snipe_message_content = {}

@client.event
async def on_message_delete(message):
    snipe_message_author[message.channel.id]= message.author
    snipe_message_content[message.channel.id]= message.content
    await sleep(60)
    del snipe_message_author[message.channel.id]
    del snipe_message_content[message.channel.id]





@client.command()
async def ping(ctx):
    await ctx.send('pong')

# **GENERL COMMANDS**
# WELCOMME 
@client.event
async def on_member_join(member):
    
    welcomeEmbed = discord.Embed(title=f"Welcome!", description=f"{member.mention} has joined Team Vision", color = discord.Color.blue())

    await client.get_channel(874498971823923232).send(embed=welcomeEmbed)

# Help
@client.command()
async def help(ctx):
    embed = discord.Embed(title="Vision X Help Commands: ", description="Help command for Vision Bot..." )
    for command in client.walk_commands():
        description = command.description
        if not description or description is None or description == "":
            description = "No Description Provided."
        embed.add_field(name=f"`-{command.name}{command.signature if command.signature is None else ''}`", value=description)
    await ctx.send(embed=embed)


# WANTED

@client.command()
async def wanted(ctx, member : discord.Member=None):
    if member == None:
        member = ctx.author

    wanted = Image.open("wanted.png")

    asset = member.avatar_url_as(size = 128)
    data = BytesIO(await asset.read())
    profilepic = Image.open(data)

    profilepic = profilepic.resize((300, 300))

    wanted.paste(profilepic, (226, 505))

    wanted.save("wantedpic.png")

    await ctx.send(file = discord.File("wantedpic.png"))

    os.remove("wantedpic.png")




# SEEFEFVERINFO
@client.command()
async def serverinfo(ctx):
    role_count = len(ctx.author.roles)
    list_of_bots = [bot.mention for bot in ctx.guild.members if bot.bot]
    

    serverinfoEmbed = discord.Embed(timestamp=ctx.message.created_at, color = ctx.author.color)
    serverinfoEmbed.add_field(name="Name", value=f'{ctx.guild.name}', inline=False)
    serverinfoEmbed.add_field(name="Member Count", value=ctx.guild.member_count, inline=False)
    serverinfoEmbed.add_field(name="Verification Level", value=str(ctx.guild.verification_level), inline=False)
    serverinfoEmbed.add_field(name="Highest Role", value=ctx.guild.roles[-2], inline=False)
    serverinfoEmbed.add_field(name="Number of Roles", value=str(role_count), inline=False)
    serverinfoEmbed.add_field(name="Number of Bots", value=','.join(list_of_bots), inline=False)


    await ctx.send(embed=serverinfoEmbed)




# AVATAR
@client.command()
async def avatar(ctx, *, member : discord.Member=None):

    if member == None:
        member = ctx.author
    
    embed = discord.Embed(color = ctx.author.color)
    embed.set_author(name = f"{member.name}'s Avatar")
    embed.set_image(url = member.avatar_url)
    embed.set_footer(text = f"Requested By : {ctx.author.name}")
    await ctx.send(embed=embed)



# Sniper Command
@client.command()
async def snipe(ctx):
    channel = ctx.channel
    try:
        snipeEmbed = discord.Embed(title=f"Last deleted message in #{channel.name}", description= snipe_message_content[channel.id])
        snipeEmbed.set_footer(text=f'Deleted by {snipe_message_author[channel.id]}')
        await ctx.send(embed=snipeEmbed)
    except:
        await ctx.send(f"There are no deleted messages in {channel.name}")



# emoji
@client.command()
async def emoji(ctx,*,text):
    emojis = []
    for s in text.lower():
        if s.isdecimal():
            num2emo = {'0':'zero','1':'one','2':'two',
            '3':'three','4':'four','5':'five',
            '6':'six','7':'seven','8':'eight','9':'nine'}
            emojis.append(f':{num2emo.get(s)}:')
        elif s.isalpha():
            emojis.append(f":regional_indicator_{s}:")
        else:
            emojis.append(s)
    await ctx.send(''.join(emojis))

















# **FUN COMMANDS**

# 8ball, Economy, Ping, TicTacToe, Rate


# CALCULATOR
#calculates answer
@client.event
async def on_ready():
	#turns on discord components lib
    DiscordComponents(client)
 
#buttons array
buttons = [
    [
        Button(style=ButtonStyle.grey, label='1'),
        Button(style=ButtonStyle.grey, label='2'),
        Button(style=ButtonStyle.grey, label='3'),
        Button(style=ButtonStyle.blue, label='×'),
        Button(style=ButtonStyle.red, label='Exit')
    ],
    [
        Button(style=ButtonStyle.grey, label='4'),
        Button(style=ButtonStyle.grey, label='5'),
        Button(style=ButtonStyle.grey, label='6'),
        Button(style=ButtonStyle.blue, label='÷'),
        Button(style=ButtonStyle.red, label='←')
    ],
    [
        Button(style=ButtonStyle.grey, label='7'),
        Button(style=ButtonStyle.grey, label='8'),
        Button(style=ButtonStyle.grey, label='9'),
        Button(style=ButtonStyle.blue, label='+'),
        Button(style=ButtonStyle.red, label='Clear')
    ],
    [
        Button(style=ButtonStyle.grey, label='00'),
        Button(style=ButtonStyle.grey, label='0'),
        Button(style=ButtonStyle.grey, label='.'),
        Button(style=ButtonStyle.blue, label='-'),
        Button(style=ButtonStyle.green, label='=')
    ],
]
 
#calculates answer
def calculate(exp):
    o = exp.replace('×', '*')
    o = o.replace('÷', '/')
    result = ''
    try:
        result = str(eval(o))
    except:
        result = 'An error occurred.'
    return result
 
@client.command()
async def calc(ctx):
    m = await ctx.send(content='Loading Calculators...')
    expression = 'None'
    delta = datetime.datetime.utcnow() + datetime.timedelta(minutes=5)
    e = discord.Embed(title=f'{ctx.author.name}\'s calculator | {ctx.author.id}', description=expression,
                        timestamp=delta)
    await m.edit(components=buttons, embed=e)
    while m.created_at < delta:
        res = await client.wait_for('button_click')
        if res.author.id == int(res.message.embeds[0].title.split('|')[1]) and res.message.embeds[
            0].timestamp < delta:
            expression = res.message.embeds[0].description
            if expression == 'None' or expression == 'An error occurred.':
                expression = ''
            if res.component.label == 'Exit':
                await res.respond(content='Calculator Closed', type=7)
                break
            elif res.component.label == '←':
                expression = expression[:-1]
            elif res.component.label == 'Clear':
                expression = 'None'
            elif res.component.label == '=':
                expression = calculate(expression)
            else:
                expression += res.component.label
            f = discord.Embed(title=f'{res.author.name}\'s calculator|{res.author.id}', description=expression,
                                timestamp=delta)
            await res.respond(content='', embed=f, components=buttons, type=7)








            












































# MEME
@client.command(name= 'meme', description='posts a random meme.')
async def meme(ctx):
    memeApi = urllib.request.urlopen('https://meme-api.herokuapp.com/gimme')

    memeData = json.load(memeApi)

    memeUrl = memeData['url']
    memeName = memeData['title']
    memePoster = memeData['author']
    memeSub = memeData['subreddit']
    memeLink = memeData['postLink']
    memeUps = memeData['ups']

    embed = discord.Embed(title=memeName,url=memeLink)
    embed.set_image(url=memeUrl)
    embed.set_footer(text=f'Meme by: {memePoster} | Subreddit: {memeSub} | 👍 {memeUps}')
    await ctx.send(embed=embed)


















































































# 8 BALL
#8ball! ask any question and recieve a random response
@client.command(aliases=['8ball', 'test'])
async def _8ball(ctx,*, question):
    responses = ["It is certain.",
                "It is decidedly so.",
                "Without a doubt.",
                "Yes - definitely.",
                "You may rely on it.",
                "As I see it, yes.",
                "Most likely.",
                "Outlook good.",
                "Yes.",
                "Signs point to yes.",
                "Reply hazy, try again.",
                "Ask again later.",
                "Better not tell you now.",
                "Cannot predict now.",
                "Concentrate and ask again.",
                "Don't count on it.",
                "My reply is no.",
                "My sources say no.",
                "Outlook not so good.",
                "Very doubtful."]
    await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')









# RATE
# COOL
@client.command()
async def cool(ctx):
    embed = discord.Embed(title="CoolRate", description = f"You are {random.randrange(101)}% Cool 😎 {ctx.author.mention}", color = discord.Color.random())
    await ctx.send(embed=embed)


# GAY
@client.command()
async def gay(ctx):
    embed = discord.Embed(title="GayRate", description = f"You are {random.randrange(101)}% Gay 🌈 {ctx.author.mention}", color = discord.Color.random())
    await ctx.send(embed=embed)
 

# PP
@client.command()
async def pp(ctx):
    pp = ['8D','8=======D','8===D','8====D','8==D','8=========D','8=======D','8=====D','8=========D','8=============D','8================D',]
    embed = discord.Embed(title='ppRate', description=f'Your pp is {random.choice(pp)} long 😏 {ctx.author.mention}', color=discord.Color.random())
    await ctx.send(embed=embed)

















#              **TIC TAC TOE**
player1 = ""
player2 = ""
turn = ""
gameOver = True

board = []

winningConditions = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
]

@client.command()
async def tictactoe(ctx, p1: discord.Member, p2: discord.Member):
    global count
    global player1
    global player2
    global turn
    global gameOver

    if gameOver:
        global board
        board = [":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:"]
        turn = ""
        gameOver = False
        count = 0

        player1 = p1
        player2 = p2

        # print the board
        line = ""
        for x in range(len(board)):
            if x == 2 or x == 5 or x == 8:
                line += " " + board[x]
                await ctx.send(line)
                line = ""
            else:
                line += " " + board[x]

        # determine who goes first
        num = random.randint(1, 2)
        if num == 1:
            turn = player1
            await ctx.send("It is <@" + str(player1.id) + ">'s turn.")
        elif num == 2:
            turn = player2
            await ctx.send("It is <@" + str(player2.id) + ">'s turn.")
    else:
        await ctx.send("A game is already in progress! Finish it before starting a new one.")

@client.command()
async def place(ctx, pos: int):
    global turn
    global player1
    global player2
    global board
    global count
    global gameOver

    if not gameOver:
        mark = ""
        if turn == ctx.author:
            if turn == player1:
                mark = ":regional_indicator_x:"
            elif turn == player2:
                mark = ":o2:"
            if 0 < pos < 10 and board[pos - 1] == ":white_large_square:" :
                board[pos - 1] = mark
                count += 1

                # print the board
                line = ""
                for x in range(len(board)):
                    if x == 2 or x == 5 or x == 8:
                        line += " " + board[x]
                        await ctx.send(line)
                        line = ""
                    else:
                        line += " " + board[x]

                checkWinner(winningConditions, mark)
                print(count)
                if gameOver == True:
                    await ctx.send(mark + " wins!")
                elif count >= 9:
                    gameOver = True
                    await ctx.send("It's a tie!")

                # switch turns
                if turn == player1:
                    turn = player2
                elif turn == player2:
                    turn = player1
            else:
                await ctx.send("Be sure to choose an integer between 1 and 9 (inclusive) and an unmarked tile.")
        else:
            await ctx.send("It is not your turn.")
    else:
        await ctx.send("Please start a new game using the !tictactoe command.")


def checkWinner(winningConditions, mark):
    global gameOver
    for condition in winningConditions:
        if board[condition[0]] == mark and board[condition[1]] == mark and board[condition[2]] == mark:
            gameOver = True

@tictactoe.error
async def tictactoe_error(ctx, error):
    print(error)
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please mention 2 players for this command.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Please make sure to mention/ping players (ie. <@688534433879556134>).")

@place.error
async def place_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please enter a position you would like to mark.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Please make sure to enter an integer.")







# CALCULATOR LMAO






















# **MODERATION**
#purges a message least=5 max=unlimited
@client.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount)
    em = discord.Embed(title = 'Cleared', description = f'{amount} messages')
    await ctx.send(embed=em)

# lock/anti-raid
@client.command()
@commands.has_permissions(manage_channels=True)
async def lock(ctx, channel : discord.TextChannel=None):
    overwrite = ctx.channel.overwrites_for(ctx.guild.default_role)
    overwrite.send_messages = False
    await ctx.channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
    em = discord.Embed(title = 'Locked', description = f'#{channel}')
    await ctx.send(embed=em)
@lock.error
async def lock_error(ctx, error):
    if isinstance(error,commands.CheckFailure):
        await ctx.send('You do not have permission to use this command!')


# unlock
@client.command()
@commands.has_permissions(manage_channels=True)
async def unlock(ctx, channel : discord.TextChannel=None):
    overwrite = ctx.channel.overwrites_for(ctx.guild.default_role)
    overwrite.send_messages = True
    await ctx.channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
    em = discord.Embed(title = 'Unlocked', description = f'#{channel}')
    await ctx.send(embed=em)
@unlock.error
async def unlock_error(ctx, error):
    if isinstance(error,commands.CheckFailure):
        await ctx.send('You do not have permission to use this command!')


#kicks user
@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member : discord.Member, *, reason=None):
    await member.kick(reason=reason)
    em = discord.Embed(title = 'Kicked: ', description = f'{member.mention}', colour = discord.Color.red)
    await ctx.send(embed=em)

#bans user
@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member : discord.Member, *, reason=None):
    await member.ban(reason=reason)
    em = discord.Embed(title = 'Banned: ', description = f'{member.mention}', colour = discord.Color.red)
    await ctx.send(embed=em)


#unbans user
@client.command()
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split()
    em = discord.Embed(title = 'Unbanne: ', description = f'{member.mention}', colour = discord.Color.red)
    await ctx.send(embed=em)

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.mention}')
            return

# embed
@client.command()
async def displayembed(ctx):
    embed = discord.Embed(
        title = 'Title',
        description = 'This is a description',
        colour = discord.Color.blue()
    )

    embed.set_footer(text='This is a footer')
    embed.set_image(url='https://cdn.discordapp.com/attachments/907981498999783464/908303583420747776/unknown-2.png')
    embed.set_image(url='https://cdn.discordapp.com/attachments/907981498999783464/908303583420747776/unknown-2.png')
    embed.set_author(name='Author Name',
    icon_url='https://cdn.discordapp.com/attachments/907981498999783464/908303583420747776/unknown-2.png')
    embed.add_field(name='Fleid Name', value='Field Value', inline=False)
    embed.add_field(name='Fleid Name', value='Field Value', inline=True)
    embed.add_field(name='Fleid Name', value='Field Value', inline=True)

    await ctx.send(embed=embed)


# whois
@client.command()
async def whois(ctx, member: discord.Member):

    roles = [role for role in member.roles]


    embed = discord.Embed(colour=member.color, timestamp=ctx.message.created_at)

    embed.set_author(name=f'User Info - {member}')
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)

    embed.add_field(name='ID:', value=member.id)
    embed.add_field(name='Guild name:', value=member.display_name)

    embed.add_field(name='Created at:', value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p  UTC"))
    embed.add_field(name='Join at:', value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p  UTC"))

    embed.add_field(name=f"Roles ({len(roles)})", value=" ".join([role.mention for role in roles]))
    embed.add_field(name="Top role:", value=member.top_role.mention)

    embed.add_field(name="Bot?", value=member.bot)

    await ctx.send(embed=embed)




# slowmode
@client.command()
async def slowmode(ctx,time:int):
    if (not ctx.author.guild_permissions.manage_messages):
        await ctx.send("This requires manage messages perms.")
        return
    try:
        if time == 0:
            await ctx.send('Slowmode Off')
            await ctx.channel.edit(slowmode_delay = 0)
        elif time > 21600:
            await ctx.send("You cannot set slowmode above 6 hours")
            return
        else:
            await ctx.channel.edit(slowmode_delay = time)
            await ctx.send(f"Slowmode set to {time} seconds.")
    except Exception:
        await print("oops!")


























# auto moderation
filtered_words = ["bitch", "Bitch","Dick","dick" "Fuck", "fuck", "nigger", 'Niggger', 'nigga', 'penis', 'Penis', 'Pussy', 'pussy', 'Cock', 'cock', 'motherfucker', 'Motherfucker']
@client.event
async def on_message(msg):
    for word in filtered_words:
        if word in msg.content:
            await msg.delete()

    await client.process_commands(msg)

# ADDROLE
@client.command()
async def addrole(ctx, role: discord.Role, user: discord.Member):
    if ctx.author.guild_permissons.administrator:
        await user.add_roles(role)
        await ctx.send(f'Successfully added {role.mention} to {user.mention} ')

# REMOVE ROLE
@client.command()
async def removerole(ctx, user: discord.Member, role: discord.Role):
    if ctx.author.guild_permissons.administrator:
        await user.remove_roles(role)
    await ctx.send(f'Successfully removed {role.mention} from {user.mention} ')


    
# SUGGESTION

@client.command()
async def suggest(ctx,*,suggestion):
    await ctx.channel.purge(limit=1)
    channel = discord.utils.get(ctx.guild.text_channels, name="〚🗣️〛┭suggestion┮")
    suggest = discord.Embed(title=suggestion, description=f'{ctx.author.name} has suuggested, {suggestion}.')
    sugg = await channel.send(embed=suggest)
    await channel.send(f"^^ Suggestion ID: {sugg.id}")
    await sugg.add_reaction("✅")
    await sugg.add_reaction("❌")

@client.command()
async def approve(ctx, id:int=None,*,reason=None):
    if id is None:
        return
    channel = discord.utils.get(ctx.guild.text_channels, name="〚🗣️〛┭suggestion┮")
    if channel is None:
        return
    suggestionMsg = await channel.fetch_message(id)
    embed = discord.Embed(title=f"Suggestion has been apporved", description=f"The suggestion id of '{suggestionMsg.id} has been aproved by {ctx.author.name} | Reason: {reason}")
    await channel.send(embed=embed)

@client.command()
async def deny(ctx, id:int=None,*,reason=None):
    if id is None:
        return
    channel = discord.utils.get(ctx.guild.text_channels, name="〚🗣️〛┭suggestion┮")
    if channel is None:
        return
    suggestionMsg = await channel.fetch_message(id)
    embed = discord.Embed(title=f"Suggestion has been denied", description=f"The suggestion id of '{suggestionMsg.id} has been denied by {ctx.author.name} | Reason: {reason}")
    await channel.send(embed=embed)











































client.ipc.start()
client.run(TOKEN)
