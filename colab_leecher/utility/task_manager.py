# copyright 2024 © Xron Trix | https://github.com/cinelix

import os
import pytz
import shutil
import logging
from time import time
from datetime import datetime
from asyncio import sleep
from os import path as ospath, system
from colab_leecher import OWNER, colab_bot, DUMP_ID
from colab_leecher.downlader.manager import calDownSize, get_d_name, downloadManager
from colab_leecher.utility.helper import (
    getSize,
    applyCustomName,
    keyboard,
    sysINFO,
    is_google_drive,
    is_telegram,
    is_ytdl_link,
    is_mega,
    is_terabox,
    is_torrent,
)
from colab_leecher.utility.handler import (
    Leech,
    Unzip_Handler,
    Zip_Handler,
    SendLogs,
    cancelTask,
)
from colab_leecher.utility.variables import (
    BOT,
    MSG,
    BotTimes,
    Messages,
    Paths,
    Aria2c,
    Transfer,
    TaskError,
)


async def task_starter(message, text):
    global BOT
    await message.delete()
    BOT.State.started = True
    if not BOT.State.task_going:
        src_request_msg = await message.reply_text(text)
        return src_request_msg
    else:
        msg = await message.reply_text(
            "I am already working ! Please wait until I finish !!"
        )
        await sleep(15)
        await msg.delete()
        return None


async def taskScheduler():
    global BOT, MSG, BotTimes, Messages, Paths, Transfer, TaskError

    # Always reset down_path to default working folder
    Paths.down_path = f"{Paths.WORK_PATH}/Downloads"

    src_text = []
    is_dualzip = (BOT.Mode.type == "undzip")
    is_unzip = (BOT.Mode.type == "unzip")
    is_zip = (BOT.Mode.type == "zip")
    is_dir = (BOT.Mode.mode == "dir-leech")

    # Reset state
    Messages.download_name = ""
    Messages.task_msg = "<b>🦞 TASK MODE » </b>"
    Messages.dump_task = (
        Messages.task_msg
        + f"<i>{BOT.Mode.type.capitalize()} {BOT.Mode.mode.capitalize()} as {BOT.Setting.stream_upload}</i>\n\n<b>🖇️ SOURCES » </b>"
    )
    Transfer.sent_file = []
    Transfer.sent_file_names = []
    Transfer.down_bytes = [0, 0]
    Transfer.up_bytes = [0, 0]
    Messages.download_name = ""
    Messages.task_msg = ""
    Messages.status_head = "<b>📥 DOWNLOADING » </b>\n"

    if is_dir:
        if not ospath.exists(BOT.SOURCE[0]):
            TaskError.state = True
            TaskError.text = "Task Failed. Because: Provided Directory Path Not Exists"
            logging.error(TaskError.text)
            return
        os.makedirs(Paths.temp_dirleech_path, exist_ok=True)
        Messages.dump_task += f"\n\n📂 <code>{BOT.SOURCE[0]}</code>"
        Transfer.total_down_size = getSize(BOT.SOURCE[0])
        Messages.download_name = ospath.basename(BOT.SOURCE[0])
    else:
        for link in BOT.SOURCE:
            if is_telegram(link):
                ida = "💬"
            elif is_google_drive(link):
                ida = "♻️"
            elif is_torrent(link):
                ida = "🧲"
                Messages.caution_msg = "\n\n⚠️<i><b> Torrents Are Strictly Prohibited in Google Colab</b>, Try to avoid Magnets !</i>"
            elif is_ytdl_link(link):
                ida = "🏮"
            elif is_terabox(link):
                ida = "🍑"
            elif is_mega(link):
                ida = "💾"
            else:
                ida = "🔗"
            code_link = f"\n\n{ida} <code>{link}</code>"
            if len(Messages.dump_task + code_link) >= 4096:
                src_text.append(Messages.dump_task)
                Messages.dump_task = code_link
            else:
                Messages.dump_task += code_link

    # Get current date & time
    cdt = datetime.now(pytz.timezone("Asia/Kolkata"))
    dt = cdt.strftime(" %d-%m-%Y")
    Messages.dump_task += f"\n\n<b>📆 Task Date » </b><i>{dt}</i>"
    src_text.append(Messages.dump_task)

    # Clean previous work directory safely
    if ospath.exists(Paths.WORK_PATH):
        try:
            shutil.rmtree(Paths.WORK_PATH)
        except Exception as e:
            logging.warning(f"Failed to clear WORK_PATH: {e}")

    # Recreate download path cleanly
    os.makedirs(Paths.down_path, exist_ok=True)

    # Format DUMP_ID safely
    dump_str = str(DUMP_ID)
    if dump_str.startswith("-100"):
        Messages.link_p = dump_str[4:]
    elif dump_str.startswith("-"):
        Messages.link_p = dump_str[1:]
    else:
        Messages.link_p = dump_str

    try:
        system(f"aria2c -d {Paths.WORK_PATH} -o Hero.jpg {Aria2c.pic_dwn_url}")
    except Exception:
        Paths.HERO_IMAGE = Paths.DEFAULT_HERO

    MSG.sent_msg = await colab_bot.send_message(chat_id=DUMP_ID, text=src_text[0])

    if len(src_text) > 1:
        for lin in range(1, len(src_text)):
            MSG.sent_msg = await MSG.sent_msg.reply_text(text=src_text[lin], quote=True)

    Messages.src_link = f"https://t.me/c/{Messages.link_p}/{MSG.sent_msg.id}"
    Messages.task_msg += f"__[{BOT.Mode.type.capitalize()} {BOT.Mode.mode.capitalize()} as {BOT.Setting.stream_upload}]({Messages.src_link})__\n\n"

    await MSG.status_msg.delete()
    img = Paths.THMB_PATH if ospath.exists(Paths.THMB_PATH) else Paths.HERO_IMAGE
    MSG.status_msg = await colab_bot.send_photo(
        chat_id=OWNER,
        photo=img,
        caption=Messages.task_msg
        + Messages.status_head
        + "\n📝 __Starting DOWNLOAD...__"
        + sysINFO(),
        reply_markup=keyboard(),
    )

    await calDownSize(BOT.SOURCE)

    if not is_dir:
        await get_d_name(BOT.SOURCE[0])
    else:
        Messages.download_name = ospath.basename(BOT.SOURCE[0])

    if is_zip:
        Paths.down_path = ospath.join(Paths.down_path, Messages.download_name)
        os.makedirs(Paths.down_path, exist_ok=True)

    BotTimes.current_time = time()

    if BOT.Mode.mode != "mirror":
        await Do_Leech(BOT.SOURCE, is_dir, BOT.Mode.ytdl, is_zip, is_unzip, is_dualzip)
    else:
        await Do_Mirror(BOT.SOURCE, BOT.Mode.ytdl, is_zip, is_unzip, is_dualzip)


async def Do_Leech(source, is_dir, is_ytdl, is_zip, is_unzip, is_dualzip):
    if is_dir:
        for s in source:
            if not ospath.exists(s):
                logging.error("Provided directory does not exist !")
                await cancelTask("Provided directory does not exist !")
                return
            target_path = s
            if is_zip:
                await Zip_Handler(target_path, True, False)
                await Leech(Paths.temp_zpath, True)
            elif is_unzip:
                await Unzip_Handler(target_path, False)
                await Leech(Paths.temp_unzip_path, True)
            elif is_dualzip:
                await Unzip_Handler(target_path, False)
                await Zip_Handler(Paths.temp_unzip_path, True, True)
                await Leech(Paths.temp_zpath, True)
            else:
                if ospath.isdir(s):
                    await Leech(target_path, False)
                else:
                    Transfer.total_down_size = ospath.getsize(s)
                    os.makedirs(Paths.temp_dirleech_path, exist_ok=True)
                    shutil.copy(s, Paths.temp_dirleech_path)
                    Messages.download_name = ospath.basename(s)
                    await Leech(Paths.temp_dirleech_path, True)
    else:
        await downloadManager(source, is_ytdl)

        Transfer.total_down_size = getSize(Paths.down_path)

        # Renaming Files With Custom Name
        applyCustomName()

        # Preparing To Upload
        if is_zip:
            await Zip_Handler(Paths.down_path, True, True)
            await Leech(Paths.temp_zpath, True)
        elif is_unzip:
            await Unzip_Handler(Paths.down_path, True)
            await Leech(Paths.temp_unzip_path, True)
        elif is_dualzip:
            await Unzip_Handler(Paths.down_path, True)
            await Zip_Handler(Paths.temp_unzip_path, True, True)
            await Leech(Paths.temp_zpath, True)
        else:
            await Leech(Paths.down_path, True)

    await SendLogs(True)


async def Do_Mirror(source, is_ytdl, is_zip, is_unzip, is_dualzip):
    if not ospath.exists(Paths.MOUNTED_DRIVE):
        await cancelTask(
            "Google Drive is NOT MOUNTED ! Stop the Bot and Run the Google Drive Cell to Mount, then Try again !"
        )
        return

    os.makedirs(Paths.mirror_dir, exist_ok=True)

    await downloadManager(source, is_ytdl)

    Transfer.total_down_size = getSize(Paths.down_path)

    applyCustomName()

    cdt = datetime.now()
    # Fixed: No colons in folder names for Google Drive compatibility
    cdt_ = cdt.strftime("Uploaded » %Y-%m-%d %H-%M-%S")
    mirror_dir_ = ospath.join(Paths.mirror_dir, cdt_)

    if is_zip:
        await Zip_Handler(Paths.down_path, True, True)
        shutil.copytree(Paths.temp_zpath, mirror_dir_, dirs_exist_ok=True)
    elif is_unzip:
        await Unzip_Handler(Paths.down_path, True)
        shutil.copytree(Paths.temp_unzip_path, mirror_dir_, dirs_exist_ok=True)
    elif is_dualzip:
        await Unzip_Handler(Paths.down_path, True)
        await Zip_Handler(Paths.temp_unzip_path, True, True)
        shutil.copytree(Paths.temp_zpath, mirror_dir_, dirs_exist_ok=True)
    else:
        shutil.copytree(Paths.down_path, mirror_dir_, dirs_exist_ok=True)

    await SendLogs(False)
