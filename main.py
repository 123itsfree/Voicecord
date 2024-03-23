import os
import sys
import json
import time
import requests
import websocket
from keep_alive import keep_alive

# Define constants
STATUS = "idle"  # online/dnd/idle
GUILD_ID = 730385656605311017
CHANNEL_ID = 916322268462870568
SELF_MUTE = True
SELF_DEAF = False

# Retrieve token from environment variables
usertoken = os.getenv("TOKEN")
if not usertoken:
    print("[ERROR] Please add a token inside Secrets.")
    sys.exit()

# Set headers with authorization token
headers = {"Authorization": usertoken, "Content-Type": "application/json"}

# Validate token
validate = requests.get('https://canary.discordapp.com/api/v9/users/@me', headers=headers)
if validate.status_code != 200:
    print("[ERROR] Your token might be invalid. Please check it again.")
    sys.exit()

# Extract user information
userinfo = validate.json()
username = userinfo["username"]
discriminator = userinfo["discriminator"]
userid = userinfo["id"]

# Define function to join voice channel
def joiner(token, status):
    ws = websocket.WebSocket()

    def on_message(ws, message):
        print(message)

    ws.on_message = on_message
    ws.connect('wss://gateway.discord.gg/?v=9&encoding=json')

    while True:
        time.sleep(5)  # Adjust as needed

# Define main function
def run_joiner():
    os.system("clear")  # Assuming you're running this on a Unix-like system
    print(f"Logged in as {username}#{discriminator} ({userid}).")
    while True:
        joiner(usertoken, STATUS)

# Keep the bot alive
keep_alive()

# Run the main function
run_joiner()
