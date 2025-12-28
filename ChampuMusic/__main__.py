import asyncio
import importlib

import config
from config import BANNED_USERS
from ChampuMusic import HELPABLE, LOGGER, ALL_MODULES
from ChampuMusic.core.call import Champu
from ChampuMusic.utils.database import get_banned_users, get_gbanned

# Remove global app and userbot imports

async def init():
    # Check if any STRING session is defined
    if (
        not config.STRING1
        and not config.STRING2
        and not config.STRING3
        and not config.STRING4
        and not config.STRING5
    ):
        LOGGER("ChampuMusic").error(
            "ᴀssɪsᴛᴀɴᴛ ᴄʟɪᴇɴᴛ ᴠᴀʀɪᴀʙʟᴇs ɴᴏᴛ ᴅᴇғɪɴᴇᴅ, ᴇxɪᴛɪɴɢ..."
        )
        return

    if not config.SPOTIFY_CLIENT_ID or not config.SPOTIFY_CLIENT_SECRET:
        LOGGER("ChampuMusic").warning(
            "ɴᴏ sᴘᴏᴛɪғʏ ᴠᴀʀs ᴅᴇғɪɴᴇᴅ. sᴘᴏᴛɪғʏ ǫᴜᴇʀɪᴇs ᴡᴏɴ'ᴛ ᴡᴏʀᴋ."
        )

    # ⚡ Create the Pyrogram clients inside the loop
    from ChampuMusic import ChampuBot
    from pyrogram import Client as UserClient  # if you have a separate userbot session

    app = ChampuBot()
    userbot = UserClient(
        "userbot",
        api_id=config.API_ID,
        api_hash=config.API_HASH,
        session_string=config.STRING1,  # or STRING2-5 depending on usage
    )

    await app.start()
    await userbot.start()

    # Load banned users
    try:
        for user_id in await get_gbanned():
            BANNED_USERS.add(user_id)
        for user_id in await get_banned_users():
            BANNED_USERS.add(user_id)
    except Exception:
        pass

    # Load modules
    for module in ALL_MODULES:
        imported = importlib.import_module(module)
        if getattr(imported, "__MODULE__", None) and getattr(imported, "__HELP__", None):
            HELPABLE[imported.__MODULE__.lower()] = imported

    LOGGER("ChampuMusic.plugins").info("Modules imported successfully")

    # Start voice call service
    await Champu.start()
    await Champu.decorators()

    LOGGER("ChampuMusic").info("Champu Music Bot started successfully")

    # Keep alive
    await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(init())
