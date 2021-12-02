import os
from quart import Quart, config, render_template, redirect, url_for
from quart.templating import DispatchingJinjaLoader
from quart_discord import DiscordOAuth2Session, requires_authorization, Unauthorized
from discord.ext import ipc
import discord
from config import *

app = Quart(__name__) #

app.secret_key = b'sus'
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "false"

app.config["DISCORD_CLIENT_ID"] = 914754040859090986
app.config["DISCORD_CLIENT_SECRET"] = 'KJ-ZL0Zh1b2rAX2vNRpJeJZILYVKprE5'
app.config["DISCORD_REDIRECT_URI"] = "http://127.0.0.1:5000/callback"
app.config["DISCORD_BOT_TOKEN"] = "OTEzNzE5OTQxMjQ3NjgwNTQy.YaCmAg.Q61t3JJtJwQv3Y7fSco3Zao0Xjc"


discord = DiscordOAuth2Session(app)
ipcClient = ipc.Client(secret_key="sus")

@app.route("/login/")
async def login():
    return await discord.create_session()

@app.route("/callback/")
async def callback():
    try:
        await discord.callback()
    except:
        return redirect(url_for("login"))
    return redirect(url_for("dashboard"))

@app.route("/")
async def index():
    return await render_template("index.html")

@app.route("/dashboard/")
async def dashboard():
    user = await discord.fetch_user()
    guildCount = await ipcClient.request("get_guild_count")
    guildIds = await ipcClient.request("get_guild_ids")
    try:
        userGuilds = await discord.fetch_guilds()
    except:
        return await redirect(url_for("login"))

    guilds = []
    
    for guild in userGuilds:
        if guild.permissions.manage_server:
            guild.classColor = "greenBorder" if guild.id in guildIds else "redBorder"
            guilds.append(guild)

    guilds.sort(key=lambda x: x.classColor == "redBorder")

    return await render_template("dashboard.html", user=user, guildCount= guildCount, guilds=guilds)

if __name__ == "__main__":
    app.run(debug=True)
