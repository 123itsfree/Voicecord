import os
import sys
import json
import time
import requests
import websocket
from keep_alive import keep_alive

# Define constants
STATUS = "online"  # online/dnd/idle
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
    ws.connect('wss://gateway.discord.gg/?v=9&encoding=json')
    start = json.loads(ws.recv())
    heartbeat = start['d']['heartbeat_interval']
    auth = {
        "op": 2,
        "d": {
            "token": token,
            "properties": {
                "$os": "Windows 10",
                "$browser": "Google Chrome",
                "$device": "Windows"
            },
            "presence": {
                "status": status,
                "afk": False
            }
        },
        "s": None,
        "t": None
    }
    vc = {
        "op": 4,
        "d": {
            "guild_id": GUILD_ID,
            "channel_id": CHANNEL_ID,
            "self_mute": SELF_MUTE,
            "self_deaf": SELF_DEAF
        }
    }
    ws.send(json.dumps(auth))
    ws.send(json.dumps(vc))
    time.sleep(heartbeat / 1000)
    ws.send(json.dumps({"op": 1, "d": None}))

# Define main function
def run_joiner():
    os.system("clear")  # Assuming you're running this on a Unix-like system
    print(f"Logged in as {username}#{discriminator} ({userid}).")
    while True:
        joiner(usertoken, STATUS)
        time.sleep(30)

# Keep the bot alive
keep_alive()

# Run the main function
run_joiner()
