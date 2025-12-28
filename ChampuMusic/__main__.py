import asyncio
import importlib

import config
from config import BANNED_USERS
from ChampuMusic import HELPABLE, LOGGER, app, userbot
from ChampuMusic.core.call import Champu
from ChampuMusic.plugins import ALL_MODULES
from ChampuMusic.utils.database import get_banned_users, get_gbanned


async def init():
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

    if not config.SPOTIFY_CLIENT_ID and not config.SPOTIFY_CLIENT_SECRET:
        LOGGER("ChampuMusic").warning(
            "ɴᴏ sᴘᴏᴛɪғʏ ᴠᴀʀs ᴅᴇғɪɴᴇᴅ. sᴘᴏᴛɪғʏ ǫᴜᴇʀɪᴇs ᴡᴏɴ'ᴛ ᴡᴏʀᴋ."
        )

    await app.start()
    await userbot.start()

    try:
        for user_id in await get_gbanned():
            BANNED_USERS.add(user_id)
        for user_id in await get_banned_users():
            BANNED_USERS.add(user_id)
    except Exception:
        pass

    for module in ALL_MODULES:
        imported = importlib.import_module(module)
        if getattr(imported, "__MODULE__", None) and getattr(imported, "__HELP__", None):
            HELPABLE[imported.__MODULE__.lower()] = imported

    LOGGER("ChampuMusic.plugins").info("Modules imported successfully")

    await Champu.start()
    await Champu.decorators()

    LOGGER("ChampuMusic").info("Champu Music Bot started successfully")

    # ✅ SAFE replacement for pyrogram.idle()
    await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(init())
