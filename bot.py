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
SUPPORT_CHAT = int(os.environ.get("SUPPORT_CHAT", "-1001566837125"))

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

    async def setup_web_server(self):
        """Setup web server with health check endpoint"""
        app = web.Application()
        app.router.add_get("/health", self.health_check)
        app.router.add_get("/", self.health_check)  # Root path for health checks
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, "0.0.0.0", 8000)
        await site.start()
        print("Web server started on port 8000")

    async def start(self):  
        await super().start()  
        me = await self.get_me()  
        self.mention = me.mention  
        self.username = me.username    
        self.uptime = Config.BOT_UPTIME       

        # Always start the web server for health checks
        await self.setup_web_server()
        
        print(f"{me.first_name} Is Started.....✨️")  

        # Calculate uptime using timedelta  
        uptime_seconds = int(time.time() - self.start_time)  
        uptime_string = str(timedelta(seconds=uptime_seconds))  

        for chat_id in [Config.LOG_CHANNEL]:  
            try:  
                curr = datetime.now(timezone("Asia/Kolkata"))  
                date = curr.strftime('%d %B, %Y')  
                time_str = curr.strftime('%I:%M:%S %p')  
                  
                # Send the message with the photo  
                await self.send_photo(  
                    chat_id=chat_id,  
                    photo=Config.START_PIC,  
                    caption=(  
                        "**ᴀɴʏᴀ ɪs ʀᴇsᴛᴀʀᴛᴇᴅ ᴀɢᴀɪɴ  !**\n\n"  
                        f"ɪ ᴅɪᴅɴ'ᴛ sʟᴇᴘᴛ sɪɴᴄᴇ: `{uptime_string}`"  
                    ),  
                    reply_markup=InlineKeyboardMarkup(  
                        [[  
                            InlineKeyboardButton("ᴜᴘᴅᴀᴛᴇs", url="https://t.me/codeflix_bots")  
                        ]]  
                    )  
                )  

            except Exception as e:  
                print(f"Failed to send message in chat {chat_id}: {e}")

if __name__ == "__main__":
    bot = Bot()
    bot.run()
