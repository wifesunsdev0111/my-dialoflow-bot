import logging
import os
import random

import telegram
import vk_api as vk
from dotenv import load_dotenv
from requests.adapters import HTTPAdapter
from vk_api.longpoll import VkEventType, VkLongPoll

from detect_intent import detect_intent_text
from logs_handler import TelegramLogsHandler

logger = logging.getLogger("Logger")


def reply(event, vk_api, project_id):
    intent = detect_intent_text(
        project_id=project_id,
        session_id=f"vk-{event.user_id}",
        text=event.text,
    )
    if not intent.intent.is_fallback:
        vk_api.messages.send(
            user_id=event.user_id,
            message=intent.fulfillment_text,
            random_id=random.randint(1, 1000),
        )


def main():
    load_dotenv()
    project_id=os.environ["PROJECT_ID"]
    tg_token = os.environ["TG_TOKEN"]
    tg_chat_id = os.environ["TG_CHAT_ID"]
    tg_bot = telegram.Bot(token=tg_token)
    logger.setLevel(logging.INFO)
    logger.addHandler(TelegramLogsHandler(tg_bot, tg_chat_id))
    logger.info("ВК бот запущен")

    vk_session = vk.VkApi(token=os.environ["VK_TOKEN"])
    vk_api = vk_session.get_api()
    try:
        longpoll = VkLongPoll(vk_session)
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                reply(event, vk_api, project_id)
    except Exception:
        logger.exception(msg="VK Бот упал с ошибкой:")


if __name__ == "__main__":
    main()
