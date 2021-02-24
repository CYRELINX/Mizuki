import codecs
import os
import random
import re
from datetime import datetime
from io import BytesIO
from typing import Optional

import requests
import requests as r
import wikipedia
from bs4 import BeautifulSoup
from requests import get, post
from telegram import (
    Chat,
    ChatAction,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ParseMode,
    ReplyKeyboardRemove,
    TelegramError,
    Update,
)
from telegram.error import BadRequest
from telegram.ext import CallbackContext, CommandHandler, Filters, run_async
from telegram.ext.dispatcher import run_async
from Mizuki.modules.disable import DisableAbleCommandHandler
from Mizuki.modules.helper_funcs.alternate import send_action, typing_action
from Mizuki.modules.helper_funcs.chat_status import user_admin
from Mizuki.modules.helper_funcs.filters import CustomFilters

@run_async
@typing_action
def github(update, context):
    message = update.effective_message
    text = message.text[len("/git ") :]
    usr = get(f"https://api.github.com/users/{text}").json()
    if usr.get("login"):
        text = f"*Username:* [{usr['login']}](https://github.com/{usr['login']})"

        whitelist = [
            "name",
            "id",
            "type",
            "location",
            "blog",
            "bio",
            "followers",
            "following",
            "hireable",
            "public_gists",
            "public_repos",
            "email",
            "company",
            "updated_at",
            "created_at",
        ]

        difnames = {
            "id": "Account ID",
            "type": "Account type",
            "created_at": "Account created at",
            "updated_at": "Last updated",
            "public_repos": "Public Repos",
            "public_gists": "Public Gists",
        }

        goaway = [None, 0, "null", ""]

        for x, y in usr.items():
            if x in whitelist:
                if x in difnames:
                    x = difnames[x]
                else:
                    x = x.title()

                if x == "Account created at" or x == "Last updated":
                    y = datetime.strptime(y, "%Y-%m-%dT%H:%M:%SZ")

                if y not in goaway:
                    if x == "Blog":
                        x = "Website"
                        y = f"[Here!]({y})"
                        text += "\n*{}:* {}".format(x, y)
                    else:
                        text += "\n*{}:* `{}`".format(x, y)
        reply_text = text
    else:
        reply_text = "User not found. Make sure you entered valid username!"
    message.reply_text(
        reply_text, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True
    )


@run_async
def repo(update, context):
    context.args
    message = update.effective_message
    text = message.text[len("/repo ") :]
    usr = get(f"https://api.github.com/users/{text}/repos?per_page=40").json()
    reply_text = "*Repositorys*\n"
    for i in range(len(usr)):
        reply_text += f"[{usr[i]['name']}]({usr[i]['html_url']})\n"
    message.reply_text(
        reply_text, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True
    )


GITHUB_HANDLER = DisableAbleCommandHandler("git", github, admin_ok=True)
REPO_HANDLER = DisableAbleCommandHandler("repo", repo, pass_args=True, admin_ok=True)

dispatcher.add_handler(GITHUB_HANDLER)
dispatcher.add_handler(REPO_HANDLER)
