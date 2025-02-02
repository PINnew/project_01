import httpx
import asyncio


# Проверка работы Telegram Bot
async def send_test_message():
    token = ""      # УСТОНОВИТЬ TOKEN
    chat_id = ""    # УСТОНОВИТЬ CHAT_ID
    message = "Тестовое сообщение"
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url,
                json={
                    "chat_id": chat_id,
                    "text": message,
                    "parse_mode": "HTML"
                }
            )
            response.raise_for_status()  # Проверяет, что статус ответа 200
            print("Сообщение отправлено успешно!")
            print(response.json())
    except httpx.HTTPStatusError as http_err:
        print(f"HTTP-ошибка: {http_err.response.status_code} - {http_err.response.text}")
    except Exception as err:
        print(f"Ошибка: {err}")

if __name__ == "__main__":
    asyncio.run(send_test_message())