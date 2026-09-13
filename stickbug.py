import os

import discord
from dotenv import load_dotenv


# ============================================================
# CONFIGURATION
# ============================================================

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")


# Emoji sent when someone @mentions the bot.
#
# This can be:
#   "😂"                    -> Unicode emoji
#   1543817449055584326     -> Custom Discord emoji ID
#
MENTION_EMOJI = 1543817449055584326


# Trigger strings and their reactions.
#
# Reaction values can be either:
#
#   Unicode:
#       "😂"
#
#   Custom Discord emoji ID:
#       1543817449055584326
#
TRIGGERS = {
    "stickbug": 1543817449055584326,
    "Le Stique": 1543817449055584326,
    "Le Stick": 1543817449055584326,
    "Le Stick Bug": 1543817449055584326,
    "Get Stick Bugged": 1543817449055584326
}


# ============================================================
# DISCORD SETUP
# ============================================================

intents = discord.Intents.default()

# Required to read the contents of messages.
intents.message_content = True

client = discord.Client(intents=intents)


# ============================================================
# EMOJI HELPER
# ============================================================

def get_emoji(emoji):
    """
    Converts our configuration value into something discord.py
    can use.

    If emoji is a string:
        Treat it as a Unicode emoji.

    If emoji is an integer:
        Treat it as a custom Discord emoji ID.
    """

    # Unicode emoji
    if isinstance(emoji, str):
        return emoji

    # Custom Discord emoji ID
    if isinstance(emoji, int):
        custom_emoji = client.get_emoji(emoji)

        if custom_emoji is None:
            print(f"Could not find custom emoji with ID: {emoji}")
            return None

        return custom_emoji

    print(f"Invalid emoji configuration: {emoji}")
    return None


# ============================================================
# EVENTS
# ============================================================

@client.event
async def on_ready():
    print("---------------------------------------")
    print(f"Logged in as: {client.user}")
    print(f"Bot ID: {client.user.id}")
    print("---------------------------------------")


@client.event
async def on_message(message):

    # Ignore messages sent by bots.
    # This prevents the bot from responding to itself.
    if message.author.bot:
        return

    # --------------------------------------------------------
    # Respond when someone @mentions the bot
    # --------------------------------------------------------

    if client.user.id in [user.id for user in message.mentions]:

        print(f"Bot was mentioned by {message.author}")

        emoji = get_emoji(MENTION_EMOJI)

        if emoji is not None:
            try:
                await message.channel.send(str(emoji))
                print(f"Sent mention emoji: {emoji}")

            except discord.Forbidden:
                print("Bot does not have permission to send messages here.")

            except discord.HTTPException as error:
                print(f"Could not send mention emoji: {error}")

        else:
            print(f"Could not find mention emoji: {MENTION_EMOJI}")

    # --------------------------------------------------------
    # React to trigger strings
    # --------------------------------------------------------

    message_text = message.content.casefold()

    for trigger, configured_emoji in TRIGGERS.items():

        if trigger.casefold() in message_text:

            emoji = get_emoji(configured_emoji)

            if emoji is None:
                continue

            try:
                await message.add_reaction(emoji)

            except discord.Forbidden:
                print(
                    f"Missing permission to react in "
                    f"#{message.channel}"
                )

            except discord.HTTPException as error:
                print(
                    f"Could not react with {emoji}: {error}"
                )


# ============================================================
# START BOT
# ============================================================

if DISCORD_TOKEN is None:
    raise RuntimeError(
        "DISCORD_TOKEN was not found. "
        "Make sure your .env file exists and contains "
        "DISCORD_TOKEN=your_token_here"
    )


client.run(DISCORD_TOKEN)