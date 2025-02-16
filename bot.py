import aiohttp, asyncio, warnings, pytz
from datetime import datetime, timedelta
from pytz import timezone
from pyrogram import Client, __version__
from pyrogram.raw.all import layer
from config import Config
from aiohttp import web
from route import web_server
import pyrogram.utils
import pyromod
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import os
import time

pyrogram.utils.MIN_CHANNEL_ID = -1009147483647

# Setting SUPPORT_CHAT directly here
SUPPORT_CHAT = int(os.environ.get("SUPPORT_CHAT", "-1002419010340"))

class Bot(Client):

    def __init__(self):
        super().__init__(
            name="codeflixbots",
            api_id=Config.API_ID,
            api_hash=Config.API_HASH,
            bot_token=Config.BOT_TOKEN,
            workers=200,
            plugins={"root": "plugins"},
            sleep_threshold=15,
        )
        # Initialize the bot's start time for uptime calculation
        self.start_time = time.time()

    async def health_check(self, request):
        """Handle health check requests"""
        return web.Response(text="OK", status=200)

    async def setup_health_server(self):
        """Setup minimal server for health checks"""
        try:
            app = web.Application()
            app.router.add_get("/health", self.health_check)
            app.router.add_get("/", self.health_check)
            runner = web.AppRunner(app)
            await runner.setup()
            site = web.TCPSite(runner, "0.0.0.0", 8080)
            await site.start()
            print("Health check server started on port 8080")
        except Exception as e:
            print(f"Failed to start health server: {e}")

    async def start(self):
        await super().start()
        me = await self.get_me()
        self.mention = me.mention
        self.username = me.username

        if Config.WEBHOOK:
            try:
                app = web.AppRunner(await web_server())
                await app.setup()
                await web.TCPSite(app, "0.0.0.0", 8080).start()
                print("Webhook server started")
            except Exception as e:
                print(f"Failed to start webhook server: {e}")
        else:
            await self.setup_health_server()
        
        print(f"{me.first_name} is Started.....✨️")

        # Calculate uptime using timedelta
        uptime_seconds = int(time.time() - self.start_time)
        uptime_string = str(timedelta(seconds=uptime_seconds))

        for chat_id in [Config.LOG_CHANNEL, SUPPORT_CHAT]:
            try:
                curr = datetime.now(timezone("Asia/Kolkata"))
                date = curr.strftime('%d %B, %Y')
                time_str = curr.strftime('%I:%M:%S %p')
                
                await self.send_photo(
                    chat_id=chat_id,
                    photo=Config.START_PIC,
                    caption=(
                        "**Anya is Restarted Again!**\n\n"
                        f"I didn't sleep since: `{uptime_string}`"
                    ),
                    reply_markup=InlineKeyboardMarkup(
                        [[
                            InlineKeyboardButton("Updates", url="https://t.me/codeflix_bots")
                        ]]
                    )
                )
            except Exception as e:
                print(f"Failed to send message in chat {chat_id}: {e}")


if __name__ == "__main__":
    bot = Bot()
    bot.run()
