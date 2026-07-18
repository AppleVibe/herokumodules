# █▀▀▄   █▀▄▀█ █▀█ █▀▄ █▀
# ▀▀▀█ ▄ █ ▀ █ █▄█ █▄▀ ▄█

# #### Copyright (c) 2026 Archquise #####

# 💬 Contact: https://t.me/archquise
# 🔒 Licensed under the GNU AGPLv3.
# 📄 LICENSE: https://raw.githubusercontent.com/archquise/Q.Mods/main/LICENSE
# ---------------------------------------------------------------------------------
# Name: UniversalDownloader  # noqa: ERA001
# Description: Downloads media from YouTube, VK, TikTok, and all yt-dlp supported sites
# Author: @quise_m
# ---------------------------------------------------------------------------------
# meta developer: @quise_m
# meta banner: https://raw.githubusercontent.com/archquise/qmods_meta/main/UniversalDownloader.png
# requires: yt_dlp ffmpeg
# ---------------------------------------------------------------------------------

import logging
import os
import platform
import re
import shutil
import zipfile
from http import HTTPStatus

import aiofiles
import aiohttp
from yt_dlp import YoutubeDL

from .. import loader, utils

logger = logging.getLogger(__name__)


@loader.tds
class UniversalDownloaderMod(loader.Module):
    """Downloads media from YouTube, VK, TikTok, and all yt-dlp supported sites"""  # noqa: D400, D415

    strings = {  # noqa: RUF012
        "name": "UniversalDownloader",
        "_cls_doc": "Downloads media from YouTube, VK, TikTok, and all yt-dlp supported sites",  # noqa: E501
        "select_download_type": "<tg-emoji emoji-id=5879883461711367869>⬇️</tg-emoji> <b>Select download type:</b>",  # noqa: E501
        "invalid_args": "<emoji document_id=5854929766146118183>❌</emoji> There is no arguments or they are invalid",  # noqa: E501
        "downloading": "<emoji document_id=5215484787325676090>🕐</emoji> Downloading...",  # noqa: E501
        "cookie_desc": "Cookie account (helps downloading video with strict age rating restricrions)",  # noqa: E501
        "deno_err": '<tg-emoji emoji-id=5879813604068298387>❗️</tg-emoji> <b>Error!</b> The <a href="http://deno.land/">Deno</a> JavaScript engine was not install automatically.\nThis is a required dependency for <a href="https://github.com/yt-dlp/yt-dlp">yt-dlp</a> (a library for downloading video/audio) to work correctly.\n\n<b>To continue, you need to install the engine manually, or resolve any issues preventing automatic installation and restart the userbot.</b>',  # noqa: E501
        "err": "<tg-emoji emoji-id=5879813604068298387>❗️</tg-emoji> <b>Error!</b>\n\nAdditional info: {}",  # noqa: E501
        "video": "video",
        "audio": "audio",
    }

    strings_ru = {  # noqa: RUF012
        "_cls_doc": "Скачивает медиа из YouTube, VK, TikTok и всех поддерживаемых yt-dlp сайтов",  # noqa: E501
        "select_download_type": "<tg-emoji emoji-id=5879883461711367869>⬇️</tg-emoji> <b>Выберите тип загрузки:</b>",  # noqa: E501
        "invalid_args": "<emoji document_id=5854929766146118183>❌</emoji> Нет аргументов или они неверны",  # noqa: E501
        "downloading": "<emoji document_id=5215484787325676090>🕐</emoji> Скачиваю...",
        "cookie_desc": "Куки аккаунта (помогает скачивать видео с жесткими возрастными ограничениями)",  # noqa: E501, RUF001
        "deno_err": '<tg-emoji emoji-id=5879813604068298387>❗️</tg-emoji> <b>Ошибка!</b> JS-движок <a href="http://deno.land/">Deno</a> не установился автоматически.\nЭто необходимая зависимость для корректной работы <a href="https://github.com/yt-dlp/yt-dlp">yt-dlp</a> (библиотека для скачивания видео/аудио).\n\n<b>Для продолжения вам необходимо установить движок вручную, или устранить препятствия для автоматической установки и перезагрузить юзербота.</b>',  # noqa: E501
        "err": "<tg-emoji emoji-id=5879813604068298387>❗️</tg-emoji> <b>Ошибка!</b>\n\nДоп.информация: {}",  # noqa: E501, RUF001
        "video": "видео",
        "audio": "аудио",
    }

    deno_error = (
        "Deno wasn't installed in auto-mode.",
        "Please, install it manually or resolve the issue and reboot userbot.",
    )

    def _validate_url(self, url: str) -> bool:
        """Validate URL format."""
        if not url:
            return False

        url_pattern = re.compile(
            r"https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)",
            re.IGNORECASE,
        )

        return url_pattern.match(url) is not None

    async def get_target(self) -> str:
        """Check OS and processor architecture and return right postfix."""
        system = platform.system()
        machine = platform.machine().lower()

        if system == "Windows":
            return "Windows"

        if system == "Darwin":
            return (
                "aarch64-apple-darwin" if machine == "arm64" else "x86_64-apple-darwin"
            )

        if system == "Linux":
            return (
                "aarch64-unknown-linux-gnu"
                if machine in ("aarch64", "arm64")
                else "x86_64-unknown-linux-gnu"
            )

        return "x86_64-unknown-linux-gnu"

    def _get_deno(self) -> str | None:
        if not (source := self.get("deno_source")) or source == "install_failed" or not os.path.exists(source):
            logger.critical("%s %s", *self.deno_error)
            return None
        return source


    def __init__(self):  # noqa: ANN204, D107
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "youtube_cookie",
                None,
                lambda: self.strings["cookie_desc"],
                validator=loader.validators.Hidden(),
            ),
        )

    async def client_ready(self, client, db):  # noqa: ANN001, ANN201, D102, ARG002

        deno_which = shutil.which("deno", path=os.environ.get("PATH", "") + os.pathsep + os.getcwd())  # noqa: E501

        if deno_which:
            self.set("deno_source", deno_which)
            return

        logger.warning("Deno is not installed, attempting installation...")
        target = await self.get_target()
        if target == "Windows":
            logger.critical(
                "Windows platform is unsupported, please, unload the module.",
            )
            return
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(60)) as session:
            download_link = f"https://github.com/denoland/deno/releases/latest/download/deno-{target}.zip"
            async with session.get(download_link) as resp:
                if resp.status == HTTPStatus.OK:
                    async with aiofiles.open("deno.zip", mode="wb") as f:
                        async for chunk in resp.content.iter_chunked(8192):
                            await f.write(chunk)
                else:
                    logger.critical("Failed to download Deno: HTTP %s", resp.status)
                    self.set("deno_source", "install_failed")
                    return
        if os.path.exists('deno.zip'):
            with zipfile.ZipFile("deno.zip", "r") as zip_ref:
                zip_ref.extractall()
            os.remove('deno.zip')
            os.chmod(path=os.path.join(os.getcwd(), "deno"), mode=0o755)
            self.set("deno_source", os.path.join(os.getcwd(), "deno"))
        return

    @loader.command(en_doc="Download media", ru_doc="Скачать медиа")
    async def unidlcmd(self, message) -> None:  # noqa: ANN001, D102
        args = utils.get_args(message)
        if not args or not self._validate_url(args[0]) or len(args) > 1:
            await utils.answer(message, self.strings["invalid_args"])
            return

        async def _download_media(call, download_type: str) -> None:

            if not (source := self._get_deno()):
                await call.edit(self.strings["deno_err"])
                return

            await call.answer()
            await call.delete()

            downloading_msg = await self._client.send_message(message.chat_id, self.strings["downloading"], reply_to=message.reply_to_msg_id)  # noqa: E501

            ydl_opts = {
                "quiet": True,
                "js_runtimes": {"deno": {"path": source}},
            }

            if cookie := self.get("youtube_cookie"):
                ydl_opts["cookiefile"] = cookie

            if download_type == "audio":
                ydl_opts["outtmpl"] = f"audio_{message.id}.%(ext)s"
                ydl_opts["format"] = "bestaudio/best"
                ydl_opts["postprocessors"] = [
                    {
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "mp3",
                        "preferredquality": "0",
                    },
                    {
                        "key": "FFmpegMetadata",
                        "add_metadata": True,
                    },
                    {
                        "key": "EmbedThumbnail",
                    },
                ]
                ydl_opts["writethumbnail"] = True

            if download_type == "video":
                ydl_opts["outtmpl"] = f"video_{message.id}.%(ext)s"
                ydl_opts["format"] = "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"  # noqa: E501
                ydl_opts["merge_output_format"] = "mp4"

            try:
                with YoutubeDL(ydl_opts) as ydl:
                    info = await utils.run_sync(lambda: ydl.extract_info(args[0], download=True))  # noqa: E501
                    filename = ydl.prepare_filename(info).split(".")[0] + (".mp3" if download_type == "audio" else ".mp4")  # noqa: E501
                    await self._client.send_file(message.chat_id, filename, reply_to=message.reply_to_msg_id)  # noqa: E501
                    await downloading_msg.delete()
            except Exception as e:
                logger.exception("Catched error during download!")
                await call.answer()
                await downloading_msg.edit(self.strings["err"].format(e))
            finally:
                if os.path.exists(filename):
                    os.remove(filename)


        call = await self.inline.form("🪐", message)
        await message.delete()
        await call.edit(self.strings["select_download_type"], reply_markup=[[{"text": self.strings["video"], "callback": _download_media, "args": ("video",)}, {"text": self.strings["audio"], "callback": _download_media, "args": ("audio",)}]])  # noqa: E501