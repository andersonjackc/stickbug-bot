import os
import random

import discord
from dotenv import load_dotenv


# ============================================================
# CONFIGURATION
# ============================================================

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")


# ============================================================
# RESPONSE CHANCES
# ============================================================

# Chance that the bot responds when directly @mentioned.
#
# 1.00 = 100%
# 0.75 = 75%
# 0.50 = 50%
# 0.25 = 25%
# 0.10 = 10%
# 0.00 = never
MENTION_RESPONSE_CHANCE = 1.00


# Chance that the bot sends a RANDOM MESSAGE when one of the
# trigger strings is detected.
#
# The bot will still add the configured reaction regardless.
TRIGGER_RESPONSE_CHANCE = 0.40


# If a message @mentions the bot AND contains a trigger string:
#
# False = don't potentially send two random responses
# True  = mention response AND trigger response are rolled separately
ALLOW_TRIGGER_RESPONSE_ON_MENTION = False


# ============================================================
# RANDOM RESPONSE POOL
# ============================================================

# type can be:
#
#   "text"     -> normal text
#   "youtube"  -> YouTube URL
#   "gif"      -> GIF / Tenor / Giphy URL
#   "emoji"    -> Unicode emoji OR custom Discord emoji ID
#
#
# weight controls how likely each response is AFTER the bot
# has decided to respond.
#
# These weights do NOT have to add up to 100.
#
# Example:
#   weight 50
#   weight 25
#   weight 15
#   weight 10
#
# behaves like:
#   50%
#   25%
#   15%
#   10%
#
# because they total 100.
#
# You can add as many responses as you want.

RANDOM_RESPONSES = [

    # --------------------------------------------------------
    # Text responses
    # --------------------------------------------------------

    {
        "type": "text",
        "value": "Get stick bugged.",
        "weight": 9,
    },

    {
        "type": "text",
        "value": "Can I haz bone?",
        "weight": 1,
    },

    # --------------------------------------------------------
    # Custom Discord emoji
    # --------------------------------------------------------

    {
        "type": "emoji",
        "value": 1543817449055584326,
        "weight": 50,
    },


    # --------------------------------------------------------
    # YouTube URLs
    # --------------------------------------------------------

    {
        "type": "youtube",
        "value": "https://www.youtube.com/watch?v=M5V_IXMewl4",
        "weight": 10,
    },


    # --------------------------------------------------------
    # GIF URLs
    # --------------------------------------------------------

    {
        "type": "gif",
        "value": "https://klipy.com/gifs/get-stick-bugged-lol",
        "weight": 30,
    },
]


# ============================================================
# TRIGGER STRINGS
# ============================================================

# The bot ALWAYS reacts to these when detected.
#
# The reaction can be:
#
#   Unicode:
#       "😂"
#
#   Custom Discord emoji ID:
#       1543817449055584326
#
# Separately, TRIGGER_RESPONSE_CHANCE controls whether the bot
# also sends something from RANDOM_RESPONSES.

TRIGGERS = {
    "stick": 1543817449055584326,
    "bug": 1543817449055584326,
    "stickbug": 1543817449055584326,
    "stick bug": 1543817449055584326,
    "stickbugs": 1543817449055584326,
    "stick bugs": 1543817449055584326,
    "stick-bug": 1543817449055584326,
    "stick-bugged": 1543817449055584326,
    "stickbugged": 1543817449055584326,
    "stick bugged": 1543817449055584326,
    "get stickbugged": 1543817449055584326,
    "Le Stique": 1543817449055584326,
    "Le Stick": 1543817449055584326,
    "Le Stick Bug": 1543817449055584326,
    "Get Stick Bugged": 1543817449055584326,
    "Get Stickbugged": 1543817449055584326,
    "Get stick bugged": 1543817449055584326,
    "You've been stick bugged": 1543817449055584326,
    "You got stick bugged": 1543817449055584326,
    "You have been stick bugged": 1543817449055584326,
    "I got stick bugged": 1543817449055584326,
    "we got stick bugged": 1543817449055584326,
    "stick bug time": 1543817449055584326,
    "stickbug time": 1543817449055584326,
    "stick bug moment": 1543817449055584326,
    "stickbug moment": 1543817449055584326,
    "stick bug incoming": 1543817449055584326,
    "stickbug incoming": 1543817449055584326,
    "stick bug alert": 1543817449055584326,
    "stickbug alert": 1543817449055584326,
    "stick bug detected": 1543817449055584326,
    "stickbug detected": 1543817449055584326,
    "summon the stick bug": 1543817449055584326,
    "summon stickbug": 1543817449055584326,
    "where is the stick bug": 1543817449055584326,
    "who summoned the stick bug": 1543817449055584326,
    "look at this stick bug": 1543817449055584326,
    "look a stick bug": 1543817449055584326,
    "it's a stick bug": 1543817449055584326,
    "its a stick bug": 1543817449055584326,
    "that is a stick bug": 1543817449055584326,
    "is that a stick bug": 1543817449055584326,
    "stick bugged lol": 1543817449055584326,
    "get stick bugged lol": 1543817449055584326,
}


# ============================================================
# DISCORD SETUP
# ============================================================

intents = discord.Intents.default()

# Required to read message contents.
intents.message_content = True

client = discord.Client(intents=intents)


# ============================================================
# EMOJI HELPER
# ============================================================

def get_emoji(emoji):
    """
    Converts an emoji configuration value into something
    discord.py can use.

    str:
        Treated as a Unicode emoji.

    int:
        Treated as a custom Discord emoji ID.
    """

    # Unicode emoji
    if isinstance(emoji, str):
        return emoji

    # Custom Discord emoji
    if isinstance(emoji, int):
        custom_emoji = client.get_emoji(emoji)

        if custom_emoji is None:
            print(f"Could not find custom emoji with ID: {emoji}")
            return None

        return custom_emoji

    print(f"Invalid emoji configuration: {emoji}")
    return None


# ============================================================
# RNG HELPERS
# ============================================================

def roll_chance(chance):
    """
    Returns True based on the supplied probability.

    Examples:

        1.00 -> always True
        0.50 -> approximately 50% of the time
        0.10 -> approximately 10% of the time
    """

    return random.random() < chance


def choose_random_response():
    """
    Selects one response from RANDOM_RESPONSES using
    the configured weights.
    """

    weights = [
        response["weight"]
        for response in RANDOM_RESPONSES
    ]

    return random.choices(
        RANDOM_RESPONSES,
        weights=weights,
        k=1,
    )[0]


# ============================================================
# RANDOM RESPONSE SENDER
# ============================================================

async def send_random_response(channel):
    """
    Chooses and sends one random response.
    """

    response = choose_random_response()

    response_type = response["type"]
    value = response["value"]

    print(
        f"Selected random response: "
        f"type={response_type}, value={value}"
    )

    # --------------------------------------------------------
    # Normal text
    # --------------------------------------------------------

    if response_type == "text":
        await channel.send(value)
        return

    # --------------------------------------------------------
    # YouTube URL
    # --------------------------------------------------------

    if response_type == "youtube":
        await channel.send(value)
        return

    # --------------------------------------------------------
    # GIF URL
    # --------------------------------------------------------

    if response_type == "gif":
        await channel.send(value)
        return

    # --------------------------------------------------------
    # Emoji
    # --------------------------------------------------------

    if response_type == "emoji":

        emoji = get_emoji(value)

        if emoji is None:
            return

        await channel.send(str(emoji))
        return

    # --------------------------------------------------------
    # Unknown type
    # --------------------------------------------------------

    print(
        f"Unknown response type: {response_type}"
    )


# ============================================================
# EVENTS
# ============================================================

@client.event
async def on_ready():

    print("---------------------------------------")
    print(f"Logged in as: {client.user}")
    print(f"Bot ID: {client.user.id}")
    print("---------------------------------------")

    print("Custom emojis visible to bot:")

    for emoji in client.emojis:
        print(f"  {emoji.name}: {emoji.id}")

    print("---------------------------------------")


@client.event
async def on_message(message):

    # --------------------------------------------------------
    # Ignore bot messages
    # --------------------------------------------------------

    if message.author.bot:
        return


    # --------------------------------------------------------
    # Determine whether this message @mentioned the bot
    # --------------------------------------------------------

    bot_was_mentioned = (
        client.user.id
        in [user.id for user in message.mentions]
    )


    # ========================================================
    # MENTION RESPONSE
    # ========================================================

    if bot_was_mentioned:

        print(
            f"Bot was mentioned by {message.author}"
        )

        if roll_chance(MENTION_RESPONSE_CHANCE):

            print(
                "Mention RNG succeeded. "
                "Sending random response."
            )

            try:
                await send_random_response(
                    message.channel
                )

            except discord.Forbidden:
                print(
                    "Bot does not have permission "
                    "to send messages here."
                )

            except discord.HTTPException as error:
                print(
                    f"Could not send random response: "
                    f"{error}"
                )

        else:
            print(
                "Mention RNG failed. "
                "No response sent."
            )


    # ========================================================
    # TRIGGER DETECTION
    # ========================================================

    message_text = message.content.casefold()

    trigger_was_detected = False


    # --------------------------------------------------------
    # Add reactions for matching triggers
    # --------------------------------------------------------

    for trigger, configured_emoji in TRIGGERS.items():

        if trigger.casefold() in message_text:

            trigger_was_detected = True

            print(
                f"Trigger detected: {trigger}"
            )

            emoji = get_emoji(
                configured_emoji
            )

            if emoji is None:
                continue

            try:
                await message.add_reaction(
                    emoji
                )

            except discord.Forbidden:
                print(
                    f"Missing permission to react in "
                    f"#{message.channel}"
                )

            except discord.HTTPException as error:
                print(
                    f"Could not react with "
                    f"{emoji}: {error}"
                )


    # ========================================================
    # RANDOM TRIGGER RESPONSE
    # ========================================================

    if trigger_was_detected:

        # Optionally prevent a message from getting both an
        # @mention random response and a trigger random response.
        should_roll_trigger_response = (
            ALLOW_TRIGGER_RESPONSE_ON_MENTION
            or not bot_was_mentioned
        )

        if should_roll_trigger_response:

            if roll_chance(
                TRIGGER_RESPONSE_CHANCE
            ):

                print(
                    "Trigger response RNG succeeded. "
                    "Sending random response."
                )

                try:
                    await send_random_response(
                        message.channel
                    )

                except discord.Forbidden:
                    print(
                        "Bot does not have permission "
                        "to send messages here."
                    )

                except discord.HTTPException as error:
                    print(
                        f"Could not send trigger "
                        f"response: {error}"
                    )

            else:
                print(
                    "Trigger response RNG failed. "
                    "Reaction only."
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