import os
import asyncio
import yt_dlp
import requests
from pyrogram import Client, filters
from pyrogram.types import Message
from vars import API_ID, API_HASH, BOT_TOKEN, PW_TOKEN, DOWNLOAD_PATH
from aiohttp import web

# Initialize the bot
bot = Client(
    "PW_Bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# Web server for Render deployment
routes = web.RouteTableDef()

@routes.get("/", allow_head=True)
async def root_route_handler(request):
    return web.Response(text="PW Downloader Bot is Running!")

async def start_web_server():
    app = web.Application()
    app.add_routes(routes)
    return app

# Start & Stop Bot Functions
async def start_bot():
    await bot.start()
    print("Bot is up and running")

async def stop_bot():
    await bot.stop()

async def main():
    # Start web server
    app_runner = web.AppRunner(await start_web_server())
    await app_runner.setup()
    site = web.TCPSite(app_runner, "0.0.0.0", int(os.getenv("PORT", 8080)))
    await site.start()
    print("Web Server Started on Render")

    # Start bot
    await start_bot()

    # Keep running
    try:
        while True:
            await asyncio.sleep(3600)  # Prevent auto shutdown
    except (KeyboardInterrupt, SystemExit):
        await stop_bot()

# Command: Start
@bot.on_message(filters.command(["start"]))
async def start_command(client, message):
    await message.reply_text(
        "**👋 Welcome to PW Downloader Bot!**\n\n"
        "📥 Send me a **Physics Wallah Video + PDF Link** to download both in one command."
    )

# Command: PW Video + PDF Download
@bot.on_message(filters.command(["pw"]))
async def download_pw_content(client, message: Message):
    try:
        # Ask for links (Video + PDF)
        await message.reply_text("📩 **Send the Physics Wallah Video + PDF URLs (one per line):**")
        user_input = await client.listen(message.chat.id)
        urls = user_input.text.strip().split("\n")

        video_url = None
        pdf_url = None

        # Identify Video & PDF URLs
        for url in urls:
            if "/master.mpd" in url:
                video_url = url.strip()
            elif "drive.google.com" in url or url.endswith(".pdf"):
                pdf_url = url.strip()

        if not video_url or not pdf_url:
            await message.reply_text("❌ **Invalid URLs! Please send a valid PW video (`.mpd`) and PDF link.**")
            return

        # Ask for video quality
        await message.reply_text("🎬 **Choose Resolution:**\n144, 240, 360, 480, 720, 1080")
        quality_input = await client.listen(message.chat.id)
        quality = quality_input.text.strip()

        resolution_map = {
            "144": "256x144",
            "240": "426x240",
            "360": "640x360",
            "480": "854x480",
            "720": "1280x720",
            "1080": "1920x1080"
        }
        res = resolution_map.get(quality, "720x480")

        # Ask for file name
        await message.reply_text("📌 **Enter File Name (or send 'default' to use original name):**")
        name_input = await client.listen(message.chat.id)
        file_name = name_input.text.strip()
        if file_name.lower() == "default":
            file_name = "PW_Content"

        video_file = os.path.join(DOWNLOAD_PATH, f"{file_name}.mp4")
        pdf_file = os.path.join(DOWNLOAD_PATH, f"{file_name}.pdf")

        # --- DOWNLOAD VIDEO ---
        await message.reply_text(f"⏳ **Downloading Video `{file_name}` in `{res}`...**")
        video_url_with_token = f"{video_url}?token={PW_TOKEN}"
        ydl_opts = {
            'outtmpl': video_file,
            'format': f'b[height<={quality}]/bv[height<={quality}]+ba/b/bv+ba',
            'merge_output_format': 'mp4',
            'noplaylist': True,
            'quiet': False
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url_with_token])

        # --- DOWNLOAD PDF ---
        await message.reply_text(f"⏳ **Downloading PDF `{file_name}.pdf`...**")
        if "drive.google.com" in pdf_url:
            file_id = pdf_url.split("/d/")[1].split("/")[0]
            pdf_url = f"https://drive.google.com/uc?export=download&id={file_id}"

        response = requests.get(pdf_url)
        if response.status_code == 200:
            with open(pdf_file, "wb") as file:
                file.write(response.content)

        # --- SEND FILES TO TELEGRAM ---
        await message.reply_video(
            video=video_file,
            caption=f"🎞 **Title:** {file_name}\n📚 **Source:** Physics Wallah\n⚡ **Quality:** {res}"
        )

        await message.reply_document(
            document=pdf_file,
            caption=f"📑 **Title:** {file_name}\n📚 **Source:** Physics Wallah"
        )

        # Delete files after sending
        os.remove(video_file)
        os.remove(pdf_file)

    except Exception as e:
        await message.reply_text(f"❌ **Error:** {str(e)}")

# Run the bot on Render
if __name__ == "__main__":
    asyncio.run(main())