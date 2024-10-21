from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import random
import string

# Bot tokenini shu yerga joylashtiring
TOKEN = '7121736215:AAHIfGuBXGSK5LvPOEKJpVK6EgPLAiPy4Xc'
verification_codes = {}  # Telefon raqami va tasdiqlash kodlarini saqlash uchun lug'at


def generate_code(length=6):
    """ Tasdiqlash kodi yaratadi """
    return ''.join(random.choices(string.digits, k=length))


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """ /start buyrug'iga javob beradi """
    button = KeyboardButton("📞 Telefon raqamni yuboring", request_contact=True)
    keyboard = [[button]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text('Telefon raqamingizni yuboring:', reply_markup=reply_markup)


async def handle_contact(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """ Telefon raqamni qabul qiladi va tasdiqlash kodi yuboradi """
    user = update.message.from_user
    contact = update.message.contact

    phone_number = contact.phone_number
    verification_code = generate_code()

    # Tasdiqlash kodini saqlash
    verification_codes[phone_number] = verification_code

    await update.message.reply_text(f'Sizning tasdiqlash kodingiz: {verification_code}')


def main() -> None:
    """ Botni ishga tushiradi """
    application = Application.builder().token(TOKEN).build()

    # /start buyrug'i uchun handler
    application.add_handler(CommandHandler('start', start))

    # Telefon raqamni qabul qilish uchun handler
    application.add_handler(MessageHandler(filters.CONTACT, handle_contact))

    # Botni ishga tushirish
    application.run_polling()


if __name__ == '__main__':
    main()
