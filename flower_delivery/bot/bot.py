import logging
from telegram import Bot, InputFile
from telegram.constants import ParseMode

# Логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Настройки бота
TELEGRAM_BOT_TOKEN = 'ваш_токен'
CHAT_ID = 'ваш_чат_id'

bot = Bot(token=TELEGRAM_BOT_TOKEN)


async def send_order_notification(order):
    """
    Отправляет уведомление о новом заказе в Telegram.
    :param order: объект модели Order
    """
    try:
        # Общая стоимость заказа
        total_price = sum(item.price for item in order.products.all())
        products = '\n'.join([f"{item.name} ({item.price} руб.)" for item in order.products.all()])

        # Формируем текст сообщения
        message = (
            f"<b>Новый заказ!</b>\n\n"
            f"<b>Адрес доставки:</b> {order.delivery_address}\n"
            f"<b>Комментарий:</b> {order.comment or 'Без комментария'}\n"
            f"<b>Товары:</b>\n{products}\n"
            f"<b>Общая стоимость:</b> {total_price} руб."
        )

        # Отправляем текстовое сообщение
        await bot.send_message(chat_id=CHAT_ID, text=message, parse_mode=ParseMode.HTML)

        # Отправляем изображения товаров
        for product in order.products.all():
            if product.image:
                await bot.send_photo(chat_id=CHAT_ID, photo=InputFile(product.image.path))

        logger.info("Уведомление о заказе отправлено успешно.")
    except Exception as e:
        logger.error(f"Ошибка при отправке уведомления: {e}")
