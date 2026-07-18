#                © Copyright 2025
#            ✈ https://t.me/json1c_modules
# 🆓 Released into the public domain under The Unlicense.
#
# This is free and unencumbered software released into the public domain.
# Anyone is free to copy, modify, publish, use, compile, sell, or
# distribute this software, for any purpose, commercial or non-commercial.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND.

# meta developer: @json1c_modules

import asyncio
import random
import shutil
import tempfile

from .. import loader, utils


@loader.tds
class LiquidRescaleMod(loader.Module):
    strings = {
        "name": "Liquid Rescale",
        "not_enough_args_lqp": "<emoji document_id=5474625173887917717>🧠</emoji> <b>Жмыхнуть аву:</b> \n\n<code>.lqp [реплай 💬]</code>",
        "not_enough_args_lq": "<emoji document_id=5474625173887917717>🧠</emoji> <b>Жмыхнуть фото:</b> \n\n<code>.lq [реплай 🖼]</code>",
        "processing": "<emoji document_id=5386367538735104399>⌛</emoji> <b>Обработка...</b>",
        "install_imagemagick": "Установите ImageMagick: <code>apt install imagemagick</code>"
    }

    async def lqpcmd(self, message):
        """Жмыхнуть аву [реплай 💬]"""

        reply = await message.get_reply_message()

        if not reply:
            return await utils.answer(
                message,
                self.strings("not_enough_args_lqp")
            )

        if not self.check_imagemagick():
            return await utils.answer(
                message,
                self.strings("install_imagemagick")
            )

        response = await utils.answer(
            message,
            self.strings("processing")
        )

        with (
            tempfile.NamedTemporaryFile(mode="wb+", suffix=".jpg") as tmp_in,
            tempfile.NamedTemporaryFile(mode="wb+", suffix=".jpg") as tmp_out
        ):
            await message.client.download_profile_photo(reply.from_id, tmp_in.name)
            await self.liquid_rescale(tmp_in.name, tmp_out.name)

            if isinstance(response, list): # GeekTG
                await response[0].delete()
            else:
                await response.delete()

            with open(tmp_out.name, "rb") as out_file:
                await utils.answer(
                    message,
                    out_file
                )

    async def lqcmd(self, message):
        """Жмыхнуть фото [реплай 🖼]"""

        reply = await message.get_reply_message()

        if not reply:
            return await utils.answer(
                message,
                self.strings("not_enough_args_lq")
            )

        if not reply.photo:
            return await utils.answer(
                message,
                self.strings("not_enough_args_lq")
            )

        if not self.check_imagemagick():
            return await utils.answer(
                message,
                self.strings("install_imagemagick")
            )

        response = await utils.answer(
            message,
            self.strings("processing")
        )

        with (
            tempfile.NamedTemporaryFile(mode="wb+", suffix=".jpg") as tmp_in,
            tempfile.NamedTemporaryFile(mode="wb+", suffix=".jpg") as tmp_out
        ):
            await message.client.download_media(reply.photo, tmp_in.name)
            await self.liquid_rescale(tmp_in.name, tmp_out.name)

            if isinstance(response, list): # GeekTG
                await response[0].delete()
            else:
                await response.delete()

            with open(tmp_out.name, "rb") as out_file:
                await utils.answer(
                    message,
                    out_file
                )

    def check_imagemagick(self):
        return shutil.which("magick") or shutil.which("convert")

    # thx https://github.com/mercury-devel/photoeditor/blob/main/func/editor.py
    async def liquid_rescale(self, input_path: str, output_path: str):
        if random.choice([True, False]):
            p1, p2 = "%", ""
        else:
            p1, p2 = "", "%"

        s1 = random.randint(25, 100)
        s2 = random.randint(25, 100)

        args = [
            self.check_imagemagick(),
            input_path,
            "-alpha", "set",
            "-liquid-rescale", f"{s1}{p1}x{s2}{p2}",
            output_path,
        ]

        proc = await asyncio.create_subprocess_exec(
            *args,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        _, err = await proc.communicate()

        if proc.returncode != 0:
            raise RuntimeError(
                f"ImageMagick упал с кодом {proc.returncode}:\n{err.decode(errors='ignore')}"
            )