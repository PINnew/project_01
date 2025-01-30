import logging
from telegram import Bot, InputFile
from telegram.constants import ParseMode


# Настройки бота
TELEGRAM_BOT_TOKEN = ''     # УСТОНОВИТЬ TOKEN
CHAT_ID = ''                # УСТОНОВИТЬ CHAT_ID

bot = Bot(token=TELEGRAM_BOT_TOKEN)
# Логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def send_order_notification(order):
    """
    Отправляет уведомление о новом заказе в Telegram.
    """
    try:
        # Общая стоимость заказа
        total_price = sum(product.price for product in order.products.all())
        products_text = "\n".join([f"• {product.name} - {product.price} руб." for product in order.products.all()])

        # Формируем текст сообщения
        message = (
            f"📦 <b>Новый заказ!</b>\n\n"
            f"🏠 <b>Адрес доставки:</b> {order.delivery_address}\n"
            f"💬 <b>Комментарий:</b> {order.comment or 'Нет'}\n"
            f"🛒 <b>Товары:</b>\n{products_text}\n"
            f"💰 <b>Итого:</b> {total_price} руб."
        )

        # Отправляем текстовое сообщение
        await bot.send_message(chat_id=CHAT_ID, text=message, parse_mode=ParseMode.HTML)

        # Отправляем фото каждого товара
        for product in order.products.all():
            if product.image:
                await bot.send_photo(chat_id=CHAT_ID, photo=InputFile(product.image.path))

        logger.info("✅ Уведомление о заказе отправлено успешно.")
    except Exception as e:
        logger.error(f"❌ Ошибка при отправке уведомления: {e}")
