import json

import requests
from config import settings
from domain.usecases.event import AbstractEventUseCase
from schemas.events import EventAddSchema


class GigaChatManager:
    @staticmethod
    async def get_access_token() -> str:
        url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"

        payload = "scope=GIGACHAT_API_PERS"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
            "RqUID": f"{settings.CLIENT_SECRET}",
            "Authorization": f"Basic {settings.AUTH_DATA}",
        }

        response = requests.request(
            "POST", url, headers=headers, data=payload, verify=False
        )

        return response.json()["access_token"]

    @staticmethod
    async def generate_data():
        url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
        access_token = await GigaChatManager.get_access_token()
        payload = json.dumps(
            {
                "model": "GigaChat",
                "messages": [
                    {
                        "role": "system",
                        "content": """
                    Сгенерируй 20 объектов для сущности "массовое мероприятие". Каждый объект должен содержать следующую информацию:
- title: название мероприятия (строка)
- price: стоимость билета (число)
- date: дата и время проведения (формат: "дд.мм.гггг чч:мм")
- genre: жанр мероприятия (список строк)
- rating: рейтинг мероприятия (число от 1 до 10)
- location: место проведения (список строк)

Примеры мероприятий:
1. "title": "Macan", "price": 1000, "date": "11.09.2001 09:11", "genre": ["rap"], "rating": 7, "location": ["Лужники"]
2. "title": "Баста", "price": 1500, "date": "15.10.2023 19:30", "genre": ["classical"], "rating": 9, "location": ["Концертный зал Чайковского"]
3. "title": "Obladaet", "price": 3000, "date": "05.07.2023 18:00", "genre": ["rock"], "rating": 8, "location": ["Олимпийский"]

Требования:
- Мероприятия должны быть разнообразными по жанрам и местам проведения.
- Даты мероприятий должны быть реальными и находиться в будущем.
- Рейтинги должны варьироваться от 1 до 10.
- Цена должна быть разумной для данного типа мероприятия.
- Каждое мероприятие должно иметь уникальное название.

Пожалуйста, создайте разнообразный и реалистичный набор данных. Результат верни в формате JSON без каких - либо пояснений.
                    """,
                    }
                ],
                "temperature": 1.25,
                "top_p": 0.6,
                "n": 1,
                "stream": False,
                "max_tokens": 2048,
                "repetition_penalty": 1.07,
            }
        )
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {access_token}",
        }

        response = requests.request(
            "POST", url, headers=headers, data=payload, verify=False
        )

        return response.json()

    @staticmethod
    def validate_json(s: str):
        while s[-1] != "}":
            s = s[:-1]
        return s + "]"

    @staticmethod
    async def fill_bd(event_case: AbstractEventUseCase, user_id: int):
        data = await GigaChatManager.generate_data()
        events = GigaChatManager.validate_json(data["choices"][0]["message"]["content"])
        events = json.loads(events)
        for event in events:
            try:
                event = EventAddSchema(**event)
                await event_case.add(event, user_id)

            except Exception:
                pass
