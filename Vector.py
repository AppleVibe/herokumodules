# ====================================================================================================================
#   ██████╗  ██████╗ ██╗   ██╗███╗   ███╗ ██████╗ ██████╗ ██╗   ██╗██╗     ███████╗███████╗
#  ██╔════╝ ██╔═══██╗╚██╗ ██╔╝████╗ ████║██╔═══██╗██╔══██╗██║   ██║██║     ██╔════╝██╔════╝
#  ██║  ███╗██║   ██║ ╚████╔╝ ██╔████╔██║██║   ██║██║  ██║██║   ██║██║     █████╗  ███████╗
#  ██║   ██║██║   ██║  ╚██╔╝  ██║╚██╔╝██║██║   ██║██║  ██║██║   ██║██║     ██╔══╝  ╚════██║
#  ╚██████╔╝╚██████╔╝   ██║   ██║ ╚═╝ ██║╚██████╔╝██████╔╝╚██████╔╝███████╗███████╗███████║
#   ╚═════╝  ╚═════╝    ╚═╝   ╚═╝     ╚═╝ ╚═════╝ ╚═════╝  ╚═════╝ ╚══════╝╚══════╝╚══════╝
#
#   OFFICIAL USERNAMES: @goymodules | @samsepi0l_ovf
#   MODULE: vector
#
#   THIS MODULE IS LICENSED UNDER GNU AGPLv3, PROTECTED AGAINST UNAUTHORIZED COPYING/RESALE,
#   AND ITS ORIGINAL AUTHORSHIP BELONGS TO @samsepi0l_ovf.
#   ALL OFFICIAL UPDATES, RELEASE NOTES, AND PATCHES ARE PUBLISHED IN THE TELEGRAM CHANNEL @goymodules.
# ====================================================================================================================
# meta banner: https://raw.githubusercontent.com/sepiol026-wq/GoyModules/refs/heads/main/assets/vector.png
# meta pic: https://raw.githubusercontent.com/sepiol026-wq/GoyModules/refs/heads/main/assets/vecpic.png
# meta developer: @GoyModules
# meta tags: module-catalog, search, reviews, ratings, comments, heroku, каталог-модулей, поиск, отзывы, рейтинги, комментарии, хероку

__version__ = (2, 4, 3)

import asyncio
import base64
import hashlib
import hmac
import json
import logging
import re
import time
import unicodedata
from contextlib import suppress
from typing import Any, Dict, List, Optional
from urllib.parse import quote, urljoin

import aiohttp
from herokutl.tl.functions.contacts import UnblockRequest
from herokutl.tl.functions.account import UpdateNotifySettingsRequest, GetNotifySettingsRequest
from herokutl.tl.types import InputNotifyPeer, InputPeerNotifySettings
from herokutl.types import Message

from .. import loader, utils

log = logging.getLogger("VectorMonolith")
log.setLevel(logging.DEBUG)

apirt = "https://www.0xvector.lol"
jwtrx = re.compile(r"eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+")
auths = "vektor_heroku_searchmodulesModbySepiol026-wqGithub"
lping = "#v_lang_ping"
lpong = "#v_lang:"
brrx = re.compile(r"(?:Причина|Reason|理由|Grund|R3450n|Weason|Charge):\s*(.+)", re.IGNORECASE)
btrx = re.compile(r"(?:Срок|Term|期間|Dauer|73rm|Tewm):\s*(.+)", re.IGNORECASE)

@loader.tds
class Vector(loader.Module):

    strings = {
        "lang": "en",
        "name": "Vector",
        "_cls_doc": "Search modules for Heroku.\nhttps://www.0xvector.lol",
        "v_dev_lbl": "Author:",
        "v_dev_str": "Dev:",
        "v_dev_ofc": "official",
        "v_dev_unofc": "unofficial",
        "v_info": "Info:",
        "v_tags": "Tags:",
        "v_cmds": "Usage:",
        "v_deps": "Dependencies:",
        "v_reqs": "Libs:",
        "v_hid_cmd": "+ {rem} hidden cmds.",
        "v_hid_req": "+ {rem} hidden libs.",
        "v_res_hdr": "Found Items:",
        "v_err_empty": "Specify query: {p}vector <text>",
        "v_err_404": "No records for: {q}",
        "v_err_len": "Query length is limited to 120 chars.",
        "v_err_api": "Access denied by Vector Server.",
        "v_ban_notice": "⛔ <b>Vector access blocked.</b>\n<b>Reason:</b> <code>{reason}</code>\n<b>Term:</b> <code>{term}</code>",
        "v_fb_add": "Rated successfully!",
        "v_fb_rm": "Rating cleared!",
        "v_btn_copy": "Query",
        "v_btn_dl": "Install",
        "v_page": "[{idx}/{total}]",
        "v_btn_code": "Source",
        "v_dl_ok": "Module installed successfully!",
        "v_dl_err": "Installation failed!",
        "v_lim_cfg": "Search output limits.",
        "v_max_batch_cfg": "Max modules per batch install.",
        "v_auto_upd_cfg": "Notify me about module updates (hashing-based).",
        "v_btn_sec": "🛡 Security Scan",
        "v_aud_hdr": "Code Audit: {name}",
        "v_aud_req": "Connecting to Security API...",
        "v_aud_proc": "Processing AST tree...",
        "v_btn_aud_run": "Start Scan",
        "v_aud_mem": "Loaded from session cache.",
        "v_aud_lvl": "Threat Level",
        "v_aud_stat": "Scanner Data",
        "v_aud_out": "Summary",
        "v_aud_sigs": "Triggers",
        "v_sig_crit": "Critical",
        "v_sig_warn": "Warnings",
        "v_sig_info": "Notices",
        "v_aud_none": "Not scanned yet. Takes 1 API slot.",
        "v_aud_no_txt": "No summary generated.",
        "v_aud_left": "Slots left: {remaining}/{limit}",
        "v_aud_zero": "Daily audit limit depleted.",
        "v_aud_err": "Scanner server is down.",
        "v_err_gui": "Interface rendering error.",
        "v_btn_exp": "🔽 Expand",
        "v_btn_col": "🔼 Collapse",
        "v_btn_talk": "💬 Discussion",
        "v_talk_hdr": "{emoji} <b>Thread: {name}</b>",
        "v_talk_desc": "Community reviews",
        "v_talk_num": "Posts: {count}",
        "v_talk_0": "Thread is empty. Be the first!",
        "v_talk_err": "Could not connect to thread.",
        "v_rep_ok": "Posted!",
        "v_rep_err": "Request failed.",
        "v_btn_bck": "⬅️ Back",
        "v_btn_wrt": "✍️ Post Reply",
        "v_rep_ask": "Reply to post message.\n2-1800 chars.",
        "v_rep_snt": "Uploading...",
        "v_rep_min": "Text is too short.",
        "v_rep_max": "Limit exceeded.",
        "v_rep_cncl": "Cancelled.",
        "v_loading_ui": "Searching Vector database...",
        "v_sending": "Loading...",
        "v_more_replies": "...and {count} more replies on the site.",
        "v_more_comments": "...and more comments on the site.",
        "v_upd_req": "Updating Vector...",
        "v_upd_ok": "Vector updated successfully!",
        "v_upd_err": "Update failed!",
        "v_upd_check": "Checking hashes…",
        "v_install_log_hdr": "Install log: {name}",
        "v_install_fail_forbidden": "Forbidden method: <code>{detail}</code>",
        "v_install_fail_requirements": "Pip deps failed: <code>{detail}</code>",
        "v_install_fail_dependency": "Missing dependency: <code>{detail}</code>",
        "v_install_fail_packages": "System pkgs failed: <code>{detail}</code>",
        "v_install_fail_core_overwrite": "Tried to overwrite core <code>{detail}</code>",
        "v_install_fail_ffmpeg": "Requires ffmpeg (not installed)",
        "v_install_fail_inline": "Requires inline mode (unavailable)",
        "v_install_fail_heroku_min": "Needs Heroku ≥ <code>{detail}</code>",
        "v_install_fail_not_found": "Not found in configured repos",
        "v_install_fail_download": "Failed to download module",
        "v_install_fail_unknown": "Unknown error: <code>{detail}</code>",
        "v_upd_same": "🌟 <b>You are on the latest version. Update anyway?</b>",
        "v_upd_force_btn": "🧭 Update",
        "v_dlcoll_hdr": "<b>Collection {name}</b>",
        "v_dlcoll_count": "{count} modules",
        "v_dlcoll_start": "<b>Installing all modules from collection...</b>",
        "v_dlcoll_done": "<b>All modules from collection installed</b>",
        "v_dlcoll_done_partial": "<b>Some modules failed to install</b>",
        "v_dlcoll_done_none": "<b>No modules were installed</b>",
        "v_dlcoll_fail_item": "❌ {name}: {reason}",
        "v_dlcoll_empty": "<b>Collection is empty</b>",
        "v_dlcoll_not_found": "<b>Collection not found</b>",
"v_vecdl_usage": "<b>Specify collection: </b><code>{p}vecdl <slug or URL></code>",
        "v_dlcoll_max_batch": "Collection has {total} modules, max {max} per batch. Installing first {max}…",
        "v_upd_cancel": "🚫 Cancel",
        "v_miniapp_title": "Open in Mini App",
        "v_miniapp_body": "Open Vector as a Telegram Mini App — instant auto-login, no passwords, fully encrypted session. One tap and you're in.",
        "v_miniapp_btn": "🚀 Open Vector",
    }

    strings_ru = {
        "lang": "ru",
        "_cls_doc": "Поиск модулей для Heroku.\nhttps://www.0xvector.lol",
        "v_dev_lbl": "Автор:",
        "v_dev_str": "Разраб:",
        "v_dev_ofc": "офиц",
        "v_dev_unofc": "неофиц",
        "v_info": "Инфо:",
        "v_tags": "Теги:",
        "v_cmds": "Использование:",
        "v_deps": "Зависимости:",
        "v_reqs": "Библиотеки:",
        "v_hid_cmd": "+ скрыто команд: {rem}.",
        "v_hid_req": "+ скрыто либ: {rem}.",
        "v_res_hdr": "Найденные модули:",
        "v_err_empty": "Укажите запрос: {p}vector <текст>",
        "v_err_404": "Нет записей по запросу: {q}",
        "v_err_len": "Длина запроса ограничена 120 символами.",
        "v_err_api": "Отказ в доступе от сервера Vector.",
        "v_ban_notice": "⛔ <b>Доступ к Vector заблокирован.</b>\n<b>Причина:</b> <code>{reason}</code>\n<b>Срок:</b> <code>{term}</code>",
        "v_fb_add": "Оценка добавлена!",
        "v_fb_rm": "Оценка удалена!",
        "v_btn_copy": "Запрос",
        "v_btn_dl": "Установить",
        "v_page": "[{idx}/{total}]",
        "v_btn_code": "Исходник",
        "v_dl_ok": "Модуль успешно установлен!",
        "v_dl_err": "Ошибка установки!",
        "v_lim_cfg": "Лимиты вывода поиска.",
        "v_btn_sec": "🛡 Проверка кода",
        "v_max_batch_cfg": "Макс модулей за одну установку.",
        "v_auto_upd_cfg": "Уведомлять об обновлениях модулей (по хэшам).",
        "v_aud_hdr": "Аудит кода: {name}",
        "v_aud_req": "Соединение с Security API...",
        "v_aud_proc": "Анализ AST дерева...",
        "v_btn_aud_run": "Запустить скан",
        "v_aud_mem": "Загружено из кэша сессии.",
        "v_aud_lvl": "Уровень угрозы",
        "v_aud_stat": "Данные сканера",
        "v_aud_out": "Итог",
        "v_aud_sigs": "Триггеры",
        "v_sig_crit": "Критично",
        "v_sig_warn": "Внимание",
        "v_sig_info": "Уведомления",
        "v_aud_none": "Еще не проверен. Расходует 1 слот API.",
        "v_aud_no_txt": "Описание не сгенерировано.",
        "v_aud_left": "Остаток слотов: {remaining}/{limit}",
        "v_aud_zero": "Суточный лимит проверок исчерпан.",
        "v_aud_err": "Сервер сканирования недоступен.",
        "v_err_gui": "Сбой рендеринга интерфейса.",
        "v_btn_exp": "🔽 Развернуть",
        "v_btn_col": "🔼 Свернуть",
        "v_btn_talk": "💬 Обсуждение",
        "v_talk_hdr": "{emoji} <b>Тред: {name}</b>",
        "v_talk_desc": "Отзывы комьюнити",
        "v_talk_num": "Постов: {count}",
        "v_talk_0": "Тред пуст. Будьте первым!",
        "v_talk_err": "Нет связи с тредом.",
        "v_rep_ok": "Опубликовано!",
        "v_rep_err": "Сбой запроса.",
        "v_btn_bck": "⬅️ Назад",
        "v_btn_wrt": "✍️ Написать",
        "v_rep_ask": "Отправьте текст ответом.\nОт 2 до 1800 символов.",
        "v_rep_snt": "Выгрузка...",
        "v_rep_min": "Текст слишком короткий.",
        "v_rep_max": "Превышен лимит длины.",
        "v_rep_cncl": "Отменено.",
        "v_loading_ui": "Ищем по базе Vector...",
        "v_sending": "Загрузка...",
        "v_more_replies": "...и ещё {count} ответов на сайте.",
        "v_more_comments": "...и ещё комментарии на сайте.",
        "v_upd_req": "Обновляем Vector...",
        "v_upd_ok": "Vector успешно обновлен!",
        "v_upd_err": "Ошибка обновления!",
        "v_upd_check": "Проверка хэшей…",
        "v_install_log_hdr": "Журнал установки: {name}",
        "v_install_fail_forbidden": "Запрещённый метод: <code>{detail}</code>",
        "v_install_fail_requirements": "Pip-зависимости не встали: <code>{detail}</code>",
        "v_install_fail_dependency": "Не хватает зависимости: <code>{detail}</code>",
        "v_install_fail_packages": "Системные пакеты не встали: <code>{detail}</code>",
        "v_install_fail_core_overwrite": "Пытается перезаписать ядро <code>{detail}</code>",
        "v_install_fail_ffmpeg": "Требуется ffmpeg (не установлен)",
        "v_install_fail_inline": "Требуется inline-режим (недоступен)",
        "v_install_fail_heroku_min": "Нужен Heroku ≥ <code>{detail}</code>",
        "v_install_fail_not_found": "Не найден в подключённых репозиториях",
        "v_install_fail_download": "Не удалось скачать модуль",
        "v_install_fail_unknown": "Неизвестная ошибка: <code>{detail}</code>",
        "v_upd_same": "🌟 <b>У тебя последняя версия. Обновиться принудительно?</b>",
        "v_upd_force_btn": "🧭 Обновиться",
        "v_dlcoll_hdr": "<b>Коллекция {name}</b>",
        "v_dlcoll_count": "Модулей: {count}",
        "v_dlcoll_start": "<b>Устанавливаю все модули из коллекции...</b>",
        "v_dlcoll_done": "<b>Все модули из коллекции установлены</b>",
        "v_dlcoll_done_partial": "<b>Часть модулей не установилась</b>",
        "v_dlcoll_done_none": "<b>Ни один модуль не установлен</b>",
        "v_dlcoll_fail_item": "❌ {name}: {reason}",
        "v_dlcoll_empty": "<b>Коллекция пуста</b>",
        "v_dlcoll_not_found": "<b>Коллекция не найдена</b>",
"v_vecdl_usage": "<b>Укажи коллекцию: </b><code>{p}vecdl <slug или ссылка></code>",
        "v_dlcoll_max_batch": "В коллекции {total} модулей, макс {max} за раз. Ставлю первые {max}…",
        "v_upd_cancel": "🚫 Отмена",
        "v_miniapp_title": "Открыть в Mini App",
        "v_miniapp_body": "Открой Vector как Mini App в Telegram — мгновенный автовход, без паролей, сессия зашифрована. Один тап и ты внутри.",
        "v_miniapp_btn": "🚀 Открыть Vector",
    }

    strings_jp = {
        "lang": "jp",
        "_cls_doc": "Heroku用モジュール検索。\nhttps://www.0xvector.lol",
        "v_dev_lbl": "作成者:",
        "v_dev_str": "開発:",
        "v_dev_ofc": "公式",
        "v_dev_unofc": "非公式",
        "v_info": "情報:",
        "v_tags": "タグ:",
        "v_cmds": "使い方:",
        "v_deps": "依存関係:",
        "v_reqs": "ライブラリ:",
        "v_hid_cmd": "+ 非表示コマンド: {rem}。",
        "v_hid_req": "+ 非表示ライブラリ: {rem}。",
        "v_res_hdr": "見つかったモジュール:",
        "v_err_empty": "クエリを指定してください: {p}vector <テキスト>",
        "v_err_404": "次のクエリの記録はありません: {q}",
        "v_err_len": "クエリの長さは120文字に制限されています。",
        "v_err_api": "Vectorサーバーによりアクセスが拒否されました。",
        "v_ban_notice": "⛔ <b>Vectorへのアクセスはブロックされています。</b>\n<b>理由:</b> <code>{reason}</code>\n<b>期間:</b> <code>{term}</code>",
        "v_fb_add": "評価が追加されました！",
        "v_fb_rm": "評価がクリアされました！",
        "v_btn_copy": "クエリ",
        "v_btn_dl": "インストール",
        "v_page": "[{idx}/{total}]",
        "v_btn_code": "ソース",
        "v_dl_ok": "モジュールが正常にインストールされました！",
        "v_dl_err": "インストールに失敗しました！",
        "v_lim_cfg": "検索出力制限。",
        "v_btn_sec": "🛡 セキュリティスキャン",
        "v_max_batch_cfg": "一括インストールの最大モジュール数。",
        "v_auto_upd_cfg": "モジュールの更新をハッシュで通知。",
        "v_aud_hdr": "コード監査: {name}",
        "v_aud_req": "セキュリティAPIに接続中...",
        "v_aud_proc": "ASTツリーを処理中...",
        "v_btn_aud_run": "スキャン開始",
        "v_aud_mem": "セッションキャッシュからロードされました。",
        "v_aud_lvl": "脅威レベル",
        "v_aud_stat": "スキャナデータ",
        "v_aud_out": "概要",
        "v_aud_sigs": "トリガー",
        "v_sig_crit": "クリティカル",
        "v_sig_warn": "警告",
        "v_sig_info": "通知",
        "v_aud_none": "まだスキャンされていません。1つのAPIスロットを消費します。",
        "v_aud_no_txt": "概要は生成されていません。",
        "v_aud_left": "残りスロット: {remaining}/{limit}",
        "v_aud_zero": "1日の監査制限に達しました。",
        "v_aud_err": "スキャナサーバーがダウンしています。",
        "v_err_gui": "インターフェースのレンダリングエラー。",
        "v_btn_exp": "🔽 展開",
        "v_btn_col": "🔼 折りたたむ",
        "v_btn_talk": "💬 ディスカッション",
        "v_talk_hdr": "{emoji} <b>スレッド: {name}</b>",
        "v_talk_desc": "コミュニティレビュー",
        "v_talk_num": "投稿数: {count}",
        "v_talk_0": "スレッドは空です。最初の投稿をしましょう！",
        "v_talk_err": "スレッドに接続できませんでした。",
        "v_rep_ok": "投稿されました！",
        "v_rep_err": "リクエストに失敗しました。",
        "v_btn_bck": "⬅️ 戻る",
        "v_btn_wrt": "✍️ 返信を書く",
        "v_rep_ask": "メッセージに返信してください。\n2〜1800文字。",
        "v_rep_snt": "アップロード中...",
        "v_rep_min": "テキストが短すぎます。",
        "v_rep_max": "制限を超過しました。",
        "v_rep_cncl": "キャンセルされました。",
        "v_loading_ui": "Vectorデータベースを検索中...",
        "v_sending": "読み込み中...",
        "v_more_replies": "...サイトにはさらに{count}件の返信があります。",
        "v_more_comments": "...サイトにはさらにコメントがあります。",
        "v_upd_req": "Vectorを更新中...",
        "v_upd_ok": "Vectorが正常に更新されました！",
        "v_upd_err": "更新に失敗しました！",
        "v_upd_check": "ハッシュをチェック中…",
        "v_install_log_hdr": "インストールログ: {name}",
        "v_install_fail_forbidden": "禁止されたメソッド: <code>{detail}</code>",
        "v_install_fail_requirements": "Pip依存関係の失敗: <code>{detail}</code>",
        "v_install_fail_dependency": "不足している依存関係: <code>{detail}</code>",
        "v_install_fail_packages": "システムパッケージの失敗: <code>{detail}</code>",
        "v_install_fail_core_overwrite": "コアを上書きしようとしました <code>{detail}</code>",
        "v_install_fail_ffmpeg": "ffmpegが必要です（未インストール）",
        "v_install_fail_inline": "インラインモードが必要です（利用不可）",
        "v_install_fail_heroku_min": "Heroku ≥ <code>{detail}</code>が必要です",
        "v_install_fail_not_found": "設定されたリポジトリに見つかりません",
        "v_install_fail_download": "モジュールのダウンロードに失敗",
        "v_install_fail_unknown": "不明なエラー: <code>{detail}</code>",
        "v_upd_same": "🌟 <b>最新バージョンですが、とにかくアップデートしますか？</b>",
        "v_upd_force_btn": "🧭 アップデート",
        "v_dlcoll_hdr": "<b>コレクション {name}</b>",
        "v_dlcoll_count": "{count}モジュール",
        "v_dlcoll_start": "<b>コレクションからすべてのモジュールをインストール中...</b>",
        "v_dlcoll_done": "<b>コレクションからすべてのモジュールをインストールしました</b>",
        "v_dlcoll_done_partial": "<b>一部のモジュールのインストールに失敗しました</b>",
        "v_dlcoll_done_none": "<b>モジュールがインストールされませんでした</b>",
        "v_dlcoll_fail_item": "❌ {name}: {reason}",
        "v_dlcoll_empty": "<b>コレクションは空です</b>",
        "v_dlcoll_not_found": "<b>コレクションが見つかりません</b>",
"v_vecdl_usage": "<b>コレクションを指定: </b><code>{p}vecdl <slugかURL></code>",
        "v_dlcoll_max_batch": "コレクションに{total}モジュール、最大{max}まで。最初の{max}をインストール中…",
        "v_upd_cancel": "🚫 キャンセル",
        "v_miniapp_title": "Mini Appで開く",
        "v_miniapp_body": "Telegram Mini AppとしてVectorを開く — 自動ログイン、パスワード不要、完全暗号化セッション。ワンタップで入れます。",
        "v_miniapp_btn": "🚀 Vectorを開く",
    }

    strings_ua = {
        "lang": "ua",
        "_cls_doc": "Пошук модулів для Heroku.\nhttps://www.0xvector.lol",
        "v_dev_lbl": "Автор:",
        "v_dev_str": "Розроб:",
        "v_dev_ofc": "офіц",
        "v_dev_unofc": "неофіц",
        "v_info": "Інфо:",
        "v_tags": "Теги:",
        "v_cmds": "Використання:",
        "v_deps": "Залежності:",
        "v_reqs": "Бібліотеки:",
        "v_hid_cmd": "+ приховано команд: {rem}.",
        "v_hid_req": "+ приховано ліб: {rem}.",
        "v_res_hdr": "Знайдені модулі:",
        "v_err_empty": "Вкажіть запит: {p}vector <текст>",
        "v_err_404": "Немає записів за запитом: {q}",
        "v_err_len": "Довжина запиту обмежена 120 символами.",
        "v_err_api": "Відмова в доступі від сервера Vector.",
        "v_ban_notice": "⛔ <b>Доступ до Vector заблоковано.</b>\n<b>Причина:</b> <code>{reason}</code>\n<b>Термін:</b> <code>{term}</code>",
        "v_fb_add": "Оцінка додана!",
        "v_fb_rm": "Оцінка видалена!",
        "v_btn_copy": "Запит",
        "v_btn_dl": "Встановити",
        "v_page": "[{idx}/{total}]",
        "v_btn_code": "Вихідний код",
        "v_dl_ok": "Модуль успішно встановлено!",
        "v_dl_err": "Помилка встановлення!",
        "v_lim_cfg": "Ліміти виводу пошуку.",
        "v_btn_sec": "🛡 Перевірка коду",
        "v_max_batch_cfg": "Макс модулів за одну установку.",
        "v_auto_upd_cfg": "Повідомляти про оновлення модулів (за хешами).",
        "v_aud_hdr": "Аудит коду: {name}",
        "v_aud_req": "З'єднання з Security API...",
        "v_aud_proc": "Аналіз AST дерева...",
        "v_btn_aud_run": "Запустити скан",
        "v_aud_mem": "Завантажено з кешу сесії.",
        "v_aud_lvl": "Рівень загрози",
        "v_aud_stat": "Дані сканера",
        "v_aud_out": "Підсумок",
        "v_aud_sigs": "Тригери",
        "v_sig_crit": "Критично",
        "v_sig_warn": "Увага",
        "v_sig_info": "Сповіщення",
        "v_aud_none": "Ще не перевірено. Витрачає 1 слот API.",
        "v_aud_no_txt": "Опис не згенеровано.",
        "v_aud_left": "Залишок слотів: {remaining}/{limit}",
        "v_aud_zero": "Добовий ліміт перевірок вичерпано.",
        "v_aud_err": "Сервер сканування недоступний.",
        "v_err_gui": "Збій рендерингу інтерфейсу.",
        "v_btn_exp": "🔽 Розгорнути",
        "v_btn_col": "🔼 Згорнути",
        "v_btn_talk": "💬 Обговорення",
        "v_talk_hdr": "{emoji} <b>Тред: {name}</b>",
        "v_talk_desc": "Відгуки спільноти",
        "v_talk_num": "Постів: {count}",
        "v_talk_0": "Тред порожній. Будьте першим!",
        "v_talk_err": "Немає зв'язку з тредом.",
        "v_rep_ok": "Опубліковано!",
        "v_rep_err": "Збій запиту.",
        "v_btn_bck": "⬅️ Назад",
        "v_btn_wrt": "✍️ Написати",
        "v_rep_ask": "Відправте текст відповіддю.\nВід 2 до 1800 символов.",
        "v_rep_snt": "Вивантаження...",
        "v_rep_min": "Текст занадто короткий.",
        "v_rep_max": "Перевищено ліміт довжини.",
        "v_rep_cncl": "Скасовано.",
        "v_loading_ui": "Шукаємо по базі Vector...",
        "v_sending": "Завантаження...",
        "v_more_replies": "...і ще {count} відповідей на сайті.",
        "v_more_comments": "...і ще коментарі на сайті.",
        "v_upd_req": "Оновлюємо Vector...",
        "v_upd_ok": "Vector успішно оновлено!",
        "v_upd_err": "Помилка оновлення!",
        "v_upd_check": "Перевірка хешів…",
        "v_install_log_hdr": "Журнал встановлення: {name}",
        "v_install_fail_forbidden": "Заборонений метод: <code>{detail}</code>",
        "v_install_fail_requirements": "Pip-залежності не стали: <code>{detail}</code>",
        "v_install_fail_dependency": "Бракує залежності: <code>{detail}</code>",
        "v_install_fail_packages": "Системні пакунки не стали: <code>{detail}</code>",
        "v_install_fail_core_overwrite": "Намагається перезаписати ядро <code>{detail}</code>",
        "v_install_fail_ffmpeg": "Потрібен ffmpeg (не встановлено)",
        "v_install_fail_inline": "Потрібен inline-режим (недоступний)",
        "v_install_fail_heroku_min": "Потрібен Heroku ≥ <code>{detail}</code>",
        "v_install_fail_not_found": "Не знайдено в підключених репозиторіях",
        "v_install_fail_download": "Не вдалося завантажити модуль",
        "v_install_fail_unknown": "Невідома помилка: <code>{detail}</code>",
        "v_upd_same": "🌟 <b>У тебе остання версія. Оновитися примусово?</b>",
        "v_upd_force_btn": "🧭 Оновитися",
        "v_dlcoll_hdr": "<b>Колекція {name}</b>",
        "v_dlcoll_count": "Модулів: {count}",
        "v_dlcoll_start": "<b>Встановлюю всі модулі з колекції...</b>",
        "v_dlcoll_done": "<b>Всі модулі з колекції встановлено</b>",
        "v_dlcoll_done_partial": "<b>Деякі модулі не вдалося встановити</b>",
        "v_dlcoll_done_none": "<b>Жоден модуль не встановлено</b>",
        "v_dlcoll_fail_item": "❌ {name}: {reason}",
        "v_dlcoll_empty": "<b>Колекція порожня</b>",
        "v_dlcoll_not_found": "<b>Колекцію не знайдено</b>",
"v_vecdl_usage": "<b>Вкажи колекцію: </b><code>{p}vecdl <slug або посилання></code>",
        "v_dlcoll_max_batch": "У колекції {total} модулів, макс {max} за раз. Ставлю перші {max}…",
        "v_upd_cancel": "🚫 Скасувати",
        "v_miniapp_title": "Відкрити в Mini App",
        "v_miniapp_body": "Відкрий Vector як Mini App у Telegram — миттєвий автовхід, без паролів, сесія зашифрована. Один тап і ти всередині.",
        "v_miniapp_btn": "🚀 Відкрити Vector",
    }

    strings_de = {
        "lang": "de",
        "_cls_doc": "Modulsuche für Heroku.\nhttps://www.0xvector.lol",
        "v_dev_lbl": "Autor:",
        "v_dev_str": "Entwickler:",
        "v_dev_ofc": "offiziell",
        "v_dev_unofc": "inoffiziell",
        "v_info": "Info:",
        "v_tags": "Tags:",
        "v_cmds": "Verwendung:",
        "v_deps": "Abhängigkeiten:",
        "v_reqs": "Bibliotheken:",
        "v_hid_cmd": "+ {rem} versteckte Befehle.",
        "v_hid_req": "+ {rem} versteckte Bibliotheken.",
        "v_res_hdr": "Gefundene Elemente:",
        "v_err_empty": "Suchbegriff eingeben: {p}vector <text>",
        "v_err_404": "Keine Einträge für: {q}",
        "v_err_len": "Abfragelänge ist auf 120 Zeichen begrenzt.",
        "v_err_api": "Zugriff durch Vector-Server verweigert.",
        "v_ban_notice": "⛔ <b>Zugriff auf Vector gesperrt.</b>\n<b>Grund:</b> <code>{reason}</code>\n<b>Dauer:</b> <code>{term}</code>",
        "v_fb_add": "Erfolgreich bewertet!",
        "v_fb_rm": "Bewertung gelöscht!",
        "v_btn_copy": "Abfrage",
        "v_btn_dl": "Installieren",
        "v_page": "[{idx}/{total}]",
        "v_btn_code": "Quellcode",
        "v_dl_ok": "Modul erfolgreich installiert!",
        "v_dl_err": "Installation fehlgeschlagen!",
        "v_lim_cfg": "Suchausgabe-Limits.",
        "v_btn_sec": "🛡 Sicherheits-Scan",
        "v_max_batch_cfg": "Max Module pro Batch-Installation.",
        "v_auto_upd_cfg": "Benachrichtige bei Modul-Updates (Hash-basiert).",
        "v_aud_hdr": "Code-Audit: {name}",
        "v_aud_req": "Verbindung zur Security-API...",
        "v_aud_proc": "Verarbeite AST-Baum...",
        "v_btn_aud_run": "Scan starten",
        "v_aud_mem": "Aus dem Session-Cache geladen.",
        "v_aud_lvl": "Bedrohungsstufe",
        "v_aud_stat": "Scanner-Daten",
        "v_aud_out": "Zusammenfassung",
        "v_aud_sigs": "Auslöser",
        "v_sig_crit": "Kritisch",
        "v_sig_warn": "Warnungen",
        "v_sig_info": "Hinweise",
        "v_aud_none": "Noch nicht gescannt. Verbraucht 1 API-Slot.",
        "v_aud_no_txt": "Keine Zusammenfassung generiert.",
        "v_aud_left": "Verbleibende Slots: {remaining}/{limit}",
        "v_aud_zero": "Tägliches Audit-Limit aufgebraucht.",
        "v_aud_err": "Scanner-Server ist offline.",
        "v_err_gui": "Fehler beim Rendern der Benutzeroberfläche.",
        "v_btn_exp": "🔽 Erweitern",
        "v_btn_col": "🔼 Zuklappen",
        "v_btn_talk": "💬 Diskussion",
        "v_talk_hdr": "{emoji} <b>Thread: {name}</b>",
        "v_talk_desc": "Community-Bewertungen",
        "v_talk_num": "Beiträge: {count}",
        "v_talk_0": "Der Thread ist leer. Sei der Erste!",
        "v_talk_err": "Keine Verbindung zum Thread.",
        "v_rep_ok": "Gepostet!",
        "v_rep_err": "Anfrage fehlgeschlagen.",
        "v_btn_bck": "⬅️ Zurück",
        "v_btn_wrt": "✍️ Antworten",
        "v_rep_ask": "Auf Beitrag antworten.\n2-1800 Zeichen.",
        "v_rep_snt": "Wird hochgeladen...",
        "v_rep_min": "Text ist zu kurz.",
        "v_rep_max": "Limit überschritten.",
        "v_rep_cncl": "Abgebrochen.",
        "v_loading_ui": "Durchsuche Vector-Datenbank...",
        "v_sending": "Laden...",
        "v_more_replies": "...und {count} weitere Antworten auf der Seite.",
        "v_more_comments": "...und weitere Kommentare auf der Seite.",
        "v_upd_req": "Vector wird aktualisiert...",
        "v_upd_ok": "Vector erfolgreich aktualisiert!",
        "v_upd_err": "Aktualisierung fehlgeschlagen!",
        "v_upd_check": "Überprüfe Hashes…",
        "v_install_log_hdr": "Installationsprotokoll: {name}",
        "v_install_fail_forbidden": "Verbotene Methode: <code>{detail}</code>",
        "v_install_fail_requirements": "Pip-Abhängigkeiten fehlgeschlagen: <code>{detail}</code>",
        "v_install_fail_dependency": "Fehlende Abhängigkeit: <code>{detail}</code>",
        "v_install_fail_packages": "Systempakete fehlgeschlagen: <code>{detail}</code>",
        "v_install_fail_core_overwrite": "Versucht Kern <code>{detail}</code> zu überschreiben",
        "v_install_fail_ffmpeg": "Benötigt ffmpeg (nicht installiert)",
        "v_install_fail_inline": "Benötigt Inline-Modus (nicht verfügbar)",
        "v_install_fail_heroku_min": "Benötigt Heroku ≥ <code>{detail}</code>",
        "v_install_fail_not_found": "Nicht in konfigurierten Repos gefunden",
        "v_install_fail_download": "Modul-Download fehlgeschlagen",
        "v_install_fail_unknown": "Unbekannter Fehler: <code>{detail}</code>",
        "v_upd_same": "🌟 <b>Du hast bereits die neueste Version. Trotzdem aktualisieren?</b>",
        "v_upd_force_btn": "🧭 Aktualisieren",
        "v_dlcoll_hdr": "<b>Sammlung {name}</b>",
        "v_dlcoll_count": "{count} Module",
        "v_dlcoll_start": "<b>Alle Module aus der Sammlung werden installiert...</b>",
        "v_dlcoll_done": "<b>Alle Module aus der Sammlung installiert</b>",
        "v_dlcoll_done_partial": "<b>Einige Module konnten nicht installiert werden</b>",
        "v_dlcoll_done_none": "<b>Keine Module installiert</b>",
        "v_dlcoll_fail_item": "❌ {name}: {reason}",
        "v_dlcoll_empty": "<b>Sammlung ist leer</b>",
        "v_dlcoll_not_found": "<b>Sammlung nicht gefunden</b>",
"v_vecdl_usage": "<b>Sammlung angeben: </b><code>{p}vecdl <slug oder URL></code>",
        "v_dlcoll_max_batch": "Sammlung hat {total} Module, max {max} pro Durchlauf. Installiere erste {max}…",
        "v_upd_cancel": "🚫 Abbrechen",
        "v_miniapp_title": "In Mini App öffnen",
        "v_miniapp_body": "Öffne Vector als Telegram Mini App — sofortiger Auto-Login, keine Passwörter, verschlüsselte Sitzung. Ein Tipp und du bist drin.",
        "v_miniapp_btn": "🚀 Vector öffnen",
    }

    strings_neofit = {
        "lang": "neofit",
        "_cls_doc": "Search modules for Heroku.\nhttps://www.0xvector.lol",
        "v_dev_lbl": "by",
        "v_dev_str": "dev",
        "v_dev_ofc": "verified",
        "v_dev_unofc": "3rd-party",
        "v_info": "info",
        "v_tags": "tags",
        "v_cmds": "usage",
        "v_deps": "deps:",
        "v_reqs": "deps",
        "v_hid_cmd": "+ {rem} hidden cmds.",
        "v_hid_req": "+ {rem} hidden deps.",
        "v_res_hdr": "stdout:",
        "v_err_empty": "<b>SyntaxError:</b> missing query. <code>{p}vector &lt;text&gt;</code>",
        "v_err_404": "<b>grep:</b> <code>{q}</code> not found.",
        "v_err_len": "<b>Buffer overflow:</b> max 120 chars.",
        "v_err_api": "<b>403 Forbidden</b> by Vector API.",
        "v_ban_notice": "⛔ <b>Vector blocked access.</b>\n<b>rule:</b> <code>{reason}</code>\n<b>TTL:</b> <code>{term}</code>",
        "v_fb_add": "Rated.",
        "v_fb_rm": "Rating cleared.",
        "v_btn_copy": "query",
        "v_btn_dl": "install",
        "v_page": "[{idx}/{total}]",
        "v_btn_code": "src",
        "v_dl_ok": "Installed.",
        "v_dl_err": "Install failed.",
        "v_lim_cfg": "Search output limits.",
        "v_btn_sec": "🛡 Security scan",
        "v_max_batch_cfg": "max mods per batch install.",
        "v_auto_upd_cfg": "hash-based mod update notifs on/off.",
        "v_aud_hdr": "Code audit: {name}",
        "v_aud_req": "Connecting to security API...",
        "v_aud_proc": "Parsing AST...",
        "v_btn_aud_run": "Run scan",
        "v_aud_mem": "Loaded from cache.",
        "v_aud_lvl": "Threat level",
        "v_aud_stat": "Scanner data",
        "v_aud_out": "Summary",
        "v_aud_sigs": "Signals",
        "v_sig_crit": "SIGKILL",
        "v_sig_warn": "SIGTERM",
        "v_sig_info": "SIGUSR1",
        "v_aud_none": "Not scanned yet. Uses 1 API slot.",
        "v_aud_no_txt": "No summary generated.",
        "v_aud_left": "Slots: {remaining}/{limit}",
        "v_aud_zero": "Daily limit exhausted.",
        "v_aud_err": "Scanner server is down.",
        "v_err_gui": "GUI render error.",
        "v_btn_exp": "🔽 Expand",
        "v_btn_col": "🔼 Collapse",
        "v_btn_talk": "💬 Discussion",
        "v_talk_hdr": "{emoji} <b>Thread: {name}</b>",
        "v_talk_desc": "Community reviews",
        "v_talk_num": "Posts: {count}",
        "v_talk_0": "Thread is empty. Be the first!",
        "v_talk_err": "Connection refused.",
        "v_rep_ok": "Posted.",
        "v_rep_err": "Request failed.",
        "v_btn_bck": "⬅️ Back",
        "v_btn_wrt": "✍️ Reply",
        "v_rep_ask": "Reply to post.\n2–1800 chars.",
        "v_rep_snt": "Uploading...",
        "v_rep_min": "Too short.",
        "v_rep_max": "Limit exceeded.",
        "v_rep_cncl": "Cancelled.",
        "v_loading_ui": "Searching Vector database...",
        "v_sending": "Loading...",
        "v_more_replies": "...and {count} more replies.",
        "v_more_comments": "...and more comments.",
        "v_upd_req": "Updating Vector...",
        "v_upd_ok": "Updated.",
        "v_upd_err": "Update failed.",
        "v_upd_check": "Checkin' hashes…",
        "v_install_log_hdr": "install log: {name}",
        "v_install_fail_forbidden": "forbidden method: <code>{detail}</code>",
        "v_install_fail_requirements": "pip deps failed: <code>{detail}</code>",
        "v_install_fail_dependency": "missing dep: <code>{detail}</code>",
        "v_install_fail_packages": "system pkgs failed: <code>{detail}</code>",
        "v_install_fail_core_overwrite": "core overwrite attempt: <code>{detail}</code>",
        "v_install_fail_ffmpeg": "needs ffmpeg (not found)",
        "v_install_fail_inline": "needs inline mode (dead)",
        "v_install_fail_heroku_min": "needs Heroku ≥ <code>{detail}</code>",
        "v_install_fail_not_found": "not in configured repos",
        "v_install_fail_download": "download failed",
        "v_install_fail_unknown": "unknown error: <code>{detail}</code>",
        "v_upd_same": "🌟 <b>Up to date. git pull --force?</b>",
        "v_upd_force_btn": "🧭 git pull",
        "v_dlcoll_hdr": "<b>Collection {name}</b>",
        "v_dlcoll_count": "{count} mods",
        "v_dlcoll_start": "<b>git cloning collection and installing all mods via git pull && makepkg -si...</b>",
        "v_dlcoll_done": "<b>All mods from collection installed (no errors, chad moment)</b>",
        "v_dlcoll_done_partial": "<b>Some mods failed to install (skill issue)</b>",
        "v_dlcoll_done_none": "<b>No mods installed (RTFM or gtfo, normie)</b>",
        "v_dlcoll_fail_item": "❌ {name}: {reason}",
        "v_dlcoll_empty": "<b>Empty collection, cope harder</b>",
        "v_dlcoll_not_found": "<b>404 collection not found, seethe</b>",
"v_vecdl_usage": "<b>specify collection: </b><code>{p}vecdl <slug></code>",
        "v_dlcoll_max_batch": "{total} mods, max {max}. pulling first {max}…",
        "v_upd_cancel": "🚫 abort",
        "v_miniapp_title": "$ open --mode=webapp",
        "v_miniapp_body": "> webapp_open(): tg_session=auto\n> crypto=e2ee\n> tap link below",
        "v_miniapp_btn": "🚀 Launch",
    }
    strings_tiktok = {
        "lang": "tiktok",
        "_cls_doc": "Темка для поиска модулей для Heroku.\nhttps://www.0xvector.lol",
        "v_dev_lbl": "Кодер:",
        "v_dev_str": "дев:",
        "v_dev_ofc": "офиц",
        "v_dev_unofc": "ноунэйм",
        "v_info": "Инфа:",
        "v_tags": "Теги:",
        "v_cmds": "Команды:",
        "v_deps": "Deps:",
        "v_reqs": "Либы:",
        "v_hid_cmd": "+ заныкано: {rem}",
        "v_hid_req": "+ заныкано либ: {rem}",
        "v_res_hdr": "Нашлось:",
        "v_err_empty": "Чё искать-то? Пиши: {p}vector <текст>",
        "v_err_404": "Пусто по запросу: {q}",
        "v_err_len": "Длинновато, до 120 симв.",
        "v_err_api": "Сервер Vector не пускает.",
        "v_ban_notice": "⛔ <b>Вектор тебя забанил.</b>\n<b>Причина:</b> <code>{reason}</code>\n<b>Срок:</b> <code>{term}</code>",
        "v_fb_add": "Лайк влеплен!",
        "v_fb_rm": "Лайк снят!",
        "v_btn_copy": "Запрос",
        "v_btn_dl": "Поставить",
        "v_page": "[{idx}/{total}]",
        "v_btn_code": "Код",
        "v_dl_ok": "Поставилось!",
        "v_dl_err": "Не встало!",
        "v_lim_cfg": "Лимиты выдачи.",
        "v_btn_sec": "🛡 Чек кода",
        "v_max_batch_cfg": "Макс темок за раз.",
        "v_auto_upd_cfg": "Слать уведомления при новых хэшах модулей.",
        "v_aud_hdr": "Прожарка: {name}",
        "v_aud_req": "Стучимся в API защиты...",
        "v_aud_proc": "Парсим AST...",
        "v_btn_aud_run": "Скан",
        "v_aud_mem": "Из кэша.",
        "v_aud_lvl": "Кринжометр",
        "v_aud_stat": "Дата",
        "v_aud_out": "Итог",
        "v_aud_sigs": "Редфлаги",
        "v_sig_crit": "Жёстко",
        "v_sig_warn": "Аккуратно",
        "v_sig_info": "Инфа",
        "v_aud_none": "Ещё не чекали. Жрёт 1 слот.",
        "v_aud_no_txt": "Пусто.",
        "v_aud_left": "Слотов: {remaining}/{limit}",
        "v_aud_zero": "Лимит на сегодня всё.",
        "v_aud_err": "Чекер лёг.",
        "v_err_gui": "Интерфейс крашнулся.",
        "v_btn_exp": "🔽 Открыть",
        "v_btn_col": "🔼 Закрыть",
        "v_btn_talk": "💬 Курилка",
        "v_talk_hdr": "{emoji} <b>Курилка: {name}</b>",
        "v_talk_desc": "Чё пишут люди",
        "v_talk_num": "Постов: {count}",
        "v_talk_0": "Пусто. Будь первым!",
        "v_talk_err": "Связи нет.",
        "v_rep_ok": "Улетело!",
        "v_rep_err": "Фейл.",
        "v_btn_bck": "⬅️ Назад",
        "v_btn_wrt": "✍️ Ответ",
        "v_rep_ask": "Реплай на сообщение.\nОт 2 до 1800 симв.",
        "v_rep_snt": "Пушим...",
        "v_rep_min": "Мало букав.",
        "v_rep_max": "Дохрена букав.",
        "v_rep_cncl": "Забили.",
        "v_loading_ui": "Ищем по базе Vector...",
        "v_sending": "Грузим...",
        "v_more_replies": "...и ещё {count} комментов.",
        "v_more_comments": "...и ещё спам на сайте.",
        "v_upd_req": "Качаем обнову...",
        "v_upd_ok": "Обнова залетела!",
        "v_upd_err": "Не обновилось!",
        "v_upd_check": "Чекаю хэши…",
        "v_install_log_hdr": "Лог установки: {name}",
        "v_install_fail_forbidden": "Запрещёнка: <code>{detail}</code>",
        "v_install_fail_requirements": "Пип-либы не встали: <code>{detail}</code>",
        "v_install_fail_dependency": "Не хватает: <code>{detail}</code>",
        "v_install_fail_packages": "Системные пакеты мимо: <code>{detail}</code>",
        "v_install_fail_core_overwrite": "Лезет в ядро <code>{detail}</code>",
        "v_install_fail_ffmpeg": "Нужен ffmpeg (нету)",
        "v_install_fail_inline": "Нужен inline (не раб)",
        "v_install_fail_heroku_min": "Нужен Heroku ≥ <code>{detail}</code>",
        "v_install_fail_not_found": "Нет в подключённых репах",
        "v_install_fail_download": "Не скачалось",
        "v_install_fail_unknown": "Непонятная ошибка: <code>{detail}</code>",
        "v_upd_same": "🌟 <b>У тебя ласт версия. Все равно обновить?</b>",
        "v_upd_force_btn": "🧭 Обнова",
        "v_dlcoll_hdr": "<b>Подборка {name}</b>",
        "v_dlcoll_count": "Темок: {count}",
        "v_dlcoll_start": "<b>Качаем все темки из подборки... сигма, подожди секунду, щавель уже в деле</b>",
        "v_dlcoll_done": "<b>Все темки из подборки установлены! Сигма момент</b>",
        "v_dlcoll_done_partial": "<b>Плаки, плаки. Некоторые темки не установились, кароче фейл</b>",
        "v_dlcoll_done_none": "<b>Ни одна темка не встала. Кринж</b>",
        "v_dlcoll_fail_item": "❌ {name}: {reason}",
        "v_dlcoll_empty": "<b>Подборка пустая, клоун</b>",
        "v_dlcoll_not_found": "<b>Нет такой подборки, ризз или ливни</b>",
"v_vecdl_usage": "<b>Скажи подборку: </b><code>{p}vecdl <slug или ссылка></code>",
        "v_dlcoll_max_batch": "Темок {total}, макс {max}. Ставлю первые {max}…",
        "v_upd_cancel": "🚫 Отбой",
        "v_miniapp_title": "Залетай в Mini App",
        "v_miniapp_body": "Залетай в Vector как мини апп в телеге — автовход по тг-акку, без паролей, шифрование. Один тап и ты внутри.",
        "v_miniapp_btn": "🚀 Го в Vector",
    }

    strings_leet = {
        "lang": "leet",
        "_cls_doc": "S34rch m0dul3s f0r H3r0ku.\nhttps://www.0xvector.lol",
        "v_dev_lbl": "4u7h0r:",
        "v_dev_str": "d3v:",
        "v_dev_ofc": "0ff1c14l",
        "v_dev_unofc": "un0ff1c14l",
        "v_info": "1nf0:",
        "v_tags": "T4g5:",
        "v_cmds": "U54g3:",
        "v_deps": "d3pz:",
        "v_reqs": "L1b5:",
        "v_hid_cmd": "+ {rem} h1dd3n cmd5.",
        "v_hid_req": "+ {rem} h1dd3n l1b5.",
        "v_res_hdr": "F0und:",
        "v_err_empty": "N33d qu3ry: {p}v3c70r <73x7>",
        "v_err_404": "N0 r3c0rd5 f0r: {q}",
        "v_err_len": "Qu3ry 700 l0ng (120 ch4r5 m4x).",
        "v_err_api": "4cc355 d3n13d by V3c70r 53rv3r.",
        "v_ban_notice": "⛔ <b>V3c70r 4cc355 bl0ck3d.</b>\n<b>R3450n:</b> <code>{reason}</code>\n<b>73rm:</b> <code>{term}</code>",
        "v_fb_add": "R473d!",
        "v_fb_rm": "R471ng cl34r3d!",
        "v_btn_copy": "Qu3ry",
        "v_btn_dl": "1n574ll",
        "v_page": "[{idx}/{total}]",
        "v_btn_code": "50urc3",
        "v_dl_ok": "1n574ll3d!",
        "v_dl_err": "F41l3d!",
        "v_lim_cfg": "534rch l1m175.",
        "v_btn_sec": "🛡 53cur17y 5c4n",
        "v_max_batch_cfg": "m4x m0d5 p3r b47ch.",
        "v_auto_upd_cfg": "n071fy 0n m0d h45h ch4n635.",
        "v_aud_hdr": "C0d3 4ud17: {name}",
        "v_aud_req": "C0nn3c71ng 70 53cur17y 4P1...",
        "v_aud_proc": "Pr0c3551ng A57 7r33...",
        "v_btn_aud_run": "574r7 5c4n",
        "v_aud_mem": "L04d3d fr0m c4ch3.",
        "v_aud_lvl": "7hr347 L3v3l",
        "v_aud_stat": "5c4nn3r D474",
        "v_aud_out": "5umm4ry",
        "v_aud_sigs": "7r1gg3r5",
        "v_sig_crit": "Cr171c4l",
        "v_sig_warn": "W4rn1ng5",
        "v_sig_info": "N071c35",
        "v_aud_none": "N07 5c4nn3d y37. C0575 1 4P1 5l07.",
        "v_aud_no_txt": "N0 5umm4ry.",
        "v_aud_left": "5l075 l3f7: {remaining}/{limit}",
        "v_aud_zero": "4ud17 l1m17 d3pl373d.",
        "v_aud_err": "5c4nn3r 53rv3r d0wn.",
        "v_err_gui": "GU1 3rr0r.",
        "v_btn_exp": "🔽 3xp4nd",
        "v_btn_col": "🔼 C0ll4p53",
        "v_btn_talk": "💬 D15cu55",
        "v_talk_hdr": "{emoji} <b>7hr34d: {name}</b>",
        "v_talk_desc": "C0mmun17y r3v13w5",
        "v_talk_num": "P0575: {count}",
        "v_talk_0": "7hr34d 15 3mp7y. B3 f1r57!",
        "v_talk_err": "C4n'7 c0nn3c7.",
        "v_rep_ok": "P0573d!",
        "v_rep_err": "R3qu357 f41l3d.",
        "v_btn_bck": "⬅️ B4ck",
        "v_btn_wrt": "✍️ R3ply",
        "v_rep_ask": "R3ply 70 p057.\n2-1800 ch4r5.",
        "v_rep_snt": "Upl04d1ng...",
        "v_rep_min": "700 5h0r7.",
        "v_rep_max": "L1m17 3xc33d3d.",
        "v_rep_cncl": "C4nc3ll3d.",
        "v_loading_ui": "534rch1ng V3c70r d474b453...",
        "v_sending": "L04d1ng...",
        "v_more_replies": "...4nd {count} m0r3 r3pl135.",
        "v_more_comments": "...4nd m0r3 c0mm3n75.",
        "v_upd_req": "Upd471ng V3c70r...",
        "v_upd_ok": "V3c70r upd473d!",
        "v_upd_err": "Upd473 f41l3d!",
        "v_upd_check": "Ch3ck1ng h45h35…",
        "v_install_log_hdr": "1n574ll l0g: {name}",
        "v_install_fail_forbidden": "f0rb1dd3n m37h0d: <code>{detail}</code>",
        "v_install_fail_requirements": "p1p d3p5 f41l3d: <code>{detail}</code>",
        "v_install_fail_dependency": "m1551n9 d3p: <code>{detail}</code>",
        "v_install_fail_packages": "pkg5 f41l3d: <code>{detail}</code>",
        "v_install_fail_core_overwrite": "c0r3 0v3rwr173: <code>{detail}</code>",
        "v_install_fail_ffmpeg": "n33d5 ffmp39 (n07 f0und)",
        "v_install_fail_inline": "n33d5 1nl1n3 (d34d)",
        "v_install_fail_heroku_min": "n33d5 H3r0ku ≥ <code>{detail}</code>",
        "v_install_fail_not_found": "n07 1n c0nf16'd r3p05",
        "v_install_fail_download": "d0wnl04d f41l3d",
        "v_install_fail_unknown": "unkn0wn 3rr: <code>{detail}</code>",
        "v_upd_same": "🌟 <b>U r 0n 7h3 l47357 v3r510n, pull upd4735 4nyw4y?</b>",
        "v_upd_force_btn": "🧭 Upd473",
        "v_dlcoll_hdr": "<b>C0ll3c710n {name}</b>",
        "v_dlcoll_count": "{count} m0d5",
        "v_dlcoll_start": "<b>1n574ll1n9 4ll m0d5 fr0m c0ll3c710n...</b>",
        "v_dlcoll_done": "<b>4ll m0d5 fr0m c0ll3c710n 1n574ll3d 5ucc355fully!</b>",
        "v_dlcoll_done_partial": "<b>50m3 m0d5 f41l3d 2 1n574ll, b17ch</b>",
        "v_dlcoll_done_none": "<b>N0 m0d5 1n574ll3d, f4gg07</b>",
        "v_dlcoll_fail_item": "❌ {name}: {reason}",
        "v_dlcoll_empty": "<b>3mp7y c0ll3c710n</b>",
        "v_dlcoll_not_found": "<b>C0ll3c710n n07 f0und</b>",
"v_vecdl_usage": "<b>5p3c1fy c0ll3c710n: </b><code>{p}vecdl <5lu9></code>",
        "v_dlcoll_max_batch": "{total} m0d5, m4x {max}. 1n574ll1n9 f1r57 {max}…",
        "v_upd_cancel": "🚫 n0p3",
        "v_miniapp_title": "L4unch M1n1 4pp",
        "v_miniapp_body": "L4unch V3c70r 4s 4 T3l3gr4m M1n1 4pp — 1n574n7 4u70-l091n, n0 p455w0rd5, 3ncryp73d 535510n. 0n3 74p 4nd uR 1n.",
        "v_miniapp_btn": "🚀 0p3n V3c70r",
    }

    strings_uwu = {
        "lang": "uwu",
        "_cls_doc": "Sweawch moduwes fow Hewoku >w<\nhttps://www.0xvector.lol",
        "v_dev_lbl": "Authow:",
        "v_dev_str": "dev:",
        "v_dev_ofc": "officiaw",
        "v_dev_unofc": "unofficiaw",
        "v_info": "Info:",
        "v_tags": "Tagz:",
        "v_cmds": "Usage:",
        "v_deps": "Dependencies~ :3",
        "v_reqs": "Wibs:",
        "v_hid_cmd": "+ {rem} hidden cmds.",
        "v_hid_req": "+ {rem} hidden wibs.",
        "v_res_hdr": "Found owo:",
        "v_err_empty": "hewwo pws specify quewy: {p}vectow <text>",
        "v_err_404": "N-No wecowds fow: {q} T_T",
        "v_err_len": "Quewy too wong (120 chaws) >_<",
        "v_err_api": "Access denied by Vectow Sewvew qwq.",
        "v_ban_notice": "⛔ <b>Vectow bwocked access.</b>\n<b>Weason:</b> <code>{reason}</code>\n<b>Tewm:</b> <code>{term}</code>",
        "v_fb_add": "Wated! (≧◡≦)",
        "v_fb_rm": "Wating cweawed ;w;",
        "v_btn_copy": "Quewy",
        "v_btn_dl": "Instaww",
        "v_page": "[{idx}/{total}]",
        "v_btn_code": "Souwce",
        "v_dl_ok": "Instawwed! (≧◡≦)",
        "v_dl_err": "Instaww faiwed! ;w;",
        "v_lim_cfg": "Seawch wimits.",
        "v_btn_sec": "🛡 Secuwity Scan",
        "v_max_batch_cfg": "Max moduwes pew batch.",
        "v_auto_upd_cfg": "Nya~tify when mod hashies change UwU!",
        "v_aud_hdr": "Code Audit: {name}",
        "v_aud_req": "Connecting to Secuwity API...",
        "v_aud_proc": "Pwocessing AST twee...",
        "v_btn_aud_run": "Stawt Scan",
        "v_aud_mem": "Woaded fwom cache.",
        "v_aud_lvl": "Thweat Wevew",
        "v_aud_stat": "Scannew Data",
        "v_aud_out": "Summawy",
        "v_aud_sigs": "Twiggews",
        "v_sig_crit": "Cwiticaw",
        "v_sig_warn": "Wawnings",
        "v_sig_info": "Notices",
        "v_aud_none": "Not scanned yet. Takes 1 API swot.",
        "v_aud_no_txt": "No summawy gwenerated.",
        "v_aud_left": "Swots weft: {remaining}/{limit}",
        "v_aud_zero": "Daiwy wimit depweted T_T.",
        "v_aud_err": "Scannew sewvew down qwq.",
        "v_err_gui": "GUI ewwow >_<.",
        "v_btn_exp": "🔽 Expand",
        "v_btn_col": "🔼 Cowwapse",
        "v_btn_talk": "💬 Discussion",
        "v_talk_hdr": "{emoji} <b>Thwead: {name}</b>",
        "v_talk_desc": "Community weviews",
        "v_talk_num": "Posts: {count}",
        "v_talk_0": "Thwead is empty. Be fiwst! >w<",
        "v_talk_err": "Couwdn't connect to thwead.",
        "v_rep_ok": "Posted! (≧◡≦)",
        "v_rep_err": "Wequest faiwed T_T.",
        "v_btn_bck": "⬅️ Back",
        "v_btn_wrt": "✍️ Wepwy",
        "v_rep_ask": "Wepwy to post.\n2-1800 chaws uwu.",
        "v_rep_snt": "Upwoading...",
        "v_rep_min": "Text too showt.",
        "v_rep_max": "Wimit exceeded.",
        "v_rep_cncl": "Cancewwed.",
        "v_loading_ui": "Seawching Vectow database...",
        "v_sending": "Woading... (´• ω •`)",
        "v_more_replies": "...and {count} mowe wepwies on site.",
        "v_more_comments": "...and mowe comments on site.",
        "v_upd_req": "Updating Vectow...",
        "v_upd_ok": "Vectow updated! (≧◡≦)",
        "v_upd_err": "Update faiwed! ;w;",
        "v_upd_check": "Checking hashy-washies… owo",
        "v_install_log_hdr": "Instaww wog: {name} >w<",
        "v_install_fail_forbidden": "Fowbidden method: <code>{detail}</code> ;(",
        "v_install_fail_requirements": "Pip deps faiwed: <code>{detail}</code> owo",
        "v_install_fail_dependency": "Missing dep: <code>{detail}</code> ;;w;;",
        "v_install_fail_packages": "System pkgs faiwed: <code>{detail}</code>",
        "v_install_fail_core_overwrite": "Twied to ovewwwite cowe <code>{detail}</code>",
        "v_install_fail_ffmpeg": "Needs ffmpeg (not instawwed) uwu",
        "v_install_fail_inline": "Needs inwine mode (unavaiwabwe)",
        "v_install_fail_heroku_min": "Needs Hewoku ≥ <code>{detail}</code>",
        "v_install_fail_not_found": "Not found in wepos ;w;",
        "v_install_fail_download": "Downwoad faiwed owo",
        "v_install_fail_unknown": "Unknown ewwow: <code>{detail}</code> >~<",
        "v_upd_same": "🌟 <b>You awe on da watest vewsion, puww updates anyway? (´• ω •`)</b>",
        "v_upd_force_btn": "🧭 Puww Update",
        "v_dlcoll_hdr": "<b>Cowwection {name}</b>",
        "v_dlcoll_count": "{count} moduwes",
        "v_dlcoll_start": "<b>Instawwing aww da moduwes fwom cowwection... pwease wait a wittle, nyaa~ >w<</b>",
        "v_dlcoll_done": "<b>Aww moduwes fwom cowwection instawwed successfuwwy! OwO yippee~</b>",
        "v_dlcoll_done_partial": "<b>Some moduwes faiwed to instaww... sowwy senpai :c</b>",
        "v_dlcoll_done_none": "<b>Nyooo moduwes instawwed... >///<</b>",
        "v_dlcoll_fail_item": "❌ {name}: {reason}",
        "v_dlcoll_empty": "<b>Cowwection is emptyy ;-;</b>",
        "v_dlcoll_not_found": "<b>Cowwection not found owo</b>",
"v_vecdl_usage": "<b>Pwease specify cowwection: </b><code>{p}vecdl <swug></code>",
        "v_dlcoll_max_batch": "{total} moduwes, max {max}. Instawwing fiwst {max}…",
        "v_upd_cancel": "🚫 Nu ;-;",
        "v_miniapp_title": "Open Mini App nya~",
        "v_miniapp_body": "Open Vectow as a Tewegwam Mini App — instant auto-wogin, no passwowds, encwypted session UwU. One tap and you're in!! owo",
        "v_miniapp_btn": "🚀 Open Vectow >w<",
    }

    def _detect_lang_suffix(self) -> str:
        variants = {"en", "ru", "jp", "ua", "de", "neofit", "tiktok", "leet", "uwu"}
        lang = str(self.strings.get("lang", "en")).strip().lower()
        result = lang if lang in variants else "en"
        log.debug("_detect_lang_suffix: raw=%r -> %s", lang, result)
        return result


    ICONS = {
        "search": '<tg-emoji emoji-id="5447459604524971717">🔎</tg-emoji>',
        "error": '<tg-emoji emoji-id="5388785832956016892">❌</tg-emoji>',
        "warn": '<tg-emoji emoji-id="5881702736843511327">⚠️</tg-emoji>',
        "description": '<tg-emoji emoji-id="6008090211181923982">📝</tg-emoji>',
        "command": '<tg-emoji emoji-id="5877260593903177342">⚙</tg-emoji>',
        "dependency": '<tg-emoji emoji-id="5325732612084351248">📦</tg-emoji>',
        "module": '<tg-emoji emoji-id="5924720918826848520">📦</tg-emoji>',
        "modules_list": '<tg-emoji emoji-id="5883973610606956186">🗂</tg-emoji>',
        "shield": '<tg-emoji emoji-id="5926783847453692661">🛡</tg-emoji>',
        "safe": '<tg-emoji emoji-id="5776375003280838798">✅</tg-emoji>',
        "stats": '<tg-emoji emoji-id="5877485980901971030">📊</tg-emoji>',
        "quota": '<tg-emoji emoji-id="6311858554944888333">⌚️</tg-emoji>',
        "verified": '<tg-emoji emoji-id="5958376256788502078">⭐️</tg-emoji>',
        "comments": '<tg-emoji emoji-id="5886666250158870040">💬</tg-emoji>',
        "reply": "↳",
        "broken": '<tg-emoji emoji-id="5877260593903177342">💥</tg-emoji>',
        "tag": '<tg-emoji emoji-id="5985433648810171091">🏷</tg-emoji>',
    }

    async def _safe_install(self, m_name: str, dl_url: str) -> bool:
        ldr = self.lookup("Loader")
        if not ldr or not hasattr(ldr, "download_and_install"):
            log.error("_safe_install: no Loader or download_and_install missing")
            return False

        try:
            res = await ldr.download_and_install(dl_url)
            if getattr(ldr, "fully_loaded", False):
                ldr.update_modules_in_db()
            return res == 1
        except Exception as e:
            log.warning("Install wrapper caught exception for %s: %r", m_name, e)
            return False

    def __init__(self) -> None:
        log.debug("__init__: Vector module instance created")
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "limit", 
                30, 
                lambda: self.strings("v_lim_cfg"), 
                validator=loader.validators.Integer(minimum=1, maximum=100)
            ),
            loader.ConfigValue(
                "max_batch",
                50,
                lambda: self.strings("v_max_batch_cfg"),
                validator=loader.validators.Integer(minimum=1, maximum=100)
            ),
            loader.ConfigValue(
                "auto_update_notify",
                True,
                lambda: self.strings("v_auto_upd_cfg"),
                validator=loader.validators.Boolean()
            ),
            loader.ConfigValue(
                "VectorInstall",
                True,
                lambda: "Включает или выключает Vector Install",
                validator=loader.validators.Boolean()
            ),
        )
        self.http: Optional[aiohttp.ClientSession] = None
        self.seccache: Dict[str, Dict[str, Any]] = {}
        self._cmt_calls: Dict[str, Any] = {}
        self.httpc = 0
        self.bannote = ""
        self.btid = 0
        self._list_pg = 0
        self._expanded = False

    async def client_ready(self, client: "herokutl.TelegramClient", database: "loader.Database") -> None:
        self.client = client
        self.database = database
        self.http = aiohttp.ClientSession()
        asyncio.ensure_future(self._token_keeper())
        asyncio.ensure_future(self._sync_modules_keeper())
        log.info("Vector Module Monolith Started")

    async def on_unload(self) -> None:
        log.info("on_unload: Vector module unloading")
        if self.http and not self.http.closed:
            await self.http.close()
            log.debug("on_unload: HTTP session closed")

    async def _net_req(self, method: str, path: str, token: str = "", params: dict = None, json_data: dict = None, as_bytes: bool = False, timeout: int = 15) -> Any:
        log.debug("_net_req: %s %s params=%s json=%s bytes=%s timeout=%s", method, path, bool(params), bool(json_data), as_bytes, timeout)
        if not self.http or self.http.closed:
            self.http = aiohttp.ClientSession()
            log.debug("_net_req: created new aiohttp ClientSession")
            
        url = urljoin(apirt + "/", path.lstrip("/"))
        headers = {"User-Agent": "VectorUserbotClient/2.0"}
        if token:
            headers["Authorization"] = f"Bearer {token}"

        self.httpc = 0
        try:
            async with self.http.request(method, url, params=params, json=json_data, headers=headers, timeout=aiohttp.ClientTimeout(total=timeout)) as r:
                self.httpc = r.status
                log.debug("HTTP %s %s -> %s", method, path, r.status)
                if r.status >= 300:
                    return None
                if as_bytes:
                    return await r.read()
                return await r.json(content_type=None)
        except Exception as e:
            log.warning("HTTP request failed method=%s path=%s error=%r", method, path, e)
            self.httpc = -1
            return None

    def _normalize_module(self, raw: dict) -> dict:
        log.debug("_normalize_module: name=%s version=%s", raw.get("name", "?"), raw.get("version", "?"))
        lang = self._detect_lang_suffix()
        db_suffix = {"en": "", "ua": "_ua"}.get(lang, f"_{lang}")
        cmds = []
        for c in (raw.get("commands") or []):
            if isinstance(c, dict):
                cmd_desc_key = f"desc{db_suffix}"
                cmd_desc = (c.get(cmd_desc_key) if cmd_desc_key != "desc" else None) or c.get("description") or c.get("desc") or ""
                cmds.append({
                    "name": c.get("name") or c.get("cmd") or "",
                    "description": cmd_desc,
                    "is_inline": bool(c.get("is_inline")),
                    "is_placeholder": bool(c.get("is_placeholder")),
                })

        dev = str(raw.get("developer") or raw.get("author") or "@Unknown")
        ioff = bool(
            raw.get("official") 
            or raw.get("is_official") 
            or raw.get("verified") 
            or raw.get("is_verified") 
            or raw.get("telegram_verified") 
            or raw.get("official_developer") 
            or raw.get("is_official_developer")
        )
        name = str(raw.get("name") or raw.get("class_name") or "Unknown")
        
        locales = raw.get("locales")
        desc = raw.get("description") or ""
        if isinstance(locales, dict):
            loc_key = f"description{db_suffix}"
            loc_val = locales.get(loc_key)
            if isinstance(loc_val, str) and loc_val.strip():
                desc = loc_val
        
        return {
            "name": name,
            "owner": raw.get("source_owner") or "unknown",
            "version": raw.get("version") or "?.?.?",
            "author": dev,
            "description": desc,
            "commands": cmds,
            "dependencies": [str(d) for d in (raw.get("dependencies") or [])],
            "official": ioff,
            "likes": int(raw.get("likes") or 0),
            "dislikes": int(raw.get("dislikes") or 0),
            "banner": raw.get("banner"),
            "source_url": raw.get("source_url") or f"{apirt}/modules/{quote(raw.get('source_owner', 'unknown'), safe='')}/{quote(name, safe='')}/source",
            "tags": raw.get("tags") or [],
            "dl_url": raw.get("source_url") or f"{apirt}/modules/{quote(raw.get('source_owner', 'unknown'), safe='')}/{quote(name, safe='')}/source",
        }

    @staticmethod
    def _extract_counts(data: dict):
        likes = dislikes = None
        for container in (data, data.get("module"), data.get("data"), data.get("result"), data.get("summary")):
            if not isinstance(container, dict):
                continue
            for lk in ("likes", "likes_count", "likesCount", "likeCount", "like_count"):
                v = container.get(lk)
                if v is not None:
                    try:
                        likes = int(v)
                    except (ValueError, TypeError):
                        pass
                    break
            for dk in ("dislikes", "dislikes_count", "dislikesCount", "dislikeCount", "dislike_count"):
                v = container.get(dk)
                if v is not None:
                    try:
                        dislikes = int(v)
                    except (ValueError, TypeError):
                        pass
                    break
            if likes is not None and dislikes is not None:
                break
        log.debug("_extract_counts: likes=%s dislikes=%s", likes, dislikes)
        return likes, dislikes

    def _parse_jwt(self, token: str) -> dict:
        log.debug("_parse_jwt: token len=%d", len(token) if token else 0)
        try:
            b64_part = token.split(".")[1]
            b64_part += "=" * (-len(b64_part) % 4)
            return json.loads(base64.urlsafe_b64decode(b64_part.encode()).decode())
        except Exception:
            return {}

    @staticmethod
    def _norm_hash_name(value: str) -> str:
        log.debug("_norm_hash_name: value=%r", str(value)[:64] if value else "")
        value = unicodedata.normalize("NFKC", str(value or ""))
        value = value.replace("​", "").replace("‌", "").replace("‍", "").replace("﻿", "")
        return " ".join(value.strip().split())

    async def _get_active_token(self, force: bool = False) -> str:
        log.debug("_get_active_token: force=%s", force)
        if force:
            self.set("auth_token", None)
            log.debug("_get_active_token: auth_token cleared (force)")
            
        cached = self.get("auth_token")
        if cached:
            payload = self._parse_jwt(cached)
            if payload.get("exp", 0) - time.time() > 60:
                log.debug("_get_active_token: cached token valid, exp=%s", payload.get("exp"))
                return cached
            log.debug("_get_active_token: cached token expired or expiring")

        log.info("_get_active_token: requesting fresh token")
        bot_info = await self._net_req("GET", "/api/tg-bot")
        bot_username = (bot_info or {}).get("username", "").strip().lstrip("@")
        if not bot_username:
            log.warning("No bot username returned from /api/tg-bot")
            return ""

        me = await self.client.get_me()
        uid = str(getattr(me, "id", ""))
        uname = getattr(me, "username", "") or ""
        fname = getattr(me, "first_name", "") or ""
        lname = getattr(me, "last_name", "") or ""
        dname = " ".join(filter(None, [fname, lname])).strip() or uname or uid

        uname = self._norm_hash_name(uname).lower()
        dname = self._norm_hash_name(dname)

        with suppress(Exception):
            await self.client(UnblockRequest(bot_username))

        new_jwt = ""
        ban_notice = ""
        for attempt in range(2):
            b_stamp = int(time.time() // 10) - attempt
            cmd_hash = hashlib.sha256(f"vector-token-v2|{uid}|{b_stamp}|{auths}".encode()).hexdigest()[:32]
            cmd_str = f"/{cmd_hash}"

            try:
                async with self.client.conversation(bot_username, timeout=12, exclusive=False) as conv:
                    out_msg = await conv.send_message(cmd_str)
                    try:
                        resp = await asyncio.wait_for(conv.get_response(), timeout=10)
                        txt = getattr(resp, "raw_text", getattr(resp, "text", ""))
                        match = jwtrx.search(txt)
                        if match:
                            new_jwt = match.group(0)
                        elif "заблок" in txt.lower() or "⛔" in txt:
                            ban_notice = self._format_ban_notice(txt)
                        with suppress(Exception): await out_msg.delete()
                        if new_jwt: break
                    except asyncio.TimeoutError:
                        with suppress(Exception): await out_msg.delete()
            except Exception as e:
                log.warning("Token conversation attempt=%s failed: %r", attempt, e)

        if new_jwt:
            self.set("auth_token", new_jwt)
            self.bannote = ""
            log.info("_get_active_token: new token obtained")
        elif ban_notice:
            self.bannote = ban_notice
            log.warning("_get_active_token: user banned")
        else:
            log.warning("_get_active_token: no token obtained")
        return new_jwt

    def _format_ban_notice(self, raw_text: str) -> str:
        log.debug("_format_ban_notice: raw_len=%d", len(raw_text) if raw_text else 0)
        txt = str(raw_text or "").strip()
        reason_match = brrx.search(txt)
        term_match = btrx.search(txt)

        reason_raw = reason_match.group(1).strip() if reason_match else ""
        term_raw = term_match.group(1).strip() if term_match else ""

        if not reason_raw or not term_raw:
            for line in txt.splitlines():
                if ":" not in line:
                    continue
                key, value = line.split(":", 1)
                key_l = key.strip().lower()
                val = value.strip()
                if not reason_raw and key_l in {"причина", "reason", "理由", "grund", "r3450n", "weason", "charge"}:
                    reason_raw = val
                if not term_raw and key_l in {"срок", "term", "期間", "dauer", "73rm", "tewm"}:
                    term_raw = val

        reason = utils.escape_html(reason_raw or "-")
        term = utils.escape_html(term_raw or "permanent")
        return self.strings["v_ban_notice"].format(reason=reason, term=term)

    @staticmethod
    def _plain_len(text: str) -> int:
        n = 0
        inside = False
        for ch in text:
            if ch == "<":
                inside = True
            elif ch == ">":
                inside = False
            elif not inside:
                n += 1
        return n

    @staticmethod
    def _tag_safe_truncate(text: str, cap: int) -> str:
        if len(text) <= cap:
            return text
        plain = ""
        inside = False
        tag = ""
        last_close = 0
        for i, ch in enumerate(text):
            if ch == "<":
                inside = True
                tag = "<"
            elif ch == ">" and inside:
                inside = False
                if tag.startswith("</"):
                    last_close = i + 1
                tag = ""
            elif inside:
                tag += ch
            else:
                plain += ch
            if len(plain) >= cap and not inside:
                raw = text[:i + 1]
                if tag.startswith("</"):
                    raw = text[:last_close or i + 1]
                return raw.rstrip() + "..."
        return text

    def _build_html(self, m_data: dict, current_idx: int, total_cnt: int) -> str:
        log.debug("_build_html: name=%s idx=%d/%d", m_data.get("name", "?"), current_idx, total_cnt)
        CAP = 900

        name = utils.escape_html(str(m_data.get("name", "Unknown")))
        author = utils.escape_html(str(m_data.get("author", "@Unknown")))
        ver = str(m_data.get("version", "?.?.?"))

        header = f"{self.ICONS['module']} <code>{name}</code> <b>{self.strings['v_dev_lbl']}</b> <code>{author}</code>"
        if ver != "?.?.?":
            header += f" (<code>v{utils.escape_html(ver)}</code>)"
        status_text = self.strings["v_dev_ofc"] if m_data.get("official") else self.strings["v_dev_unofc"]
        status = f"{self.ICONS['verified']} <b>{self.strings['v_dev_str']}</b> <code>{status_text}</code>"
        page = f"{self.ICONS['modules_list']} <i>{self.strings['v_page'].format(idx=current_idx, total=total_cnt)}</i>" if total_cnt > 1 else ""

        pfx = [header, status]
        if page:
            pfx.append(page)
        used = len("\n".join(pfx))

        desc = m_data.get("description")
        desc_block = ""
        if desc and used < CAP - 20:
            desc_raw = re.sub(r'(https?://\S+|www\.\S+)', r'<code>\1</code>', utils.escape_html(str(desc)))
            hdr = f"\n{self.ICONS['description']} <b>{self.strings['v_info']}</b>\n<blockquote expandable>"
            ftr = "</blockquote>"
            room = CAP - used - len(hdr) - len(ftr) - 8
            if room > 0:
                if len(desc_raw) > room:
                    desc_raw = desc_raw[:room - 3].rstrip() + "..."
                if desc_raw:
                    desc_block = f"{hdr}{desc_raw}{ftr}"

        cmds = m_data.get("commands", [])
        cmd_block = ""
        if cmds:
            est = used + len(desc_block) + 30
            if est < CAP:
                hdr = f"\n\n{self.ICONS['command']} <b>{self.strings['v_cmds']}</b>\n<blockquote expandable>"
                ftr = "</blockquote>"
                room = CAP - used - len(desc_block) - len(hdr) - len(ftr) - 5
                if room > 0:
                    cl = []
                    for c in cmds:
                        cn = utils.escape_html(str(c.get("name", "")))
                        cd = utils.escape_html(str(c.get("description", ""))).split("\n")[0]
                        if c.get("is_placeholder"):
                            line = f"<code>{{{cn}}}</code> {cd}"
                        elif c.get("is_inline"):
                            bot = getattr(getattr(self, "inline", None), "bot_username", None) or "bot"
                            line = f"<code>@{utils.escape_html(bot)} {cn}</code> {cd}"
                        else:
                            line = f"<code>{self.get_prefix()}{cn}</code> {cd}"
                        if room - len(line) - 1 < 0:
                            break
                        cl.append(line)
                        room -= len(line) + 1
                    if cl:
                        if len(cl) < len(cmds):
                            cl.append(f"... +{len(cmds) - len(cl)} more")
                        cmd_block = f"{hdr}{chr(10).join(cl)}{ftr}"

        pfx_plain = self._plain_len("\n".join(pfx))
        desc_plain = self._plain_len(desc_block)
        cmd_plain = self._plain_len(cmd_block)
        cur_plain = pfx_plain + desc_plain + cmd_plain

        tags = m_data.get("tags", [])
        tags_block = ""
        log.debug("_build_html: name=%s tags=%s", m_data.get("name", "?"), tags)
        if tags:
            hdr = f"\n\n{self.ICONS['tag']} <b>{self.strings.get('v_tags', 'Tags')}</b>\n<blockquote expandable>"
            ftr = "</blockquote>"
            hdr_plain = self._plain_len(hdr)
            room = CAP - cur_plain - hdr_plain - self._plain_len(ftr)
            log.debug("_build_html tags: cur_plain=%d room=%d", cur_plain, room)
            if room > 0:
                tl = []
                for t in tags:
                    tt = utils.escape_html(str(t))
                    room_needed = self._plain_len(f"<em>{tt}</em>") + 3
                    if room - room_needed < 0:
                        break
                    tl.append(f"<em>{tt}</em>")
                    room -= room_needed
                if tl:
                    tags_block = f"{hdr}{' · '.join(tl)}{ftr}"
                    log.debug("_build_html tags: built %d tags", len(tl))
                else:
                    log.debug("_build_html tags: tl empty, skipping")
            else:
                log.debug("_build_html tags: room <= 0, skipping")

        deps = m_data.get("dependencies", [])
        dep_block = ""
        if deps:
            hdr = f"\n\n{self.ICONS['dependency']} <b>{self.strings.get('v_deps', 'Dependencies')}</b>\n<blockquote expandable>"
            ftr = "</blockquote>"
            tags_plain = self._plain_len(tags_block)
            room = CAP - cur_plain - tags_plain - self._plain_len(hdr) - self._plain_len(ftr)
            if room > 0:
                dl = []
                for d in deps:
                    dt = utils.escape_html(str(d))
                    room_needed = self._plain_len(f"<code>{dt}</code>") + 3
                    if room - room_needed < 0:
                        break
                    dl.append(f"<code>{dt}</code>")
                    room -= room_needed
                if dl:
                    dep_block = f"{hdr}{', '.join(dl)}{ftr}"

        return self._tag_safe_truncate(("\n".join(pfx) + desc_block + cmd_block + tags_block + dep_block).rstrip(), CAP)

    def _build_kbd(self, item: dict, idx: int, group: list, search_phrase: str, is_expanded: bool = False, comments_pg: int = 0) -> list:
        log.debug("_build_kbd: name=%s idx=%d expanded=%s", item.get("name", "?"), idx, is_expanded)
        m_name = str(item.get("name", ""))
        m_owner = str(item.get("owner", "unknown"))
        kbd = [
            [
                {"text": self.strings["v_btn_copy"], "copy": search_phrase},
                {"text": self.strings["v_btn_dl"], "callback": self.cb_install, "args": (m_owner, m_name, idx, group, search_phrase)},
                {"text": self.strings["v_btn_code"], "url": item.get("source_url")},
            ],
            [
                {"text": f"👍 {item.get('likes', 0)}", "callback": self.cb_rate, "args": (m_owner, m_name, "like", idx, group, search_phrase)},
                {"text": f"👎 {item.get('dislikes', 0)}", "callback": self.cb_rate, "args": (m_owner, m_name, "dislike", idx, group, search_phrase)},
            ]
        ]
        
        if group and len(group) > 1:
            prev_i = (idx - 1) % len(group)
            next_i = (idx + 1) % len(group)
            kbd.append([
                {"text": "◀️", "callback": self.cb_nav, "args": (prev_i, group, search_phrase, is_expanded)},
                {"text": self.strings["v_page"].format(idx=idx + 1, total=len(group)), "callback": self.cb_list, "args": (idx, group, search_phrase)},
                {"text": "▶️", "callback": self.cb_nav, "args": (next_i, group, search_phrase, is_expanded)},
            ])
            
        kbd.append([{
            "text": self.strings["v_btn_col" if is_expanded else "v_btn_exp"],
            "callback": self.cb_toggle,
            "args": (m_owner, m_name, idx, group, search_phrase, not is_expanded)
        }])
        
        if is_expanded:
            kbd.append([
                {"text": self.strings["v_btn_talk"], "callback": self.cb_comments, "args": (m_owner, m_name, idx, group, search_phrase, comments_pg, is_expanded)},
                {"text": self.strings["v_btn_sec"], "callback": self.cb_sec_check, "args": (m_owner, m_name, idx, group, search_phrase, is_expanded)},
            ])
            
        return kbd

    async def _token_keeper(self) -> None:
        while True:
            await asyncio.sleep(20 * 3600)
            log.info("_token_keeper: refreshing token")
            await self._get_active_token(force=True)

    async def _run_search(self, q: str, lang_sfx: str = "", _retried: bool = False) -> Any:
        token = await self._get_active_token()
        if not token:
            log.warning("_run_search: no token")
            return [], False

        log.info("_run_search: q=%r token=%s", q, bool(token))
        raw_res = await self._net_req("GET", "/api/search", token=token, params={"q": q, "limit": str(self.config["limit"]), "lang": lang_sfx})

        if raw_res is None and self.httpc != 401:
            if not _retried:
                log.warning("_run_search: first attempt failed (httpc=%s), retrying", self.httpc)
                return await self._run_search(q, lang_sfx, _retried=True)
            log.error("_run_search: retry also failed, httpc=%s", self.httpc)
            return None, True

        if self.httpc == 401:
            log.info("_run_search: got 401, forcing token refresh")
            token = await self._get_active_token(force=True)
            if not token:
                return [], False
            raw_res = await self._net_req("GET", "/api/search", token=token, params={"q": q, "limit": str(self.config["limit"]), "lang": lang_sfx})

        if raw_res is None and self.httpc != 401:
            log.error("_run_search: API error after token refresh, httpc=%s", self.httpc)
            return None, True

        m_list = []
        if isinstance(raw_res, dict):
            m_list = raw_res.get("results", [])
        elif isinstance(raw_res, list):
            m_list = raw_res
        m_list = [self._normalize_module(x) for x in m_list if isinstance(x, dict)]
        log.info("_run_search: %d results", len(m_list))
        return m_list, True

    async def _show_result_form(self, target: Any, m_list: list, q: str) -> None:
        item = m_list[0]
        self._list_pg = 0
        self._expanded = False
        kbd = self._build_kbd(item, 0, m_list, q)
        text = self._build_html(item, 1, len(m_list))
        await self.inline.form(text, target, reply_markup=kbd, photo=item.get("banner"), silent=True)

    async def _show_search_fail(self, target: Any, m_list: list, token_ok: bool, q: str) -> None:
        if not token_ok:
            log.warning("vectorcmd: no token")
            await utils.answer(target, self.bannote or f"{self.ICONS['error']} <b>{self.strings['v_err_api']}</b>", reply_markup=[[{"text": self.strings["v_upd_cancel"], "action": "close"}]])
        elif m_list is None:
            log.error("vectorcmd: API unreachable")
            await utils.answer(target, f"{self.ICONS['error']} <b>{self.strings['v_err_api']}</b>", reply_markup=[[{"text": self.strings["v_upd_cancel"], "action": "close"}]])
        elif not m_list:
            log.debug("vectorcmd: no results")
            await utils.answer(target, f"{self.ICONS['error']} <b>{self.strings['v_err_404'].format(q=f'<code>{utils.escape_html(q)}</code>')}</b>", reply_markup=[[{"text": self.strings["v_upd_cancel"], "action": "close"}]])

    @loader.command(
        en_doc="<query> — search modules in Vector.",
        ru_doc="<запрос> — поиск модулей в Vector.",
        jp_doc="<クエリ> — Vectorでモジュールを検索。",
        ua_doc="<запит> — пошук модулів у Vector.",
        de_doc="<Abfrage> — Suche nach Modulen in Vector.",
        neofit_doc="<query> — grep modules in Vector.",
        tiktok_doc="<запрос> — чекнуть темки (модули) в Vector.",
        leet_doc="<qu3ry> — 534rch m0dul35 1n V3c70r.",
        uwu_doc="<quewy> — seawch moduwes in Vectow (´• ω •`)."
    )
    async def vectorcmd(self, msg: Message):
        q = utils.get_args_raw(msg)
        log.info("vectorcmd: query=%r", q)
        if not q:
            log.debug("vectorcmd: empty query, aborting")
            return await utils.answer(msg, f"{self.ICONS['error']} <b>{self.strings['v_err_empty'].format(p=f'<code>{self.get_prefix()}')}</code></b>")
        if len(q) > 120:
            return await utils.answer(msg, f"{self.ICONS['warn']} <b>{self.strings['v_err_len']}</b>")

        lang_sfx = self._detect_lang_suffix()
        search_task = asyncio.ensure_future(self._run_search(q, lang_sfx))
        log.debug("vectorcmd: search launched, racing with form")

        await asyncio.sleep(0.05)

        if search_task.done():
            log.info("vectorcmd: search beat form, sending result directly")
            m_list, token_ok = search_task.result()
            if not token_ok or not m_list:
                return await self._show_search_fail(msg, m_list, token_ok, q)
            return await self._show_result_form(msg, m_list, q)

        log.debug("vectorcmd: form won race, sending loading")
        form = await self.inline.form(
            f"{self.ICONS['search']} <b>{self.strings['v_loading_ui']}</b>",
            msg,
            reply_markup=[[{"text": "ㅤ", "callback": self.cb_dummy}]],
            photo="https://raw.githubusercontent.com/sepiol026-wq/GoyModules/refs/heads/main/assets/vsearch.png",
            silent=True
        )
        log.debug("vectorcmd: loading form sent, awaiting search")

        m_list, token_ok = await search_task
        if not token_ok or not m_list:
            return await self._show_search_fail(form, m_list, token_ok, q)

        item = m_list[0]
        self._list_pg = 0
        self._expanded = False
        kbd = self._build_kbd(item, 0, m_list, q)
        text = self._build_html(item, 1, len(m_list))
        await utils.answer(form, text, reply_markup=kbd, photo=item.get("banner"))

    @loader.command(
        en_doc="[-f|--force] — update Vector module.",
        ru_doc="[-f|--force] — обновить модуль Vector.",
        jp_doc="[-f|--force] — Vectorモジュールを更新します。",
        ua_doc="[-f|--force] — оновити модуль Vector.",
        de_doc="[-f|--force] — Vector-Modul aktualisieren.",
        neofit_doc="[-f|--force] — git pull Vector.",
        tiktok_doc="[-f|--force] — обновить эту темку.",
        leet_doc="[-f|--force] — Upd473 V3c70r m0dul3.",
        uwu_doc="[-f|--force] — Update Vectow moduwe owo."
    )
    async def vecupdate(self, msg: Message):
        args = utils.get_args_raw(msg)
        force = "-f" in args or "--force" in args
        log.info("vecupdate: force=%s args=%r", force, args)

        m_owner = "sepiol026-wq"
        m_name = "Vector"
        dl_path = f"/modules/{m_owner}/{quote(m_name, safe='')}/source"
        dl_url = f"{apirt}/modules/{m_owner}/{quote(m_name, safe='')}/source"
        log.debug("vecupdate: dl_url=%s", dl_url)

        if force:
            log.info("vecupdate: force flag set, installing immediately")
            await utils.answer(msg, f"{self.ICONS['search']} <b>{self.strings['v_upd_req']}</b>")
            ok = await self._safe_install(m_name, dl_url)
            if ok:
                log.info("vecupdate: force install successful")
                await utils.answer(msg, f"{self.ICONS['safe']} <b>{self.strings['v_upd_ok']}</b>")
            else:
                log.warning("vecupdate: force install failed")
                await utils.answer(msg, f"{self.ICONS['error']} <b>{self.strings['v_upd_err']}</b>")
            return

        await utils.answer(msg, f"{self.ICONS['search']} <b>{self.strings['v_upd_check']}</b>")

        token = await self._get_active_token()
        if not token:
            log.warning("vecupdate: no token, aborting")
            return await utils.answer(msg, self.bannote or f"{self.ICONS['error']} <b>{self.strings['v_err_api']}</b>")

        src_bytes = await self._net_req("GET", dl_path, token=token, as_bytes=True)
        if not src_bytes:
            log.warning("vecupdate: download returned no bytes, installing anyway")
            await utils.answer(msg, f"{self.ICONS['search']} <b>{self.strings['v_upd_req']}</b>")
            ok = await self._safe_install(m_name, dl_url)
            if ok:
                await utils.answer(msg, f"{self.ICONS['safe']} <b>{self.strings['v_upd_ok']}</b>")
            else:
                await utils.answer(msg, f"{self.ICONS['error']} <b>{self.strings['v_upd_err']}</b>")
            return

        log.debug("vecupdate: downloaded %d bytes", len(src_bytes))
        remote_hash = hashlib.sha256(src_bytes).hexdigest()

        import inspect, sys
        local_hash = ""

        mod = sys.modules.get(self.__class__.__module__)
        loader = getattr(mod, '__loader__', None)

        if loader and hasattr(loader, 'get_source'):
            try:
                src = loader.get_source(self.__class__.__module__)
                if src:
                    local_hash = hashlib.sha256(src.encode("utf-8")).hexdigest()
                    log.debug("vecupdate: got local via __loader__.get_source(), len=%d", len(src))
            except Exception as e:
                log.debug("vecupdate: __loader__.get_source() failed: %r", e)

        if not local_hash and mod:
            try:
                src = inspect.getsource(mod)
                local_hash = hashlib.sha256(src.encode("utf-8")).hexdigest()
                log.debug("vecupdate: got local via inspect.getsource(module), len=%d", len(src))
            except Exception:
                pass

        if local_hash:
            log.debug("vecupdate: local_hash=%s remote_hash=%s", local_hash[:16], remote_hash[:16])
        else:
            log.warning("vecupdate: could not read local source, assuming hashes differ")

        if remote_hash == local_hash:
            log.info("vecupdate: hashes match, showing force-update prompt")
            await self.inline.form(
                message=msg,
                text=f"{self.ICONS['search']} <b>{self.strings['v_upd_req']}</b>\n\n{self.strings['v_upd_same']}",
                reply_markup=[
                    [
                        {"text": self.strings["v_upd_force_btn"], "callback": self._vecupdate_force, "args": (dl_url,), "style": "primary"},
                        {"text": self.strings["v_upd_cancel"], "action": "close", "style": "danger"},
                    ]
                ],
            )
            return

        log.info("vecupdate: hashes differ, proceeding with install")
        await utils.answer(msg, f"{self.ICONS['search']} <b>{self.strings['v_upd_req']}</b>")

        ok = await self._safe_install(m_name, dl_url)
        if ok:
            log.info("vecupdate: install successful")
            await utils.answer(msg, f"{self.ICONS['safe']} <b>{self.strings['v_upd_ok']}</b>")
        else:
            log.warning("vecupdate: install failed")
            await utils.answer(msg, f"{self.ICONS['error']} <b>{self.strings['v_upd_err']}</b>")

    async def _vecupdate_force(self, call: Any, dl_url: str):
        log.info("_vecupdate_force: force update triggered, url=%s", dl_url)
        with suppress(Exception):
            await call.answer()
        await call.edit(f"{self.ICONS['search']} <b>{self.strings['v_upd_req']}</b>")
        ok = await self._safe_install("Vector", dl_url)
        if ok:
            log.info("_vecupdate_force: force install successful")
            await call.edit(f"{self.ICONS['safe']} <b>{self.strings['v_upd_ok']}</b>")
        else:
            log.warning("_vecupdate_force: force install failed")
            await call.edit(f"{self.ICONS['error']} <b>{self.strings['v_upd_err']}</b>")

    def _hash_module_source(self, mod_instance: Any) -> str | None:
        try:
            import inspect, sys
            mod = sys.modules.get(mod_instance.__class__.__module__)
            if not mod:
                return None
            src = inspect.getsource(mod)
            return hashlib.sha256(src.encode("utf-8")).hexdigest()
        except Exception:
            return None

    async def _sync_installed_modules(self) -> bool:
        token = await self._get_active_token()
        if not token:
            return False
        lang = self._detect_lang_suffix()
        modules_data = []
        for mod in list(self.allmodules.modules):
            h = self._hash_module_source(mod)
            if not h:
                continue
            modules_data.append({
                "class_name": mod.__class__.__name__,
                "contentHash": h,
                "language": lang,
            })
        if not modules_data:
            return False
        res = await self._net_req("PUT", "/api/users/me/modules", token=token, json_data={"modules": modules_data})
        return bool(res and res.get("ok"))

    async def _sync_modules_keeper(self) -> None:
        first_run = True
        while True:
            if not first_run:
                await asyncio.sleep(86_400)
            first_run = False
            if not self.config.get("auto_update_notify", True):
                continue
            try:
                await self._sync_installed_modules()
            except Exception:
                pass

    @loader.command(
        en_doc="<slug or URL> — download and install entire module collection from Vector.",
        ru_doc="<slug_или_ссылка> — скачать и установить всю коллекцию модулей из Vector.",
        jp_doc="<slugかURL> — Vectorからコレクション全体をダウンロードしてインストール。",
        ua_doc="<slug_або_посилання> — завантажити та встановити всю колекцію модулів із Vector.",
        de_doc="<slug_oder_url> — gesamte Modulsammlung von Vector herunterladen und installieren.",
        neofit_doc="<slug or URL> — pull entire module collection from Vector.",
        tiktok_doc="<slug_или_ссылка> — скачать и вкатить всю подборку темок из Vector.",
        leet_doc="<5lu9_0r_url> — pull 3n71r3 m0dul3 c0ll3c710n fr0m V3c70r.",
        uwu_doc="<swug-ow-url> — downwoad and instaww entiwe moduwe cowwection fwom Vectow (・ω・)."
    )
    async def vecdlcmd(self, msg: Message):
        raw_arg = utils.get_args_raw(msg).strip()
        slug = raw_arg.split("/collections/")[-1].split("/")[0].split("?")[0] if "/collections/" in raw_arg else raw_arg
        log.info("vecdl: raw=%r slug=%r", raw_arg, slug)
        if not slug:
            return await utils.answer(msg, f"{self.ICONS['error']} <b>Specify collection: </b><code>{self.get_prefix()}vecdl {'<slug or URL>'}</code>")

        token = await self._get_active_token()
        if not token:
            return await utils.answer(msg, self.bannote or f"{self.ICONS['error']} <b>{self.strings['v_err_api']}</b>")

        raw = await self._net_req("GET", f"/api/collections/{quote(slug, safe='')}", token=token)
        if not raw or not raw.get("ok"):
            return await utils.answer(msg, f"{self.ICONS['error']} <b>{self.strings['v_dlcoll_not_found']}</b>")

        col = raw["collection"]
        modules = [entry["module"] for entry in (col.get("modules") or []) if entry.get("module")]
        if not modules:
            return await utils.answer(msg, f"{self.ICONS['warn']} <b>{self.strings['v_dlcoll_empty']}</b>")

        await utils.answer(msg, f"{self.ICONS['search']} <b>{self.strings['v_sending']}</b>")

        max_batch = int(self.config.get("max_batch", 50))
        total_orig = len(modules)
        if total_orig > max_batch:
            modules = modules[:max_batch]

        col_name = col.get("name", slug)
        await self.inline.form(
            f"{self.ICONS['modules_list']} {self.strings['v_dlcoll_hdr'].format(name=utils.escape_html(col_name))}\n{self.strings['v_dlcoll_count'].format(count=len(modules))}",
            msg,
            reply_markup=[[
                {"text": self.strings["v_btn_dl"], "callback": self._vecdl_install, "args": (modules, col_name)},
                {"text": self.strings["v_upd_cancel"], "action": "close"},
            ]],
            silent=True
        )
        return

    async def _vecdl_install(self, cb: Any, modules: list, col_name: str):
        log.info("_vecdl_install: count=%d name=%r", len(modules), col_name)
        with suppress(Exception): await cb.answer()
        max_batch = int(self.config.get("max_batch", 50))
        total_orig = len(modules)
        if total_orig > max_batch:
            modules = modules[:max_batch]

        await utils.answer(cb, f"{self.ICONS['modules_list']} {self.strings['v_dlcoll_hdr'].format(name=utils.escape_html(col_name))}\n{self.strings['v_dlcoll_count'].format(count=len(modules))}\n\n{self.ICONS['search']} {self.strings['v_dlcoll_start']}", reply_markup=[[{"text": "…", "callback": self.cb_dummy}]])

        ok = 0
        failed: List[str] = []
        for mod in modules:
            dl_url = mod.get("source_download_url") or mod.get("source_raw_url") or f"{apirt}/modules/{quote(str(mod.get('source_owner', 'unknown')), safe='')}/{quote((mod.get('name') or ''), safe='')}/source"
            m_name = mod.get("name", "?")
            ok_flag = await self._safe_install(m_name, dl_url)
            if ok_flag:
                ok += 1
            else:
                failed.append(self.strings('v_dlcoll_fail_item').format(name=utils.escape_html(m_name), reason=self.strings("v_dl_err")))
            await asyncio.sleep(2)

        if ok == len(modules):
            result = f"{self.ICONS['safe']} {self.strings['v_dlcoll_done']}"
        elif ok > 0:
            result = f"{self.ICONS['warn']} {self.strings['v_dlcoll_done_partial']}"
        else:
            result = f"{self.ICONS['error']} {self.strings['v_dlcoll_done_none']}"

        result += f"\n<b>{ok}/{len(modules)}</b>"
        if failed:
            result += "\n\n" + "\n".join(failed[:8])
            if len(failed) > 8:
                result += f"\n… +{len(failed) - 8} more"
        if total_orig > max_batch:
            result += f"\n\n<i>{self.strings['v_dlcoll_max_batch'].format(total=total_orig, max=max_batch)}</i>"

        await utils.answer(cb, result, reply_markup=[[{"text": "✖️", "action": "close"}]])

    @loader.watcher()
    async def vector_install_payload_watcher(self, msg: Message):
        if getattr(msg, "out", False):
            return
        if not self.config.get("VectorInstall", True):
            return
        if not self.btid:
            try:
                binfo = await self._net_req("GET", "/api/tg-bot")
                buname = (binfo or {}).get("username", "").strip().lstrip("@")
                if buname:
                    ent = await self.client.get_entity(buname)
                    self.btid = getattr(ent, "id", 0)
            except Exception:
                self.btid = -1
        if self.btid <= 0:
            return
        sid = getattr(msg, "sender_id", None) or getattr(getattr(msg, "sender", None), "id", None) or 0
        if sid and int(sid) != self.btid:
            return
        text = (getattr(msg, "raw_text", None) or "").strip()
        log.debug("vector_install_payload_watcher: text_len=%d starts_with_payload=%s", len(text), text.startswith("#v_payload:") if len(text) > 5 else False)
        saved_notify = None
        notify_peer = None
        with suppress(Exception):
            peer = await self._client.get_input_entity(msg.chat_id)
            notify_peer = InputNotifyPeer(peer=peer)
        if notify_peer is not None:
            with suppress(Exception):
                saved_notify = await self._client(GetNotifySettingsRequest(notify_peer))
            with suppress(Exception):
                await self._client(UpdateNotifySettingsRequest(
                    peer=notify_peer,
                    settings=InputPeerNotifySettings(mute_until=2**31 - 1)
                ))
        try:
            if text == lping:
                log.debug("vector_install_payload_watcher: lang ping received")
                with suppress(Exception):
                    await self._client.send_message(msg.chat_id, f"{lpong}{self._detect_lang_suffix()}")
                with suppress(Exception):
                    await msg.delete()
                return
            if not text.startswith("#v_payload:"):
                return

            parts = text.split(":", 4)
            if len(parts) != 5:
                log.debug("vector_install_payload_watcher: invalid parts count=%d", len(parts))
                return
            _, owner_module, action, ts_raw, signature = parts
            if "|" in owner_module:
                owner, module_name = owner_module.split("|", 1)
            else:
                owner, module_name = "unknown", owner_module
            log.info("vector_install_payload_watcher: owner=%s module=%s action=%s", owner, module_name, action)
            if not owner_module or not action or not ts_raw or not signature:
                return
            if action not in {"install", "like", "dislike", "update"}:
                return
            if not re.fullmatch(r"[^:]+", module_name):
                return
            if not ts_raw.isdigit():
                return

            ts = int(ts_raw)
            now = int(time.time())
            if abs(now - ts) > 60:
                return

            local_payload = f"{owner_module}:{action}:{ts}"
            local_signature = hmac.new(
                auths.encode("utf-8"),
                local_payload.encode("utf-8"),
                hashlib.sha256,
            ).hexdigest()
            if not hmac.compare_digest(local_signature, signature):
                return

            with suppress(Exception):
                await msg.delete()

            async def send_feedback(status: str, reason: str = "", banned_until: str = "") -> None:
                feedback_ts = int(time.time())
                safe_reason = (reason or "").replace(":", " ").strip()
                safe_until = (banned_until or "").replace(":", " ").strip()
                feedback_payload = f"{owner_module}:{action}:{status}:{feedback_ts}:{safe_reason}:{safe_until}"
                feedback_signature = hmac.new(
                    auths.encode("utf-8"),
                    feedback_payload.encode("utf-8"),
                    hashlib.sha256,
                ).hexdigest()
                with suppress(Exception):
                    await self._client.send_message(
                        msg.chat_id,
                        f"#v_feedback:{owner_module}:{action}:{status}:{feedback_ts}:{safe_reason}:{safe_until}:{feedback_signature}",
                    )
                with suppress(Exception):
                    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=5)) as _s:
                        await _s.post(
                            f"{apirt}/api/tg-bot/install-feedback",
                            json={"owner_module": owner_module, "status": status, "reason": safe_reason},
                            headers={"content-type": "application/json", "x-bot-secret": auths},
                        )

            token = await self._get_active_token()
            if not token:
                reason = "User is banned" if not self.bannote else self.bannote
                await send_feedback("banned", reason, "permanent")
                return

            if action == "install":
                log.info("vector_install_payload_watcher: install action for %s/%s", owner, module_name)
                dl_url = f"{apirt}/modules/{quote(owner, safe='')}/{quote(module_name, safe='')}/source"
                ok = await self._safe_install(module_name, dl_url)
                log.info("vector_install_payload_watcher: install result=%s", ok)
                await send_feedback("ok" if ok else "error")
                return

            if action == "update":
                log.info("vector_install_payload_watcher: update action for module_id=%s", owner_module)
                mod_info = await self._net_req("GET", f"/api/modules/by-id/{quote(owner_module, safe='')}", token=token)
                if not mod_info or not mod_info.get("ok"):
                    await send_feedback("error", "module not found")
                    return
                mod_data = mod_info.get("module", {})
                mod_name = mod_data.get("name", "")
                mod_owner = mod_data.get("source_owner", "")
                if not mod_name:
                    await send_feedback("error", "invalid module data")
                    return
                dl_url = f"{apirt}/modules/{quote(mod_owner, safe='')}/{quote(mod_name, safe='')}/source"
                ok = await self._safe_install(mod_name, dl_url)
                log.info("vector_install_payload_watcher: update result=%s", ok)
                await send_feedback("ok" if ok else "error")
                return

            log.info("vector_install_payload_watcher: rate action %s for %s/%s", action, owner, module_name)
            uid = self._parse_jwt(token).get("sub", "")
            res = await self._net_req("POST", f"/api/rate/{quote(str(uid), safe='')}/{quote(owner, safe='')}/{quote(module_name, safe='')}/{action}", token=token)
            if not res and self.httpc in {401, 403}:
                log.warning("vector_install_payload_watcher: banned (401/403)")
                await send_feedback("banned", "User is banned", "permanent")
                return
            await send_feedback("ok" if res and res.get("ok") else "error")
        finally:
            if notify_peer is not None:
                with suppress(Exception):
                    await self._client(UpdateNotifySettingsRequest(
                        peer=notify_peer,
                        settings=InputPeerNotifySettings(
                            mute_until=getattr(saved_notify, 'mute_until', 0) if saved_notify is not None else 0,
                        )
                    ))

    @loader.command(
        en_doc="— open Vector as Telegram Mini App.",
        ru_doc="— открыть Vector как Mini App в Telegram.",
        ua_doc="— відкрити Vector як Mini App у Telegram.",
        de_doc="— Vector als Telegram Mini App öffnen.",
        jp_doc="— VectorをTelegram Mini Appとして開く。",
        neofit_doc="— $ ./mini_app --launch",
        tiktok_doc="— открыть Vector как мини апп в телеге.",
        leet_doc="— 0p3n V3c70r 4s T3l3gr4m M1n1 4pp.",
        uwu_doc="— open Vectow as Tewegwam Mini App nya~",
    )
    async def vecmecmd(self, msg: Message):
        await utils.answer(msg, f"{self.ICONS['search']} <b>{self.strings['v_sending']}</b>")
        bot_info = await self._net_req("GET", "/api/tg-bot")
        bot_uname = (bot_info or {}).get("username", "").strip().lstrip("@")
        if not bot_uname:
            await utils.answer(msg, self.strings["v_err_api"])
            return
        text = f"{self.ICONS['shield']} <b>{self.strings['v_miniapp_title']}</b>\n\n{self.strings['v_miniapp_body']}"
        link = f"https://t.me/{bot_uname}/vector"
        await self.inline.form(
            text, msg,
            reply_markup=[[
                {"text": self.strings["v_miniapp_btn"], "url": link},
                {"text": self.strings["v_upd_cancel"], "action": "close"},
            ]],
            silent=True
        )

    async def cb_dummy(self, cb: Any):
        log.debug("cb_dummy: no-op callback")
        with suppress(Exception): await cb.answer()

    async def cb_nav(self, cb: Any, target_i: int, group: list, q: str, expanded: Optional[bool] = None, comments_pg: int = 0):
        if expanded is None:
            expanded = getattr(self, '_expanded', False)
        self._expanded = expanded
        log.debug("cb_nav: target_i=%d group_len=%d expanded=%s", target_i, len(group) if group else 0, expanded)
        with suppress(Exception): await cb.answer()
        if 0 <= target_i < len(group):
            item = group[target_i]
            await utils.answer(cb, self._build_html(item, target_i + 1, len(group)), reply_markup=self._build_kbd(item, target_i, group, q, expanded, comments_pg), photo=item.get("banner"))

    async def cb_list(self, cb: Any, curr_i: int, group: list, q: str):
        log.debug("cb_list: curr_i=%d group_len=%d", curr_i, len(group) if group else 0)
        with suppress(Exception): await cb.answer()
        total_pages = max(1, (len(group) + 4) // 5)
        pg = self._list_pg % total_pages
        start, end = pg * 5, min((pg + 1) * 5, len(group))
        kb = []
        for i in range(start, end):
            m = group[i]
            kb.append([{"text": f"{i + 1}. {m.get('name')} by {m.get('author')}", "callback": self.cb_nav, "args": (i, group, q)}])
        prev_pg = (pg - 1) % total_pages
        next_pg = (pg + 1) % total_pages
        kb.append([
            {"text": "◀️", "callback": self.cb_page, "args": (prev_pg, group, q, curr_i)},
            {"text": self.strings['v_page'].format(idx=pg + 1, total=total_pages), "callback": self.cb_dummy},
            {"text": "▶️", "callback": self.cb_page, "args": (next_pg, group, q, curr_i)},
        ])
        kb.append([{"text": self.strings['v_btn_bck'], "callback": self.cb_nav, "args": (curr_i, group, q)}])
        await utils.answer(cb, f"{self.ICONS['modules_list']} <b>{self.strings['v_res_hdr']}</b>", reply_markup=kb)

    async def cb_page(self, cb: Any, pg: int, group: list, q: str, orig_i: int):
        self._list_pg = pg
        log.debug("cb_page: pg=%d group_len=%d orig_i=%d", pg, len(group) if group else 0, orig_i)
        with suppress(Exception): await cb.answer()
        total_pages = max(1, (len(group) + 4) // 5)
        start, end = pg * 5, min((pg + 1) * 5, len(group))
        kb = []
        for i in range(start, end):
            m = group[i]
            kb.append([{"text": f"{i + 1}. {m.get('name')} by {m.get('author')}", "callback": self.cb_nav, "args": (i, group, q)}])
        prev_pg = (pg - 1) % total_pages
        next_pg = (pg + 1) % total_pages
        kb.append([
            {"text": "◀️", "callback": self.cb_page, "args": (prev_pg, group, q, orig_i)},
            {"text": self.strings['v_page'].format(idx=pg + 1, total=total_pages), "callback": self.cb_dummy},
            {"text": "▶️", "callback": self.cb_page, "args": (next_pg, group, q, orig_i)},
        ])
        kb.append([{"text": self.strings['v_btn_bck'], "callback": self.cb_nav, "args": (orig_i, group, q)}])
        await utils.answer(cb, f"{self.ICONS['modules_list']} <b>{self.strings['v_res_hdr']}</b>", reply_markup=kb)

    async def cb_toggle(self, cb: Any, m_owner: str, m_name: str, i: int, group: list, q: str, exp: bool):
        self._expanded = exp
        log.debug("cb_toggle: name=%s idx=%d exp=%s", m_name, i, exp)
        with suppress(Exception): await cb.answer()
        item = group[i] if group and 0 <= i < len(group) else {"name": m_name, "source_url": f"{apirt}/modules/{quote(m_owner, safe='')}/{quote(m_name, safe='')}/source"}
        await utils.answer(cb, self._build_html(item, i + 1, len(group or [item])), reply_markup=self._build_kbd(item, i, group, q, exp), photo=item.get("banner"))

    async def cb_rate(self, cb: Any, m_owner: str, m_name: str, action: str, i: int, group: list, q: str):
        log.info("cb_rate: name=%s action=%s", m_name, action)
        token = await self._get_active_token()
        if not token:
            with suppress(Exception): await cb.answer(self.bannote or self.strings["v_err_api"], show_alert=True)
            return
            
        uid = self._parse_jwt(token).get("sub", "")
        res = await self._net_req("POST", f"/api/rate/{quote(str(uid), safe='')}/{quote(m_owner, safe='')}/{quote(m_name, safe='')}/{action}", token=token)
        if not res or not res.get("ok"):
            token = await self._get_active_token(force=True)
            uid = self._parse_jwt(token).get("sub", "")
            res = await self._net_req("POST", f"/api/rate/{quote(str(uid), safe='')}/{quote(m_owner, safe='')}/{quote(m_name, safe='')}/{action}", token=token)
            if not res or not res.get("ok"):
                with suppress(Exception): await cb.answer(self.strings["v_dl_err"], show_alert=True)
                return

        new_likes, new_dislikes = self._extract_counts(res)
        log.debug("cb_rate: new likes=%s dislikes=%s", new_likes, new_dislikes)
        if group and i < len(group):
            if new_likes is not None:
                group[i]["likes"] = new_likes
            if new_dislikes is not None:
                group[i]["dislikes"] = new_dislikes
            item = group[i]
        else:
            item = {"name": m_name, "likes": new_likes or 0, "dislikes": new_dislikes or 0, "source_url": f"{apirt}/modules/{quote(m_owner, safe='')}/{quote(m_name, safe='')}/source"}
            
        await utils.answer(cb, self._build_html(item, i + 1, len(group or [item])), reply_markup=self._build_kbd(item, i, group, q), photo=item.get("banner"))
        s_val = res.get("rating", {}).get("state")
        with suppress(Exception): await cb.answer(self.strings["v_fb_rm" if s_val == "removed" else "v_fb_add"], show_alert=True)

    async def cb_install(self, cb: Any, m_owner: str, m_name: str, i: int, group: list, q: str):
        log.info("cb_install: name=%s", m_name)
        token = await self._get_active_token()
        if not token:
            log.warning("cb_install: no token")
            with suppress(Exception): await cb.answer(self.bannote or self.strings["v_err_api"], show_alert=True)
            return

        dl_url = f"{apirt}/modules/{quote(m_owner, safe='')}/{quote(m_name, safe='')}/source"
        ok = await self._safe_install(m_name, dl_url)
        key = "v_dl_ok" if ok else "v_dl_err"
        with suppress(Exception): await cb.answer(self.strings[key], show_alert=True)

    async def cb_sec_check(self, cb: Any, m_owner: str, m_name: str, i: int, group: list, q: str, expanded: bool = False):
        log.info("cb_sec_check: name=%s", m_name)
        def _get_sec_kb(has_run: bool, payload: dict = None):
            k = []
            if not has_run:
                chk = (payload or {}).get("check") or {}
                static = chk.get("details", {}).get("static", {})
                if not (static.get("score", "?") == "?" and static.get("risk", "unknown") == "unknown"):
                    k.append([{"text": self.strings["v_btn_aud_run"], "callback": self.cb_sec_run, "args": (m_owner, m_name, i, group, q, expanded)}])
            k.append([{"text": self.strings["v_btn_code"], "url": f"{apirt}/modules/{quote(m_owner, safe='')}/{quote(m_name, safe='')}/source"}])
            k.append([{"text": self.strings["v_btn_bck"], "callback": self.cb_nav, "args": (i, group or [], q, expanded)}])
            return k

        cached = self.seccache.get(m_name)
        if cached and cached.get("check"):
            log.debug("cb_sec_check: cache hit for %s", m_name)
            return await utils.answer(cb, f"{self.ICONS['safe']} <i>{self.strings['v_aud_mem']}</i>\n\n{self._fmt_sec(m_name, cached)}", reply_markup=_get_sec_kb(True, cached))

        with suppress(Exception): await cb.answer()
        token = await self._get_active_token()
        if not token:
            with suppress(Exception): await cb.answer(self.bannote or self.strings["v_err_api"], show_alert=True)
            return
        res = await self._net_req("GET", f"/api/modules/{quote(m_owner, safe='')}/{quote(m_name, safe='')}/security-check", token=token)
        
        if not res or self.httpc >= 400:
            log.warning("cb_sec_check: API error for %s, http=%s", m_name, self.httpc)
            return await utils.answer(cb, f"{self.ICONS['error']} <b>{self.strings['v_aud_err']}</b>", reply_markup=_get_sec_kb(True))

        if res.get("check"):
            self.seccache[m_name] = res
            log.debug("cb_sec_check: cached result for %s", m_name)
        await utils.answer(cb, self._fmt_sec(m_name, res), reply_markup=_get_sec_kb(bool(res.get("checked")), res))

    async def cb_sec_run(self, cb: Any, m_owner: str, m_name: str, i: int, group: list, q: str, expanded: bool = False):
        log.info("cb_sec_run: name=%s", m_name)
        await utils.answer(cb, f"{self.ICONS['search']} <b>{self.strings['v_aud_proc']}</b>", reply_markup=[[{"text": self.strings["v_btn_bck"], "callback": self.cb_nav, "args": (i, group or [], q, expanded)}]])
        token = await self._get_active_token()
        if not token:
            with suppress(Exception): await cb.answer(self.bannote or self.strings["v_err_api"], show_alert=True)
            return
        res = await self._net_req("POST", f"/api/modules/{quote(m_owner, safe='')}/{quote(m_name, safe='')}/security-check", token=token, timeout=120)
        
        if self.httpc == 429:
            log.warning("cb_sec_run: rate limited (429)")
            return await utils.answer(cb, f"{self.ICONS['warn']} <b>{self.strings['v_aud_zero']}</b>", reply_markup=[[{"text": self.strings["v_btn_bck"], "callback": self.cb_nav, "args": (i, group or [], q, expanded)}]])
        if not res or self.httpc >= 400:
            log.warning("cb_sec_run: API error, http=%s", self.httpc)
            return await utils.answer(cb, f"{self.ICONS['error']} <b>{self.strings['v_aud_err']}</b>", reply_markup=[[{"text": self.strings["v_btn_bck"], "callback": self.cb_nav, "args": (i, group or [], q, expanded)}]])

        log.info("cb_sec_run: scan complete for %s", m_name)
        if res.get("check"):
            self.seccache[m_name] = res
            log.debug("cb_sec_run: cached result for %s", m_name)
        await utils.answer(cb, self._fmt_sec(m_name, res), reply_markup=[
            [{"text": self.strings["v_btn_code"], "url": f"{apirt}/modules/{quote(m_owner, safe='')}/{quote(m_name, safe='')}/source"}],
            [{"text": self.strings["v_btn_bck"], "callback": self.cb_nav, "args": (i, group or [], q, expanded)}],
        ])

    def _fmt_sec(self, m_name: str, payload: dict) -> str:
        log.debug("_fmt_sec: name=%s has_check=%s", m_name, bool(payload.get("check")))
        chk = payload.get("check")
        qta = payload.get("quota") or (chk.get("quota") if chk else None) or {}
        if not chk:
            return (f"{self.ICONS['shield']} <b>{self.strings['v_aud_hdr'].format(name=m_name)}</b>\n\n"
                    f"{self.ICONS['warn']} {self.strings['v_aud_none']}\n"
                    f"{self.ICONS['quota']} <i>{self.strings['v_aud_left'].format(remaining=qta.get('remaining', '?'), limit=qta.get('limit', '?'))}</i>")

        v = str(chk.get("verdict", "unknown"))
        v_icon = self.ICONS.get(v, self.ICONS['shield'])
        static = chk.get("details", {}).get("static", {})
        fnds = static.get("findings", {})
        
        lines = [
            f"{v_icon} <b>{self.strings['v_aud_hdr'].format(name=m_name)}</b>\n",
            f"{self.ICONS['shield']} <b>{self.strings['v_aud_lvl']}:</b> <code>{chk.get('label', v)}</code> (<code>{chk.get('confidence', 0)}%</code>)",
        ]
        if static.get("score", "?") != "?" or static.get("risk", "unknown") != "unknown":
            lines.append(f"{self.ICONS['stats']} <b>{self.strings['v_aud_stat']}:</b> risk <code>{static.get('risk', 'unknown')}</code>, score <code>{static.get('score', '?')}</code>")
        lines.append(f"{self.ICONS['description']} <b>{self.strings['v_aud_out']}:</b>\n<blockquote expandable>{chk.get('summary', self.strings['v_aud_no_txt'])}</blockquote>")
        
        f_blocks = []
        for hdr, key in [(self.strings["v_sig_crit"], "critical"), (self.strings["v_sig_warn"], "warning"), (self.strings["v_sig_info"], "info")]:
            arr = fnds.get(key, [])
            if arr: f_blocks.append(f"<b>{hdr}</b>: " + ", ".join(x.get("title", "?") for x in arr[:3]))
        if f_blocks:
            lines.append(f"{self.ICONS['search']} <b>{self.strings['v_aud_sigs']}:</b>\n<blockquote expandable>{chr(10).join(f_blocks)}</blockquote>")
            
        remaining = qta.get("remaining", "?")
        if remaining != "?":
            lines.append(f"{self.ICONS['quota']} <i>{self.strings['v_aud_left'].format(remaining=remaining, limit=qta.get('limit', '?'))}</i>")
        return "\n".join(lines)

    async def cb_comments(self, cb: Any, m_owner: str, m_name: str, i: int, group: list, q: str, pg: int = 0, expanded: bool = False, _comments: list = None):
        log.info("cb_comments: name=%s pg=%d cached=%s", m_name, pg, bool(_comments))
        with suppress(Exception): await cb.answer()
        if _comments is not None:
            comments = _comments
        else:
            token = await self._get_active_token()
            if not token:
                log.warning("cb_comments: no token")
                with suppress(Exception): await cb.answer(self.bannote or self.strings["v_err_api"], show_alert=True)
                return
            res = await self._net_req("GET", f"/api/modules/{quote(m_owner, safe='')}/{quote(m_name, safe='')}/comments", token=token)
            
            if not res or not isinstance(res, dict):
                log.warning("cb_comments: bad response for %s", m_name)
                with suppress(Exception): await cb.answer(self.strings["v_talk_err"], show_alert=True)
                return
            comments = res.get("comments", [])
        self._cmt_calls[m_name] = cb
        log.debug("cb_comments: %d comments for %s", len(comments), m_name)

        roots = [c for c in comments if not c.get("parent_id")]
        total_pages = max(1, (len(roots) + 4) // 5)
        pg = max(0, min(pg, total_pages - 1))

        prev_pg = (pg - 1) % total_pages if total_pages > 1 else 0
        next_pg = (pg + 1) % total_pages if total_pages > 1 else 0
            
        kb = [[
            {"text": self.strings["v_btn_wrt"], "input": self.strings["v_rep_ask"], "handler": self.cb_post_comment, "args": (m_owner, m_name, i, group, q, pg, expanded)},
        ], [
        ]]

        if total_pages > 1:
            kb.append([
                {"text": "◀️", "callback": self.cb_comments, "args": (m_owner, m_name, i, group, q, prev_pg, expanded)},
                {"text": self.strings["v_page"].format(idx=pg + 1, total=total_pages), "callback": self.cb_dummy},
                {"text": "▶️", "callback": self.cb_comments, "args": (m_owner, m_name, i, group, q, next_pg, expanded)},
            ])

        kb.append([{"text": self.strings["v_btn_code"], "url": f"{apirt}/modules/{quote(m_owner, safe='')}/{quote(m_name, safe='')}/source"}])
        kb.append([{"text": self.strings["v_btn_bck"], "callback": self.cb_nav, "args": (i, group or [], q, expanded, pg)}])
        
        item = group[i] if group and 0 <= i < len(group) else {}
        await utils.answer(cb, self._fmt_comments(comments, m_name, pg), reply_markup=kb, photo=item.get("banner"))

    async def cb_post_comment(self, cb: Any, text: str, m_owner: str, m_name: str, i: int, group: list, q: str, pg: int = 0, expanded: bool = False):
        log.info("cb_post_comment: name=%s text_len=%d", m_name, len(text) if text else 0)
        token = await self._get_active_token()
        if not token:
            log.warning("cb_post_comment: no token")
            with suppress(Exception): await cb.answer(self.bannote or self.strings["v_err_api"], show_alert=True)
            return
        c_txt = str(text or "").strip()
        if not c_txt:
            log.debug("cb_post_comment: empty text, cancelled")
            with suppress(Exception): await cb.answer(self.strings["v_rep_cncl"], show_alert=True)
            return
        if len(c_txt) < 2 or len(c_txt) > 1800:
            with suppress(Exception): await cb.answer(self.strings["v_rep_min" if len(c_txt) < 2 else "v_rep_max"], show_alert=True)
            return

        with suppress(Exception): await cb.answer(self.strings["v_rep_snt"], show_alert=True)
        res = await self._net_req("POST", f"/api/modules/{quote(m_owner, safe='')}/{quote(m_name, safe='')}/comments", token=token, json_data={"body": c_txt})
        
        if not res:
            log.warning("cb_post_comment: API error posting to %s", m_name)
            with suppress(Exception): await cb.answer(self.strings["v_rep_err"], show_alert=True)
            return
        
        log.info("cb_post_comment: posted to %s successfully", m_name)
            
        with suppress(Exception): await cb.answer(self.strings["v_rep_ok"], show_alert=True)
        
        await asyncio.sleep(1.5)
        
        cached = res.get("comments") if isinstance(res, dict) else None
        orig = self._cmt_calls.get(m_name, cb)
        await self.cb_comments(orig, m_owner, m_name, i, group, q, pg, expanded, _comments=cached)

    def _fmt_comments(self, comments: list, m_name: str, pg: int = 0, pp: int = 5) -> str:
        log.debug("_fmt_comments: name=%s count=%d pg=%d", m_name, len(comments) if comments else 0, pg)
        h = f"{self.strings['v_talk_hdr'].format(emoji=self.ICONS['comments'], name=m_name)}\n<b>{self.strings['v_talk_desc']}</b>\n<i>{self.strings['v_talk_num'].format(count=len(comments))}</i>"
        if not comments: return f"{h}\n\n{self.strings['v_talk_0']}"
        
        roots, chmap = [], {}
        for c in comments:
            pid = c.get("parent_id")
            if pid: chmap.setdefault(str(pid), []).append(c)
            else: roots.append(c)
            if c.get("replies"): chmap.setdefault(str(c.get("id")), []).extend(c["replies"])

        total_pages = max(1, (len(roots) + pp - 1) // pp)
        pg = max(0, min(pg, total_pages - 1))
        start, end = pg * pp, min((pg + 1) * pp, len(roots))
        page_roots = roots[start:end]

        blks = [h]
        if total_pages > 1:
            blks.append(f"<i>{self.strings['v_page'].format(idx=pg + 1, total=total_pages)}</i>")
        for r in page_roots:
            rid = str(r.get("id"))
            
            raw_uname = r.get("author_username")
            uname = (str(raw_uname).strip() if raw_uname else "").lstrip("@")
            meta = [f"@{utils.escape_html(uname)}"] if uname else []
            ts = str(r.get("created_at", "")).replace("T", " ").replace("Z", "").strip()
            if ts: meta.append(utils.escape_html(ts[:16]))
            meta_str = f" <i>{' · '.join(meta)}</i>" if meta else ""
            edit_mark = " *" if r.get("can_edit") else ""
            
            auth = f"<b>{utils.escape_html(r.get('author_name') or r.get('author_username') or 'Unknown')}</b>{edit_mark}{meta_str}"
            blks.append(f"╭─ {auth}\n╰─\n<blockquote>{utils.escape_html(str(r.get('body', '')))}</blockquote>")
            
            subs = chmap.get(rid, [])
            for s in subs[:4]:
                raw_s_uname = s.get("author_username")
                s_uname = (str(raw_s_uname).strip() if raw_s_uname else "").lstrip("@")
                s_meta = [f"@{utils.escape_html(s_uname)}"] if s_uname else []
                s_ts = str(s.get("created_at", "")).replace("T", " ").replace("Z", "").strip()
                if s_ts: s_meta.append(utils.escape_html(s_ts[:16]))
                s_meta_str = f" <i>{' · '.join(s_meta)}</i>" if s_meta else ""
                s_edit_mark = " *" if s.get("can_edit") else ""
                
                s_auth = f"<b>{utils.escape_html(s.get('author_name') or s.get('author_username') or 'Unknown')}</b>{s_edit_mark}{s_meta_str}"
                blks.append(f"  {self.ICONS['reply']} {s_auth}\n<blockquote>{utils.escape_html(str(s.get('body', '')))}</blockquote>")
                
            if len(subs) > 4: blks.append(f"  <i>{self.strings['v_more_replies'].format(count=len(subs)-4)}</i>")
            
        return "\n\n".join(blks)